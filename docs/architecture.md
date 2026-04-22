# FieldOps Copilot — Architecture

## Overview

FieldOps Copilot is a **local-first** inspection workflow system. A **FastAPI** service exposes HTTP APIs; **LangGraph** orchestrates multimodal analysis, retrieval, drafting, validation, and optional human-in-the-loop approval. A **Next.js** frontend provides the operator UI (Phase 1: screens and design system; live wiring in later phases).

Official design references:

- [LangGraph workflows & agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## Memory layers

### A. Execution state

Held in **`GraphState`** ([`backend/app/schemas/state.py`](../backend/app/schemas/state.py)) and persisted by the LangGraph **checkpointer** (`MemorySaver` in Phase 1). Includes OCR bundles, vision summaries, anomaly findings, triage outputs, fused evidence, retrieved chunks, draft report, rule/review results, and export Markdown.

### B. Thread memory

**`messages`** in `GraphState` uses the LangGraph **`add_messages`** reducer for conversational follow-ups (for example, “rewrite shorter”, “focus on anomaly only”). Checkpoints are scoped by **`thread_id`** in `config.configurable`.

### C. Project memory

**`ProjectMemoryStore`** ([`backend/app/memory/project_store.py`](../backend/app/memory/project_store.py)) persists JSON per `project_id` under `data/processed/project_memory/`. Use it for templates, equipment aliases, recurring reviewer fixes, and pointers to approved reports—not a knowledge graph in v1.

## Pipeline nodes

Node implementations live under [`backend/app/nodes/`](../backend/app/nodes/). The compiled graph is built in [`backend/app/graph/builder.py`](../backend/app/graph/builder.py): sequential modality branches (each node no-ops when not applicable), then fusion → RAG → outline → draft → rules → reviewer → optional revision loop → human approval → export.

## Model adapters (swap-friendly)

Stubs for **Gemma** (LLM), **Phi-4-multimodal** (VLM), **PaddleOCR**, **anomalib PatchCore**, **BGE-M3** + reranker, and **LightGBM** are planned under [`backend/app/models/`](../backend/app/models/README.md); Phase 1 uses deterministic placeholders inside nodes.

## API surface

| Endpoint | Role |
|----------|------|
| `POST /api/v1/sessions` | New `thread_id` |
| `POST /api/v1/ingest` | Multipart upload + first `ainvoke` |
| `POST /api/v1/graph/invoke` | Follow-up message (checkpoint required) |
| `GET /api/v1/graph/state/{thread_id}` | UI state snapshot |
| `POST /api/v1/approval` | Approval / HITL resume or dev-mode state patch |

## Configuration

| Variable | Meaning |
|----------|---------|
| `FIELDOPS_DATA_DIR` | Root for `raw/` uploads and processed artifacts (default: repo `data/`) |
| `FIELDOPS_CORS_ORIGINS` | JSON list or comma-separated origins (via settings parsing if extended) |
| `FIELDOPS_SKIP_HITL_INTERRUPT` | If `true`, `human_approval` does not call `interrupt()` (default `true`) |

## Future work

- Sqlite / Postgres checkpointer for durable threads.
- Streaming / SSE for step progress.
- Real models and eval scripts under `backend/scripts/`.
