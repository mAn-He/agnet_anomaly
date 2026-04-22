"""Outline generation (planner LLM — Gemma adapter later)."""

from __future__ import annotations

from typing import Any

from app.schemas.state import GraphState


async def planner_outline(state: GraphState) -> dict[str, Any]:
    """Stub outline from fused evidence and retrieved chunks."""
    titles = [
        "Scope and equipment",
        "Observations",
        "Measurements and checklist",
        "Anomaly assessment",
        "Risk and severity",
        "Recommended actions",
        "References",
    ]
    body = "\n".join(f"- {t}" for t in titles)
    return {
        "outline": body,
        "pipeline_step": "planner_outline",
    }
