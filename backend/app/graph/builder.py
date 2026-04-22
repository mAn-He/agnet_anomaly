"""Compile the FieldOps inspection LangGraph."""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.graph.edges import (
    route_after_input_router,
    route_after_merge_anomaly,
    route_after_merge_document,
    route_after_merge_tabular,
    route_after_merge_vision,
    route_after_review,
)
from app.memory.checkpointer import get_checkpointer
from app.nodes import (
    anomaly_detector,
    document_parser,
    draft_writer,
    final_export,
    fusion_node,
    human_approval,
    input_intake,
    input_router,
    planner_outline,
    retriever,
    reviewer_agent,
    revision_node,
    rule_checker,
    tabular_triage,
    text_normalizer,
    vision_analyzer,
)
from app.nodes.pipeline_gates import (
    merge_after_anomaly,
    merge_after_document,
    merge_after_tabular,
    merge_after_vision,
    skip_anomaly,
    skip_document_parser,
    skip_tabular,
    skip_text_normalizer,
    skip_vision,
)
from app.schemas.state import GraphState


def build_graph():
    """Create uncompiled graph definition."""
    g = StateGraph(GraphState)

    g.add_node("input_intake", input_intake)
    g.add_node("input_router", input_router)
    g.add_node("document_parser", document_parser)
    g.add_node("skip_document_parser", skip_document_parser)
    g.add_node("merge_after_document", merge_after_document)
    g.add_node("vision_analyzer", vision_analyzer)
    g.add_node("skip_vision", skip_vision)
    g.add_node("merge_after_vision", merge_after_vision)
    g.add_node("anomaly_detector", anomaly_detector)
    g.add_node("skip_anomaly", skip_anomaly)
    g.add_node("merge_after_anomaly", merge_after_anomaly)
    g.add_node("tabular_triage", tabular_triage)
    g.add_node("skip_tabular", skip_tabular)
    g.add_node("merge_after_tabular", merge_after_tabular)
    g.add_node("text_normalizer", text_normalizer)
    g.add_node("skip_text_normalizer", skip_text_normalizer)
    g.add_node("fusion_node", fusion_node)
    g.add_node("retriever", retriever)
    g.add_node("planner_outline", planner_outline)
    g.add_node("draft_writer", draft_writer)
    g.add_node("rule_checker", rule_checker)
    g.add_node("reviewer_agent", reviewer_agent)
    g.add_node("revision_node", revision_node)
    g.add_node("human_approval", human_approval)
    g.add_node("final_export", final_export)

    g.add_edge(START, "input_intake")
    g.add_edge("input_intake", "input_router")
    g.add_conditional_edges(
        "input_router",
        route_after_input_router,
        {
            "document_parser": "document_parser",
            "skip_document_parser": "skip_document_parser",
        },
    )
    g.add_edge("document_parser", "merge_after_document")
    g.add_edge("skip_document_parser", "merge_after_document")
    g.add_conditional_edges(
        "merge_after_document",
        route_after_merge_document,
        {
            "vision_analyzer": "vision_analyzer",
            "skip_vision": "skip_vision",
        },
    )
    g.add_edge("vision_analyzer", "merge_after_vision")
    g.add_edge("skip_vision", "merge_after_vision")
    g.add_conditional_edges(
        "merge_after_vision",
        route_after_merge_vision,
        {
            "anomaly_detector": "anomaly_detector",
            "skip_anomaly": "skip_anomaly",
        },
    )
    g.add_edge("anomaly_detector", "merge_after_anomaly")
    g.add_edge("skip_anomaly", "merge_after_anomaly")
    g.add_conditional_edges(
        "merge_after_anomaly",
        route_after_merge_anomaly,
        {
            "tabular_triage": "tabular_triage",
            "skip_tabular": "skip_tabular",
        },
    )
    g.add_edge("tabular_triage", "merge_after_tabular")
    g.add_edge("skip_tabular", "merge_after_tabular")
    g.add_conditional_edges(
        "merge_after_tabular",
        route_after_merge_tabular,
        {
            "text_normalizer": "text_normalizer",
            "skip_text_normalizer": "skip_text_normalizer",
        },
    )
    g.add_edge("text_normalizer", "fusion_node")
    g.add_edge("skip_text_normalizer", "fusion_node")
    g.add_edge("fusion_node", "retriever")
    g.add_edge("retriever", "planner_outline")
    g.add_edge("planner_outline", "draft_writer")
    g.add_edge("draft_writer", "rule_checker")
    g.add_edge("rule_checker", "reviewer_agent")

    g.add_conditional_edges(
        "reviewer_agent",
        route_after_review,
        {
            "human_approval": "human_approval",
            "revision_node": "revision_node",
        },
    )
    g.add_edge("revision_node", "draft_writer")
    g.add_edge("human_approval", "final_export")
    g.add_edge("final_export", END)

    return g


def compile_workflow():
    """Compiled graph with checkpointer for thread persistence."""
    return build_graph().compile(checkpointer=get_checkpointer())
