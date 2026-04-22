"""Draft report writer (Gemma / open LLM adapter later)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import InspectionReportDraft, ReportSection
from app.schemas.state import GraphState


async def draft_writer(state: GraphState) -> dict[str, Any]:
    """Produce a structured draft with citations from retrieved_docs."""
    retrieved = state.get("retrieved_docs") or []
    cite_ids = [r.get("chunk_id", "") for r in retrieved]

    sections = [
        ReportSection(
            title="Scope and equipment",
            body="Inspection covers provided artifacts and notes for the current thread.",
            citations=cite_ids[:1],
        ),
        ReportSection(
            title="Observations",
            body="Vision and OCR modules (when enabled) contribute evidence for this draft.",
            citations=cite_ids,
        ),
        ReportSection(
            title="Anomaly assessment",
            body="Stub anomaly scores suggest no immediate defect signal at default threshold.",
            citations=[],
        ),
    ]
    draft = InspectionReportDraft(
        title="Field Inspection Draft",
        equipment_id="EQ-UNKNOWN",
        inspection_date="TBD",
        sections=sections,
        action_items=[
            "Confirm inspection date and equipment ID with site lead.",
            "Replace stub models with production OCR/VLM/anomaly pipelines.",
        ],
    )
    return {
        "draft_report": draft.model_dump(mode="json"),
        "pipeline_step": "draft_writer",
    }
