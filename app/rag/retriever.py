from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app.config.settings import BASE_DIR


_TOKEN_PATTERN = re.compile(r"[a-záàâãéêíóôõúç0-9]+", re.IGNORECASE)
_STOP_WORDS = {
    "a", "as", "com", "da", "de", "do", "e", "em", "o", "os", "para",
    "por", "que", "se", "um", "uma", "na", "no", "nas", "nos", "sobre",
}


class KnowledgeRetriever:
    """Retrieve operational knowledge documents using a deterministic local index."""

    def __init__(self, knowledge_dir: Path | None = None) -> None:
        self.knowledge_dir = knowledge_dir or BASE_DIR / "data" / "knowledge_base"

    def _documents(self) -> list[dict[str, Any]]:
        documents = []
        for path in sorted(self.knowledge_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            title = text.splitlines()[0].removeprefix("# ").strip() or path.stem
            documents.append({"source": path.name, "title": title, "content": text})
        return documents

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token.casefold()
            for token in _TOKEN_PATTERN.findall(text)
            if token.casefold() not in _STOP_WORDS
        }

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        if not query.strip() or top_k <= 0:
            return []

        query_tokens = self._tokens(query)
        ranked: list[dict[str, Any]] = []
        for document in self._documents():
            document_tokens = self._tokens(document["content"])
            matches = query_tokens & document_tokens
            if not matches:
                continue
            result = dict(document)
            result["score"] = round(len(matches) / max(len(query_tokens), 1), 4)
            result["matched_terms"] = sorted(matches)
            ranked.append(result)

        ranked.sort(key=lambda item: (-item["score"], item["source"]))
        return ranked[:top_k]