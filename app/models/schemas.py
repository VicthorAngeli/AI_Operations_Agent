from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    customer_id: int = Field(..., ge=1)
    message: str = Field(..., min_length=5, max_length=5000)


class CustomerAnalysis(BaseModel):
    intent: str
    category: str
    subcategory: str
    sentiment: str
    priority: str
    urgency: str
    recurrence_detected: bool = False


class RootCauseAssessment(BaseModel):
    possible_root_cause: str
    contributing_factors: list[str] = Field(default_factory=list)
    risk_level: str
    recommendation: str


class DecisionOutcome(BaseModel):
    decision: str
    justification: str
    escalated: bool = False


class EvaluationResult(BaseModel):
    relevance: int = Field(ge=0, le=100)
    policy_compliance: int = Field(ge=0, le=100)
    clarity: int = Field(ge=0, le=100)
    completeness: int = Field(ge=0, le=100)
    hallucination_risk: str
    overall_score: int = Field(ge=0, le=100)


class ExecutionResult(BaseModel):
    execution_id: str
    customer_id: int
    summary: str
    classification: dict[str, Any] | None = None
    decision: dict[str, Any] | None = None
    final_response: str | None = None
    evaluation: dict[str, Any] | None = None
