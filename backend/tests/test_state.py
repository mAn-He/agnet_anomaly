"""Graph state defaults and shape."""

from app.schemas.state import default_graph_state


def test_default_graph_state_has_identity_and_lists() -> None:
    s = default_graph_state(thread_id="t", project_id="p", run_id="r")
    assert s["thread_id"] == "t"
    assert s["project_id"] == "p"
    assert s["run_id"] == "r"
    assert s["artifacts"] == []
    assert s["retrieved_docs"] == []
    assert s["messages"] == []
    assert s["errors"] == []
    assert s["project_context_refs"] == []
    assert s["revision_count"] == 0
