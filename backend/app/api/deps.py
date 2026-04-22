"""FastAPI dependencies."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Request

from app.config import Settings, get_settings
from app.graph.builder import compile_workflow
from app.memory.project_store import FileProjectMemoryStore


@lru_cache(maxsize=1)
def get_compiled_graph():
    """Singleton compiled LangGraph (Phase 1: in-process)."""
    return compile_workflow()


def get_project_store(request: Request) -> FileProjectMemoryStore:
    """Per-app project memory (JSON files under data/processed/project_memory)."""
    base = get_settings().data_dir / "processed" / "project_memory"
    return FileProjectMemoryStore(base)


def settings_dep() -> Settings:
    return get_settings()
