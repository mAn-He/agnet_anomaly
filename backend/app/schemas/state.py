"""LangGraph shared state (TypedDict + reducers)."""

from __future__ import annotations

import operator
from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class GraphState(TypedDict, total=False):
    """Execution + thread memory for one workflow run.

    Complex nested objects are stored as dicts for checkpoint serialization.
    Use Pydantic model_validate in nodes when stronger typing is needed.
    """

    # Identity
    thread_id: str
    project_id: str
    run_id: str

    # Inputs (replaced by input_intake for each analytical run)
    artifacts: list[dict[str, Any]]

    # Routing
    modalities_present: list[str]
    route_flags: dict[str, bool]
    next_node_hint: str | None

    # Module outputs (optional until filled)
    ocr_bundle: dict[str, Any] | None
    vision_summaries: list[dict[str, Any]]
    anomaly_findings: list[dict[str, Any]]
    tabular_triage: dict[str, Any] | None
    normalized_notes: str | None

    fused_evidence: dict[str, Any] | None
    retrieved_docs: Annotated[list[dict[str, Any]], operator.add]

    outline: str | None
    draft_report: dict[str, Any] | None
    revision_count: int

    rule_result: dict[str, Any] | None
    review_result: dict[str, Any] | None

    approval_status: Literal["pending", "approved", "rejected"]
    human_feedback: str | None

    final_export_markdown: str | None

    # Project memory handles (loaded via ProjectMemoryStore in nodes)
    project_context_refs: Annotated[list[str], operator.add]

    # Thread memory (follow-ups: "rewrite shorter", etc.)
    messages: Annotated[list[AnyMessage], add_messages]

    # Control / diagnostics
    errors: Annotated[list[str], operator.add]
    pipeline_step: str


def default_graph_state(
    *,
    thread_id: str,
    project_id: str,
    run_id: str,
    artifacts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Initial state for a new analytical run."""
    return {
        "thread_id": thread_id,
        "project_id": project_id,
        "run_id": run_id,
        "artifacts": artifacts or [],
        "modalities_present": [],
        "route_flags": {},
        "next_node_hint": None,
        "ocr_bundle": None,
        "vision_summaries": [],
        "anomaly_findings": [],
        "tabular_triage": None,
        "normalized_notes": None,
        "fused_evidence": None,
        "retrieved_docs": [],
        "outline": None,
        "draft_report": None,
        "revision_count": 0,
        "rule_result": None,
        "review_result": None,
        "approval_status": "pending",
        "human_feedback": None,
        "final_export_markdown": None,
        "project_context_refs": [],
        "messages": [],
        "errors": [],
        "pipeline_step": "init",
    }
