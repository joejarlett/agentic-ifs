"""Tests for agentic_ifs.dialogue — LLM dialogue system for Part speech.

Uses a MockDialogueProvider to test all IFS constraints and orchestration
logic without requiring real API keys or network access.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from agentic_ifs import (
    Exile,
    Firefighter,
    Manager,
    ProtectionGraph,
    SelfSystem,
)
from agentic_ifs.dialogue import (
    DialogueContext,
    PartDialogue,
    build_part_system_prompt,
)
from agentic_ifs.parts import IPart


# ---------------------------------------------------------------------------
# Mock provider
# ---------------------------------------------------------------------------


class MockDialogueProvider:
    """Test double that returns predictable responses."""

    def __init__(self, response: str = "I hear you.") -> None:
        self.response = response
        self.last_part: IPart | None = None
        self.last_context: DialogueContext | None = None
        self.last_system_prompt: str | None = None
        self.call_count: int = 0

    def generate_part_response(
        self,
        part: IPart,
        context: DialogueContext,
        system_prompt: str,
    ) -> str:
        self.last_part = part
        self.last_context = context
        self.last_system_prompt = system_prompt
        self.call_count += 1
        return self.response


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_dialogue(
    graph: ProtectionGraph,
    self_energy: float = 0.8,
    response: str = "I hear you.",
) -> tuple[PartDialogue, MockDialogueProvider]:
    """Create a PartDialogue with a MockDialogueProvider and given self_energy."""
    provider = MockDialogueProvider(response=response)
    self_system = SelfSystem(self_energy=self_energy)
    dialogue = PartDialogue(
        provider=provider,
        graph=graph,
        self_system=self_system,
    )
    return dialogue, provider


# ---------------------------------------------------------------------------
# Tests: speak_as
# ---------------------------------------------------------------------------


class TestSpeakAs:
    def test_speak_as_happy_path(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """High self_energy, valid Part, mock provider returns response."""
        dialogue, provider = _make_dialogue(populated_graph, self_energy=0.8)

        result = dialogue.speak_as(manager.id, "How are you feeling?")

        assert result == "I hear you."
        assert provider.call_count == 1

    def test_speak_as_requires_self_energy(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Low self_energy raises ValueError — unblend first."""
        dialogue, _ = _make_dialogue(populated_graph, self_energy=0.3)

        with pytest.raises(ValueError, match="Self-energy too low"):
            dialogue.speak_as(manager.id, "How are you feeling?")

    def test_speak_as_invalid_part(
        self, populated_graph: ProtectionGraph,
    ) -> None:
        """Nonexistent Part raises ValueError."""
        dialogue, _ = _make_dialogue(populated_graph, self_energy=0.8)
        fake_id = uuid4()

        with pytest.raises(ValueError, match="not found in graph"):
            dialogue.speak_as(fake_id, "Hello?")

    def test_speak_as_tracks_history(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """After speaking, history has facilitator + part messages."""
        dialogue, _ = _make_dialogue(populated_graph, self_energy=0.8)

        dialogue.speak_as(manager.id, "How are you feeling?")

        history = dialogue.get_history(manager.id)
        assert len(history) == 2
        assert history[0].role == "facilitator"
        assert history[0].content == "How are you feeling?"
        assert history[1].role == "part"
        assert history[1].content == "I hear you."

    def test_speak_as_passes_context(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Verify mock received correct DialogueContext."""
        dialogue, provider = _make_dialogue(populated_graph, self_energy=0.8)

        dialogue.speak_as(
            manager.id,
            "What do you need?",
            current_step="befriend",
        )

        ctx = provider.last_context
        assert ctx is not None
        assert ctx.self_energy == 0.8
        assert ctx.current_step == "befriend"
        assert ctx.facilitator_message == "What do you need?"
        assert ctx.is_direct_access is False

    def test_speak_as_logs_event(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Session log has 'dialogue' event."""
        dialogue, _ = _make_dialogue(populated_graph, self_energy=0.8)

        dialogue.speak_as(manager.id, "Tell me about yourself.")

        log = dialogue.self_system.session_log
        dialogue_events = [e for e in log if e.event_type == "dialogue"]
        assert len(dialogue_events) == 1
        assert dialogue_events[0].part_id == manager.id
        assert "Tell me about yourself." in dialogue_events[0].description


# ---------------------------------------------------------------------------
# Tests: direct_access
# ---------------------------------------------------------------------------


class TestDirectAccess:
    def test_direct_access_bypasses_self_energy(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Direct Access works even with low self_energy."""
        dialogue, provider = _make_dialogue(populated_graph, self_energy=0.2)

        result = dialogue.direct_access(manager.id, "I need to talk to you.")

        assert result == "I hear you."
        assert provider.call_count == 1

    def test_direct_access_logs_event(
        self, populated_graph: ProtectionGraph, firefighter: Firefighter,
    ) -> None:
        """Session log has 'direct_access' event."""
        dialogue, _ = _make_dialogue(populated_graph, self_energy=0.2)

        dialogue.direct_access(firefighter.id, "Can you tell me what happened?")

        log = dialogue.self_system.session_log
        da_events = [e for e in log if e.event_type == "direct_access"]
        assert len(da_events) == 1
        assert da_events[0].part_id == firefighter.id

    def test_direct_access_context_flag(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Mock received is_direct_access=True in the context."""
        dialogue, provider = _make_dialogue(populated_graph, self_energy=0.2)

        dialogue.direct_access(manager.id, "Hello, Part.")

        ctx = provider.last_context
        assert ctx is not None
        assert ctx.is_direct_access is True


# ---------------------------------------------------------------------------
# Tests: build_part_system_prompt
# ---------------------------------------------------------------------------


class TestBuildSystemPrompt:
    def test_build_system_prompt_manager(self, manager: Manager) -> None:
        """System prompt includes narrative, age, intent, strategies."""
        prompt = build_part_system_prompt(manager)

        assert manager.narrative in prompt
        assert f"age {manager.age}" in prompt
        assert manager.intent in prompt
        assert "perfectionism" in prompt
        assert "rigidity" in prompt.lower()

    def test_build_system_prompt_exile_with_burden(self, exile: Exile) -> None:
        """Includes burden content for an Exile with a burden."""
        prompt = build_part_system_prompt(exile)

        assert exile.narrative in prompt
        assert "I am not enough" in prompt
        assert "emotional charge" in prompt.lower()

    def test_build_system_prompt_exile_no_burden(self) -> None:
        """No burden text when Exile has no burden."""
        exile_no_burden = Exile(
            narrative="The Lost Child — withdrawn and invisible",
            age=5,
            intent="Stay invisible to avoid conflict",
            emotional_charge=0.3,
        )
        prompt = build_part_system_prompt(exile_no_burden)

        assert exile_no_burden.narrative in prompt
        assert "burden" not in prompt.lower()
        assert "emotional charge" in prompt.lower()

    def test_build_system_prompt_firefighter(
        self, firefighter: Firefighter,
    ) -> None:
        """System prompt includes emergency behaviors for Firefighters."""
        prompt = build_part_system_prompt(firefighter)

        assert firefighter.narrative in prompt
        assert "avoidance" in prompt
        assert "emergency behaviors" in prompt.lower()

    def test_build_system_prompt_direct_access(self, manager: Manager) -> None:
        """Direct Access flag adds therapist instruction."""
        prompt = build_part_system_prompt(manager, is_direct_access=True)

        assert "therapist is speaking directly to you" in prompt.lower()


# ---------------------------------------------------------------------------
# Tests: history management
# ---------------------------------------------------------------------------


class TestHistoryManagement:
    def test_get_history(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Returns a copy of conversation — modifying it does not affect internal state."""
        dialogue, _ = _make_dialogue(populated_graph, self_energy=0.8)

        dialogue.speak_as(manager.id, "Hello.")
        history = dialogue.get_history(manager.id)
        history.clear()  # modify the returned copy

        # Internal history should be unaffected
        assert len(dialogue.get_history(manager.id)) == 2

    def test_clear_history(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Clears conversation history for a Part."""
        dialogue, _ = _make_dialogue(populated_graph, self_energy=0.8)

        dialogue.speak_as(manager.id, "Hello.")
        assert len(dialogue.get_history(manager.id)) == 2

        dialogue.clear_history(manager.id)
        assert len(dialogue.get_history(manager.id)) == 0

    def test_multiple_turns(
        self, populated_graph: ProtectionGraph, manager: Manager,
    ) -> None:
        """Multi-turn conversation builds history correctly."""
        dialogue, provider = _make_dialogue(
            populated_graph, self_energy=0.8, response="Response",
        )

        dialogue.speak_as(manager.id, "Turn 1")
        dialogue.speak_as(manager.id, "Turn 2")
        dialogue.speak_as(manager.id, "Turn 3")

        history = dialogue.get_history(manager.id)
        assert len(history) == 6  # 3 facilitator + 3 part messages

        # Verify alternating pattern
        for i, msg in enumerate(history):
            expected_role = "facilitator" if i % 2 == 0 else "part"
            assert msg.role == expected_role

        # Verify the provider received history on later calls
        # The last call should have had 4 messages in history (2 turns)
        assert provider.last_context is not None
        assert len(provider.last_context.conversation_history) == 4

        assert provider.call_count == 3
