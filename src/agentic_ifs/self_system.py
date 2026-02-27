"""SelfSystem — the operating environment for the internal system.

Self is not an agent. Self is the system's ground state — a global attractor.
When Self-energy is high, Parts can relax their protective roles. When Parts
blend, they occlude Self-energy.

IFS axiom: **Self is never damaged.** ``self_potential`` is always 1.0 (the
sun). ``self_energy`` is what's currently accessible (the sunlight reaching
the ground after cloud cover from blended Parts).

Key design decisions:
    - ``self_potential`` is documented as a constant — do not modify.
    - ``self_energy`` defaults to 0.3 (typical session start with Managers
      running). Not 1.0 — that would model an unburdened system with no
      work to do.
    - ``blend()`` and ``unblend()`` live here as instance methods. No
      duplication in dynamics.py.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field


class BlendState(BaseModel):
    """Represents a Part blending with (assuming control of) the system.

    IFS: Blending occurs when a Part's state overwrites the Self's state,
    assuming control of I/O channels. The individual no longer observes
    the Part — they *become* it. ``blending_percentage`` tracks how much
    control the Part has taken.

    States: UNBLENDED (0.0) ↔ PARTIALLY_BLENDED ↔ FULLY_BLENDED (1.0)
    """

    part_id: UUID
    blending_percentage: float = Field(
        ge=0.0,
        le=1.0,
        description="How much I/O is Part-controlled (0.0–1.0)",
    )
    occlusion_mask: dict[str, float] = Field(
        default_factory=dict,
        description=(
            "Maps Self quality names to reduction values. "
            "e.g. {'calm': 0.8} means 80%% of calm is occluded. "
            "Used in V2 for 8C vector; stored but not computed in V1."
        ),
    )


class LogEntry(BaseModel):
    """A timestamped event in the session log."""

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    event_type: str = Field(description="Category of event (e.g. 'blend', 'unblend', 'six_fs')")
    description: str
    part_id: UUID | None = Field(
        default=None,
        description="Part involved in this event, if any",
    )


class SelfSystem(BaseModel):
    """The operating environment. Not an agent.

    IFS: Self is the system's ground state — always present, never damaged,
    only occluded by blending Parts.

    - ``self_potential`` represents the immutable core (always 1.0).
      **Treat as a constant — do not modify.**
    - ``self_energy`` is what's currently accessible after blending effects.
      Recalculated automatically when Parts blend or unblend.

    The occlusion formula (from IFS Self-Energy Baseline research):

        ``self_energy = self_potential × (1 - max_blend)``

    where ``max_blend`` is the highest ``blending_percentage`` among active
    blends. This models the IFS principle that the most dominant Part
    determines system behaviour.
    """

    self_potential: float = Field(
        default=1.0,
        description="The undamaged core — treat as constant (always 1.0)",
    )
    self_energy: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Dynamic — recalculated from active blends",
    )
    active_blends: list[BlendState] = Field(default_factory=list)
    session_log: list[LogEntry] = Field(default_factory=list)

    def recalculate(self) -> None:
        """Recalculate ``self_energy`` from current blends.

        Uses the max-blend occlusion model: the most blended Part
        determines accessible Self-energy.
        """
        max_blend = max(
            (b.blending_percentage for b in self.active_blends),
            default=0.0,
        )
        self.self_energy = self.self_potential * (1.0 - max_blend)

    def blend(self, blend_state: BlendState) -> None:
        """Add or update a Part's blend and recalculate ``self_energy``.

        If the Part is already blended, its blend state is replaced.
        Otherwise, a new blend is added.

        IFS: A Part steps into the seat of consciousness and begins
        controlling the system's I/O.
        """
        # Replace existing blend for same part_id
        self.active_blends = [
            b for b in self.active_blends if b.part_id != blend_state.part_id
        ]
        self.active_blends.append(blend_state)
        self.recalculate()
        self.session_log.append(
            LogEntry(
                event_type="blend",
                description=f"Part blended at {blend_state.blending_percentage:.0%}",
                part_id=blend_state.part_id,
            )
        )

    def unblend(self, part_id: UUID) -> None:
        """Remove a Part's BlendState and recalculate ``self_energy``.

        IFS: The Part steps back from the seat of consciousness,
        allowing Self to observe it rather than *be* it.
        """
        self.active_blends = [
            b for b in self.active_blends if b.part_id != part_id
        ]
        self.recalculate()
        self.session_log.append(
            LogEntry(
                event_type="unblend",
                description="Part unblended",
                part_id=part_id,
            )
        )
