from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent
from app.rag.retriever import KnowledgeRetriever


class KnowledgeAgent(BaseAgent):
    name = "knowledge_agent"

    def __init__(self, retriever: KnowledgeRetriever | None = None) -> None:
        self.retriever = retriever or KnowledgeRetriever()

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        query_parts = [state.get("user_request", "")]
        classification = state.get("classification") or {}
        query_parts.extend(str(value) for value in classification.values())
        documents = self.retriever.search(" ".join(query_parts))

        state["retrieved_documents"] = documents
        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        state["execution_metadata"]["knowledge_sources"] = [
            document["source"] for document in documents
        ]
        return state