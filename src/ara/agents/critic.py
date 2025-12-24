from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ara.core.state import ARAState
from ara.tools.citations import groundedness_score, enforce_min_citations


CRITIC_SYS = """You are the Critic agent.

Given the plan + evidence items, identify:
- missing research coverage (rubric not addressed)
- unsupported claims (no citations)
- weak evidence quality
- missing counterarguments
- unclear assumptions

Return ONLY JSON:
{
  "status": "ok" | "needs_more_research",
  "notes": ["... actionable fix ...", ...],
  "target_questions": ["... targeted research question to add ...", ...]
}
"""


def make_critic(model: str = "gpt-4o-mini", temperature: float = 0.0) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)


async def critic_node(state: ARAState) -> ARAState:
    if not state.plan:
        state.status = "failed"
        state.critic_notes.append("Missing plan; cannot critique.")
        return state

    # Hard checks first (engineering guardrails)
    issues = enforce_min_citations(state.evidence, min_citations=1)
    g = groundedness_score(state.evidence)

    llm = make_critic()
    payload = {
        "plan": state.plan.model_dump(),
        "rubric": state.plan.rubric,
        "evidence": [e.model_dump() for e in state.evidence],
        "hard_checks": {"citation_issues": issues, "groundedness": g},
    }

    msgs = [SystemMessage(content=CRITIC_SYS), HumanMessage(content=str(payload))]
    resp = await llm.ainvoke(msgs)

    import json
    parsed = json.loads(resp.content)

    state.status = parsed["status"]
    state.critic_notes = parsed.get("notes", [])
    target_questions = parsed.get("target_questions", [])

    state.add_trace("critic", {"raw": resp.content, "hard_checks": payload["hard_checks"]})

    # If we need more research, append targeted questions (bounded by loop)
    if state.status == "needs_more_research" and target_questions:
        # Avoid runaway growth
        for tq in target_questions[:3]:
            if tq not in state.plan.research_questions:
                state.plan.research_questions.append(tq)

    # increment critique round
    state.critique_round += 1
    return state
