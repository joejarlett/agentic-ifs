"""Session — thin convenience facade over the composable core.

A Session bundles ``ProtectionGraph``, ``SelfSystem``, ``TrailheadLog``,
and ``SixFsStateMachine`` into a single coordinated unit. It delegates
all operations to the underlying components — it is not a different
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

IFS meaning: a Session represents a single therapeutic encounter — a
bounded context in which Parts are engaged and the system moves toward
greater Self-energy.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from .dynamics import is_self_led, self_preservation_ratio
from .graph import Edge, PolarizationEdge, ProtectionGraph
from .parts import IPart
from .self_system import BlendState, SelfSystem
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
    and ``SixFsStateMachine`` as a coordinated unit. All methods delegate
    to the underlying objects.

    IFS: A Session represents a single therapeutic encounter — a bounded
    context in which Parts are engaged and the system moves toward greater
    Self-energy.

    Parameters
    ----------
    initial_self_energy:
        Starting ``self_energy`` value. Default 0.3 reflects a typical
        person arriving at a session with Managers already running.
    """

    def __init__(self, initial_self_energy: float = 0.3) -> None:
        self._graph = ProtectionGraph()
        self._self_system = SelfSystem(self_energy=initial_self_energy)
        self._trailhead_log = TrailheadLog()
        self._workflow = SixFsStateMachine(
            graph=self._graph,
            self_system=self._self_system,
            log=self._trailhead_log,
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

    # --- Export ---

    def export_parts_map(self) -> dict[str, Any]:
        """Export the Parts Map as a JSON-serialisable dict.

        Output is compatible with force-directed graph visualisation
        tools (D3.js, Gephi, Cytoscape).
        """
        return self._graph.to_json()
