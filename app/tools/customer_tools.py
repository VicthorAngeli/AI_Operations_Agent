from __future__ import annotations

from typing import Any

from app.database.repository import DatabaseRepository


def get_customer(customer_id: int) -> dict[str, Any] | None:
    repository = DatabaseRepository()
    return repository.fetch_customer(customer_id)


def get_customer_history(customer_id: int) -> list[dict[str, Any]]:
    repository = DatabaseRepository()
    return repository.fetch_customer_history(customer_id)


def get_product(product_id: int) -> dict[str, Any] | None:
    repository = DatabaseRepository()
    return repository.fetch_product(product_id)


def get_previous_tickets(customer_id: int) -> list[dict[str, Any]]:
    repository = DatabaseRepository()
    return repository.fetch_customer_tickets(customer_id)


def get_customer_metrics(customer_id: int) -> dict[str, Any]:
    repository = DatabaseRepository()
    tickets = repository.fetch_customer_tickets(customer_id)
    interactions = repository.fetch_customer_history(customer_id)
    return {
        "customer_id": customer_id,
        "total_tickets": len(tickets),
        "open_tickets": sum(1 for item in tickets if item["status"] == "open"),
        "resolved_tickets": sum(1 for item in tickets if item["status"] == "resolved"),
        "interaction_count": len(interactions),
        "last_sentiment": interactions[0]["sentiment"] if interactions else "unknown",
    }
