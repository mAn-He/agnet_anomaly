"""Modality-aware graph routing (skip branches when not needed)."""

from __future__ import annotations

import asyncio

from app.graph.builder import compile_workflow
from app.schemas.inputs import Modality, UploadedArtifact
from app.schemas.state import default_graph_state


def test_text_only_skips_vision_and_anomaly() -> None:
    async def _run() -> None:
        graph = compile_workflow()
        tid = "t-text"
        art = UploadedArtifact(
            artifact_id="a1",
            modality=Modality.TEXT,
            mime_type="text/plain",
            text_content="Line stopped; check bearing temp.",
        )
        state = default_graph_state(
            thread_id=tid,
            project_id="p",
            run_id="r1",
            artifacts=[art.model_dump(mode="json")],
        )
        out = await graph.ainvoke(state, {"configurable": {"thread_id": tid}})
        assert out.get("vision_summaries") == []
        assert out.get("anomaly_findings") == []
        assert out.get("normalized_notes")
        assert out.get("final_export_markdown")

    asyncio.run(_run())


def test_image_runs_vision_and_anomaly() -> None:
    async def _run() -> None:
        graph = compile_workflow()
        tid = "t-img"
        art = UploadedArtifact(
            artifact_id="a1",
            modality=Modality.IMAGE,
            mime_type="image/png",
            filename="x.png",
            storage_path="raw/t-img/x.png",
        )
        state = default_graph_state(
            thread_id=tid,
            project_id="p",
            run_id="r2",
            artifacts=[art.model_dump(mode="json")],
        )
        out = await graph.ainvoke(state, {"configurable": {"thread_id": tid}})
        assert len(out.get("vision_summaries") or []) >= 1
        assert len(out.get("anomaly_findings") or []) >= 1

    asyncio.run(_run())
