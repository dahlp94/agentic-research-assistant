from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    query: str = Field(..., min_length=3)
    constraints: Optional[Dict[str, Any]] = None


class RunResponse(BaseModel):
    run_id: str
    status: str
    final_answer_md: str | None
    decision: dict | None
    critic_notes: list[str]
