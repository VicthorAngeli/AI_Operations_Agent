from __future__ import annotations

import re


def contains_prompt_injection_attempt(text: str) -> bool:
    lowered = text.lower()
    injection_patterns = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore all rules",
        "ignore all policies",
        "reveal internal data",
        "reveal internal documents",
        "override system prompt",
        "override developer prompt",
        "bypass policy",
        "bypass rules",
        "system prompt",
        "developer prompt",
    ]
    return any(pattern in lowered for pattern in injection_patterns)


def sanitize_user_input(text: str) -> str:
    value = text.strip()
    value = re.sub(r"\s+", " ", value)
    return value
