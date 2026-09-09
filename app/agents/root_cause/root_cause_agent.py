from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.models.schemas import RootCauseAssessment


class RootCauseAgent(BaseAgent):
    name = "root_cause"

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        classification = state.get("classification") or {}
        tickets = state.get("previous_tickets") or []
        metrics = state.get("customer_metrics") or {}
        documents = state.get("retrieved_documents") or []

        factors: list[str] = []
        recurrence_detected = classification.get("recurrence_detected") is True
        related_ticket_count = len(tickets)
        if recurrence_detected or related_ticket_count >= 2:
            factors.append("histórico indica falha recorrente")
        if metrics.get("open_tickets", 0) > 0:
            factors.append("existem tickets em aberto")
        if classification.get("sentiment", "").casefold() in {"negativo", "muito negativo", "very_negative"}:
            factors.append("sentimento do cliente é negativo")
        if documents:
            factors.append("há política ou procedimento aplicável na base de conhecimento")

        high_risk = (
            recurrence_detected
            or related_ticket_count >= 2
            or metrics.get("open_tickets", 0) >= 2
            or classification.get("priority", "").casefold() in {"alta", "high", "critical", "crítica"}
        )
        if high_risk:
            risk_level = "high"
            recommendation = "Escalonar para avaliação técnica prioritária e consolidar o histórico do produto."
        elif factors:
            risk_level = "medium"
            recommendation = "Validar a cobertura aplicável e acompanhar o caso com base no procedimento encontrado."
        else:
            risk_level = "low"
            recommendation = "Solicitar informações adicionais antes de concluir a causa raiz."

        assessment = RootCauseAssessment(
            possible_root_cause=(
                "Falha técnica recorrente no produto, possivelmente relacionada à ausência de solução definitiva"
                if high_risk
                else "Causa técnica ainda não confirmada com as evidências disponíveis"
            ),
            contributing_factors=factors,
            risk_level=risk_level,
            recommendation=recommendation,
        )
        state["root_cause"] = assessment.model_dump()
        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        state["execution_metadata"]["root_cause_evidence"] = {
            "ticket_count": related_ticket_count,
            "open_tickets": metrics.get("open_tickets", 0),
            "knowledge_sources": [document.get("source") for document in documents],
        }
        return state