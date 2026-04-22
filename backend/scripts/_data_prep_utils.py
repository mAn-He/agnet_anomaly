"""Shared helpers for dataset prep scripts (stdlib-only MVP)."""

from __future__ import annotations

import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path
from typing import Any


def repo_root_from_script(script_path: str | Path) -> Path:
    """`backend/scripts/foo.py` → repository root (parent of `backend/`)."""
    return Path(script_path).resolve().parents[2]


def resolve_safe(root: Path, *parts: str) -> Path:
    """Join path parts under root; reject traversal outside root."""
    p = (root.joinpath(*parts)).resolve()
    root_r = root.resolve()
    if root_r not in p.parents and p != root_r:
        raise ValueError(f"Resolved path escapes repo root: {p}")
    return p


def resolve_under_repo(root: Path, relative: str | Path) -> Path:
    """Resolve `root / relative` where `relative` may contain slashes."""
    p = (root / Path(relative)).resolve()
    root_r = root.resolve()
    try:
        p.relative_to(root_r)
    except ValueError as e:
        raise ValueError(f"Path escapes repo root: {p}") from e
    return p


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, obj: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def download_url(url: str, dest: Path, chunk: int = 1 << 20) -> None:
    """Stream download with a browser-like User-Agent (some mirrors block default)."""
    ensure_dir(dest.parent)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "fieldops-copilot-data-prep/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as out:
        shutil.copyfileobj(resp, out, length=chunk)


def extract_zip(zip_path: Path, dest_dir: Path) -> None:
    ensure_dir(dest_dir)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()
