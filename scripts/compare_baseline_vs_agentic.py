from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from datetime import datetime

from ara.core.runner import run_query
from ara.baselines.single_agent import run_single_agent


TASKS = [
    "What is LangGraph and why use it?",
    "Compare FAISS vs Pinecone for a small startup.",
    "Should a team use LangGraph or AutoGen for production agents?",
]

async def main():
    results = []

    for q in TASKS:
        print(f"\n=== TASK ===\n{q}\n")

        # Baseline
        baseline_out = run_single_agent(q)
        print("Baseline done.")

        # Agentic
        agentic_state = await run_query(q)
        print("Agentic done.")

        row = {
            "query": q,
            "baseline_answer": baseline_out["final_answer"],
            "agentic_answer": agentic_state.final_answer_md,
            "agentic_status": agentic_state.status,
            "critic_notes": agentic_state.critic_notes,
            "agentic_confidence": (
                agentic_state.decision.confidence
                if agentic_state.decision
                else None
            ),
        }
        results.append(row)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = f"outputs/comparisons/baseline_vs_agentic_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nWrote comparison results to {out_path}")

if __name__ == "__main__":
    asyncio.run(main())
