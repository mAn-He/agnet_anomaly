"""Heuristic modality detection from MIME type and filename."""

from __future__ import annotations

from app.schemas.inputs import Modality, UploadedArtifact


def infer_modality(mime_type: str, filename: str | None) -> Modality:
    """Best-effort modality from MIME and extension."""
    mt = (mime_type or "").lower()
    name = (filename or "").lower()

    if mt.startswith("image/"):
        if "pdf" in name or name.endswith(".pdf"):
            return Modality.PDF
        if any(name.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff")):
            return Modality.IMAGE
        return Modality.DOCUMENT_IMAGE

    if mt == "application/pdf" or name.endswith(".pdf"):
        return Modality.PDF

    if mt in ("text/plain", "text/markdown") or name.endswith(".txt"):
        return Modality.TEXT

    if mt in ("text/csv", "application/json") or name.endswith(".csv"):
        return Modality.TABULAR

    return Modality.UNKNOWN


def enrich_artifact_modality(artifact: UploadedArtifact) -> UploadedArtifact:
    """Fill UNKNOWN modality using `infer_modality`."""
    if artifact.modality != Modality.UNKNOWN:
        return artifact
    return artifact.model_copy(
        update={"modality": infer_modality(artifact.mime_type, artifact.filename)}
    )
