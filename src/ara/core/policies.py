from __future__ import annotations

from ara.core.state import ARAState


def should_loop_back_to_research(state: ARAState) -> bool:
    """Bounded critique loop policy."""
    if state.status != "needs_more_research":
        return False
    return state.critique_round < state.max_critique_rounds


def mark_failed_if_still_unresolved(state: ARAState) -> None:
    if state.status == "needs_more_research" and state.critique_round >= state.max_critique_rounds:
        state.status = "failed"
        state.critic_notes.append(
            "Max critique rounds reached. Returning best-effort output with uncertainty."
        )
