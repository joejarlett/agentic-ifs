"""Tests for agentic_ifs.self_system — SelfSystem, BlendState, LogEntry."""

from __future__ import annotations

from uuid import uuid4

import pytest

from agentic_ifs import BlendState, SelfSystem


class TestBlendState:
    def test_creation(self) -> None:
        bs = BlendState(part_id=uuid4(), blending_percentage=0.7)
        assert bs.blending_percentage == 0.7
        assert bs.occlusion_mask == {}

    def test_with_occlusion_mask(self) -> None:
        bs = BlendState(
            part_id=uuid4(),
            blending_percentage=0.8,
            occlusion_mask={"calm": 0.9, "clarity": 0.5},
        )
        assert bs.occlusion_mask["calm"] == 0.9


class TestSelfSystem:
    def test_defaults(self) -> None:
        ss = SelfSystem()
        assert ss.self_potential == 1.0
        assert ss.self_energy == 0.3
        assert ss.active_blends == []
        assert ss.session_log == []

    def test_recalculate_no_blends(self) -> None:
        ss = SelfSystem()
        ss.recalculate()
        assert ss.self_energy == 1.0  # No blends → full access

    def test_recalculate_single_blend(self) -> None:
        ss = SelfSystem()
        ss.active_blends = [
            BlendState(part_id=uuid4(), blending_percentage=0.7),
        ]
        ss.recalculate()
        assert ss.self_energy == pytest.approx(0.3)  # 1.0 * (1 - 0.7)

    def test_recalculate_multiple_blends_uses_max(self) -> None:
        ss = SelfSystem()
        ss.active_blends = [
            BlendState(part_id=uuid4(), blending_percentage=0.3),
            BlendState(part_id=uuid4(), blending_percentage=0.8),
            BlendState(part_id=uuid4(), blending_percentage=0.5),
        ]
        ss.recalculate()
        assert ss.self_energy == pytest.approx(0.2)  # 1.0 * (1 - 0.8)

    def test_recalculate_full_blend(self) -> None:
        ss = SelfSystem()
        ss.active_blends = [
            BlendState(part_id=uuid4(), blending_percentage=1.0),
        ]
        ss.recalculate()
        assert ss.self_energy == pytest.approx(0.0)

    def test_blend_adds_and_recalculates(self) -> None:
        ss = SelfSystem()
        part_id = uuid4()
        ss.blend(BlendState(part_id=part_id, blending_percentage=0.6))
        assert len(ss.active_blends) == 1
        assert ss.self_energy == pytest.approx(0.4)  # 1.0 * (1 - 0.6)

    def test_blend_replaces_existing(self) -> None:
        ss = SelfSystem()
        part_id = uuid4()
        ss.blend(BlendState(part_id=part_id, blending_percentage=0.3))
        ss.blend(BlendState(part_id=part_id, blending_percentage=0.8))
        assert len(ss.active_blends) == 1
        assert ss.self_energy == pytest.approx(0.2)  # 1.0 * (1 - 0.8)

    def test_unblend_removes_and_recalculates(self) -> None:
        ss = SelfSystem()
        part_id = uuid4()
        ss.blend(BlendState(part_id=part_id, blending_percentage=0.7))
        assert ss.self_energy == pytest.approx(0.3)

        ss.unblend(part_id)
        assert len(ss.active_blends) == 0
        assert ss.self_energy == pytest.approx(1.0)

    def test_unblend_nonexistent_is_safe(self) -> None:
        ss = SelfSystem()
        ss.unblend(uuid4())  # Should not raise
        assert ss.self_energy == pytest.approx(1.0)

    def test_blend_logs_event(self) -> None:
        ss = SelfSystem()
        part_id = uuid4()
        ss.blend(BlendState(part_id=part_id, blending_percentage=0.5))
        assert len(ss.session_log) == 1
        assert ss.session_log[0].event_type == "blend"
        assert ss.session_log[0].part_id == part_id

    def test_unblend_logs_event(self) -> None:
        ss = SelfSystem()
        part_id = uuid4()
        ss.blend(BlendState(part_id=part_id, blending_percentage=0.5))
        ss.unblend(part_id)
        assert len(ss.session_log) == 2
        assert ss.session_log[1].event_type == "unblend"

    def test_self_potential_stays_constant(self) -> None:
        ss = SelfSystem()
        ss.blend(BlendState(part_id=uuid4(), blending_percentage=0.9))
        assert ss.self_potential == 1.0
        ss.unblend(ss.active_blends[0].part_id)
        assert ss.self_potential == 1.0

    def test_custom_initial_self_energy(self) -> None:
        ss = SelfSystem(self_energy=0.05)
        assert ss.self_energy == 0.05
