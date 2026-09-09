from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4
from typing import Any

from app.agents.customer_analysis.customer_analysis_agent import CustomerAnalysisAgent
from app.agents.data_agent.data_agent import DataAgent
from app.agents.decision.decision_agent import DecisionAgent
from app.agents.evaluator.evaluation_agent import EvaluationAgent
from app.agents.knowledge_agent.knowledge_agent import KnowledgeAgent
from app.agents.orchestrator.orchestrator_agent import OrchestratorAgent
from app.agents.response.response_agent import ResponseAgent
from app.agents.root_cause.root_cause_agent import RootCauseAgent
from app.database.init_db import init_database
from app.database.repository import DatabaseRepository
from app.models.state import AgentState
from app.utils.validators import contains_prompt_injection_attempt, sanitize_user_input


WORKFLOW_AGENTS = (
    OrchestratorAgent,
    CustomerAnalysisAgent,
    DataAgent,
    KnowledgeAgent,
    RootCauseAgent,
    DecisionAgent,
    ResponseAgent,
    EvaluationAgent,
)


def build_workflow() -> dict[str, Any]:
    """Return the explicit execution contract for the operational workflow."""
    return {
        "name": "ai_operations_workflow",
        "entry": "orchestrator",
        "nodes": [agent.name for agent in WORKFLOW_AGENTS],
        "status": "executable",
    }


def validate_state(state: AgentState) -> bool:
    return isinstance(state, dict) and bool(state.get("user_request"))


def run_workflow(state: AgentState) -> AgentState:
    """Execute every agent in the approved order using the shared state."""
    if not validate_state(state):
        raise ValueError("user_request is required to execute the workflow.")
    if contains_prompt_injection_attempt(state["user_request"]):
        raise ValueError("The request was rejected by the prompt-injection guardrail.")

    init_database()
    state["user_request"] = sanitize_user_input(state["user_request"])
    state.setdefault("execution_metadata", {})
    state["execution_metadata"]["execution_id"] = str(uuid4())
    state["execution_metadata"]["workflow"] = build_workflow()["name"]
    repository = DatabaseRepository()

    for agent_type in WORKFLOW_AGENTS:
        started_at = datetime.now(timezone.utc)
        started_timer = perf_counter()
        state = agent_type().run(state)
        finished_at = datetime.now(timezone.utc)
        repository.save_agent_execution(
            execution_id=state["execution_metadata"]["execution_id"],
            agent_name=agent_type.name,
            started_at=started_at.isoformat(),
            finished_at=finished_at.isoformat(),
            duration_ms=round((perf_counter() - started_timer) * 1000),
            result={
                "status": "completed",
                "state_keys": sorted(state.keys()),
            },
        )

    state["execution_metadata"]["status"] = "completed"
    return state
