"""Conditional routing helpers."""

from __future__ import annotations

from app.config import get_settings
from app.schemas.state import GraphState


def _flags(state: GraphState) -> dict[str, bool]:
    return state.get("route_flags") or {}


def route_after_input_router(state: GraphState) -> str:
    """Run OCR branch only when PDF / document_image is present."""
    return "document_parser" if _flags(state).get("needs_document") else "skip_document_parser"


def route_after_merge_document(state: GraphState) -> str:
    """Vision/VLM only when raster image modality is present."""
    return "vision_analyzer" if _flags(state).get("needs_vision") else "skip_vision"


def route_after_merge_vision(state: GraphState) -> str:
    """Anomaly scoring only when image inspection branch is active."""
    return "anomaly_detector" if _flags(state).get("needs_anomaly") else "skip_anomaly"


def route_after_merge_anomaly(state: GraphState) -> str:
    """Tabular triage when tabular/sensor payloads exist."""
    return "tabular_triage" if _flags(state).get("needs_tabular") else "skip_tabular"


def route_after_merge_tabular(state: GraphState) -> str:
    """Normalize worker notes when text modality is present."""
    return "text_normalizer" if _flags(state).get("needs_text") else "skip_text_normalizer"


def route_after_review(state: GraphState) -> str:
    """After reviewer_agent: revise, approve, or escalate."""
    settings = get_settings()
    rr = state.get("review_result") or {}
    if rr.get("passed"):
        return "human_approval"
    rev = int(state.get("revision_count") or 0)
    if rev < settings.max_revision_iterations:
        return "revision_node"
    return "human_approval"
