"""Graph router — manage edges and polarizations between Parts."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import TypeAdapter

from agentic_ifs import Edge, PartUnion, PolarizationEdge

from demo.models import AddEdgeRequest, AddPolarizationRequest
from demo.store import get_session

router = APIRouter(tags=["graph"])

part_adapter = TypeAdapter(PartUnion)


@router.post("/sessions/{session_id}/edges", status_code=201)
def add_edge(session_id: UUID, body: AddEdgeRequest) -> dict[str, Any]:
    """Add a directed relationship edge between two Parts.

    Edge types: ``protects``, ``polarized``, ``allied``.
    Both source and target Parts must already exist in the session.
    """
    session = get_session(session_id)
    edge = Edge(
        source_id=body.source_id,
        target_id=body.target_id,
        edge_type=body.edge_type,
    )
    session.add_edge(edge)
    return edge.model_dump(mode="json")


@router.get("/sessions/{session_id}/edges")
def list_edges(session_id: UUID) -> list[dict[str, Any]]:
    """List all relationship edges in the session."""
    session = get_session(session_id)
    return [e.model_dump(mode="json") for e in session.graph.edges]


@router.post("/sessions/{session_id}/polarizations", status_code=201)
def add_polarization(session_id: UUID, body: AddPolarizationRequest) -> dict[str, Any]:
    """Declare a polarization between two Parts.

    IFS: Polarization is a feedback loop where two Parts escalate in
    opposition. Must be explicitly declared in V1.
    """
    session = get_session(session_id)
    edge = PolarizationEdge(
        part_a_id=body.part_a_id,
        part_b_id=body.part_b_id,
        tension_level=body.tension_level,
    )
    session.add_polarization(edge)
    return edge.model_dump(mode="json")


@router.get("/sessions/{session_id}/protectors/{exile_id}")
def get_protectors(session_id: UUID, exile_id: UUID) -> list[dict[str, Any]]:
    """Get all Parts that protect a given Exile.

    Returns Managers and Firefighters organized around the specified Exile.
    """
    session = get_session(session_id)
    protectors = session.graph.get_protectors_of(exile_id)
    return [part_adapter.dump_python(p, mode="json") for p in protectors]
