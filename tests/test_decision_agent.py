from __future__ import annotations

from app.agents.decision.decision_agent import DecisionAgent


def test_decision_agent_escalates_high_risk_case() -> None:
    state = {
        "classification": {
            "priority": "Alta",
            "recurrence_detected": True,
        },
        "root_cause": {"risk_level": "high"},
        "customer_metrics": {"open_tickets": 1},
        "retrieved_documents": [{"source": "recurring_failure_procedure.md"}],
    }

    result = DecisionAgent().run(state)

    assert result["decision"] == {
        "decision": "escalate_technical",
        "justification": "Escalonar para avaliação técnica prioritária devido ao risco operacional, histórico do caso e evidências disponíveis.",
        "escalated": True,
    }
    assert result["execution_metadata"]["decision_evidence"]["open_tickets"] == 1


def test_decision_agent_is_conservative_for_low_risk_case() -> None:
    result = DecisionAgent().run(
        {
            "classification": {"priority": "Baixa"},
            "root_cause": {"risk_level": "low"},
            "customer_metrics": {"open_tickets": 0},
        }
    )

    assert result["decision"]["decision"] == "provide_initial_guidance"
    assert result["decision"]["escalated"] is False