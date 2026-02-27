"""Workflow router — the 6 Fs state machine endpoints."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter

from agentic_ifs import Trailhead

from demo.models import CreateTrailheadRequest
from demo.store import get_session

router = APIRouter(tags=["workflow"])


@router.post("/sessions/{session_id}/workflow/find")
def find(session_id: UUID, body: CreateTrailheadRequest) -> dict[str, Any]:
    """6 Fs Step 1: Find — locate the Part signalled by the trailhead.

    Creates a Trailhead from the request body and initiates the 6 Fs
    process.
    """
    session = get_session(session_id)
    trailhead = Trailhead(
        trailhead_type=body.trailhead_type,
        intensity=body.intensity,
        description=body.description,
        associated_part_id=body.associated_part_id,
    )
    result = session.find(trailhead)
    return result.model_dump(mode="json")


@router.post("/sessions/{session_id}/workflow/focus/{part_id}")
def focus(session_id: UUID, part_id: UUID) -> dict[str, Any]:
    """6 Fs Step 2: Focus — direct attention to the Part."""
    session = get_session(session_id)
    result = session.focus(part_id)
    return result.model_dump(mode="json")


@router.post("/sessions/{session_id}/workflow/flesh-out/{part_id}")
def flesh_out(session_id: UUID, part_id: UUID) -> dict[str, Any]:
    """6 Fs Step 3: Flesh Out — gather metadata about the Part."""
    session = get_session(session_id)
    result = session.flesh_out(part_id)
    return result.model_dump(mode="json")


@router.post("/sessions/{session_id}/workflow/feel-toward/{part_id}")
def feel_toward(session_id: UUID, part_id: UUID) -> dict[str, Any]:
    """6 Fs Step 4: Feel Toward — the critical Self-energy gate.

    If self_energy is below COMPASSION_THRESHOLD, returns
    ``unblend_required`` indicating which Part must be unblended first.
    """
    session = get_session(session_id)
    result = session.feel_toward(part_id)
    return result.model_dump(mode="json")


@router.post("/sessions/{session_id}/workflow/befriend/{part_id}")
def befriend(session_id: UUID, part_id: UUID) -> dict[str, Any]:
    """6 Fs Step 5: Befriend — build relationship, update trust."""
    session = get_session(session_id)
    result = session.befriend(part_id)
    return result.model_dump(mode="json")


@router.post("/sessions/{session_id}/workflow/fear/{part_id}")
def fear(session_id: UUID, part_id: UUID) -> dict[str, Any]:
    """6 Fs Step 6: Fear — identify the Part's worst-case scenarios."""
    session = get_session(session_id)
    result = session.fear(part_id)
    return result.model_dump(mode="json")
