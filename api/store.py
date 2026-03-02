"""In-memory session store for the API.

Simple dict-based store keyed by UUID. No persistence — sessions are lost
on server restart.
"""

from __future__ import annotations

from uuid import UUID, uuid4

from agentic_ifs import Session

_sessions: dict[UUID, Session] = {}


def create_session(initial_self_energy: float = 0.3) -> UUID:
    """Create a new Session and return its ID."""
    sid = uuid4()
    _sessions[sid] = Session(initial_self_energy=initial_self_energy)
    return sid


def get_session(session_id: UUID) -> Session:
    """Retrieve a Session by ID. Raises KeyError if not found."""
    if session_id not in _sessions:
        raise KeyError(f"Session {session_id} not found")
    return _sessions[session_id]


def list_sessions() -> list[UUID]:
    """Return all active session IDs."""
    return list(_sessions.keys())


def delete_session(session_id: UUID) -> None:
    """Delete a session. No-op if it does not exist."""
    _sessions.pop(session_id, None)
