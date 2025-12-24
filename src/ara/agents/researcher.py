from __future__ import annotations

from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ara.core.state import ARAState, EvidenceItem, Citation
from ara.tools.web_search import search_web

RESEARCHER_SYS = """You are the Researcher agent.

You will be given:
- a single research question
- optional constraints

Task:
1) Propose 2-4 key claims that answer the question.
2) For each claim, attach at least 1 citation object from provided search results.
3) Be conservative: if search results are weak placeholders, state uncertainty.

Return ONLY JSON list matching:
[
  {
    "question": "...",
    "claim": "...",
    "citations": [{"source":"...","snippet":"...","confidence":0.0}]
  }
]
"""


def make_researcher(model: str = "gpt-4o-mini", temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)


async def researcher_node(state: ARAState) -> ARAState:
    if not state.plan:
        state.status = "failed"
        state.critic_notes.append("Missing plan; cannot research.")
        return state

    llm = make_researcher()
    all_items: List[EvidenceItem] = []

    for q in state.plan.research_questions:
        results = search_web(q, k=5)
        prompt = {
            "question": q,
            "constraints": state.constraints,
            "search_results": results,
        }

        msgs = [
            SystemMessage(content=RESEARCHER_SYS),
            HumanMessage(content=str(prompt)),
        ]
        resp = await llm.ainvoke(msgs)

        import json
        parsed = json.loads(resp.content)
        for item in parsed:
            # pydantic validation
            ev = EvidenceItem(
                question=item["question"],
                claim=item["claim"],
                citations=[Citation(**c) for c in item.get("citations", [])],
            )
            all_items.append(ev)

        state.add_trace("researcher", {"question": q, "raw": resp.content, "results": results})

    # Replace evidence each run to keep it simple; in v2 you can merge/dedupe.
    state.evidence = all_items
    return state
