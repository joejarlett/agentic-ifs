"""Export router — Parts Map export for visualisation tools."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter

from api.store import get_session

router = APIRouter(tags=["export"])


@router.get("/sessions/{session_id}/parts-map")
def parts_map(session_id: UUID) -> dict[str, Any]:
    """Export the Parts Map as JSON.

    Output is compatible with force-directed graph visualisation tools
    (D3.js, Gephi, Cytoscape). Contains nodes (Parts) and edges
    (relationships including polarizations).
    """
    session = get_session(session_id)
    return session.export_parts_map()
