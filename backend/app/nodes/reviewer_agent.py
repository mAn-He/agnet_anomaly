"""LLM reviewer for tone, evidence, and hallucination risk (Gemma adapter later)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import ReviewIssue, ReviewResult
from app.schemas.state import GraphState


async def reviewer_agent(state: GraphState) -> dict[str, Any]:
    """Stub reviewer: pass when rule checker passed and draft has minimal content."""
    rules = state.get("rule_result") or {}
    draft = state.get("draft_report") or {}

    passed = bool(rules.get("passed")) and bool(draft.get("sections"))
    issues: list[ReviewIssue] = []
    if not passed:
        issues.append(
            ReviewIssue(
                code="RULE_GATE",
                message="Draft failed rule checker; revise before release.",
                severity="blocker",
            )
        )

    rr = ReviewResult(
        passed=passed,
        hallucination_risk="low",
        unsupported_claims=[],
        issues=issues,
        suggested_edits=[] if passed else ["Address rule checker findings and add citations."],
    )
    return {
        "review_result": rr.model_dump(mode="json"),
        "pipeline_step": "reviewer_agent",
    }
