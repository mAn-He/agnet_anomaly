"""Multipart ingest and initial pipeline run."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Annotated, Union

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.api.deps import get_compiled_graph, get_settings
from app.schemas.inputs import Modality, UploadedArtifact
from app.schemas.state import default_graph_state
from app.services.modality_detect import infer_modality

router = APIRouter(prefix="/api/v1", tags=["ingest"])


class IngestResponse(BaseModel):
    thread_id: str
    run_id: str
    artifacts_saved: int
    message: str = Field(default="Ingest complete; graph invoked.")


@router.post("/ingest", response_model=IngestResponse)
async def ingest(
    thread_id: Annotated[str, Form()],
    project_id: Annotated[str, Form()] = "default",
    notes: Annotated[str | None, Form()] = None,
    files: Annotated[
        Union[list[UploadFile], None],
        File(description="Optional inspection images / PDFs."),
    ] = None,
) -> IngestResponse:
    """Save uploads under data/raw/{thread_id}/ and run the graph once."""
    settings = get_settings()
    graph = get_compiled_graph()
    run_id = str(uuid.uuid4())

    dest_root = settings.data_dir / "raw" / thread_id
    dest_root.mkdir(parents=True, exist_ok=True)

    artifacts: list[dict] = []

    if notes and notes.strip():
        artifacts.append(
            UploadedArtifact(
                artifact_id=str(uuid.uuid4()),
                modality=Modality.TEXT,
                mime_type="text/plain",
                filename=None,
                text_content=notes.strip(),
            ).model_dump(mode="json")
        )

    upload_list = files or []
    for uf in upload_list:
        fname = uf.filename or "upload.bin"
        safe_name = f"{uuid.uuid4().hex}_{Path(fname).name}"
        path = dest_root / safe_name
        content = await uf.read()
        path.write_bytes(content)
        rel = str(path.relative_to(settings.data_dir))
        mime = uf.content_type or "application/octet-stream"
        mod = infer_modality(mime, fname)
        artifacts.append(
            UploadedArtifact(
                artifact_id=str(uuid.uuid4()),
                modality=mod,
                mime_type=mime,
                filename=fname,
                storage_path=rel.replace("\\", "/"),
            ).model_dump(mode="json")
        )

    if not artifacts:
        raise HTTPException(status_code=400, detail="No notes or files provided.")

    state = default_graph_state(
        thread_id=thread_id,
        project_id=project_id,
        run_id=run_id,
        artifacts=artifacts,
    )
    config = {"configurable": {"thread_id": thread_id}}
    await graph.ainvoke(state, config)

    return IngestResponse(
        thread_id=thread_id,
        run_id=run_id,
        artifacts_saved=len(artifacts),
    )
