"""Tests for agentic_ifs.workflow — 6 Fs, Trailheads, FocusShift."""

from __future__ import annotations

from uuid import uuid4

import pytest

from agentic_ifs import (
    BlendState,
    Manager,
    ProtectionGraph,
    SelfSystem,
    SixFsStateMachine,
    SixFsStep,
    Trailhead,
    TrailheadLog,
    TrailheadType,
)
from agentic_ifs.workflow import FocusShift


class TestTrailhead:
    def test_creation(self, sample_trailhead: Trailhead) -> None:
        assert sample_trailhead.trailhead_type == TrailheadType.SOMATIC
        assert sample_trailhead.intensity == 0.6
        assert sample_trailhead.associated_part_id is not None

    def test_default_no_part(self) -> None:
        t = Trailhead(
            trailhead_type=TrailheadType.COGNITIVE,
            intensity=0.4,
            description="Recurring thought: I'm going to fail",
        )
        assert t.associated_part_id is None
        assert t.timestamp is not None


class TestTrailheadLog:
    def test_add(self) -> None:
        log = TrailheadLog()
        t = Trailhead(
            trailhead_type=TrailheadType.SOMATIC,
            intensity=0.5,
            description="test",
        )
        log.add(t)
        assert len(log.entries) == 1
        assert log.entries[0] is t

    def test_get_by_type(self) -> None:
        log = TrailheadLog()
        somatic = Trailhead(
            trailhead_type=TrailheadType.SOMATIC,
            intensity=0.5,
            description="body",
        )
        cognitive = Trailhead(
            trailhead_type=TrailheadType.COGNITIVE,
            intensity=0.4,
            description="thought",
        )
        log.add(somatic)
        log.add(cognitive)

        somatic_results = log.get_by_type(TrailheadType.SOMATIC)
        assert len(somatic_results) == 1
        assert somatic_results[0].description == "body"

    def test_get_by_part(self, exile) -> None:
        log = TrailheadLog()
        t = Trailhead(
            trailhead_type=TrailheadType.VISUAL,
            intensity=0.7,
            description="image of child",
            associated_part_id=exile.id,
        )
        log.add(t)
        results = log.get_by_part(exile.id)
        assert len(results) == 1


class TestFocusShift:
    def test_creation(self) -> None:
        fs = FocusShift(
            from_subject="My boss",
            to_subject="My Anger Part",
        )
        assert fs.from_subject == "My boss"
        assert fs.to_subject == "My Anger Part"
        assert fs.trailhead_id is None
        assert fs.timestamp is not None


class TestSixFsStateMachine:
    """Test the 6 Fs workflow — the core game loop."""

    @pytest.fixture
    def workflow(
        self,
        populated_graph: ProtectionGraph,
    ) -> SixFsStateMachine:
        ss = SelfSystem(self_energy=0.8)  # Self-led
        log = TrailheadLog()
        return SixFsStateMachine(
            graph=populated_graph,
            self_system=ss,
            log=log,
        )

    @pytest.fixture
    def blended_workflow(
        self,
        populated_graph: ProtectionGraph,
        manager: Manager,
    ) -> SixFsStateMachine:
        ss = SelfSystem(self_energy=0.8)
        # Blend the manager heavily → self_energy drops below threshold
        ss.blend(BlendState(part_id=manager.id, blending_percentage=0.8))
        log = TrailheadLog()
        return SixFsStateMachine(
            graph=populated_graph,
            self_system=ss,
            log=log,
        )

    def test_find(self, workflow: SixFsStateMachine, sample_trailhead: Trailhead) -> None:
        result = workflow.find(sample_trailhead)
        assert result.step == SixFsStep.FIND
        assert result.next_step == SixFsStep.FOCUS
        assert result.target_part_id == sample_trailhead.associated_part_id
        assert len(workflow.log.entries) == 1

    def test_focus(self, workflow: SixFsStateMachine, exile) -> None:
        result = workflow.focus(exile.id)
        assert result.step == SixFsStep.FOCUS
        assert result.next_step == SixFsStep.FLESH_OUT
        assert result.target_part_id == exile.id

    def test_focus_invalid_part(self, workflow: SixFsStateMachine) -> None:
        with pytest.raises(ValueError):
            workflow.focus(uuid4())

    def test_flesh_out(self, workflow: SixFsStateMachine, exile) -> None:
        result = workflow.flesh_out(exile.id)
        assert result.step == SixFsStep.FLESH_OUT
        assert result.next_step == SixFsStep.FEEL_TOWARD
        assert "Age: 7" in result.notes

    def test_feel_toward_self_led(self, workflow: SixFsStateMachine, exile) -> None:
        """When Self-energy is sufficient, proceed to BEFRIEND."""
        result = workflow.feel_toward(exile.id)
        assert result.step == SixFsStep.FEEL_TOWARD
        assert result.next_step == SixFsStep.BEFRIEND
        assert result.unblend_required is None

    def test_feel_toward_blended(
        self,
        blended_workflow: SixFsStateMachine,
        exile,
        manager: Manager,
    ) -> None:
        """When Self-energy is low, signal that unblending is needed."""
        result = blended_workflow.feel_toward(exile.id)
        assert result.step == SixFsStep.FEEL_TOWARD
        assert result.next_step is None  # Blocked
        assert result.unblend_required == manager.id

    def test_befriend_increments_trust(self, workflow: SixFsStateMachine, exile) -> None:
        original_trust = exile.trust_level
        result = workflow.befriend(exile.id)
        assert result.step == SixFsStep.BEFRIEND
        assert result.next_step == SixFsStep.FEAR
        assert exile.trust_level == original_trust + 0.1

    def test_befriend_caps_trust(self, workflow: SixFsStateMachine, exile) -> None:
        exile.trust_level = 0.95
        workflow.befriend(exile.id)
        assert exile.trust_level == 1.0

    def test_fear(self, workflow: SixFsStateMachine, exile) -> None:
        result = workflow.fear(exile.id)
        assert result.step == SixFsStep.FEAR
        assert result.next_step is None  # 6 Fs complete

    def test_happy_path(
        self,
        workflow: SixFsStateMachine,
        exile,
        sample_trailhead: Trailhead,
    ) -> None:
        """Walk through the entire 6 Fs for a Self-led session."""
        r1 = workflow.find(sample_trailhead)
        assert r1.next_step == SixFsStep.FOCUS

        r2 = workflow.focus(exile.id)
        assert r2.next_step == SixFsStep.FLESH_OUT

        r3 = workflow.flesh_out(exile.id)
        assert r3.next_step == SixFsStep.FEEL_TOWARD

        r4 = workflow.feel_toward(exile.id)
        assert r4.next_step == SixFsStep.BEFRIEND

        r5 = workflow.befriend(exile.id)
        assert r5.next_step == SixFsStep.FEAR

        r6 = workflow.fear(exile.id)
        assert r6.next_step is None  # Complete

    def test_session_log_populated(
        self,
        workflow: SixFsStateMachine,
        exile,
        sample_trailhead: Trailhead,
    ) -> None:
        """Verify that running the 6 Fs creates session log entries."""
        workflow.find(sample_trailhead)
        workflow.focus(exile.id)
        workflow.flesh_out(exile.id)
        workflow.feel_toward(exile.id)
        assert len(workflow.self_system.session_log) == 4
        assert all(
            entry.event_type == "six_fs"
            for entry in workflow.self_system.session_log
        )
