from __future__ import annotations

from app.agents.customer_analysis.customer_analysis_agent import CustomerAnalysisAgent
from app.agents.orchestrator.orchestrator_agent import OrchestratorAgent


def test_orchestrator_agent_sets_execution_metadata() -> None:
    state = {"user_request": "Meu refrigerador parou de funcionar."}
    result = OrchestratorAgent().run(state)

    assert result["execution_metadata"]["status"] == "orchestrator_ready"
    assert "orchestrator" in result["execution_metadata"]["agents"]


def test_customer_analysis_agent_sets_classification() -> None:
    state = {"user_request": "Meu refrigerador parou de funcionar novamente."}
    result = CustomerAnalysisAgent().run(state)

    assert result["classification"]["category"] == "Problema Técnico"
    assert result["classification"]["recurrence_detected"] is True
