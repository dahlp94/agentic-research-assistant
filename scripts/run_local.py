from dotenv import load_dotenv
load_dotenv()

#import os
#print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))


import asyncio
import sys
from rich import print

from ara.core.runner import run_query
from ara.core.tracing import write_run_artifacts


async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_local.py \"your query\"")
        raise SystemExit(1)

    q = sys.argv[1]
    state = await run_query(q, constraints={"audience": "applied_ai_engineer"})

    print(f"[bold]Run ID:[/bold] {state.run_metadata.run_id if state.run_metadata else 'run'}")
    print(f"[bold]Status:[/bold] {state.status}")
    if state.critic_notes:
        print("[bold]Critic notes:[/bold]")
        for n in state.critic_notes:
            print(f" - {n}")

    if state.final_answer_md:
        print("\n[bold]Final Answer (Markdown):[/bold]\n")
        print(state.final_answer_md)

    path = write_run_artifacts(state)
    print(f"\n[dim]Wrote artifacts to {path}[/dim]")


if __name__ == "__main__":
    asyncio.run(main())
