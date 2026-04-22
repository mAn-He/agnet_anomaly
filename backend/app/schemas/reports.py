"""Report drafts, evidence bundles, and validation results."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class OCRField(BaseModel):
    """Single extracted checklist / form field."""

    name: str
    value: str | None = None
    confidence: float | None = None


class OCRBundle(BaseModel):
    """Structured output from document_parser / OCR pipeline."""

    raw_text: str = ""
    fields: list[OCRField] = Field(default_factory=list)
    source_artifact_ids: list[str] = Field(default_factory=list)


class VisionSummary(BaseModel):
    """VLM summary for one image artifact."""

    artifact_id: str
    summary: str = ""
    labels: list[str] = Field(default_factory=list)


class AnomalyRegion(BaseModel):
    """Optional localization hint (normalized 0–1 bbox)."""

    x: float
    y: float
    w: float
    h: float
    score: float


class AnomalyFinding(BaseModel):
    """Anomaly detector output for one image."""

    artifact_id: str
    anomaly_score: float = 0.0
    suspected_defect: bool = False
    regions: list[AnomalyRegion] = Field(default_factory=list)
    heatmap_path: str | None = None


class TabularTriageResult(BaseModel):
    """LightGBM / tabular severity triage."""

    predicted_severity: Literal["low", "medium", "high", "critical"] = "low"
    maintenance_priority: float = 0.0
    class_probabilities: dict[str, float] = Field(default_factory=dict)
    feature_snapshot: dict[str, Any] = Field(default_factory=dict)


class FusedEvidence(BaseModel):
    """Merged signals before retrieval and drafting."""

    summary_bullets: list[str] = Field(default_factory=list)
    key_entities: dict[str, str] = Field(default_factory=dict)
    evidence_refs: list[str] = Field(default_factory=list)


class RetrievedChunk(BaseModel):
    """One RAG hit with provenance for citations."""

    chunk_id: str
    text: str
    source_uri: str
    score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class ReportSection(BaseModel):
    """Structured section in the inspection report."""

    title: str
    body: str = ""
    citations: list[str] = Field(default_factory=list)


class InspectionReportDraft(BaseModel):
    """Draft inspection report (writer output)."""

    title: str = "Inspection Report"
    equipment_id: str | None = None
    inspection_date: str | None = None
    sections: list[ReportSection] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list)
    markdown_export: str | None = None


class RuleIssue(BaseModel):
    """Single rule violation or warning."""

    code: str
    message: str
    severity: Literal["error", "warning"] = "error"


class RuleCheckResult(BaseModel):
    """Deterministic template / policy checks."""

    passed: bool = True
    issues: list[RuleIssue] = Field(default_factory=list)


class ReviewIssue(BaseModel):
    """Reviewer finding."""

    code: str
    message: str
    severity: Literal["blocker", "major", "minor"] = "major"


class ReviewResult(BaseModel):
    """LLM reviewer outcome."""

    passed: bool = False
    hallucination_risk: Literal["low", "medium", "high"] = "low"
    unsupported_claims: list[str] = Field(default_factory=list)
    issues: list[ReviewIssue] = Field(default_factory=list)
    suggested_edits: list[str] = Field(default_factory=list)
