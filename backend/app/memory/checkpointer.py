"""LangGraph checkpointer factory (MemorySaver for local dev)."""

from langgraph.checkpoint.memory import MemorySaver


def get_checkpointer() -> MemorySaver:
    """Return a process-local checkpointer. Swap for SqliteSaver for durability."""
    return MemorySaver()
