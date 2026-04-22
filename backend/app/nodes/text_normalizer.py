"""Normalize free-text worker notes."""

from __future__ import annotations

from typing import Any

from app.schemas.state import GraphState


async def text_normalizer(state: GraphState) -> dict[str, Any]:
    """Concatenate and trim text artifacts."""
    flags = state.get("route_flags") or {}
    if not flags.get("needs_text"):
        return {"pipeline_step": "text_normalizer_skipped", "normalized_notes": None}

    parts: list[str] = []
    for a in state.get("artifacts") or []:
        if a.get("modality") == "text" and a.get("text_content"):
            parts.append(a["text_content"].strip())

    merged = "\n".join(parts) if parts else None
    return {
        "normalized_notes": merged,
        "pipeline_step": "text_normalizer",
    }
