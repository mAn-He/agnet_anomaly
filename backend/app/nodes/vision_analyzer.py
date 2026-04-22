"""Multimodal VLM summary (Phi-4-multimodal / Qwen2.5-VL adapters later)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import VisionSummary
from app.schemas.state import GraphState


async def vision_analyzer(state: GraphState) -> dict[str, Any]:
    """Stub vision summaries for image artifacts."""
    flags = state.get("route_flags") or {}
    if not flags.get("needs_vision"):
        return {"pipeline_step": "vision_analyzer_skipped"}

    summaries: list[dict[str, Any]] = []
    for a in state.get("artifacts") or []:
        if a.get("modality") != "image":
            continue
        vs = VisionSummary(
            artifact_id=a["artifact_id"],
            summary="[Stub VLM] Equipment appears intact; lighting adequate for inspection.",
            labels=["stub", "mvp"],
        )
        summaries.append(vs.model_dump(mode="json"))

    return {
        "vision_summaries": summaries,
        "pipeline_step": "vision_analyzer",
    }
