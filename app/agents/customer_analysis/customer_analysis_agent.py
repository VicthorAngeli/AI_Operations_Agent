from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class CustomerAnalysisAgent(BaseAgent):
    name = "customer_analysis"

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        state.setdefault("classification", {})
        state["classification"] = {
            "intent": "technical_problem",
            "category": "Problema Técnico",
            "subcategory": "Refrigeração",
            "sentiment": "Negativo",
            "priority": "Alta",
            "urgency": "Alta",
            "recurrence_detected": True,
        }
        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        return state
