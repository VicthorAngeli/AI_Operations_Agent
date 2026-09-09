from __future__ import annotations

from time import perf_counter

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_handles_repeated_requests() -> None:
    client = TestClient(app)
    started_at = perf_counter()
    responses = [client.get("/health") for _ in range(25)]
    elapsed_seconds = perf_counter() - started_at

    assert all(response.status_code == 200 for response in responses)
    assert elapsed_seconds < 10