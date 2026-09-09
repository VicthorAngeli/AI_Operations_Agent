from __future__ import annotations

import hmac
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

from app.config.logging import logger
from app.config.settings import settings
from app.database.init_db import init_database
from app.database.repository import DatabaseRepository
from app.graph.workflow import run_workflow
from app.models.schemas import AnalyzeRequest, ExecutionResult
from app.services.metrics import metrics
from app.services.rate_limiter import RateLimiter

app = FastAPI(title=settings.APP_NAME, version="0.1.0")
rate_limiter = RateLimiter(settings.RATE_LIMIT_REQUESTS, settings.RATE_LIMIT_WINDOW_SECONDS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.API_ALLOWED_ORIGINS.split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    started_at = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        metrics.record_http_request(
            request.method,
            500,
            (perf_counter() - started_at) * 1000,
        )
        raise

    metrics.record_http_request(
        request.method,
        response.status_code,
        (perf_counter() - started_at) * 1000,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.middleware("http")
async def limit_analysis_requests(request: Request, call_next):
    if request.url.path == "/analyze":
        client_host = request.client.host if request.client else "unknown"
        allowed, retry_after = rate_limiter.allow(client_host)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."},
                headers={"Retry-After": str(retry_after)},
            )
    return await call_next(request)


@app.middleware("http")
async def protect_sensitive_endpoints(request: Request, call_next):
    protected_paths = {"/analyze", "/metrics"}
    if request.url.path.startswith("/executions/"):
        protected_paths.add(request.url.path)
    if request.url.path in protected_paths:
        configured_token = settings.API_AUTH_TOKEN
        supplied_token = request.headers.get("X-API-Key", "")
        if settings.APP_ENV.casefold() == "production" and not configured_token:
            return JSONResponse(
                status_code=503,
                content={"detail": "API_AUTH_TOKEN is not configured."},
            )
        if configured_token and not hmac.compare_digest(supplied_token, configured_token):
            return JSONResponse(
                status_code=401,
                content={"detail": "A valid X-API-Key is required."},
            )
    return await call_next(request)


@app.get("/health")
def health_check() -> dict[str, str]:
    logger.info("Health check requested")
    return {"status": "ok", "app": settings.APP_NAME}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics_endpoint() -> str:
    return metrics.render_prometheus()


@app.get("/ready")
def readiness_check() -> dict[str, str]:
    try:
        init_database()
        DatabaseRepository().fetch_one("SELECT 1")
    except Exception as error:
        logger.exception("Readiness check failed: %s", error)
        raise HTTPException(status_code=503, detail="Database is not ready.") from error
    return {"status": "ready", "app": settings.APP_NAME}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Operations Agent is running."}


@app.post("/analyze", response_model=ExecutionResult)
def analyze(request: AnalyzeRequest) -> ExecutionResult:
    try:
        state = run_workflow(
            {
                "customer_id": request.customer_id,
                "user_request": request.message,
            }
        )
    except ValueError as error:
        metrics.record_workflow("failure")
        raise HTTPException(status_code=400, detail=str(error)) from error

    metrics.record_workflow("success")
    metadata = state.get("execution_metadata", {})
    return ExecutionResult(
        execution_id=metadata["execution_id"],
        customer_id=request.customer_id,
        summary=state.get("final_response", ""),
        classification=state.get("classification"),
        decision=state.get("decision"),
        final_response=state.get("final_response"),
        evaluation=state.get("evaluation"),
    )


@app.get("/executions/{execution_id}")
def get_execution(execution_id: str) -> dict[str, object]:
    executions = DatabaseRepository().fetch_execution(execution_id)
    if not executions:
        raise HTTPException(status_code=404, detail="Execution not found.")
    return {"execution_id": execution_id, "agents": executions}
