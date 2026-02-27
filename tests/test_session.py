"""Tests for agentic_ifs.session — Session convenience facade."""

from __future__ import annotations

import json

import pytest

from agentic_ifs import (
    BlendState,
    BodyMap,
    Burden,
    BurdenType,
    Edge,
    EdgeType,
    Exile,
    FivePs,
    Firefighter,
    Manager,
    PolarizationEdge,
    ProtectionGraph,
    SelfSystem,
    SixFsStep,
    Trailhead,
    TrailheadLog,
    TrailheadType,
    UnburdeningElement,
)
from agentic_ifs.session import Session
from agentic_ifs.workflow import FocusShift


class TestSessionCreation:
    def test_default_creation(self) -> None:
        session = Session()
        assert isinstance(session.graph, ProtectionGraph)
        assert isinstance(session.self_system, SelfSystem)
        assert isinstance(session.trailhead_log, TrailheadLog)
        assert session.self_system.self_energy == 0.3

    def test_custom_self_energy(self) -> None:
        session = Session(initial_self_energy=0.05)
        assert session.self_system.self_energy == 0.05


class TestSessionDelegation:
    @pytest.fixture
    def session(self) -> Session:
        return Session(initial_self_energy=0.8)

    def test_add_part(self, session: Session, manager: Manager) -> None:
        session.add_part(manager)
        assert manager.id in session.graph.nodes

    def test_add_edge(
        self,
        session: Session,
        manager: Manager,
        exile: Exile,
    ) -> None:
        session.add_part(manager)
        session.add_part(exile)
        session.add_edge(Edge(
            source_id=manager.id,
            target_id=exile.id,
            edge_type=EdgeType.PROTECTS,
        ))
        assert len(session.graph.edges) == 1

    def test_add_polarization(
        self,
        session: Session,
        manager: Manager,
        firefighter: Firefighter,
    ) -> None:
        session.add_part(manager)
        session.add_part(firefighter)
        session.add_polarization(PolarizationEdge(
            part_a_id=manager.id,
            part_b_id=firefighter.id,
        ))
        assert len(session.graph.polarization_edges) == 1

    def test_blend_and_unblend(self, session: Session, manager: Manager) -> None:
        session.add_part(manager)
        session.blend(BlendState(
            part_id=manager.id,
            blending_percentage=0.7,
        ))
        assert session.self_system.self_energy == pytest.approx(0.3)

        session.unblend(manager.id)
        assert session.self_system.self_energy == pytest.approx(1.0)


class TestSessionWorkflow:
    def test_six_fs_delegation(
        self,
        manager: Manager,
        exile: Exile,
    ) -> None:
        session = Session(initial_self_energy=0.8)
        session.add_part(manager)
        session.add_part(exile)
        session.add_edge(Edge(
            source_id=manager.id,
            target_id=exile.id,
            edge_type=EdgeType.PROTECTS,
        ))

        trailhead = Trailhead(
            trailhead_type=TrailheadType.SOMATIC,
            intensity=0.6,
            description="Chest tightness",
            associated_part_id=exile.id,
        )

        r1 = session.find(trailhead)
        assert r1.step == SixFsStep.FIND

        r2 = session.focus(exile.id)
        assert r2.step == SixFsStep.FOCUS

        r3 = session.flesh_out(exile.id)
        assert r3.step == SixFsStep.FLESH_OUT

        r4 = session.feel_toward(exile.id)
        assert r4.step == SixFsStep.FEEL_TOWARD
        assert r4.next_step == SixFsStep.BEFRIEND  # Self-led

        r5 = session.befriend(exile.id)
        assert r5.step == SixFsStep.BEFRIEND

        r6 = session.fear(exile.id)
        assert r6.step == SixFsStep.FEAR
        assert r6.next_step is None


class TestSessionMetrics:
    def test_is_self_led(self) -> None:
        session = Session(initial_self_energy=0.8)
        assert session.is_self_led is True

    def test_is_not_self_led(self) -> None:
        session = Session(initial_self_energy=0.3)
        assert session.is_self_led is False

    def test_preservation_ratio_no_parts(self) -> None:
        session = Session()
        assert session.preservation_ratio == 1.0


