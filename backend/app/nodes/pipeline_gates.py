"""Passthrough skip + merge nodes for modality-aware routing (MVP graph skeleton).

Heavy modules (OCR, VLM, anomaly, …) stay in dedicated node files; this module only
marks explicit skip/merge steps so logs and checkpoints read like a real branchy DAG.
"""

from __future__ import annotations

from typing import Any

from app.schemas.state import GraphState


async def skip_document_parser(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "skip_document_parser"}


async def skip_vision(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "skip_vision"}


async def skip_anomaly(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "skip_anomaly"}


async def skip_tabular(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "skip_tabular"}


async def skip_text_normalizer(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "skip_text_normalizer"}


async def merge_after_document(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "merge_after_document"}


async def merge_after_vision(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "merge_after_vision"}


async def merge_after_anomaly(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "merge_after_anomaly"}


async def merge_after_tabular(state: GraphState) -> dict[str, Any]:
    return {"pipeline_step": "merge_after_tabular"}
