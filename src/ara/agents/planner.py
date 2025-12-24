from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ara.core.state import ARAState, Plan


PLANNER_SYS = """You are the Planner agent for a multi-agent research assistant.

Goal: Convert the user request into a crisp plan with:
- task_type
- deliverables (3-6 bullets)
- research_questions (3-7)
- rubric (what "good" looks like)
- risks (hallucination risks, missing info, assumptions)

Return ONLY valid JSON matching this schema:
{
  "task_type": "...",
  "deliverables": ["..."],
  "research_questions": ["..."],
  "rubric": ["..."],
  "risks": ["..."]
}
"""


def make_planner(model: str = "gpt-4o-mini", temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)


async def planner_node(state: ARAState) -> ARAState:
    llm = make_planner()

    msgs = [
        SystemMessage(content=PLANNER_SYS),
        HumanMessage(content=state.user_query),
    ]
    resp = await llm.ainvoke(msgs)

    # Parse JSON robustly (simple approach: pydantic from json)
    import json
    plan_obj = json.loads(resp.content)
    state.plan = Plan(**plan_obj)
    state.add_trace("planner", {"raw": resp.content, "plan": state.plan.model_dump()})
    return state