class TestSessionFocusShift:
    def test_record_focus_shift(self) -> None:
        session = Session()
        fs = FocusShift(from_subject="My boss", to_subject="My Anger")
        session.record_focus_shift(fs)
        assert len(session.focus_shifts) == 1
        assert session.focus_shifts[0].from_subject == "My boss"

    def test_focus_shifts_returns_copy(self) -> None:
        session = Session()
        fs = FocusShift(from_subject="test", to_subject="test")
        session.record_focus_shift(fs)
        shifts = session.focus_shifts
        shifts.clear()  # Mutating the returned list
        assert len(session.focus_shifts) == 1  # Original unchanged


class TestSessionExport:
    def test_export_parts_map(
        self,
        manager: Manager,
        firefighter: Firefighter,
        exile: Exile,
    ) -> None:
        session = Session()
        session.add_part(manager)
        session.add_part(firefighter)
        session.add_part(exile)
        session.add_edge(Edge(
            source_id=manager.id,
            target_id=exile.id,
            edge_type=EdgeType.PROTECTS,
        ))

        parts_map = session.export_parts_map()
        assert "nodes" in parts_map
        assert "edges" in parts_map
        assert len(parts_map["nodes"]) == 3
        assert len(parts_map["edges"]) == 1

        # Should be JSON-serialisable
        json_str = json.dumps(parts_map)
        assert json_str  # Non-empty


class TestSessionV2Properties:
    def test_modifiers_default_none(self) -> None:
        session = Session()
        assert session.modifiers is None

    def test_modifiers_passed(self) -> None:
        mods = FivePs(patience=0.9)
        session = Session(modifiers=mods)
        assert session.modifiers is mods

    def test_body_map_default_empty(self) -> None:
        session = Session()
        assert isinstance(session.body_map, BodyMap)
        assert session.body_map.markers == []

    def test_body_map_passed(self) -> None:
        bm = BodyMap()
        session = Session(body_map=bm)
        assert session.body_map is bm

    def test_dialogue_default_none(self) -> None:
        session = Session()
        assert session.dialogue is None

    def test_unburdening_available(self) -> None:
        session = Session()
        assert session.unburdening is not None


class TestSessionUnburdening:
    def test_full_unburdening_via_session(self) -> None:
        session = Session(initial_self_energy=0.8)
        exile = Exile(
            narrative="abandoned child",
            age=5,
            intent="hold pain",
            emotional_charge=0.9,
            burden=Burden(
                burden_type=BurdenType.PERSONAL,
                origin="Age 5, school rejection",
                content="I am not wanted",
            ),
        )
        session.add_part(exile)

        r1 = session.witness(exile.id)
        assert r1.next_step is not None

        r2 = session.retrieve(exile.id)
        assert r2.next_step is not None

        r3 = session.purge(exile.id, UnburdeningElement.WATER)
        assert r3.next_step is not None

        r4 = session.invite(exile.id, ["safety", "belonging"])
        assert r4.next_step is None  # Complete
        assert exile.burden is None
        assert exile.invited_qualities == ["safety", "belonging"]


class TestSessionDialogue:
    def test_speak_as_without_provider_raises(self) -> None:
        from uuid import uuid4

        session = Session()
        with pytest.raises(RuntimeError, match="No dialogue provider"):
            session.speak_as(uuid4(), "hello")

    def test_direct_access_without_provider_raises(self) -> None:
        from uuid import uuid4

        session = Session()
        with pytest.raises(RuntimeError, match="No dialogue provider"):
            session.direct_access(uuid4(), "hello")


class TestSessionDetectPolarization:
    def test_detect_polarization_via_session(self) -> None:
        session = Session(initial_self_energy=0.8)
        exile = Exile(
            narrative="lonely child",
            age=6,
            intent="hold loneliness",
            emotional_charge=0.7,
        )
        mgr = Manager(
            narrative="controller",
            age=10,
            intent="prevent vulnerability",
            trust_level=0.2,
            strategies=["control"],
            rigidity=0.8,
        )
        ff = Firefighter(
            narrative="escapist",
            age=13,
            intent="numb the pain",
            trust_level=0.3,
            pain_threshold=0.5,
            extinguishing_behaviors=["gaming"],
        )
        session.add_part(exile)
        session.add_part(mgr)
        session.add_part(ff)
        session.add_edge(Edge(
            source_id=mgr.id, target_id=exile.id, edge_type=EdgeType.PROTECTS,
        ))
        session.add_edge(Edge(
            source_id=ff.id, target_id=exile.id, edge_type=EdgeType.PROTECTS,
        ))

        suggestions = session.detect_polarization()
        assert len(suggestions) == 1
        assert suggestions[0].part_a_id == mgr.id
        assert suggestions[0].part_b_id == ff.id
