"""Visual anomaly scores (anomalib PatchCore in later phases)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import AnomalyFinding
from app.schemas.state import GraphState


async def anomaly_detector(state: GraphState) -> dict[str, Any]:
    """Stub anomaly scores for image artifacts."""
    flags = state.get("route_flags") or {}
    if not flags.get("needs_anomaly"):
        return {"pipeline_step": "anomaly_detector_skipped"}

    findings: list[dict[str, Any]] = []
    for a in state.get("artifacts") or []:
        if a.get("modality") != "image":
            continue
        af = AnomalyFinding(
            artifact_id=a["artifact_id"],
            anomaly_score=0.12,
            suspected_defect=False,
            heatmap_path=None,
        )
        findings.append(af.model_dump(mode="json"))

    return {
        "anomaly_findings": findings,
        "pipeline_step": "anomaly_detector",
    }
