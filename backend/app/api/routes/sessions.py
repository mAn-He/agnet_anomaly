"""Thread/session lifecycle."""

from __future__ import annotations

import uuid

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


class SessionCreateResponse(BaseModel):
    thread_id: str = Field(..., description="LangGraph thread_id for checkpoints.")
    project_id: str = Field(default="default", description="Logical project for memory scoping.")


@router.post("", response_model=SessionCreateResponse)
async def create_session() -> SessionCreateResponse:
    """Create a new conversation / analysis thread."""
    return SessionCreateResponse(
        thread_id=str(uuid.uuid4()),
        project_id="default",
    )
