from __future__ import annotations

from app.agents.data_agent.data_agent import DataAgent
from app.database.init_db import init_database
from app.tools.customer_tools import (
    get_customer,
    get_customer_history,
    get_customer_metrics,
    get_previous_tickets,
    get_product,
)


def test_data_tools_return_expected_values() -> None:
    init_database()

    customer = get_customer(1001)
    assert customer is not None
    assert customer["name"] == "João Silva"

    history = get_customer_history(1001)
    assert len(history) >= 1

    product = get_product(2001)
    assert product is not None
    assert product["category"] == "refrigeracao"

    tickets = get_previous_tickets(1001)
    assert len(tickets) >= 2

    metrics = get_customer_metrics(1001)
    assert metrics["customer_id"] == 1001
    assert metrics["open_tickets"] >= 0


def test_data_agent_enriches_state() -> None:
    init_database()

    state = {"customer_id": 1001, "user_request": "Meu refrigerador parou de funcionar novamente."}
    result = DataAgent().run(state)

    assert result["customer_data"]["id"] == 1001
    assert len(result["customer_history"]) >= 1
    assert result["customer_metrics"]["customer_id"] == 1001
