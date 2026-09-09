from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class OrchestratorAgent(BaseAgent):
    name = "orchestrator"

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        state["execution_metadata"]["status"] = "orchestrator_ready"
        return state
