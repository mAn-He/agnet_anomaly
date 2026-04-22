"""Merge module outputs into fused evidence for RAG + drafting."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import FusedEvidence
from app.schemas.state import GraphState


async def fusion_node(state: GraphState) -> dict[str, Any]:
    """Combine OCR, vision, anomaly, tabular, and notes into one bundle."""
    bullets: list[str] = []
    if state.get("ocr_bundle"):
        bullets.append("Checklist / form fields extracted (see OCR bundle).")
    if state.get("vision_summaries"):
        bullets.append(f"{len(state['vision_summaries'])} vision summary(ies) available.")
    if state.get("anomaly_findings"):
        bullets.append("Anomaly scores computed (see anomaly findings).")
    if state.get("tabular_triage"):
        bullets.append("Tabular triage suggests baseline severity.")
    if state.get("normalized_notes"):
        bullets.append("Worker notes normalized.")

    fe = FusedEvidence(
        summary_bullets=bullets or ["No modality-specific evidence; minimal run."],
        key_entities={"line": "UNSPECIFIED"},
        evidence_refs=[a.get("artifact_id", "") for a in state.get("artifacts") or []],
    )
    return {
        "fused_evidence": fe.model_dump(mode="json"),
        "pipeline_step": "fusion_node",
    }
