from dotenv import load_dotenv
load_dotenv()

from __future__ import annotations

from fastapi import FastAPI
from ara.api.schemas import RunRequest, RunResponse
from ara.core.runner import run_query
from ara.core.tracing import write_run_artifacts

app = FastAPI(title="Agentic Research Assistant", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}


@app.post("/run", response_model=RunResponse)
async def run(req: RunRequest) -> RunResponse:
    state = await run_query(req.query, constraints=req.constraints or {})
    _ = write_run_artifacts(state)

    run_id = state.run_metadata.run_id if state.run_metadata else "run"
    return RunResponse(
        run_id=run_id,
        status=state.status,
        final_answer_md=state.final_answer_md,
        decision=state.decision.model_dump() if state.decision else None,
        critic_notes=state.critic_notes,
    )
