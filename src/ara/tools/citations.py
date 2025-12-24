from __future__ import annotations

from typing import List
from ara.core.state import EvidenceItem


def groundedness_score(evidence: List[EvidenceItem]) -> float:
    """Fraction of evidence items that have at least one citation."""
    if not evidence:
        return 0.0
    grounded = sum(1 for e in evidence if len(e.citations) > 0)
    return grounded / len(evidence)


def enforce_min_citations(evidence: List[EvidenceItem], min_citations: int = 1) -> List[str]:
    """Return issues if any evidence item lacks citations."""
    issues: List[str] = []
    for i, e in enumerate(evidence):
        if len(e.citations) < min_citations:
            issues.append(f"Evidence item #{i+1} for question '{e.question}' needs citations.")
    return issues
