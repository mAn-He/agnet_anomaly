"""FastAPI entrypoint for FieldOps Copilot."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import approval, graph, health, ingest, sessions
from app.config import get_settings

APP_TITLE = "FieldOps Copilot API"


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=APP_TITLE, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(sessions.router)
    app.include_router(ingest.router)
    app.include_router(graph.router)
    app.include_router(approval.router)

    return app


app = create_app()
