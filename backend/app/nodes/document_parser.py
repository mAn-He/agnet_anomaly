"""OCR / PDF checklist extraction (PaddleOCR in later phases)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import OCRBundle, OCRField
from app.schemas.state import GraphState


async def document_parser(state: GraphState) -> dict[str, Any]:
    """Stub: empty OCR bundle unless document modality present."""
    flags = state.get("route_flags") or {}
    if not flags.get("needs_document"):
        return {"pipeline_step": "document_parser_skipped", "ocr_bundle": None}

    arts = state.get("artifacts") or []
    doc_ids = [
        a["artifact_id"]
        for a in arts
        if a.get("modality") in ("pdf", "document_image")
    ]
    bundle = OCRBundle(
        raw_text="[Stub OCR] Connect PaddleOCR for production text and layout.",
        fields=[OCRField(name="line_id", value="LINE-01", confidence=0.5)],
        source_artifact_ids=doc_ids,
    )
    return {
        "ocr_bundle": bundle.model_dump(mode="json"),
        "pipeline_step": "document_parser",
    }
