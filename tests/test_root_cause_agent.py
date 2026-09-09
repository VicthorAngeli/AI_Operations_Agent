from __future__ import annotations

from app.agents.root_cause.root_cause_agent import RootCauseAgent


def test_root_cause_agent_identifies_recurring_failure_risk() -> None:
    state = {
        "classification": {
            "priority": "Alta",
            "sentiment": "Negativo",
            "recurrence_detected": True,
        },
        "previous_tickets": [{"id": 1}, {"id": 2}],
        "customer_metrics": {"open_tickets": 1},
        "retrieved_documents": [{"source": "recurring_failure_procedure.md"}],
    }

    result = RootCauseAgent().run(state)

    assert result["root_cause"]["risk_level"] == "high"
    assert "histórico indica falha recorrente" in result["root_cause"]["contributing_factors"]
    assert result["execution_metadata"]["root_cause_evidence"]["ticket_count"] == 2


def test_root_cause_agent_does_not_overstate_without_evidence() -> None:
    result = RootCauseAgent().run({"classification": {}, "user_request": "Preciso de ajuda."})

    assert result["root_cause"]["risk_level"] == "low"
    assert "não confirmada" in result["root_cause"]["possible_root_cause"]