from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.tools.customer_tools import (
    get_customer,
    get_customer_history,
    get_customer_metrics,
    get_previous_tickets,
    get_product,
)


class DataAgent(BaseAgent):
    name = "data_agent"

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        customer_id = state.get("customer_id")
        if not customer_id:
            raise ValueError("customer_id is required for DataAgent.")

        customer = get_customer(customer_id)
        history = get_customer_history(customer_id)
        tickets = get_previous_tickets(customer_id)
        metrics = get_customer_metrics(customer_id)

        product_id = tickets[0]["product_id"] if tickets else None
        product = get_product(product_id) if product_id else None

        state["customer_data"] = customer
        state["customer_history"] = history
        state["previous_tickets"] = tickets
        state["customer_metrics"] = metrics
        state["product_data"] = product

        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        state["execution_metadata"]["tools_used"] = [
            "get_customer",
            "get_customer_history",
            "get_previous_tickets",
            "get_customer_metrics",
            "get_product",
        ]
        return state
