from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

SINGLE_AGENT_SYS = """You are a single-pass assistant.

Answer the user's question directly.
Be helpful and concise.
Do not mention agents, plans, or critiques.
"""

def run_single_agent(query: str, model: str = "gpt-4o-mini") -> dict:
    llm = ChatOpenAI(model=model, temperature=0.2)

    msgs = [
        SystemMessage(content=SINGLE_AGENT_SYS),
        HumanMessage(content=query),
    ]

    resp = llm.invoke(msgs)

    return {
        "final_answer": resp.content,
        "confidence": None,  # baseline does not self-calibrate
        "citations": None,   # baseline is ungrounded
    }
