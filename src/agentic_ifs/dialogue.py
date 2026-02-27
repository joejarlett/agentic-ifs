"""LLM Dialogue System — bringing Parts to life through generated responses.

This module provides a framework-agnostic dialogue system that enables
IFS Parts to "speak" through LLM-generated responses. Each Part responds
in character — maintaining its developmental age, narrative, protective
intent, and emotional state.

IFS theory: In therapy, a key technique is to have the client speak *as*
a Part (not *about* it). The facilitator (Self or therapist) addresses
the Part directly, and the Part responds from its own perspective. This
module replicates that process computationally.

Key components:
    - ``DialogueMessage`` / ``DialogueContext``: data structures for
      conversation state
    - ``DialogueProvider``: protocol for any LLM backend (Gemini, Claude,
      local models, rule-based systems)
    - ``build_part_system_prompt()``: constructs IFS-grounded system prompts
      from Part data
    - ``PartDialogue``: orchestrator that enforces IFS constraints
      (Self-energy checks, Direct Access mode) and bridges the simulation
      engine with any LLM backend

Design decisions:
    - ``DialogueProvider`` is a ``typing.Protocol``, not an ABC. Any object
      with a matching ``generate_part_response`` method is valid — no
      inheritance required.
    - System prompts are built from Part data at call time, so they always
      reflect the Part's current state (trust level, emotional charge, etc.).
    - Direct Access mode bypasses the Self-energy check — in IFS, a skilled
      therapist can speak directly to a Part without going through Self.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal, Protocol
from uuid import UUID

from pydantic import BaseModel, Field

from .dynamics import COMPASSION_THRESHOLD
from .graph import ProtectionGraph
from .parts import Exile, Firefighter, IPart, Manager
from .self_system import LogEntry, SelfSystem


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class DialogueMessage(BaseModel):
    """A single message in a Part dialogue conversation.

    IFS: Each exchange between the facilitator (Self/therapist) and a Part
    is a step in the therapeutic process. The facilitator speaks *to* the
    Part, and the Part responds from its own perspective.

    ``role`` is either "facilitator" (Self/therapist speaking to the Part)
    or "part" (the Part responding).
    """

    role: Literal["facilitator", "part"]
    content: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class DialogueContext(BaseModel):
    """Context passed to a DialogueProvider for response generation.

    Bundles the current system state, conversation history, and
    facilitator message into a single object for the provider.

    IFS: Context matters — a Part's response depends on how much
    Self-energy is present, what step of the 6 Fs the system is in,
    and whether a therapist is using Direct Access.
    """

    self_energy: float = Field(
        description="Current Self-energy level (0.0-1.0)",
    )
    current_step: str | None = Field(
        default=None,
        description="Which 6F step is active, if in a workflow",
    )
    facilitator_message: str = Field(
        description="What the facilitator/Self says to the Part",
    )
    conversation_history: list[DialogueMessage] = Field(
        default_factory=list,
        description="Prior messages in this Part's dialogue",
    )
    is_direct_access: bool = Field(
        default=False,
        description="Whether a therapist is speaking directly to the Part",
    )
    system_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Extra context for the provider (model params, etc.)",
    )


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


class DialogueProvider(Protocol):
    """Framework-agnostic interface for generating Part responses.

    Implement this protocol with any LLM backend (Google Gemini,
    Anthropic Claude, OpenAI, local models, or even rule-based systems).

    IFS: The provider is the "voice" mechanism — it generates speech
    that is consistent with the Part's character, age, and protective
    intent. The provider does not interpret or modify IFS semantics;
    it renders them into natural language.
    """

    def generate_part_response(
        self, part: IPart, context: DialogueContext, system_prompt: str,
    ) -> str: ...


# ---------------------------------------------------------------------------
# System prompt builder
# ---------------------------------------------------------------------------


def build_part_system_prompt(
    part: IPart,
    *,
    is_direct_access: bool = False,
) -> str:
    """Build an IFS-grounded system prompt for LLM Part dialogue.

    Constructs a system prompt from a Part's data that instructs the LLM
    to speak *as* the Part — maintaining its developmental age, narrative,
    protective intent, and emotional state.

    IFS principles encoded in the prompt:
        - Part speaks in first person
        - Part maintains its developmental age and perspective
        - Part expresses its protective intent
        - Part's strategies/behaviors shape its voice
        - All Parts have positive intent, even when behaviors seem harmful

    Parameters
    ----------
    part:
        The Part whose voice the LLM will assume.
    is_direct_access:
        If ``True``, adds instructions indicating a therapist is
        speaking directly to the Part (bypassing Self).

    Returns
    -------
    str
        The complete system prompt for the LLM.
    """
    lines: list[str] = []

    # Core identity
    lines.append(
        f"You are a Part in an Internal Family Systems. "
        f"You are {part.narrative}."
    )
    lines.append(
        f"You were formed at age {part.age}. "
        f"You still see the world from that age."
    )
    lines.append(f"Your protective intent: {part.intent}")
    lines.append(f"Your trust in Self is currently {part.trust_level:.0%}.")

    # Type-specific details
    if isinstance(part, Manager):
        if part.strategies:
            lines.append(f"Your strategies: {', '.join(part.strategies)}")
        lines.append(f"Your rigidity: {part.rigidity:.0%}")

    elif isinstance(part, Firefighter):
        if part.extinguishing_behaviors:
            lines.append(
                f"Your emergency behaviors: "
                f"{', '.join(part.extinguishing_behaviors)}"
            )

    elif isinstance(part, Exile):
        if part.burden is not None:
            lines.append(f"You carry this burden: {part.burden.content}")
        lines.append(f"Your emotional charge: {part.emotional_charge:.0%}")

    # IFS behavioral instructions
    lines.append(
        "Speak in first person. Express your feelings and needs "
        "authentically. You have positive intent even if your behavior "
        "seems harmful."
    )

    # Direct Access mode
    if is_direct_access:
        lines.append(
            "A therapist is speaking directly to you. You may respond "
            "more openly than you would through Self."
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


class PartDialogue:
    """Orchestrator for LLM-powered Part dialogue.

    Bridges the IFS simulation engine with any LLM backend via the
    ``DialogueProvider`` protocol. Enforces IFS constraints:

    - **Self-energy check** before dialogue (unless Direct Access) — if
      Self-energy is below ``COMPASSION_THRESHOLD``, another Part has
      blended and must be unblended first.
    - **Conversation history** tracking per Part, so multi-turn dialogue
      builds context.
    - **System prompt** reflects the Part's current state at each call.
    - **Session logging** — every dialogue exchange is recorded as a
      ``LogEntry`` in the ``SelfSystem`` session log.

    IFS: This class models the facilitator's (Self's) act of speaking
    to a Part and receiving its response. The facilitator must have
    sufficient Self-energy to engage compassionately — otherwise, another
    Part is running the show.

    Parameters
    ----------
    provider:
        Any object satisfying the ``DialogueProvider`` protocol.
    graph:
        The ``ProtectionGraph`` containing the system's Parts.
    self_system:
        The ``SelfSystem`` providing Self-energy state and session log.
    """

    def __init__(
        self,
        provider: DialogueProvider,
        graph: ProtectionGraph,
        self_system: SelfSystem,
    ) -> None:
        self.provider = provider
        self.graph = graph
        self.self_system = self_system
        self._histories: dict[UUID, list[DialogueMessage]] = {}

    def _get_part(self, part_id: UUID) -> IPart:
        """Look up a Part by ID, raising ValueError if not found."""
        part = self.graph.nodes.get(part_id)
        if part is None:
            raise ValueError(f"Part {part_id} not found in graph")
        return part

    def speak_as(
        self,
        part_id: UUID,
        facilitator_message: str,
        current_step: str | None = None,
    ) -> str:
        """Generate a Part's response to a facilitator message.

        IFS: Self (the facilitator) speaks to a Part and the Part responds.
        This requires sufficient Self-energy — if another Part has blended,
        the facilitator cannot engage with compassion and curiosity.

        Parameters
        ----------
        part_id:
            UUID of the Part to speak as.
        facilitator_message:
            What Self/facilitator says to the Part.
        current_step:
            Which 6F step is active, if the dialogue occurs within
            a structured workflow.

        Returns
        -------
        str
            The Part's generated response.

        Raises
        ------
        ValueError
            If the Part is not in the graph, or if Self-energy is
            below ``COMPASSION_THRESHOLD``.
        """
        part = self._get_part(part_id)

        # Self-energy gate
        if self.self_system.self_energy <= COMPASSION_THRESHOLD:
            raise ValueError(
                "Self-energy too low for dialogue \u2014 unblend first"
            )

        # Build system prompt from Part's current state
        system_prompt = build_part_system_prompt(part)

        # Assemble context
        history = self._histories.get(part_id, [])
        context = DialogueContext(
            self_energy=self.self_system.self_energy,
            current_step=current_step,
            facilitator_message=facilitator_message,
            conversation_history=list(history),
        )

        # Generate response
        response = self.provider.generate_part_response(
            part, context, system_prompt,
        )

        # Track conversation history
        facilitator_msg = DialogueMessage(
            role="facilitator", content=facilitator_message,
        )
        part_msg = DialogueMessage(role="part", content=response)

        if part_id not in self._histories:
            self._histories[part_id] = []
        self._histories[part_id].append(facilitator_msg)
        self._histories[part_id].append(part_msg)

        # Log session event
        self.self_system.session_log.append(
            LogEntry(
                event_type="dialogue",
                description=(
                    f"Facilitator: {facilitator_message!r} | "
                    f"Part response: {response!r}"
                ),
                part_id=part_id,
            )
        )

        return response

    def direct_access(
        self,
        part_id: UUID,
        therapist_message: str,
    ) -> str:
        """Generate a Part's response in Direct Access mode.

        IFS: Direct Access is a technique where a skilled therapist
        speaks directly to a Part, bypassing the client's Self. This
        is used when Self-energy is too low for normal dialogue, or
        when the therapist needs to negotiate with a protective Part.

        No Self-energy check is performed — Direct Access bypasses Self.

        Parameters
        ----------
        part_id:
            UUID of the Part to speak to directly.
        therapist_message:
            What the therapist says directly to the Part.

        Returns
        -------
        str
            The Part's generated response.

        Raises
        ------
        ValueError
            If the Part is not in the graph.
        """
        part = self._get_part(part_id)

        # Build system prompt with Direct Access flag
        system_prompt = build_part_system_prompt(
            part, is_direct_access=True,
        )

        # Assemble context
        history = self._histories.get(part_id, [])
        context = DialogueContext(
            self_energy=self.self_system.self_energy,
            facilitator_message=therapist_message,
            conversation_history=list(history),
            is_direct_access=True,
        )

        # Generate response
        response = self.provider.generate_part_response(
            part, context, system_prompt,
        )

        # Track conversation history
        facilitator_msg = DialogueMessage(
            role="facilitator", content=therapist_message,
        )
        part_msg = DialogueMessage(role="part", content=response)

        if part_id not in self._histories:
            self._histories[part_id] = []
        self._histories[part_id].append(facilitator_msg)
        self._histories[part_id].append(part_msg)

        # Log session event
        self.self_system.session_log.append(
            LogEntry(
                event_type="direct_access",
                description=(
                    f"Therapist (Direct Access): {therapist_message!r} | "
                    f"Part response: {response!r}"
                ),
                part_id=part_id,
            )
        )

        return response

    def get_history(self, part_id: UUID) -> list[DialogueMessage]:
        """Return a copy of the conversation history for a Part.

        IFS: The conversation record shows the arc of the relationship
        between Self/therapist and the Part over the course of a session.

        Parameters
        ----------
        part_id:
            UUID of the Part whose history to retrieve.

        Returns
        -------
        list[DialogueMessage]
            A copy of the conversation history (empty list if no history).
        """
        return list(self._histories.get(part_id, []))

    def clear_history(self, part_id: UUID) -> None:
        """Clear conversation history for a Part.

        IFS: Starting a fresh conversation — previous exchanges are
        no longer carried as context for the LLM.

        Parameters
        ----------
        part_id:
            UUID of the Part whose history to clear.
        """
        self._histories.pop(part_id, None)
