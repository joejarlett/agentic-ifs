"""ProtectionGraph — the directed graph of Part relationships.

IFS models the internal system as a network of Parts with typed
relationships: protection (Manager/Firefighter → Exile), polarization
(two Parts locked in mutual escalation), and alliance (cooperative Parts).

This module provides:
    - ``Edge`` and ``EdgeType`` for general relationships
    - ``PolarizationEdge`` for explicitly declared polarization (V1)
    - ``ProtectionGraph`` as the graph container with query methods
    - ``to_json()`` for Parts Map export (JSON for D3.js, Gephi, etc.)
"""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from .parts import Exile, IPart, PartUnion


class EdgeType(str, Enum):
    """Types of relationships between Parts.

    IFS:
        - PROTECTS: a Protector (Manager or Firefighter) guards an Exile
        - POLARIZED: two Parts locked in mutual escalation (deadlock)
        - ALLIED: Parts cooperating toward a shared protective goal
    """

    PROTECTS = "protects"
    POLARIZED = "polarized"
    ALLIED = "allied"


class Edge(BaseModel):
    """A directed relationship between two Parts.

    ``source_id`` → ``target_id`` with a typed relationship.
    For PROTECTS edges: source is the Protector, target is the Exile.
    """

    source_id: UUID
    target_id: UUID
    edge_type: EdgeType


class PolarizationEdge(BaseModel):
    """Explicit declaration of polarization between two Parts.

    IFS: Polarization is a feedback loop where two Parts escalate in
    opposition — e.g. Perfectionist Manager ↔ Procrastinator Firefighter.
    When one activates, the other escalates.

    Must be explicitly declared in V1 — auto-detection is V2 scope.

    Computational equivalent: Deadlock / Resource Contention.
    """

    part_a_id: UUID
    part_b_id: UUID
    tension_level: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Intensity of the polarized conflict (0.0–1.0)",
    )


class ProtectionGraph(BaseModel):
    """The internal system's relationship graph.

    Contains all Parts (nodes) and their relationships (edges). This is
    the data structure behind the "Parts Map" — a sociogram of the
    internal system.

    Nodes use the ``PartUnion`` discriminated union for correct Pydantic
    serialisation/deserialisation of Part subtypes.
    """

    nodes: dict[UUID, PartUnion] = Field(default_factory=dict)
    edges: list[Edge] = Field(default_factory=list)
    polarization_edges: list[PolarizationEdge] = Field(default_factory=list)

    def add_part(self, part: IPart) -> None:
        """Add a Part to the graph."""
        self.nodes[part.id] = part  # type: ignore[assignment]

    def remove_part(self, part_id: UUID) -> None:
        """Remove a Part and all its edges from the graph."""
        self.nodes.pop(part_id, None)
        self.edges = [
            e for e in self.edges
            if e.source_id != part_id and e.target_id != part_id
        ]
        self.polarization_edges = [
            pe for pe in self.polarization_edges
            if pe.part_a_id != part_id and pe.part_b_id != part_id
        ]

    def add_edge(self, edge: Edge) -> None:
        """Add a directed edge between two Parts.

        Both source and target must already exist in the graph.
        """
        if edge.source_id not in self.nodes:
            raise ValueError(f"Source Part {edge.source_id} not in graph")
        if edge.target_id not in self.nodes:
            raise ValueError(f"Target Part {edge.target_id} not in graph")
        self.edges.append(edge)

    def add_polarization(self, edge: PolarizationEdge) -> None:
        """Declare a polarization between two Parts.

        IFS: This is an explicit declaration by the researcher/facilitator
        that these two Parts are locked in mutual escalation.
        """
        if edge.part_a_id not in self.nodes:
            raise ValueError(f"Part A {edge.part_a_id} not in graph")
        if edge.part_b_id not in self.nodes:
            raise ValueError(f"Part B {edge.part_b_id} not in graph")
        self.polarization_edges.append(edge)

    def get_protectors_of(self, exile_id: UUID) -> list[IPart]:
        """Return all Parts that protect a given Exile.

        IFS: Finds the Managers and Firefighters organized around an Exile.
        """
        protector_ids = [
            e.source_id for e in self.edges
            if e.target_id == exile_id and e.edge_type == EdgeType.PROTECTS
        ]
        return [self.nodes[pid] for pid in protector_ids if pid in self.nodes]

    def get_exiles(self) -> list[Exile]:
        """Return all Exile Parts in the graph."""
        return [p for p in self.nodes.values() if isinstance(p, Exile)]

    def get_polarized_pairs(self) -> list[PolarizationEdge]:
        """Return all declared polarization relationships."""
        return list(self.polarization_edges)

    def get_shared_exiles(self, part_a_id: UUID, part_b_id: UUID) -> list[Exile]:
        """Return Exiles protected by both ``part_a`` and ``part_b``.

        IFS: When two Protectors guard the same Exile, they are more
        likely to be polarized — each escalating its strategy to keep
        the Exile's pain contained.

        Used by ``detect_polarization()`` to identify potential pairs.
        """
        a_targets = {
            e.target_id for e in self.edges
            if e.source_id == part_a_id and e.edge_type == EdgeType.PROTECTS
        }
        b_targets = {
            e.target_id for e in self.edges
            if e.source_id == part_b_id and e.edge_type == EdgeType.PROTECTS
        }
        shared_ids = a_targets & b_targets
        exiles: list[Exile] = [
            self.nodes[pid]  # type: ignore[misc]
            for pid in shared_ids
            if pid in self.nodes and isinstance(self.nodes[pid], Exile)
        ]
        return exiles

    def to_json(self) -> dict[str, Any]:
        """Export the Parts Map as a JSON-serialisable dict.

        Output format is compatible with force-directed graph visualisation
        tools (D3.js, Gephi, Cytoscape).

        Node size = emotional_charge (for Exiles) or rigidity (for Managers).
        Edge colour convention: PROTECTS=green, POLARIZED=red, ALLIED=blue.
        """
        nodes = []
        for part in self.nodes.values():
            node: dict[str, Any] = {
                "id": str(part.id),
                "label": part.narrative[:50] if part.narrative else "",
                "type": part.part_type,
                "state": part.state.value if hasattr(part, "state") else None,
                "trust_level": part.trust_level,
            }
            if isinstance(part, Exile):
                node["emotional_charge"] = part.emotional_charge
            nodes.append(node)

        edges: list[dict[str, Any]] = [
            {
                "source": str(e.source_id),
                "target": str(e.target_id),
                "type": e.edge_type.value,
            }
            for e in self.edges
        ]

        # Include polarization edges as a special edge type
        for pe in self.polarization_edges:
            edges.append({
                "source": str(pe.part_a_id),
                "target": str(pe.part_b_id),
                "type": "polarized",
                "tension": pe.tension_level,
            })

        return {"nodes": nodes, "edges": edges}
