# Agentic Research & Decision Assistant (LangGraph)

A **production-oriented multi-agent AI system** that performs structured research and decision-making using explicit orchestration, safety checks, and traceable outputs.

This project is designed as an **Applied AI Engineer portfolio artifact**, emphasizing **reliability, debuggability, and system design** over prompt-only demos.

---

## 🔍 What This System Does

Given an open-ended task (for example: *“Compare X vs Y and recommend one”*), the system runs a **multi-agent workflow**:

* **Planner** — decomposes the task into research questions, deliverables, and a rubric
* **Researcher** — gathers evidence and produces structured claims with citations
* **Critic** — checks for unsupported claims, weak evidence, missing counterarguments, and unclear assumptions
* **Decider** — synthesizes a final recommendation with tradeoffs, confidence, and next steps

The system is intentionally **safety-first**: when evidence is insufficient, it lowers confidence or requests additional research instead of hallucinating.

---

## 🧠 Why LangGraph?

This project uses **LangGraph** to model agent execution as an explicit **graph / state machine**, rather than an opaque chain of prompts.

This enables:

* bounded retry loops (no runaway agents)
* deterministic routing logic
* inspectable intermediate state
* clean separation between agents

These properties are critical for **production agent systems**.

---

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
  - JSON trace (full execution state)
  - Markdown report (user-facing output)
```

All agents operate over a **shared typed state**, making execution traceable and debuggable.

---

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
│       │   ├── app.py
│       │   └── schemas.py
│       │
│       ├── agents/              # Role-specialized agents
│       │   ├── planner.py
│       │   ├── researcher.py
│       │   ├── critic.py
│       │   └── decider.py
│       │
│       ├── core/                # Orchestration & shared logic
│       │   ├── state.py         # Typed shared state (Pydantic)
│       │   ├── runner.py        # LangGraph wiring & execution
│       │   ├── policies.py      # Retry & safety policies
│       │   └── tracing.py       # Artifact persistence
│       │
│       ├── tools/               # External tool interfaces
│       │   ├── web_search.py
│       │   └── citations.py
│       │
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

This structure separates **agent logic**, **orchestration**, and **infrastructure concerns**, making the system easier to extend, test, and reason about as complexity grows.

---

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

Artifacts are written to `outputs/sample_runs/` as JSON and Markdown files.

---

## 🛡️ Safety & Reliability Features

* **Typed shared state** (Pydantic)
* **Critic-driven validation** of evidence quality
* **Bounded retry loops** to prevent infinite agent cycles
* **Explicit failure modes** when evidence is insufficient
* **Deterministic artifacts** for auditing and debugging

This mirrors real-world constraints in enterprise AI systems.

---

## 🧩 Design Decisions

This project prioritizes **reliability, observability, and controlled execution** over raw generation quality.

### 1️⃣ Explicit Agent Roles vs. Single “Super-Agent”

Separate Planner, Researcher, Critic, and Decider agents improve debuggability and localize failures at the cost of additional orchestration complexity.

### 2️⃣ LangGraph for Orchestration

Agent execution is modeled as an explicit graph/state machine to enable deterministic routing, bounded retries, and inspectable control flow.

### 3️⃣ Typed Shared State (Pydantic)

All agents read/write to a structured state object, preventing schema drift and enabling artifact persistence and validation.

### 4️⃣ Critic-Driven Validation

A dedicated Critic agent enforces evidence quality and can halt or redirect execution, reducing hallucinations.

### 5️⃣ Bounded Retry Loops

Critique → research cycles are explicitly limited to ensure predictable execution and bounded cost.

### 6️⃣ Artifact-First Outputs

Every run produces a full JSON execution trace and a user-facing Markdown report for transparency and debugging.

### 7️⃣ Placeholder Tooling Before Optimization

Tooling is stubbed initially to validate control flow before integrating real data sources.

### 8️⃣ Safety Over Fluency

The system prefers low-confidence or insufficient-evidence outputs over confident but unsupported answers.

---

## 📦 Project Status

**Implemented**

* Planner → Researcher → Critic → Decider pipeline
* LangGraph orchestration with conditional routing
* CLI + FastAPI interface
* Run artifacts (JSON + Markdown)
* Safe failure behavior

**Planned / In Progress**

* Real web search integration (Tavily / Bing / SerpAPI)
* Citation quality scoring
* Cost & latency tracking per agent
* Offline evaluation harness
* Caching and model routing

---

## 🧪 Development Notes

* Web search is currently stubbed.
* The Critic correctly flags placeholder citations.
* This behavior is intentional and demonstrates safe defaults.

---

## 🎯 Who This Is For

This project is intended to demonstrate skills relevant to:

* Applied AI Engineer
* LLM Platform Engineer
* Agentic Systems Engineer

It focuses on **system design, safety, and reliability**, not prompt hacking.

---

## 📌 Key Takeaway

> This repository demonstrates how to build **agentic AI systems that are safe, inspectable, and production-ready**, rather than brittle prompt pipelines.

---