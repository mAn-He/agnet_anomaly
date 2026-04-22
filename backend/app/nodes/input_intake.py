"""Validate artifacts and initialize pipeline step."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import HumanMessage

from app.schemas.inputs import UploadedArtifact
from app.schemas.state import GraphState
from app.services.modality_detect import enrich_artifact_modality


async def input_intake(state: GraphState) -> dict[str, Any]:
    """Normalize artifacts and seed thread messages."""
    raw = state.get("artifacts") or []
    normalized: list[dict[str, Any]] = []
    for a in raw:
        art = UploadedArtifact.model_validate(a)
        art = enrich_artifact_modality(art)
        normalized.append(art.model_dump(mode="json"))

    names = [a.get("filename") or a.get("artifact_id") for a in normalized]
    msg = HumanMessage(
        content=f"Intake: {len(normalized)} artifact(s): {', '.join(str(n) for n in names)}"
    )
    return {
        "artifacts": normalized,
        "pipeline_step": "input_intake",
        "messages": [msg],
    }
