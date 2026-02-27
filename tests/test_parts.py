"""Tests for agentic_ifs.parts — Part classes, enums, and discriminated union."""

from __future__ import annotations

from datetime import timedelta
from uuid import UUID

import pytest
from pydantic import TypeAdapter, ValidationError

from agentic_ifs import (
    Burden,
    BurdenType,
    Exile,
    ExileState,
    Firefighter,
    FirefighterState,
    IPart,
    Manager,
    ManagerState,
    PartUnion,
)


class TestManagerState:
    def test_values(self) -> None:
        assert ManagerState.IDLE == "idle"
        assert ManagerState.SCANNING == "scanning"
        assert ManagerState.BLOCKING == "blocking"


class TestFirefighterState:
    def test_values(self) -> None:
        assert FirefighterState.DORMANT == "dormant"
        assert FirefighterState.ACTIVE == "active"
        assert FirefighterState.COOLDOWN == "cooldown"


class TestExileState:
    def test_values(self) -> None:
        assert ExileState.ISOLATED == "isolated"
        assert ExileState.LEAKING == "leaking"
        assert ExileState.FLOODING == "flooding"
        assert ExileState.UNBURDENED == "unburdened"


class TestBurden:
    def test_creation(self) -> None:
        burden = Burden(
            burden_type=BurdenType.PERSONAL,
            origin="Age 7, school failure",
            content="I am not enough",
            emotional_charge=0.9,
        )
        assert burden.burden_type == BurdenType.PERSONAL
        assert burden.content == "I am not enough"
        assert burden.emotional_charge == 0.9

    def test_defaults(self) -> None:
        burden = Burden(
            burden_type=BurdenType.LEGACY,
            origin="Grandmother's famine trauma",
            content="There is never enough",
        )
        assert burden.emotional_charge == 0.5

    def test_charge_validation(self) -> None:
        with pytest.raises(ValidationError):
            Burden(
                burden_type=BurdenType.PERSONAL,
                origin="test",
                content="test",
                emotional_charge=1.5,
            )


class TestManager:
    def test_creation(self, manager: Manager) -> None:
        assert isinstance(manager.id, UUID)
        assert manager.part_type == "manager"
        assert manager.state == ManagerState.IDLE
        assert manager.rigidity == 0.8
        assert "perfectionism" in manager.strategies

    def test_defaults(self) -> None:
        m = Manager(narrative="test", age=10, intent="protect")
        assert m.part_type == "manager"
        assert m.state == ManagerState.IDLE
        assert m.rigidity == 0.5
        assert m.triggers == []
        assert m.strategies == []
        assert m.trust_level == 0.5
        assert m.is_visible is True

    def test_is_ipart(self, manager: Manager) -> None:
        assert isinstance(manager, IPart)


class TestFirefighter:
    def test_creation(self, firefighter: Firefighter) -> None:
        assert firefighter.part_type == "firefighter"
        assert firefighter.state == FirefighterState.DORMANT
        assert firefighter.pain_threshold == 0.6
        assert firefighter.refractory_period == timedelta(hours=2)

    def test_default_refractory_period(self) -> None:
        f = Firefighter(narrative="test", age=10, intent="protect")
        assert f.refractory_period == timedelta(minutes=30)

    def test_is_ipart(self, firefighter: Firefighter) -> None:
        assert isinstance(firefighter, IPart)


class TestExile:
    def test_creation(self, exile: Exile) -> None:
        assert exile.part_type == "exile"
        assert exile.state == ExileState.ISOLATED
        assert exile.is_visible is False
        assert exile.burden is not None
        assert exile.burden.content == "I am not enough"
        assert exile.emotional_charge == 0.7

    def test_hidden_by_default(self) -> None:
        e = Exile(narrative="test", age=5, intent="hold pain")
        assert e.is_visible is False

    def test_no_burden_by_default(self) -> None:
        e = Exile(narrative="test", age=5, intent="hold pain")
        assert e.burden is None

    def test_is_ipart(self, exile: Exile) -> None:
        assert isinstance(exile, IPart)


