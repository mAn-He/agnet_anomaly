"""Rule-based validation (required sections, placeholders, etc.)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import RuleCheckResult, RuleIssue
from app.schemas.state import GraphState


async def rule_checker(state: GraphState) -> dict[str, Any]:
    """Check template requirements; Phase 1 uses light rules."""
    draft = state.get("draft_report") or {}
    issues: list[RuleIssue] = []

    if not draft.get("sections"):
        issues.append(
            RuleIssue(code="SEC_EMPTY", message="Report has no sections.", severity="error")
        )

    date = draft.get("inspection_date")
    if not date or str(date).upper() == "TBD":
        issues.append(
            RuleIssue(
                code="DATE_TBD",
                message="Inspection date is missing or placeholder TBD.",
                severity="warning",
            )
        )

    equip = draft.get("equipment_id")
    if not equip or "UNKNOWN" in str(equip).upper():
        issues.append(
            RuleIssue(
                code="EQUIP_PLACEHOLDER",
                message="Equipment identifier needs confirmation.",
                severity="warning",
            )
        )

    action_items = draft.get("action_items") or []
    if not action_items:
        issues.append(
            RuleIssue(code="NO_ACTIONS", message="No action items listed.", severity="error")
        )

    retrieved = state.get("retrieved_docs") or []
    if not retrieved:
        issues.append(
            RuleIssue(
                code="NO_CITATIONS",
                message="No retrieved SOP chunks to cite (stub retrieval may be empty).",
                severity="warning",
            )
        )

    errors = [i for i in issues if i.severity == "error"]
    result = RuleCheckResult(passed=len(errors) == 0, issues=issues)
    return {
        "rule_result": result.model_dump(mode="json"),
        "pipeline_step": "rule_checker",
    }
