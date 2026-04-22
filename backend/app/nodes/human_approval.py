"""Human-in-the-loop checkpoint (interrupt when enabled)."""

from __future__ import annotations

from typing import Any

from app.config import get_settings
from app.schemas.state import GraphState

try:
    from langgraph.types import interrupt
except Exception:  # pragma: no cover - optional depending on LangGraph build
    interrupt = None  # type: ignore[misc, assignment]


async def human_approval(state: GraphState) -> dict[str, Any]:
    """Pause for operator approval or pass through in dev mode."""
    settings = get_settings()
    if settings.skip_hitl_interrupt or interrupt is None:
        return {
            "approval_status": "approved",
            "human_feedback": None,
            "pipeline_step": "human_approval_auto",
        }

    payload = {
        "thread_id": state.get("thread_id"),
        "run_id": state.get("run_id"),
        "draft_report": state.get("draft_report"),
    }
    resume = interrupt(payload)
    approved = bool((resume or {}).get("approved", False))
    return {
        "approval_status": "approved" if approved else "rejected",
        "human_feedback": (resume or {}).get("feedback"),
        "pipeline_step": "human_approval",
    }
