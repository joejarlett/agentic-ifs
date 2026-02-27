"""Dynamics router — blending, unblending, metrics, and session log."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter

from agentic_ifs import BlendState

from demo.models import BlendRequest, MetricsResponse
from demo.store import get_session

router = APIRouter(tags=["dynamics"])


@router.post("/sessions/{session_id}/blend")
def blend(session_id: UUID, body: BlendRequest) -> dict[str, float]:
    """Blend a Part with the system.

    IFS: The Part steps into the seat of consciousness and begins
    controlling the system's I/O. Returns the resulting self_energy.
    """
    session = get_session(session_id)
    blend_state = BlendState(
        part_id=body.part_id,
        blending_percentage=body.blending_percentage,
        occlusion_mask=body.occlusion_mask,
    )
    session.blend(blend_state)
    return {"self_energy": session.self_system.self_energy}


@router.post("/sessions/{session_id}/unblend/{part_id}")
def unblend(session_id: UUID, part_id: UUID) -> dict[str, float]:
    """Unblend a Part from the system.

    IFS: The Part steps back from the seat of consciousness, allowing
    Self to observe it rather than *be* it. Returns the resulting
    self_energy.
    """
    session = get_session(session_id)
    session.unblend(part_id)
    return {"self_energy": session.self_system.self_energy}


@router.get("/sessions/{session_id}/metrics")
def metrics(session_id: UUID) -> MetricsResponse:
    """Get system metrics for a session.

    Returns self_energy, self_potential, is_self_led, preservation_ratio,
    and the count of active blends.
    """
    session = get_session(session_id)
    return MetricsResponse(
        self_energy=session.self_system.self_energy,
        self_potential=session.self_system.self_potential,
        is_self_led=session.is_self_led,
        preservation_ratio=session.preservation_ratio,
        active_blend_count=len(session.self_system.active_blends),
    )


@router.get("/sessions/{session_id}/blends")
def list_blends(session_id: UUID) -> list[dict[str, Any]]:
    """List all active BlendStates in the session."""
    session = get_session(session_id)
    return [b.model_dump(mode="json") for b in session.self_system.active_blends]


@router.get("/sessions/{session_id}/log")
def session_log(session_id: UUID) -> list[dict[str, Any]]:
    """Get the full session log (all timestamped events)."""
    session = get_session(session_id)
    return [entry.model_dump(mode="json") for entry in session.self_system.session_log]
