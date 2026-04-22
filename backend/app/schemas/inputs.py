"""Input artifacts and modality typing."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Modality(str, Enum):
    """Detected or declared input modality."""

    IMAGE = "image"
    PDF = "pdf"
    DOCUMENT_IMAGE = "document_image"
    TEXT = "text"
    TABULAR = "tabular"
    SENSOR = "sensor"
    UNKNOWN = "unknown"


class UploadedArtifact(BaseModel):
    """A single user-provided file or inline payload reference."""

    artifact_id: str = Field(..., description="Stable id within the thread.")
    modality: Modality = Modality.UNKNOWN
    mime_type: str = "application/octet-stream"
    filename: str | None = None
    # Relative path under data_dir/raw/{thread_id}/ (server-side); no raw bytes in state.
    storage_path: str | None = None
    # Inline text (e.g. worker notes) when modality is TEXT.
    text_content: str | None = None
    # Optional structured sensor / tabular row as JSON-like dict.
    structured_payload: dict[str, Any] | None = None

    model_config = {"extra": "forbid"}
