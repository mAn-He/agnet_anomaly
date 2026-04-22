"""Revision loop: increment counter and add steering messages."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import HumanMessage

from app.schemas.state import GraphState


async def revision_node(state: GraphState) -> dict[str, Any]:
    """Prepare another draft pass after failed review."""
    n = int(state.get("revision_count") or 0) + 1
    feedback = (state.get("review_result") or {}).get("suggested_edits") or []
    msg = HumanMessage(
        content=f"Revision {n}: apply reviewer feedback: {feedback!s}",
    )
    return {
        "revision_count": n,
        "messages": [msg],
        "pipeline_step": "revision_node",
    }
