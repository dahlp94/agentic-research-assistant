from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A lightweight citation object. In production, include URL + publisher + retrieved_at."""
    source: str = Field(..., description="Where this evidence came from (url/title).")
    snippet: str = Field(..., description="Short supporting excerpt or paraphrase.")
    confidence: float = Field(0.7, ge=0.0, le=1.0)


class EvidenceItem(BaseModel):
    question: str
    claim: str
    citations: List[Citation] = Field(default_factory=list)


class Plan(BaseModel):
    task_type: str = Field(..., description="e.g., compare/recommend, summarize, debug, design")
    deliverables: List[str] = Field(default_factory=list)
    research_questions: List[str] = Field(default_factory=list)
    rubric: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)


class Decision(BaseModel):
    recommendation: str
    rationale: str
    tradeoffs: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    confidence: float = Field(0.6, ge=0.0, le=1.0)
    next_steps: List[str] = Field(default_factory=list)


RunStatus = Literal["ok", "needs_more_research", "failed"]


class RunMetadata(BaseModel):
    run_id: str
    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    cost_usd: float = 0.0


class ARAState(BaseModel):
    user_query: str
    constraints: Dict[str, Any] = Field(default_factory=dict)

    plan: Optional[Plan] = None
    evidence: List[EvidenceItem] = Field(default_factory=list)

    critic_notes: List[str] = Field(default_factory=list)
    status: RunStatus = "ok"

    decision: Optional[Decision] = None
    final_answer_md: Optional[str] = None

    critique_round: int = 0
    max_critique_rounds: int = 2

    run_metadata: Optional[RunMetadata] = None

    # tracing
    trace: List[Dict[str, Any]] = Field(default_factory=list)

    def add_trace(self, node: str, payload: Dict[str, Any]) -> None:
        self.trace.append({"node": node, **payload})
