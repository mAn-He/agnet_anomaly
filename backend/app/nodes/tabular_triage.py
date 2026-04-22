"""Tabular / sensor triage (LightGBM in later phases)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import TabularTriageResult
from app.schemas.state import GraphState


async def tabular_triage(state: GraphState) -> dict[str, Any]:
    """Stub severity prediction when tabular/sensor modality present."""
    flags = state.get("route_flags") or {}
    if not flags.get("needs_tabular"):
        return {"pipeline_step": "tabular_triage_skipped", "tabular_triage": None}

    snap: dict[str, Any] = {}
    for a in state.get("artifacts") or []:
        if a.get("modality") in ("tabular", "sensor") and a.get("structured_payload"):
            snap.update(a["structured_payload"])

    tri = TabularTriageResult(
        predicted_severity="low",
        maintenance_priority=0.2,
        feature_snapshot=snap or {"note": "no structured_payload provided"},
    )
    return {
        "tabular_triage": tri.model_dump(mode="json"),
        "pipeline_step": "tabular_triage",
    }
