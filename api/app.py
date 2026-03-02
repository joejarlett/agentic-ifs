"""Main FastAPI application for the agentic-ifs API.

A thin REST wrapper around the agentic-ifs library, designed for
frontend integration, interactive exploration, and Swagger-based
experimentation.
"""

from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import dynamics, export, graph, parts, sessions, workflow

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="agentic-ifs API",
    description=(
        "REST wrapper around the **agentic-ifs** library — Internal Family "
        "Systems as multi-agent computational architecture.\n\n"
        "This API exposes sessions, Parts, the protection graph, blending "
        "dynamics, the 6 Fs workflow, and Parts Map export.\n\n"
        "**Not clinical software.** For research, simulation, and "
        "philosophical exploration only."
    ),
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

cors_origins = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

API_PREFIX = "/api/v1"

app.include_router(sessions.router, prefix=API_PREFIX)
app.include_router(parts.router, prefix=API_PREFIX)
app.include_router(graph.router, prefix=API_PREFIX)
app.include_router(workflow.router, prefix=API_PREFIX)
app.include_router(dynamics.router, prefix=API_PREFIX)
app.include_router(export.router, prefix=API_PREFIX)

# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Return 422 for validation / value errors from the library."""
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(KeyError)
async def key_error_handler(request: Request, exc: KeyError) -> JSONResponse:
    """Return 404 for missing sessions or Parts."""
    return JSONResponse(status_code=404, content={"detail": str(exc)})


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


@app.get("/")
def root() -> dict[str, str]:
    """Welcome endpoint with link to interactive docs."""
    return {
        "message": "agentic-ifs API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
