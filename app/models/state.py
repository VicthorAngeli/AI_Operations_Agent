from __future__ import annotations

from typing import Any, TypedDict, NotRequired


class AgentState(TypedDict):
    user_request: str
    customer_id: NotRequired[int | None]
    customer_data: NotRequired[dict[str, Any] | None]
    customer_history: NotRequired[list[dict[str, Any]]]
    previous_tickets: NotRequired[list[dict[str, Any]]]
    customer_metrics: NotRequired[dict[str, Any]]
    product_data: NotRequired[dict[str, Any] | None]
    classification: NotRequired[dict[str, Any] | None]
    retrieved_documents: NotRequired[list[dict[str, Any]]]
    root_cause: NotRequired[dict[str, Any] | None]
    decision: NotRequired[dict[str, Any] | None]
    final_response: NotRequired[str]
    evaluation: NotRequired[dict[str, Any] | None]
    errors: NotRequired[list[str]]
    execution_metadata: NotRequired[dict[str, Any]]
