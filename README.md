# Agentic Research & Decision Assistant (LangGraph)

A **production-oriented multi-agent AI system** for structured research and decision-making, built with explicit orchestration, safety checks, and traceable outputs.

This project is designed as an **Applied AI Engineer portfolio artifact**, emphasizing **reliability, debuggability, and ownership of outcomes** over prompt-only demos.


## 🔍 Problem Statement

Teams increasingly rely on LLMs for research and decision-making, but most agent-based systems:

* hallucinate confidently when evidence is weak
* lack traceability into intermediate reasoning
* fail silently or unpredictably
* are difficult to debug or evaluate

**This project explores how explicit agent orchestration, validation, and failure modes can make LLM-based decision systems safer and more production-ready.**


## 🧪 Product Hypotheses

This system is built around a set of testable hypotheses:

1. **Structured multi-agent workflows reduce hallucinations** compared to single-agent prompting.
2. **Explicit validation and failure modes improve trust** over fluent but unsupported answers.
3. **Tool and evidence quality dominate model size** for decision quality in research tasks.
4. **Inspectable intermediate state enables faster iteration and debugging** in agent systems.

The architecture and planned evaluations are designed to validate these hypotheses incrementally.


## 🔁 What This System Does

Given an open-ended task (for example: *“Compare X vs Y and recommend one”*), the system executes a **multi-agent workflow**:

* **Planner** — decomposes the task into research questions, deliverables, evaluation rubric, and risks
* **Researcher** — gathers evidence and produces structured claims with citations
* **Critic** — validates evidence quality, flags unsupported claims, missing counterarguments, and unclear assumptions
* **Decider** — synthesizes a final recommendation with tradeoffs, confidence, and next steps

The system is intentionally **safety-first**: when evidence is insufficient, it lowers confidence or requests additional research instead of hallucinating.


## 🧠 Why LangGraph?

This project uses **LangGraph** to model agent execution as an explicit **graph / state machine**, rather than an opaque chain of prompts.

This enables:

* bounded retry loops (no runaway agents)
* deterministic routing logic
* inspectable intermediate state
* clean separation between agent roles

These properties are critical for **production-grade agent systems**, where reliability and control matter more than raw fluency.


## 🏗️ Architecture (High Level)

```
User Query
   ↓
Planner
  (task type, research questions, rubric, risks)
   ↓
Researcher
  (claims + citations)
   ↓
Critic
  ├─ if issues found → targeted re-research (bounded)
  └─ else
   ↓
Decider
  (recommendation, tradeoffs, confidence)
   ↓
Artifacts
  - JSON execution trace (full state)
  - Markdown report (user-facing output)
```

All agents operate over a **shared, typed state**, making execution fully traceable and debuggable.


## 📁 Repository Structure

```txt
agentic-research-assistant/
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── src/
│   └── ara/
│       ├── api/                 # FastAPI service layer
│       ├── agents/              # Role-specialized agents
│       ├── core/                # Orchestration, state, policies
│       ├── tools/               # External tool interfaces
│       └── __init__.py
│
├── scripts/
│   └── run_local.py             # CLI entry point
│
├── outputs/
│   └── sample_runs/             # JSON traces & Markdown reports
│
└── tests/
    └── test_state_machine.py
```

This structure cleanly separates **agent logic**, **control flow**, and **infrastructure concerns**, enabling incremental extension as the system grows.


## 🚀 Quickstart

### Local CLI

```bash
pip install -e .
python scripts/run_local.py "Compare Redis vs Postgres for caching LLM outputs. Recommend one."
```

### API

```bash
uvicorn ara.api.app:app --reload --port 8000
```

POST `/run`:

```json
{
  "query": "Pick a vector database for a small team shipping RAG. Compare FAISS, Qdrant, and Pinecone."
}
```

Each run produces **auditable artifacts** in `outputs/sample_runs/`.


## 🛡️ Safety & Reliability Features

* **Typed shared state** (Pydantic)
* **Critic-driven validation** of evidence quality
* **Explicit failure modes** when evidence is insufficient
* **Bounded retry loops** to prevent infinite agent cycles
* **Deterministic artifacts** for auditing and debugging

These design choices reflect real-world constraints in enterprise AI systems.


## 🧩 Key Design Decisions

This project prioritizes **controlled execution and observability** over raw generation quality.

* **Explicit agent roles** improve debuggability and isolate failures
* **LangGraph orchestration** enables deterministic routing and bounded retries
* **Typed shared state** prevents schema drift and supports validation
* **Critic agent** enforces evidence quality and reduces hallucinations
* **Artifact-first outputs** enable offline evaluation and inspection
* **Safety over fluency**: low confidence is preferred to unsupported certainty


## 📦 Project Status

**Implemented**

* Planner → Researcher → Critic → Decider pipeline
* LangGraph orchestration with conditional routing
* CLI + FastAPI interface
* Full execution artifacts (JSON + Markdown)
* Safe failure behavior

**Planned / In Progress**

* Real web search integration
* Citation quality scoring
* Cost & latency tracking per agent
* Offline evaluation harness
* Caching and model routing


## 🎯 Intended Audience

This project is designed to demonstrate skills relevant to:

* Applied AI Engineer
* LLM Platform Engineer
* Agentic Systems Engineer

It emphasizes **system design, reliability, and ownership**, not prompt hacking.


## 📌 Key Takeaway

> This repository demonstrates how to move from an ambiguous problem to a **production-oriented agentic AI system** by forming testable hypotheses, validating behavior early, and iterating toward reliable, inspectable outcomes.
