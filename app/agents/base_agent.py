from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Base class for all specialized agents."""

    name: str = "base_agent"

    @abstractmethod
    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
