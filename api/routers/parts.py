"""Parts router — add and query Parts within a session."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import TypeAdapter

from agentic_ifs import PartUnion

from api.store import get_session

router = APIRouter(tags=["parts"])

part_adapter = TypeAdapter(PartUnion)


@router.post("/sessions/{session_id}/parts", status_code=201)
def add_part(session_id: UUID, body: dict[str, Any]) -> dict[str, Any]:
    """Add a Part to the session.

    Accepts a raw JSON body with a ``part_type`` discriminator field
    (``"manager"``, ``"firefighter"``, or ``"exile"``). Pydantic validates
    and deserialises to the correct Part subclass.
    """
    session = get_session(session_id)
    part = part_adapter.validate_python(body)
    session.add_part(part)
    return part_adapter.dump_python(part, mode="json")


@router.get("/sessions/{session_id}/parts")
def list_parts(session_id: UUID) -> list[dict[str, Any]]:
    """List all Parts in the session."""
    session = get_session(session_id)
    return [
        part_adapter.dump_python(part, mode="json")
        for part in session.graph.nodes.values()
    ]


@router.get("/sessions/{session_id}/parts/{part_id}")
def get_part(session_id: UUID, part_id: UUID) -> dict[str, Any]:
    """Get a specific Part by ID."""
    session = get_session(session_id)
    if part_id not in session.graph.nodes:
        raise KeyError(f"Part {part_id} not found in session {session_id}")
    part = session.graph.nodes[part_id]
    return part_adapter.dump_python(part, mode="json")
