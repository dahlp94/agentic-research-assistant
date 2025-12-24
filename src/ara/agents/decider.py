from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ara.core.state import ARAState, Decision


DECIDER_SYS = """You are the Decider agent.

You must produce a final decision-quality answer for an applied engineering audience.

Rules:
- Use only the evidence provided. If evidence is weak, say so and reduce confidence.
- Provide: recommendation, rationale, tradeoffs, assumptions, next_steps, confidence (0-1).
- Also produce a markdown report for the user.

Return ONLY JSON:
{
  "decision": {
    "recommendation": "...",
    "rationale": "...",
    "tradeoffs": ["..."],
    "assumptions": ["..."],
    "confidence": 0.0,
    "next_steps": ["..."]
  },
  "final_answer_md": "..."
}
"""


def make_decider(model: str = "gpt-4o-mini", temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)


async def decider_node(state: ARAState) -> ARAState:
    if not state.plan:
        state.status = "failed"
        state.critic_notes.append("Missing plan; cannot decide.")
        return state

    llm = make_decider()
    payload = {
        "user_query": state.user_query,
        "plan": state.plan.model_dump(),
        "evidence": [e.model_dump() for e in state.evidence],
        "critic_notes": state.critic_notes,
        "status": state.status,
    }
    msgs = [SystemMessage(content=DECIDER_SYS), HumanMessage(content=str(payload))]
    resp = await llm.ainvoke(msgs)

    import json
    parsed = json.loads(resp.content)

    state.decision = Decision(**parsed["decision"])
    state.final_answer_md = parsed["final_answer_md"]
    state.add_trace("decider", {"raw": resp.content, "decision": state.decision.model_dump()})
    return state
