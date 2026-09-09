from __future__ import annotations

from app.agents.response.response_agent import ResponseAgent


def test_response_agent_handles_technical_escalation() -> None:
    result = ResponseAgent().run(
        {
            "customer_data": {"name": "João Silva"},
            "product_data": {"name": "Refrigerador Smart Pro"},
            "decision": {"decision": "escalate_technical"},
        }
    )

    assert "João Silva" in result["final_response"]
    assert "Refrigerador Smart Pro" in result["final_response"]
    assert "avaliação prioritária" in result["final_response"]
    assert result["execution_metadata"]["response_metadata"]["decision_used"] == "escalate_technical"


def test_response_agent_requests_details_for_low_evidence_case() -> None:
    result = ResponseAgent().run(
        {
            "decision": {"decision": "provide_initial_guidance"},
        }
    )

    assert "precisamos confirmar alguns detalhes" in result["final_response"]
    assert "diagnóstico" not in result["final_response"].lower()