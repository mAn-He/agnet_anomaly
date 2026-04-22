"""Human approval / HITL resume (interrupt wiring in later phase)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.api.deps import get_compiled_graph, get_settings
from app.utils.state_serialize import serialize_state

router = APIRouter(prefix="/api/v1", tags=["approval"])


class ApprovalBody(BaseModel):
    thread_id: str
    approved: bool = True
    feedback: str | None = Field(default=None)


@router.post("/approval")
async def submit_approval(body: ApprovalBody) -> dict[str, Any]:
    """Persist approval intent; when interrupts are enabled, use Command(resume=...)."""
    settings = get_settings()
    graph = get_compiled_graph()
    config = {"configurable": {"thread_id": body.thread_id}}
    snap = graph.get_state(config)
    if not snap or not snap.values:
        raise HTTPException(status_code=404, detail="Unknown thread_id")

    if not settings.skip_hitl_interrupt:
        try:
            from langgraph.types import Command
        except Exception as e:  # pragma: no cover
            raise HTTPException(status_code=501, detail="Command resume not available") from e

        resume = {"approved": body.approved, "feedback": body.feedback}
        out = await graph.ainvoke(Command(resume=resume), config)  # type: ignore[arg-type]
        return serialize_state(out)

    # Dev mode: patch checkpoint values without re-running full graph.
    await graph.aupdate_state(
        config,
        {
            "approval_status": "approved" if body.approved else "rejected",
            "human_feedback": body.feedback,
            "pipeline_step": "approval_api_patch",
        },
    )
    snap2 = graph.get_state(config)
    return serialize_state(snap2.values or {})
