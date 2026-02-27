"""Tests for agentic_ifs.graph — ProtectionGraph, edges, Parts Map export."""

from __future__ import annotations

from uuid import uuid4

import pytest

from agentic_ifs import (
    Edge,
    EdgeType,
    Exile,
    Manager,
    PolarizationEdge,
    ProtectionGraph,
)


class TestProtectionGraph:
    def test_add_part(self, manager: Manager) -> None:
        graph = ProtectionGraph()
        graph.add_part(manager)
        assert manager.id in graph.nodes
        assert graph.nodes[manager.id] is manager

    def test_add_edge(self, manager: Manager, exile: Exile) -> None:
        graph = ProtectionGraph()
        graph.add_part(manager)
        graph.add_part(exile)
        edge = Edge(
            source_id=manager.id,
            target_id=exile.id,
            edge_type=EdgeType.PROTECTS,
        )
        graph.add_edge(edge)
        assert len(graph.edges) == 1

    def test_add_edge_validates_source(self, exile: Exile) -> None:
        graph = ProtectionGraph()
        graph.add_part(exile)
        with pytest.raises(ValueError, match="Source Part"):
            graph.add_edge(Edge(
                source_id=uuid4(),
                target_id=exile.id,
                edge_type=EdgeType.PROTECTS,
            ))

    def test_add_edge_validates_target(self, manager: Manager) -> None:
        graph = ProtectionGraph()
        graph.add_part(manager)
        with pytest.raises(ValueError, match="Target Part"):
            graph.add_edge(Edge(
                source_id=manager.id,
                target_id=uuid4(),
                edge_type=EdgeType.PROTECTS,
            ))

    def test_add_polarization(self, manager: Manager, firefighter) -> None:
        graph = ProtectionGraph()
        graph.add_part(manager)
        graph.add_part(firefighter)
        pe = PolarizationEdge(
            part_a_id=manager.id,
            part_b_id=firefighter.id,
            tension_level=0.8,
        )
        graph.add_polarization(pe)
        assert len(graph.polarization_edges) == 1
        assert graph.polarization_edges[0].tension_level == 0.8

    def test_add_polarization_validates_parts(self, manager: Manager) -> None:
        graph = ProtectionGraph()
        graph.add_part(manager)
        with pytest.raises(ValueError, match="Part B"):
            graph.add_polarization(PolarizationEdge(
                part_a_id=manager.id,
                part_b_id=uuid4(),
            ))

    def test_get_protectors_of(self, populated_graph: ProtectionGraph, exile: Exile) -> None:
        protectors = populated_graph.get_protectors_of(exile.id)
        assert len(protectors) == 2
        part_types = {p.part_type for p in protectors}
        assert part_types == {"manager", "firefighter"}

    def test_get_protectors_of_nonexistent(self, populated_graph: ProtectionGraph) -> None:
        protectors = populated_graph.get_protectors_of(uuid4())
        assert protectors == []

    def test_get_exiles(self, populated_graph: ProtectionGraph) -> None:
        exiles = populated_graph.get_exiles()
        assert len(exiles) == 1
        assert isinstance(exiles[0], Exile)

    def test_get_polarized_pairs(self, populated_graph: ProtectionGraph) -> None:
        pairs = populated_graph.get_polarized_pairs()
        assert len(pairs) == 1
        assert pairs[0].tension_level == 0.7

    def test_remove_part(self, populated_graph: ProtectionGraph, manager: Manager) -> None:
        populated_graph.remove_part(manager.id)
        assert manager.id not in populated_graph.nodes
        # Edges involving the manager should be removed too
        for edge in populated_graph.edges:
            assert edge.source_id != manager.id
            assert edge.target_id != manager.id
        for pe in populated_graph.polarization_edges:
            assert pe.part_a_id != manager.id
            assert pe.part_b_id != manager.id


class TestPartsMapExport:
    def test_to_json_structure(self, populated_graph: ProtectionGraph) -> None:
        result = populated_graph.to_json()
        assert "nodes" in result
        assert "edges" in result
        assert isinstance(result["nodes"], list)
        assert isinstance(result["edges"], list)

    def test_to_json_node_fields(self, populated_graph: ProtectionGraph) -> None:
        result = populated_graph.to_json()
        for node in result["nodes"]:
            assert "id" in node
            assert "label" in node
            assert "type" in node
            assert "state" in node
            assert "trust_level" in node

    def test_to_json_exile_has_charge(self, populated_graph: ProtectionGraph) -> None:
        result = populated_graph.to_json()
        exile_nodes = [n for n in result["nodes"] if n["type"] == "exile"]
        assert len(exile_nodes) == 1
        assert "emotional_charge" in exile_nodes[0]

    def test_to_json_edge_fields(self, populated_graph: ProtectionGraph) -> None:
        result = populated_graph.to_json()
        for edge in result["edges"]:
            assert "source" in edge
            assert "target" in edge
            assert "type" in edge

    def test_to_json_includes_polarization(self, populated_graph: ProtectionGraph) -> None:
        result = populated_graph.to_json()
        polarized_edges = [e for e in result["edges"] if e["type"] == "polarized"]
        assert len(polarized_edges) == 1
        assert "tension" in polarized_edges[0]

    def test_to_json_round_trip_serialisable(self, populated_graph: ProtectionGraph) -> None:
        import json

        result = populated_graph.to_json()
        # Should not raise — confirms JSON-serialisable
        json_str = json.dumps(result)
        restored = json.loads(json_str)
        assert len(restored["nodes"]) == len(result["nodes"])


class TestGraphSerialisation:
    """Test that the ProtectionGraph with PartUnion deserialises correctly."""

    def test_round_trip(self, populated_graph: ProtectionGraph) -> None:
        json_str = populated_graph.model_dump_json()
        restored = ProtectionGraph.model_validate_json(json_str)
        assert len(restored.nodes) == 3

        # Check discriminated union preserved types
        for node in restored.nodes.values():
            assert node.part_type in ("manager", "firefighter", "exile")

        managers = [n for n in restored.nodes.values() if isinstance(n, Manager)]
        assert len(managers) == 1
