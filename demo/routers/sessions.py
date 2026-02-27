"""Sessions router — create, list, get, and delete IFS sessions."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Response

from demo.models import CreateSessionRequest, SessionSummary
from demo.store import create_session, delete_session, get_session, list_sessions

router = APIRouter(tags=["sessions"])


@router.post("/sessions", status_code=201)
def create(body: CreateSessionRequest | None = None) -> SessionSummary:
    """Create a new IFS session.

    Returns a SessionSummary with the new session ID and initial metrics.
    """
    req = body or CreateSessionRequest()
    sid = create_session(initial_self_energy=req.initial_self_energy)
    session = get_session(sid)
    return SessionSummary(
        session_id=sid,
        self_energy=session.self_system.self_energy,
        is_self_led=session.is_self_led,
        preservation_ratio=session.preservation_ratio,
        part_count=len(session.graph.nodes),
    )


@router.get("/sessions")
def list_all() -> list[UUID]:
    """List all active session IDs."""
    return list_sessions()


@router.get("/sessions/{session_id}")
def get(session_id: UUID) -> SessionSummary:
    """Get a summary of a specific session."""
    session = get_session(session_id)
    return SessionSummary(
        session_id=session_id,
        self_energy=session.self_system.self_energy,
        is_self_led=session.is_self_led,
        preservation_ratio=session.preservation_ratio,
        part_count=len(session.graph.nodes),
    )


@router.delete("/sessions/{session_id}", status_code=204)
def delete(session_id: UUID) -> Response:
    """Delete a session. Returns 204 No Content."""
    delete_session(session_id)
    return Response(status_code=204)
