"""Project-scoped memory (templates, equipment aliases) — no knowledge graph in v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProjectMemoryStore(Protocol):
    """Abstract store for reusable project preferences and snippets."""

    def get(self, project_id: str, key: str, default: Any = None) -> Any: ...

    def set(self, project_id: str, key: str, value: Any) -> None: ...


class FileProjectMemoryStore:
    """JSON file per project under base_dir."""

    def __init__(self, base_dir: Path) -> None:
        self._base = base_dir
        self._base.mkdir(parents=True, exist_ok=True)

    def _path(self, project_id: str) -> Path:
        safe = project_id.replace("/", "_")
        return self._base / f"{safe}.json"

    def get(self, project_id: str, key: str, default: Any = None) -> Any:
        path = self._path(project_id)
        if not path.exists():
            return default
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get(key, default)

    def set(self, project_id: str, key: str, value: Any) -> None:
        path = self._path(project_id)
        data: dict[str, Any] = {}
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
        data[key] = value
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
