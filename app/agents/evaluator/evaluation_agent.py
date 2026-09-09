from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.models.schemas import EvaluationResult


class EvaluationAgent(BaseAgent):
    name = "evaluation"

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        response = str(state.get("final_response", "")).strip()
        decision_code = (state.get("decision") or {}).get("decision", "")
        lower_response = response.casefold()

        internal_markers = {
            "recomendação interna",
            "risk_level",
            "root_cause",
            "prompt injection",
        }
        contains_internal_marker = any(marker in lower_response for marker in internal_markers)
        relevance = 100 if response else 0
        policy_compliance = 0 if contains_internal_marker else 100
        clarity = 100 if response and response[-1:] in ".!?" else 70 if response else 0

        expected_terms = {
            "escalate_technical": {"prioritária", "encaminhar"},
            "continue_investigation": {"acompanhamento", "próxima etapa"},
            "provide_initial_guidance": {"detalhes", "envie"},
        }.get(decision_code, set())
        completeness = 100 if expected_terms and all(term in lower_response for term in expected_terms) else 60
        if not response:
            completeness = 0

        hallucination_risk = "high" if contains_internal_marker else "medium" if not response else "low"
        scores = [relevance, policy_compliance, clarity, completeness]
        result = EvaluationResult(
            relevance=relevance,
            policy_compliance=policy_compliance,
            clarity=clarity,
            completeness=completeness,
            hallucination_risk=hallucination_risk,
            overall_score=round(sum(scores) / len(scores)),
        )
        state["evaluation"] = result.model_dump()
        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        state["execution_metadata"]["evaluation_evidence"] = {
            "response_length": len(response),
            "decision_checked": decision_code,
            "internal_marker_found": contains_internal_marker,
        }
        return state