class TestPartUnion:
    """Test the discriminated union for round-trip serialisation."""

    def test_manager_round_trip(self, manager: Manager) -> None:
        adapter = TypeAdapter(PartUnion)
        json_str = adapter.dump_json(manager)
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, Manager)
        assert restored.id == manager.id
        assert restored.part_type == "manager"

    def test_firefighter_round_trip(self, firefighter: Firefighter) -> None:
        adapter = TypeAdapter(PartUnion)
        json_str = adapter.dump_json(firefighter)
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, Firefighter)
        assert restored.id == firefighter.id

    def test_exile_round_trip(self, exile: Exile) -> None:
        adapter = TypeAdapter(PartUnion)
        json_str = adapter.dump_json(exile)
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, Exile)
        assert restored.id == exile.id
        assert restored.burden is not None
        assert restored.burden.content == "I am not enough"

    def test_discriminator_rejects_invalid(self) -> None:
        adapter = TypeAdapter(PartUnion)
        with pytest.raises(ValidationError):
            adapter.validate_python({
                "part_type": "invalid",
                "narrative": "test",
                "age": 10,
                "intent": "test",
            })


# ---------------------------------------------------------------------------
# V2: Legacy Burden Lineage
# ---------------------------------------------------------------------------


class TestBurdenLineage:
    def test_burden_lineage_default(self) -> None:
        """Burden() has empty lineage by default — backward compatible."""
        burden = Burden(
            burden_type=BurdenType.PERSONAL,
            origin="Age 7, school failure",
            content="I am not enough",
        )
        assert burden.lineage == []

    def test_burden_lineage_populated(self) -> None:
        """Burden with a legacy lineage chain."""
        burden = Burden(
            burden_type=BurdenType.LEGACY,
            origin="Grandmother's famine trauma",
            content="There is never enough",
            lineage=["grandmother", "mother", "self"],
        )
        assert burden.lineage == ["grandmother", "mother", "self"]

    def test_burden_generation_depth(self) -> None:
        """generation_depth returns len(lineage)."""
        burden = Burden(
            burden_type=BurdenType.LEGACY,
            origin="Grandmother's famine trauma",
            content="There is never enough",
            lineage=["grandmother", "mother", "self"],
        )
        assert burden.generation_depth == 3

    def test_burden_generation_depth_zero(self) -> None:
        """No lineage means generation_depth is 0 (personal burden)."""
        burden = Burden(
            burden_type=BurdenType.PERSONAL,
            origin="Age 7, school failure",
            content="I am not enough",
        )
        assert burden.generation_depth == 0

    def test_burden_lineage_serialization(self) -> None:
        """JSON round-trip preserves lineage."""
        burden = Burden(
            burden_type=BurdenType.LEGACY,
            origin="Grandmother's famine trauma",
            content="There is never enough",
            lineage=["grandmother", "mother", "self"],
        )
        json_str = burden.model_dump_json()
        restored = Burden.model_validate_json(json_str)
        assert restored.lineage == ["grandmother", "mother", "self"]
        assert restored.generation_depth == 3


# ---------------------------------------------------------------------------
# V2: Exile invited_qualities
# ---------------------------------------------------------------------------


class TestExileInvitedQualities:
    def test_exile_invited_qualities_default(self) -> None:
        """Exile() has empty invited_qualities by default — backward compatible."""
        exile = Exile(narrative="test", age=5, intent="hold pain")
        assert exile.invited_qualities == []

    def test_exile_invited_qualities_populated(self) -> None:
        """Exile with invited_qualities set."""
        exile = Exile(
            narrative="test",
            age=5,
            intent="hold pain",
            invited_qualities=["playfulness", "curiosity"],
        )
        assert exile.invited_qualities == ["playfulness", "curiosity"]
