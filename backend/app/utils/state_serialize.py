"""Serialize graph state for JSON responses."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import BaseMessage


def message_to_dict(m: BaseMessage) -> dict[str, Any]:
    return {"type": m.type, "content": m.content}


def serialize_state(values: dict[str, Any]) -> dict[str, Any]:
    """Make checkpoint values JSON-safe (messages, etc.)."""
    out: dict[str, Any] = {}
    for k, v in values.items():
        if k == "messages" and v is not None:
            out[k] = [message_to_dict(m) if isinstance(m, BaseMessage) else m for m in v]
        else:
            out[k] = v
    return out
