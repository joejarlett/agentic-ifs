"""Request and response Pydantic schemas for the demo API.

Thin request wrappers. Library models (SixFsResult, BlendState, Edge, etc.)
are returned directly from endpoints where possible.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from agentic_ifs import EdgeType, TrailheadType


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class CreateSessionRequest(BaseModel):
    """Body for POST /sessions."""

    initial_self_energy: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Starting self-energy (0.0-1.0). Default 0.3 reflects Managers running.",
    )


class AddEdgeRequest(BaseModel):
    """Body for POST /sessions/{session_id}/edges."""

    source_id: UUID
    target_id: UUID
    edge_type: EdgeType


class AddPolarizationRequest(BaseModel):
    """Body for POST /sessions/{session_id}/polarizations."""

    part_a_id: UUID
    part_b_id: UUID
    tension_level: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Intensity of the polarized conflict (0.0-1.0)",
    )


class BlendRequest(BaseModel):
    """Body for POST /sessions/{session_id}/blend."""

    part_id: UUID
    blending_percentage: float = Field(
        ge=0.0,
        le=1.0,
        description="How much I/O is Part-controlled (0.0-1.0)",
    )
    occlusion_mask: dict[str, float] = Field(
        default_factory=dict,
        description="Maps Self quality names to reduction values (V2 8C vector prep)",
    )


class CreateTrailheadRequest(BaseModel):
    """Body for POST /sessions/{session_id}/workflow/find."""

    trailhead_type: TrailheadType
    intensity: float = Field(
        ge=0.0,
        le=1.0,
        description="Intensity of the signal (0.0-1.0)",
    )
    description: str
    associated_part_id: UUID | None = None


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class SessionSummary(BaseModel):
    """Summary of a session's current state."""

    session_id: UUID
    self_energy: float
    is_self_led: bool
    preservation_ratio: float
    part_count: int


class MetricsResponse(BaseModel):
    """System metrics for a session."""

    self_energy: float
    self_potential: float
    is_self_led: bool
    preservation_ratio: float
    active_blend_count: int
