from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    step_id: int
    tool: str
    reason: str
    args: dict[str, Any] = Field(default_factory=dict)


class AnalysisPlan(BaseModel):
    user_question: str
    interpretation: str
    steps: list[PlanStep]
    final_answer_style: str = "summary"
