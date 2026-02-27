"""Tests for agentic_ifs.dynamics — metrics and thresholds."""

from __future__ import annotations

from uuid import uuid4

import pytest

from agentic_ifs import (
    COMPASSION_THRESHOLD,
    BlendState,
    Edge,
    EdgeType,
    Exile,
    Firefighter,
    Manager,
    ProtectionGraph,
    SelfSystem,
    is_self_led,
    self_preservation_ratio,
)
from agentic_ifs.dynamics import detect_polarization


class TestCompassionThreshold:
    def test_value(self) -> None:
        assert COMPASSION_THRESHOLD == 0.5


class TestIsSelfLed:
    def test_above_threshold(self) -> None:
        ss = SelfSystem(self_energy=0.7)
        assert is_self_led(ss) is True

    def test_at_threshold(self) -> None:
        ss = SelfSystem(self_energy=0.5)
        assert is_self_led(ss) is False  # Must be strictly above

    def test_below_threshold(self) -> None:
        ss = SelfSystem(self_energy=0.3)
        assert is_self_led(ss) is False

    def test_crisis_state(self) -> None:
        ss = SelfSystem(self_energy=0.05)
        assert is_self_led(ss) is False

    def test_after_blend(self) -> None:
        ss = SelfSystem()
        ss.blend(BlendState(part_id=uuid4(), blending_percentage=0.8))
        assert is_self_led(ss) is False

    def test_after_unblend(self) -> None:
        ss = SelfSystem()
        pid = uuid4()
        ss.blend(BlendState(part_id=pid, blending_percentage=0.8))
        ss.unblend(pid)
        assert is_self_led(ss) is True


class TestSelfPreservationRatio:
    def test_no_exiles(self) -> None:
        ss = SelfSystem(self_energy=0.5)
        graph = ProtectionGraph()
        assert self_preservation_ratio(ss, graph) == 1.0

    def test_zero_activation(self) -> None:
        ss = SelfSystem(self_energy=0.5)
        graph = ProtectionGraph()
        exile = Exile(
            narrative="test",
            age=5,
            intent="hold pain",
            emotional_charge=0.0,
        )
        graph.add_part(exile)
        assert self_preservation_ratio(ss, graph) == 1.0

    def test_balanced(self) -> None:
        ss = SelfSystem(self_energy=0.5)
        graph = ProtectionGraph()
        exile = Exile(
            narrative="test",
            age=5,
            intent="hold pain",
            emotional_charge=0.5,
        )
        graph.add_part(exile)
        ratio = self_preservation_ratio(ss, graph)
        assert ratio == pytest.approx(1.0)  # 0.5 / 0.5 = 1.0

    def test_low_self_energy(self) -> None:
        ss = SelfSystem(self_energy=0.1)
        graph = ProtectionGraph()
        exile = Exile(
            narrative="test",
            age=5,
            intent="hold pain",
            emotional_charge=0.5,
        )
        graph.add_part(exile)
        ratio = self_preservation_ratio(ss, graph)
        assert ratio == pytest.approx(0.2)  # 0.1 / 0.5

    def test_capped_at_one(self) -> None:
        ss = SelfSystem(self_energy=0.9)
        graph = ProtectionGraph()
        exile = Exile(
            narrative="test",
            age=5,
            intent="hold pain",
            emotional_charge=0.3,
        )
        graph.add_part(exile)
        ratio = self_preservation_ratio(ss, graph)
        assert ratio == 1.0  # Capped

    def test_multiple_exiles(self) -> None:
        ss = SelfSystem(self_energy=0.3)
        graph = ProtectionGraph()
        for i in range(3):
            graph.add_part(Exile(
                narrative=f"exile {i}",
                age=5 + i,
                intent="hold pain",
                emotional_charge=0.5,
            ))
        ratio = self_preservation_ratio(ss, graph)
        assert ratio == pytest.approx(0.2)  # 0.3 / 1.5


