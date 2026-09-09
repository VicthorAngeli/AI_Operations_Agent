from __future__ import annotations

from app.agents.knowledge_agent.knowledge_agent import KnowledgeAgent
from app.rag.retriever import KnowledgeRetriever


def test_retriever_returns_ranked_operational_documents() -> None:
    documents = KnowledgeRetriever().search(
        "falha recorrente refrigerador garantia", top_k=2
    )

    assert documents
    assert documents[0]["score"] > 0
    assert documents[0]["source"] in {
        "recurring_failure_procedure.md",
        "warranty_policy.md",
    }
    assert documents[0]["matched_terms"]


def test_knowledge_agent_enriches_state_with_sources() -> None:
    state = {
        "user_request": "Meu refrigerador apresentou falha recorrente durante a garantia.",
        "classification": {"category": "refrigeracao", "recurrence_detected": True},
    }

    result = KnowledgeAgent().run(state)

    assert result["retrieved_documents"]
    assert result["execution_metadata"]["agents"] == ["knowledge_agent"]
    assert result["execution_metadata"]["knowledge_sources"]