"""Set modalities_present and route flags for downstream nodes."""

from __future__ import annotations

from typing import Any

from app.schemas.inputs import Modality
from app.schemas.state import GraphState


async def input_router(state: GraphState) -> dict[str, Any]:
    """Derive which branches are relevant; downstream nodes no-op when skipped."""
    modalities: set[str] = set()
    route_flags = {
        "needs_document": False,
        "needs_vision": False,
        "needs_anomaly": False,
        "needs_tabular": False,
        "needs_text": False,
    }
    for a in state.get("artifacts") or []:
        m = a.get("modality") or Modality.UNKNOWN.value
        modalities.add(str(m))
        if m in (Modality.PDF.value, Modality.DOCUMENT_IMAGE.value):
            route_flags["needs_document"] = True
        if m == Modality.IMAGE.value:
            route_flags["needs_vision"] = True
            route_flags["needs_anomaly"] = True
        if m == Modality.PDF.value:
            route_flags["needs_document"] = True
        if m == Modality.TEXT.value:
            route_flags["needs_text"] = True
        if m in (Modality.TABULAR.value, Modality.SENSOR.value):
            route_flags["needs_tabular"] = True

    return {
        "modalities_present": sorted(modalities),
        "route_flags": route_flags,
        "pipeline_step": "input_router",
        "next_node_hint": None,
    }
