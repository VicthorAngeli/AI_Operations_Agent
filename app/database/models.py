from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Customer:
    id: int
    name: str
    email: str
    segment: str
    status: str


@dataclass
class Product:
    id: int
    name: str
    category: str
    warranty_days: int
    sku: str


@dataclass
class Ticket:
    id: int
    customer_id: int
    product_id: int
    issue_type: str
    priority: str
    status: str
    description: str
    created_at: str


@dataclass
class Interaction:
    id: int
    customer_id: int
    channel: str
    summary: str
    sentiment: str
    created_at: str


@dataclass
class AgentExecution:
    id: int
    execution_id: str
    agent_name: str
    started_at: str
    finished_at: str | None
    duration_ms: int | None
    result: dict[str, Any] | None
