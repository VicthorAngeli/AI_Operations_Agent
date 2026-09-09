from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.models.schemas import DecisionOutcome


class DecisionAgent(BaseAgent):
    name = "decision"

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        classification = state.get("classification") or {}
        root_cause = state.get("root_cause") or {}
        metrics = state.get("customer_metrics") or {}
        documents = state.get("retrieved_documents") or []

        risk_level = str(root_cause.get("risk_level", "low")).casefold()
        priority = str(classification.get("priority", "")).casefold()
        recurrence = classification.get("recurrence_detected") is True
        open_tickets = metrics.get("open_tickets", 0)
        high_priority = priority in {"alta", "high", "crítica", "critical"}
        escalated = risk_level == "high" or (high_priority and (recurrence or open_tickets > 0))

        if escalated:
            decision = "escalate_technical"
            justification = (
                "Escalonar para avaliação técnica prioritária devido ao risco operacional, "
                "histórico do caso e evidências disponíveis."
            )
        elif risk_level == "medium":
            decision = "continue_investigation"
            justification = (
                "Continuar a investigação, validar a política aplicável e acompanhar a resolução "
                "antes de encerrar o atendimento."
            )
        else:
            decision = "provide_initial_guidance"
            justification = (
                "Fornecer orientação inicial e solicitar informações adicionais, pois não há "
                "evidências suficientes para uma ação de maior impacto."
            )

        outcome = DecisionOutcome(
            decision=decision,
            justification=justification,
            escalated=escalated,
        )
        state["decision"] = outcome.model_dump()
        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        state["execution_metadata"]["decision_evidence"] = {
            "risk_level": risk_level,
            "priority": priority,
            "recurrence_detected": recurrence,
            "open_tickets": open_tickets,
            "knowledge_sources_count": len(documents),
        }
        return state