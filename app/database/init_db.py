from __future__ import annotations

import sqlite3
from pathlib import Path

from app.config.settings import BASE_DIR, settings


def init_database() -> None:
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///./"):
        db_path = (BASE_DIR / db_url.replace("sqlite:///./", "", 1)).resolve()
    elif db_url.startswith("sqlite:///"):
        db_path = Path(db_url.replace("sqlite:///", "", 1)).resolve()
    else:
        db_path = (BASE_DIR / "ai_operations_agent.db").resolve()

    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                segment TEXT NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                warranty_days INTEGER NOT NULL,
                sku TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                issue_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                channel TEXT NOT NULL,
                summary TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS agent_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                duration_ms INTEGER,
                result TEXT
            );
            """
        )

        connection.execute(
            "INSERT OR IGNORE INTO customers (id, name, email, segment, status) VALUES (?, ?, ?, ?, ?)",
            (1001, "João Silva", "joao.silva@email.com", "premium", "active"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO customers (id, name, email, segment, status) VALUES (?, ?, ?, ?, ?)",
            (1002, "Maria Oliveira", "maria.oliveira@email.com", "standard", "active"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO customers (id, name, email, segment, status) VALUES (?, ?, ?, ?, ?)",
            (1003, "Pedro Souza", "pedro.souza@email.com", "vip", "at_risk"),
        )

        connection.execute(
            "INSERT OR IGNORE INTO products (id, name, category, warranty_days, sku) VALUES (?, ?, ?, ?, ?)",
            (2001, "Refrigerador Smart Pro", "refrigeracao", 365, "REF-001"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO products (id, name, category, warranty_days, sku) VALUES (?, ?, ?, ?, ?)",
            (2002, "Lavadora EcoMax", "lavanderia", 540, "LAV-002"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO products (id, name, category, warranty_days, sku) VALUES (?, ?, ?, ?, ?)",
            (2003, "Ar Condicionado Flex", "climatizacao", 730, "AC-003"),
        )

        connection.execute(
            "INSERT OR IGNORE INTO tickets (id, customer_id, product_id, issue_type, priority, status, description, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, 1001, 2001, "refrigeracao", "HIGH", "resolved", "Refrigerador desligou durante a noite.", "2025-01-10T10:00:00"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO tickets (id, customer_id, product_id, issue_type, priority, status, description, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (2, 1001, 2001, "refrigeracao", "HIGH", "open", "Refrigerador não estabiliza a temperatura.", "2025-04-05T08:40:00"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO tickets (id, customer_id, product_id, issue_type, priority, status, description, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (3, 1001, 2001, "refrigeracao", "HIGH", "open", "Cliente reporta nova falha e pouca resposta da assistência.", "2026-09-01T09:15:00"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO tickets (id, customer_id, product_id, issue_type, priority, status, description, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (4, 1002, 2002, "lavanderia", "MEDIUM", "resolved", "Lavadora apresentou vazamento no painel.", "2026-02-14T15:00:00"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO tickets (id, customer_id, product_id, issue_type, priority, status, description, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (5, 1003, 2003, "climatizacao", "CRITICAL", "open", "Ar-condicionado sem refrigeração após manutenção.", "2026-08-22T11:10:00"),
        )

        connection.execute(
            "INSERT OR IGNORE INTO interactions (id, customer_id, channel, summary, sentiment, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (1, 1001, "whatsapp", "Cliente relata problema recorrente no refrigerador.", "negative", "2026-08-29T10:00:00"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO interactions (id, customer_id, channel, summary, sentiment, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (2, 1001, "call_center", "Cliente solicita solução urgente e reclama da falta de resposta.", "very_negative", "2026-09-01T09:20:00"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO interactions (id, customer_id, channel, summary, sentiment, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (3, 1002, "email", "Cliente questiona validade da garantia após falha técnica.", "neutral", "2026-05-09T17:30:00"),
        )

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized.")
