"""Tests for agentic_ifs.unburdening — the Exile unburdening pipeline."""

from __future__ import annotations

from uuid import uuid4

import pytest

from agentic_ifs import (
    BlendState,
    Burden,
    BurdenType,
    Exile,
    ExileState,
    Manager,
    ProtectionGraph,
    SelfSystem,
    UnburdeningElement,
    UnburdeningStateMachine,
    UnburdeningStep,
)


class TestUnburdeningStateMachine:
    """Test the unburdening pipeline — the core healing process for Exiles."""

    @pytest.fixture
    def high_energy_system(self) -> SelfSystem:
        """A SelfSystem with energy above COMPASSION_THRESHOLD."""
        return SelfSystem(self_energy=0.8)

    @pytest.fixture
    def low_energy_system(self, manager: Manager) -> SelfSystem:
        """A SelfSystem with energy below COMPASSION_THRESHOLD due to blending."""
        ss = SelfSystem(self_energy=0.8)
        ss.blend(BlendState(part_id=manager.id, blending_percentage=0.8))
        return ss

    @pytest.fixture
    def machine(
        self,
        populated_graph: ProtectionGraph,
        high_energy_system: SelfSystem,
    ) -> UnburdeningStateMachine:
        return UnburdeningStateMachine(
            graph=populated_graph,
            self_system=high_energy_system,
        )

    @pytest.fixture
    def blended_machine(
        self,
        populated_graph: ProtectionGraph,
        low_energy_system: SelfSystem,
    ) -> UnburdeningStateMachine:
        return UnburdeningStateMachine(
            graph=populated_graph,
            self_system=low_energy_system,
        )

    # -------------------------------------------------------------------
    # 1. witness — happy path
    # -------------------------------------------------------------------

    def test_witness_happy_path(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """High self_energy, Exile with burden — witness succeeds."""
        result = machine.witness(exile.id)

        assert result.step == UnburdeningStep.WITNESSING
        assert result.exile_id == exile.id
        assert result.next_step == UnburdeningStep.RETRIEVAL
        assert result.unblend_required is None
        assert "I am not enough" in result.notes
        assert machine.current_step == UnburdeningStep.WITNESSING
        assert machine.target_exile_id == exile.id

    # -------------------------------------------------------------------
    # 2. witness — requires self-energy
    # -------------------------------------------------------------------

    def test_witness_requires_self_energy(
        self,
        blended_machine: UnburdeningStateMachine,
        exile: Exile,
        manager: Manager,
    ) -> None:
        """Low self_energy returns unblend_required."""
        result = blended_machine.witness(exile.id)

        assert result.step == UnburdeningStep.WITNESSING
        assert result.next_step is None
        assert result.unblend_required == manager.id
        assert blended_machine.current_step is None  # Not advanced

    # -------------------------------------------------------------------
    # 3. witness — exile must exist
    # -------------------------------------------------------------------

    def test_witness_exile_must_exist(
        self,
        machine: UnburdeningStateMachine,
    ) -> None:
        """ValueError for nonexistent exile."""
        with pytest.raises(ValueError, match="not in graph"):
            machine.witness(uuid4())

    # -------------------------------------------------------------------
    # 4. witness — exile must have burden
    # -------------------------------------------------------------------

    def test_witness_exile_must_have_burden(
        self,
        machine: UnburdeningStateMachine,
    ) -> None:
        """ValueError for Exile with no burden."""
        unburdened_exile = Exile(
            narrative="Already healed",
            age=5,
            intent="Hold joy",
            burden=None,
        )
        machine.graph.add_part(unburdened_exile)

        with pytest.raises(ValueError, match="no burden"):
            machine.witness(unburdened_exile.id)

    # -------------------------------------------------------------------
    # 5. retrieve — after witness
    # -------------------------------------------------------------------

    def test_retrieve_after_witness(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """Normal flow: retrieve after witness succeeds."""
        machine.witness(exile.id)
        result = machine.retrieve(exile.id)

        assert result.step == UnburdeningStep.RETRIEVAL
        assert result.exile_id == exile.id
        assert result.next_step == UnburdeningStep.PURGING
        assert result.unblend_required is None
        assert exile.state == ExileState.LEAKING
        assert machine.current_step == UnburdeningStep.RETRIEVAL

    # -------------------------------------------------------------------
    # 6. retrieve — requires witness first
    # -------------------------------------------------------------------

    def test_retrieve_requires_witness_first(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """ValueError if called before witness."""
        with pytest.raises(ValueError, match="Cannot retrieve before witnessing"):
            machine.retrieve(exile.id)

    # -------------------------------------------------------------------
    # 7. retrieve — requires self-energy
    # -------------------------------------------------------------------

    def test_retrieve_requires_self_energy(
        self,
        populated_graph: ProtectionGraph,
        exile: Exile,
        manager: Manager,
    ) -> None:
        """Low self_energy during retrieve returns unblend_required."""
        # Start with high energy for witness, then blend for retrieve
        ss = SelfSystem(self_energy=0.8)
        machine = UnburdeningStateMachine(graph=populated_graph, self_system=ss)
        machine.witness(exile.id)

        # Now blend a Part to drop self_energy
        ss.blend(BlendState(part_id=manager.id, blending_percentage=0.8))

        result = machine.retrieve(exile.id)

        assert result.step == UnburdeningStep.RETRIEVAL
        assert result.next_step is None
        assert result.unblend_required == manager.id

    # -------------------------------------------------------------------
    # 8. purge — after retrieve
    # -------------------------------------------------------------------

    def test_purge_after_retrieve(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """Purge sets burden to None and emotional_charge to 0.1."""
        machine.witness(exile.id)
        machine.retrieve(exile.id)
        result = machine.purge(exile.id, UnburdeningElement.WATER)

        assert result.step == UnburdeningStep.PURGING
        assert result.next_step == UnburdeningStep.INVITATION
        assert result.unblend_required is None
        assert exile.burden is None
        assert exile.emotional_charge == pytest.approx(0.1)
        assert "water" in result.notes

    # -------------------------------------------------------------------
    # 9. purge — requires retrieve first
    # -------------------------------------------------------------------

    def test_purge_requires_retrieve_first(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """ValueError if called before retrieve."""
        machine.witness(exile.id)
        # Skip retrieve
        with pytest.raises(ValueError, match="Cannot purge before retrieval"):
            machine.purge(exile.id, UnburdeningElement.FIRE)

    # -------------------------------------------------------------------
    # 10. purge — different elements work
    # -------------------------------------------------------------------

    def test_purge_element_choice(
        self,
        populated_graph: ProtectionGraph,
        exile: Exile,
    ) -> None:
        """All five elements work for purging."""
        for element in UnburdeningElement:
            # Reset exile for each iteration
            exile.burden = Burden(
                burden_type=BurdenType.PERSONAL,
                origin="Age 7, school failure",
                content="I am not enough",
                emotional_charge=0.9,
            )
            exile.emotional_charge = 0.7

            ss = SelfSystem(self_energy=0.8)
            machine = UnburdeningStateMachine(graph=populated_graph, self_system=ss)

            machine.witness(exile.id)
            machine.retrieve(exile.id)
            result = machine.purge(exile.id, element)

            assert result.step == UnburdeningStep.PURGING
            assert element.value in result.notes
            assert exile.burden is None

    # -------------------------------------------------------------------
    # 11. invite — after purge
    # -------------------------------------------------------------------

    def test_invite_after_purge(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """Invite sets invited_qualities and ExileState.UNBURDENED."""
        machine.witness(exile.id)
        machine.retrieve(exile.id)
        machine.purge(exile.id, UnburdeningElement.LIGHT)

        qualities = ["playfulness", "curiosity", "lightness"]
        result = machine.invite(exile.id, qualities)

        assert result.step == UnburdeningStep.INVITATION
        assert result.next_step is None  # Pipeline complete
        assert result.unblend_required is None
        assert exile.invited_qualities == qualities
        assert exile.state == ExileState.UNBURDENED
        assert machine.current_step == UnburdeningStep.COMPLETE

    # -------------------------------------------------------------------
    # 12. invite — requires purge first
    # -------------------------------------------------------------------

    def test_invite_requires_purge_first(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """ValueError if called before purge."""
        machine.witness(exile.id)
        machine.retrieve(exile.id)
        # Skip purge
        with pytest.raises(ValueError, match="Cannot invite before purging"):
            machine.invite(exile.id, ["playfulness"])

    # -------------------------------------------------------------------
    # 13. full pipeline
    # -------------------------------------------------------------------

    def test_full_pipeline(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """All 4 steps in sequence — verify final state."""
        # Verify initial state
        assert exile.burden is not None
        assert exile.state == ExileState.ISOLATED
        assert exile.invited_qualities == []

        # Step 1: Witness
        r1 = machine.witness(exile.id)
        assert r1.next_step == UnburdeningStep.RETRIEVAL

        # Step 2: Retrieve
        r2 = machine.retrieve(exile.id)
        assert r2.next_step == UnburdeningStep.PURGING
        assert exile.state == ExileState.LEAKING

        # Step 3: Purge
        r3 = machine.purge(exile.id, UnburdeningElement.EARTH)
        assert r3.next_step == UnburdeningStep.INVITATION
        assert exile.burden is None
        assert exile.emotional_charge == pytest.approx(0.1)

        # Step 4: Invite
        qualities = ["safety", "joy", "playfulness"]
        r4 = machine.invite(exile.id, qualities)
        assert r4.next_step is None

        # Final state verification
        assert exile.state == ExileState.UNBURDENED
        assert exile.invited_qualities == qualities
        assert exile.burden is None
        assert exile.emotional_charge == pytest.approx(0.1)
        assert machine.current_step == UnburdeningStep.COMPLETE

    # -------------------------------------------------------------------
    # 14. session log populated
    # -------------------------------------------------------------------

    def test_session_log_populated(
        self,
        machine: UnburdeningStateMachine,
        exile: Exile,
    ) -> None:
        """All steps log events to the session log."""
        machine.witness(exile.id)
        machine.retrieve(exile.id)
        machine.purge(exile.id, UnburdeningElement.FIRE)
        machine.invite(exile.id, ["curiosity"])

        unburdening_entries = [
            entry for entry in machine.self_system.session_log
            if entry.event_type == "unburdening"
        ]
        assert len(unburdening_entries) == 4
        assert all(
            entry.part_id == exile.id
            for entry in unburdening_entries
        )

        # Verify each stage is logged in order
        descriptions = [e.description for e in unburdening_entries]
        assert "WITNESSING" in descriptions[0]
        assert "RETRIEVAL" in descriptions[1]
        assert "PURGING" in descriptions[2]
        assert "INVITATION" in descriptions[3]
