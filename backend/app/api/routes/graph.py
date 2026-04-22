"""Graph invoke and state inspection."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from app.api.deps import get_compiled_graph
from app.utils.state_serialize import serialize_state

router = APIRouter(prefix="/api/v1/graph", tags=["graph"])


class InvokeBody(BaseModel):
    thread_id: str
    user_message: str | None = Field(
        default=None,
        description="Optional follow-up instruction (appended to thread messages).",
    )


@router.post("/invoke")
async def invoke_graph(body: InvokeBody) -> dict[str, Any]:
    """Continue or start-from-checkpoint with an optional user message."""
    graph = get_compiled_graph()
    config = {"configurable": {"thread_id": body.thread_id}}
    snap = graph.get_state(config)
    if not snap or not snap.values:
        raise HTTPException(
            status_code=404,
            detail="No checkpoint for thread_id. Ingest files first.",
        )
    patch: dict[str, Any] = {}
    if body.user_message:
        patch["messages"] = [HumanMessage(content=body.user_message)]
    out = await graph.ainvoke(patch, config)
    return serialize_state(out)


@router.get("/state/{thread_id}")
async def get_graph_state(thread_id: str) -> dict[str, Any]:
    """Return latest checkpoint values for UI."""
    graph = get_compiled_graph()
    config = {"configurable": {"thread_id": thread_id}}
    snap = graph.get_state(config)
    if not snap or not snap.values:
        raise HTTPException(status_code=404, detail="Unknown thread_id")
    return serialize_state(snap.values)
