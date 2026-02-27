"""Session — thin convenience facade over the composable core.

A Session bundles ``ProtectionGraph``, ``SelfSystem``, ``TrailheadLog``,
``SixFsStateMachine``, and (V2) ``UnburdeningStateMachine``, ``BodyMap``,
and ``PartDialogue`` into a single coordinated unit. It delegates all
operations to the underlying components — it is not a different
implementation, just an ergonomic surface.

Usage::

    # Composable (full control)
    graph = ProtectionGraph()
    self_system = SelfSystem()
    log = TrailheadLog()

    # Session (convenience wrapper — same objects underneath)
    session = Session()
    session.add_part(manager)
    result = session.find(trailhead)
    parts_map = session.export_parts_map()

    # V2: unburdening
    session.witness(exile.id)
    session.retrieve(exile.id)
    session.reparent(exile.id, "I needed someone to say I was safe")
    session.purge(exile.id, UnburdeningElement.WATER)
    session.invite(exile.id, ["playfulness", "lightness"])

IFS meaning: a Session represents a single therapeutic encounter — a
bounded context in which Parts are engaged and the system moves toward
greater Self-energy.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from .dialogue import DialogueProvider, PartDialogue
from .dynamics import detect_polarization, is_self_led, self_preservation_ratio
from .graph import Edge, PolarizationEdge, ProtectionGraph
from .modifiers import FivePs
from .parts import IPart
from .self_system import BlendState, SelfSystem
from .somatic import BodyMap
from .unburdening import (
    UnburdeningElement,
    UnburdeningResult,
    UnburdeningStateMachine,
)
from .workflow import (
    FocusShift,
    SixFsResult,
    SixFsStateMachine,
    Trailhead,
    TrailheadLog,
)


class Session:
    """Convenience wrapper for the composable core.

    Creates and wires ``ProtectionGraph``, ``SelfSystem``, ``TrailheadLog``,
    ``SixFsStateMachine``, and optionally ``UnburdeningStateMachine``,
    ``BodyMap``, and ``PartDialogue`` as a coordinated unit.

    IFS: A Session represents a single therapeutic encounter — a bounded
    context in which Parts are engaged and the system moves toward greater
    Self-energy.

    Parameters
    ----------
    initial_self_energy:
        Starting ``self_energy`` value. Default 0.3 reflects a typical
        person arriving at a session with Managers already running.
    modifiers:
        Optional ``FivePs`` interaction modifiers for the facilitator.
        Affects compassion threshold, trust increments, and Self-energy
        checks in the 6 Fs workflow.
    body_map:
        Optional ``BodyMap`` for tracking somatic markers. If not
        provided, a new empty BodyMap is created.
    dialogue_provider:
        Optional ``DialogueProvider`` for LLM-powered Part dialogue.
        If provided, enables ``speak_as()`` and ``direct_access()``
        methods.
    """

    def __init__(
        self,
        initial_self_energy: float = 0.3,
        *,
        modifiers: FivePs | None = None,
        body_map: BodyMap | None = None,
        dialogue_provider: DialogueProvider | None = None,
    ) -> None:
        self._graph = ProtectionGraph()
        self._self_system = SelfSystem(self_energy=initial_self_energy)
        self._trailhead_log = TrailheadLog()
        self._modifiers = modifiers
        self._workflow = SixFsStateMachine(
            graph=self._graph,
            self_system=self._self_system,
            log=self._trailhead_log,
            modifiers=modifiers,
        )
        self._unburdening = UnburdeningStateMachine(
            graph=self._graph,
            self_system=self._self_system,
        )
        self._body_map = body_map or BodyMap()
        self._dialogue: PartDialogue | None = None
        if dialogue_provider is not None:
            self._dialogue = PartDialogue(
                provider=dialogue_provider,
                graph=self._graph,
                self_system=self._self_system,
            )
        self._focus_shifts: list[FocusShift] = []

    # --- Property accessors for underlying components ---

    @property
    def graph(self) -> ProtectionGraph:
        """The internal system's relationship graph."""
        return self._graph

    @property
    def self_system(self) -> SelfSystem:
        """The Self operating environment."""
        return self._self_system

    @property
    def trailhead_log(self) -> TrailheadLog:
        """The session's trailhead log."""
        return self._trailhead_log

    @property
    def workflow(self) -> SixFsStateMachine:
        """The 6 Fs state machine."""
        return self._workflow

    @property
    def modifiers(self) -> FivePs | None:
        """The 5 Ps interaction modifiers, if configured."""
        return self._modifiers

    @property
    def unburdening(self) -> UnburdeningStateMachine:
        """The unburdening pipeline state machine."""
        return self._unburdening

    @property
    def body_map(self) -> BodyMap:
        """The session's somatic body map."""
        return self._body_map

    @property
    def dialogue(self) -> PartDialogue | None:
        """The Part dialogue orchestrator, if a provider was given."""
        return self._dialogue

    @property
    def focus_shifts(self) -> list[FocusShift]:
        """All U-Turn markers recorded in this session."""
        return list(self._focus_shifts)

    # --- Graph delegates ---

    def add_part(self, part: IPart) -> None:
        """Add a Part to the internal system."""
        self._graph.add_part(part)

    def add_edge(self, edge: Edge) -> None:
        """Add a relationship edge between two Parts."""
        self._graph.add_edge(edge)

    def add_polarization(self, edge: PolarizationEdge) -> None:
        """Declare a polarization between two Parts."""
        self._graph.add_polarization(edge)

    # --- SelfSystem delegates ---

    def blend(self, blend_state: BlendState) -> None:
        """Blend a Part with the system."""
        self._self_system.blend(blend_state)

    def unblend(self, part_id: UUID) -> None:
        """Unblend a Part from the system."""
        self._self_system.unblend(part_id)

    # --- Workflow delegates (6 Fs) ---

    def find(self, trailhead: Trailhead) -> SixFsResult:
        """6 Fs Step 1: Locate the Part signalled by the trailhead."""
        return self._workflow.find(trailhead)

    def focus(self, part_id: UUID) -> SixFsResult:
        """6 Fs Step 2: Direct attention to the Part."""
        return self._workflow.focus(part_id)

    def flesh_out(self, part_id: UUID) -> SixFsResult:
        """6 Fs Step 3: Gather metadata about the Part."""
        return self._workflow.flesh_out(part_id)

    def feel_toward(self, part_id: UUID) -> SixFsResult:
        """6 Fs Step 4: Check Self-energy presence (critical gate)."""
        return self._workflow.feel_toward(part_id)

    def befriend(self, part_id: UUID) -> SixFsResult:
        """6 Fs Step 5: Build relationship with the Part."""
        return self._workflow.befriend(part_id)

    def fear(self, part_id: UUID) -> SixFsResult:
        """6 Fs Step 6: Identify the Part's worst-case scenarios."""
        return self._workflow.fear(part_id)

    # --- Unburdening delegates (V2) ---

    def witness(self, exile_id: UUID) -> UnburdeningResult:
        """Unburdening Stage 1: Self witnesses the Exile's burden."""
        return self._unburdening.witness(exile_id)

    def retrieve(self, exile_id: UUID) -> UnburdeningResult:
        """Unburdening Stage 2: Retrieve the Exile from the trauma scene."""
        return self._unburdening.retrieve(exile_id)

    def reparent(
        self, exile_id: UUID, what_was_needed: str,
    ) -> UnburdeningResult:
        """Unburdening Stage 3: Self gives the Exile what it needed."""
        return self._unburdening.reparent(exile_id, what_was_needed)

    def purge(
        self, exile_id: UUID, element: UnburdeningElement,
    ) -> UnburdeningResult:
        """Unburdening Stage 4: Release the burden via an element."""
        return self._unburdening.purge(exile_id, element)

    def invite(
        self, exile_id: UUID, new_qualities: list[str],
    ) -> UnburdeningResult:
        """Unburdening Stage 5: Exile takes on new qualities."""
        return self._unburdening.invite(exile_id, new_qualities)

    # --- Dialogue delegates (V2) ---

    def speak_as(
        self,
        part_id: UUID,
        facilitator_message: str,
        current_step: str | None = None,
    ) -> str:
        """Generate a Part's response to a facilitator message.

        Requires a ``dialogue_provider`` to have been passed at construction.
        """
        if self._dialogue is None:
            raise RuntimeError(
                "No dialogue provider configured — pass dialogue_provider "
                "to Session() to enable Part dialogue"
            )
        return self._dialogue.speak_as(part_id, facilitator_message, current_step)

    def direct_access(self, part_id: UUID, therapist_message: str) -> str:
        """Generate a Part's response in Direct Access mode (bypasses Self).

        Requires a ``dialogue_provider`` to have been passed at construction.
        """
        if self._dialogue is None:
            raise RuntimeError(
                "No dialogue provider configured — pass dialogue_provider "
                "to Session() to enable Part dialogue"
            )
        return self._dialogue.direct_access(part_id, therapist_message)

    # --- U-Turn ---

    def record_focus_shift(self, focus_shift: FocusShift) -> None:
        """Record a U-Turn — the pivot from external to internal focus."""
        self._focus_shifts.append(focus_shift)

    # --- Metrics ---

    @property
    def is_self_led(self) -> bool:
        """Whether the system is currently Self-led."""
        return is_self_led(self._self_system)

    @property
    def preservation_ratio(self) -> float:
        """Ratio of Self-energy to total Part activation."""
        return self_preservation_ratio(self._self_system, self._graph)

    def detect_polarization(
        self, trust_threshold: float = 0.4,
    ) -> list[PolarizationEdge]:
        """Suggest polarized pairs from graph structure (V2).

        Returns ``PolarizationEdge`` suggestions — not auto-added to graph.
        """
        return detect_polarization(self._graph, trust_threshold)

    # --- Export ---

    def export_parts_map(self) -> dict[str, Any]:
        """Export the Parts Map as a JSON-serialisable dict.

        Output is compatible with force-directed graph visualisation
        tools (D3.js, Gephi, Cytoscape).
        """
        return self._graph.to_json()