class TestDetectPolarization:
    """Tests for detect_polarization() — V2 heuristic detection."""

    def _make_graph_with_shared_exile(
        self,
        mgr_trust: float = 0.2,
        ff_trust: float = 0.3,
    ) -> tuple[ProtectionGraph, Manager, Firefighter, Exile]:
        """Helper: create a graph with a Manager and Firefighter protecting the same Exile."""
        graph = ProtectionGraph()
        exile = Exile(
            narrative="abandoned child",
            age=5,
            intent="hold pain",
            emotional_charge=0.8,
        )
        mgr = Manager(
            narrative="perfectionist",
            age=10,
            intent="prevent failure",
            trust_level=mgr_trust,
            strategies=["overwork"],
            rigidity=0.7,
        )
        ff = Firefighter(
            narrative="procrastinator",
            age=12,
            intent="numb pain",
            trust_level=ff_trust,
            pain_threshold=0.6,
            extinguishing_behaviors=["avoidance"],
        )
        graph.add_part(exile)
        graph.add_part(mgr)
        graph.add_part(ff)
        graph.add_edge(Edge(source_id=mgr.id, target_id=exile.id, edge_type=EdgeType.PROTECTS))
        graph.add_edge(Edge(source_id=ff.id, target_id=exile.id, edge_type=EdgeType.PROTECTS))
        return graph, mgr, ff, exile

    def test_detects_low_trust_pair(self) -> None:
        graph, mgr, ff, _ = self._make_graph_with_shared_exile(
            mgr_trust=0.2, ff_trust=0.3,
        )
        suggestions = detect_polarization(graph)
        assert len(suggestions) == 1
        edge = suggestions[0]
        assert edge.part_a_id == mgr.id
        assert edge.part_b_id == ff.id

    def test_tension_level(self) -> None:
        graph, _, _, _ = self._make_graph_with_shared_exile(
            mgr_trust=0.2, ff_trust=0.3,
        )
        suggestions = detect_polarization(graph)
        # tension = 1.0 - min(0.2, 0.3) = 0.8
        assert suggestions[0].tension_level == 0.8

    def test_high_trust_not_detected(self) -> None:
        graph, _, _, _ = self._make_graph_with_shared_exile(
            mgr_trust=0.8, ff_trust=0.7,
        )
        suggestions = detect_polarization(graph)
        assert suggestions == []

    def test_one_high_trust_not_detected(self) -> None:
        graph, _, _, _ = self._make_graph_with_shared_exile(
            mgr_trust=0.2, ff_trust=0.8,
        )
        suggestions = detect_polarization(graph)
        assert suggestions == []

    def test_custom_threshold(self) -> None:
        graph, _, _, _ = self._make_graph_with_shared_exile(
            mgr_trust=0.5, ff_trust=0.5,
        )
        # Default threshold 0.4 — these don't qualify
        assert detect_polarization(graph) == []
        # Raise threshold to 0.6 — now they qualify
        suggestions = detect_polarization(graph, trust_threshold=0.6)
        assert len(suggestions) == 1

    def test_no_shared_exile_no_detection(self) -> None:
        graph = ProtectionGraph()
        exile_a = Exile(narrative="a", age=5, intent="hold", emotional_charge=0.5)
        exile_b = Exile(narrative="b", age=6, intent="hold", emotional_charge=0.5)
        mgr = Manager(
            narrative="ctrl", age=10, intent="prevent",
            trust_level=0.1, strategies=["plan"], rigidity=0.5,
        )
        ff = Firefighter(
            narrative="numb", age=12, intent="escape",
            trust_level=0.1, pain_threshold=0.5, extinguishing_behaviors=["drink"],
        )
        graph.add_part(exile_a)
        graph.add_part(exile_b)
        graph.add_part(mgr)
        graph.add_part(ff)
        graph.add_edge(Edge(source_id=mgr.id, target_id=exile_a.id, edge_type=EdgeType.PROTECTS))
        graph.add_edge(Edge(source_id=ff.id, target_id=exile_b.id, edge_type=EdgeType.PROTECTS))
        assert detect_polarization(graph) == []

    def test_already_polarized_excluded(self) -> None:
        from agentic_ifs.graph import PolarizationEdge

        graph, mgr, ff, _ = self._make_graph_with_shared_exile(
            mgr_trust=0.2, ff_trust=0.3,
        )
        # Manually add them as already polarized
        graph.polarization_edges.append(
            PolarizationEdge(
                part_a_id=mgr.id,
                part_b_id=ff.id,
                tension_level=0.7,
            )
        )
        suggestions = detect_polarization(graph)
        assert suggestions == []

    def test_empty_graph(self) -> None:
        graph = ProtectionGraph()
        assert detect_polarization(graph) == []
