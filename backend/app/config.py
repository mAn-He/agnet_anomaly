"""Application settings (env-driven)."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _repo_data_dir() -> Path:
    """Resolve default `data/` next to repository root (parent of `backend/`)."""
    return Path(__file__).resolve().parents[2] / "data"


class Settings(BaseSettings):
    """Runtime configuration."""

    model_config = SettingsConfigDict(
        env_prefix="FIELDOPS_",
        env_file=".env",
        extra="ignore",
    )

    data_dir: Path = Field(default_factory=_repo_data_dir)
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    max_revision_iterations: int = 3
    # When True, human_approval does not call interrupt() so invoke() completes without resume.
    skip_hitl_interrupt: bool = True


def get_settings() -> Settings:
    return Settings()
