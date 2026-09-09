from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from app.config.settings import BASE_DIR, settings


class DatabaseRepository:
    """Thin repository layer that encapsulates SQLite access."""

    def __init__(self, database_path: str | None = None) -> None:
        self.database_path = database_path or self._resolve_database_path()

    @staticmethod
    def _resolve_database_path() -> str:
        db_url = settings.DATABASE_URL
        if db_url.startswith("sqlite://"):
            if db_url.startswith("sqlite:///"):
                candidate = db_url.replace("sqlite:///", "", 1)
                if candidate.startswith("./"):
                    return str((BASE_DIR / candidate[2:]).resolve())
                return str(Path(candidate).resolve())
            if db_url.startswith("sqlite:///./"):
                relative = db_url.replace("sqlite:///./", "", 1)
                return str((BASE_DIR / relative).resolve())
        return db_url.replace("sqlite://", "")

    def get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()

    def fetch_customer(self, customer_id: int) -> dict[str, Any] | None:
        row = self.fetch_one(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,),
        )
        return dict(row) if row else None

    def fetch_customer_history(self, customer_id: int) -> list[dict[str, Any]]:
        rows = self.execute(
            """
            SELECT *
            FROM interactions
            WHERE customer_id = ?
            ORDER BY created_at DESC
            """,
            (customer_id,),
        )
        return [dict(row) for row in rows]

    def fetch_customer_tickets(self, customer_id: int) -> list[dict[str, Any]]:
        rows = self.execute(
            """
            SELECT *
            FROM tickets
            WHERE customer_id = ?
            ORDER BY created_at DESC
            """,
            (customer_id,),
        )
        return [dict(row) for row in rows]

    def fetch_product(self, product_id: int) -> dict[str, Any] | None:
        row = self.fetch_one(
            "SELECT * FROM products WHERE id = ?",
            (product_id,),
        )
        return dict(row) if row else None

    def save_agent_execution(
        self,
        execution_id: str,
        agent_name: str,
        started_at: str,
        finished_at: str,
        duration_ms: int,
        result: dict[str, Any],
    ) -> None:
        with self.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO agent_executions
                    (execution_id, agent_name, started_at, finished_at, duration_ms, result)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    execution_id,
                    agent_name,
                    started_at,
                    finished_at,
                    duration_ms,
                    json.dumps(result, ensure_ascii=False),
                ),
            )

    def fetch_execution(self, execution_id: str) -> list[dict[str, Any]]:
        rows = self.execute(
            """
            SELECT execution_id, agent_name, started_at, finished_at, duration_ms, result
            FROM agent_executions
            WHERE execution_id = ?
            ORDER BY id ASC
            """,
            (execution_id,),
        )
        return [
            {
                **dict(row),
                "result": json.loads(row["result"]) if row["result"] else None,
            }
            for row in rows
        ]
