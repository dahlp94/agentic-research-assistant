from __future__ import annotations

import time
import uuid
from typing import Any, Dict

from langgraph.graph import StateGraph, END

from ara.core.state import ARAState, RunMetadata
from ara.core.policies import should_loop_back_to_research, mark_failed_if_still_unresolved
from ara.agents.planner import planner_node
from ara.agents.researcher import researcher_node
from ara.agents.critic import critic_node
from ara.agents.decider import decider_node


def build_graph() -> Any:
    g = StateGraph(ARAState)

    g.add_node("planner", planner_node)
    g.add_node("researcher", researcher_node)
    g.add_node("critic", critic_node)
    g.add_node("decider", decider_node)

    g.set_entry_point("planner")
    g.add_edge("planner", "researcher")
    g.add_edge("researcher", "critic")

    # conditional edge: loop back to researcher or proceed
    def route_after_critic(state: ARAState) -> str:
        if isinstance(state, dict):
            state = ARAState(**state)
        if should_loop_back_to_research(state):
            return "researcher"
        mark_failed_if_still_unresolved(state)
        return "decider"

    g.add_conditional_edges("critic", route_after_critic, {
        "researcher": "researcher",
        "decider": "decider",
    })

    g.add_edge("decider", END)
    return g.compile()


async def run_query(user_query: str, constraints: Dict[str, Any] | None = None) -> ARAState:
    run_id = str(uuid.uuid4())[:8]
    start = time.time()

    state = ARAState(
        user_query=user_query,
        constraints=constraints or {},
        run_metadata=RunMetadata(run_id=run_id),
    )

    graph = build_graph()
    out = await graph.ainvoke(state)

    # LangGraph may return a dict depending on version/config; normalize to ARAState.
    if isinstance(out, dict):
        out = ARAState(**out)

    latency_ms = int((time.time() - start) * 1000)
    if out.run_metadata:
        out.run_metadata.latency_ms = latency_ms

    return out
