# Agentic Research & Decision Assistant (LangGraph)

A portfolio-grade multi-agent system that:
- decomposes a user task (Planner)
- gathers evidence (Researcher)
- critiques for missing support / weak logic (Critic)
- outputs a final recommendation + tradeoffs + confidence (Decider)

This repo is optimized for **Applied AI Engineer** roles:
- clean modular architecture
- typed state & structured outputs
- bounded critique loops for reliability
- tracing + run artifacts
- FastAPI integration

## Architecture (high level)

User Query
  -> Planner (JSON plan + research questions + rubric)
  -> Researcher (evidence notes + citations)
  -> Critic (issues / missing evidence)
  -> [if issues] Targeted research loop (bounded)
  -> Decider (final recommendation, tradeoffs, confidence)
  -> Outputs: JSON trace + Markdown report

## Quickstart

```bash
pip install -e .
export OPENAI_API_KEY="..."
python scripts/run_local.py "Compare Redis vs Postgres for caching LLM outputs. Recommend one."
uvicorn ara.api.app:app --reload --port 8000
````

POST `/run`:

```json
{"query":"Pick a vector DB for a small team shipping RAG. Compare FAISS, Qdrant, Pinecone."}
```

## Notes

* Tools are intentionally minimal. For production:

  * add a real web search tool (SerpAPI/Bing/etc)
  * add retrieval memory (vector store)
  * add caching and model routing
  * add auth + rate limiting


## Current Status

- Multi-agent pipeline (Planner → Researcher → Critic → Decider) implemented
- Safety-first behavior: system refuses to hallucinate without evidence
- Placeholder web search used for development; real search integration planned
- CLI + FastAPI interface available
- Run artifacts (JSON + Markdown) persisted for traceability
