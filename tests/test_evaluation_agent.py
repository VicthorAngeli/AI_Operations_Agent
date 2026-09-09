from __future__ import annotations

from app.agents.evaluator.evaluation_agent import EvaluationAgent


def test_evaluation_agent_accepts_compliant_escalation_response() -> None:
    result = EvaluationAgent().run(
        {
            "decision": {"decision": "escalate_technical"},
            "final_response": (
                "Olá, João. Vamos encaminhar o caso para avaliação prioritária. "
                "Retornaremos com a próxima ação."
            ),
        }
    )

    assert result["evaluation"]["hallucination_risk"] == "low"
    assert result["evaluation"]["overall_score"] == 100
    assert result["execution_metadata"]["evaluation_evidence"]["internal_marker_found"] is False


def test_evaluation_agent_flags_internal_content() -> None:
    result = EvaluationAgent().run(
        {
            "decision": {"decision": "continue_investigation"},
            "final_response": "Recomendação interna: risk_level high.",
        }
    )

    assert result["evaluation"]["policy_compliance"] == 0
    assert result["evaluation"]["hallucination_risk"] == "high"