"""Tests for agentic_ifs.dynamics — metrics and thresholds."""

from __future__ import annotations

from uuid import uuid4

import pytest

from agentic_ifs import (
    COMPASSION_THRESHOLD,
    BlendState,
    Exile,
    ProtectionGraph,
    SelfSystem,
    is_self_led,
    self_preservation_ratio,
)


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
