"""RAG retrieval (BGE-M3 + reranker in later phases)."""

from __future__ import annotations

from typing import Any

from app.schemas.reports import RetrievedChunk
from app.schemas.state import GraphState


async def retriever(state: GraphState) -> dict[str, Any]:
    """Stub retrieval: optional dev fixture chunk."""
    chunk = RetrievedChunk(
        chunk_id="stub-1",
        text="[Stub SOP] Inspect guarding, torque marks, and thermal discoloration per internal WI-123.",
        source_uri="stub://sop/wi-123",
        score=0.42,
        metadata={"collection": "dev"},
    )
    return {
        "retrieved_docs": [chunk.model_dump(mode="json")],
        "project_context_refs": [f"run:{state.get('run_id', '')}"],
        "pipeline_step": "retriever",
    }
