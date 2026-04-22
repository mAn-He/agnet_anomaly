"""Serialize final Markdown export."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import InspectionReportDraft
from app.schemas.state import GraphState


def _draft_to_markdown(draft: dict[str, Any]) -> str:
    d = InspectionReportDraft.model_validate(draft)
    lines = [f"# {d.title}", ""]
    if d.equipment_id:
        lines.append(f"**Equipment:** {d.equipment_id}")
    if d.inspection_date:
        lines.append(f"**Date:** {d.inspection_date}")
    lines.append("")
    for s in d.sections:
        lines.append(f"## {s.title}")
        lines.append(s.body)
        if s.citations:
            lines.append(f"*Citations:* {', '.join(s.citations)}")
        lines.append("")
    if d.action_items:
        lines.append("## Action items")
        for ai in d.action_items:
            lines.append(f"- {ai}")
    return "\n".join(lines).strip()


async def final_export(state: GraphState) -> dict[str, Any]:
    """Build final_export_markdown from draft_report."""
    draft = state.get("draft_report") or {}
    md = _draft_to_markdown(draft) if draft else "# Empty report\n"
    return {
        "final_export_markdown": md,
        "pipeline_step": "final_export",
    }
