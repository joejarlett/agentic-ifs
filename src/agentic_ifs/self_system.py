"""SelfSystem — the operating environment for the internal system.

Self is not an agent. Self is the system's ground state — a global attractor.
When Self-energy is high, Parts can relax their protective roles. When Parts
blend, they occlude Self-energy.

IFS axiom: **Self is never damaged.** ``self_potential`` is always 1.0 (the
sun). ``self_energy`` is what's currently accessible (the sunlight reaching
the ground after cloud cover from blended Parts).

V2 enhancement: Self-energy is now an **8C vector** — Curiosity, Calm,
Clarity, Compassion, Confidence, Courage, Creativity, Connectedness. Each
quality can be independently occluded by blending Parts via
``BlendState.occlusion_mask``. The scalar ``self_energy`` is the mean of
all 8 qualities, preserving backward compatibility with V1 code.

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
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SELF_QUALITIES: tuple[str, ...] = (
    "curiosity", "calm", "clarity", "compassion",
    "confidence", "courage", "creativity", "connectedness",
)
"""The 8 Cs of Self — the qualities that define Self-energy in IFS.

IFS (Schwartz): When Self is present, the individual has access to these
eight qualities. Blending with a Part reduces specific qualities — e.g.
an anxious Manager blending reduces Calm and Clarity.
"""


# ---------------------------------------------------------------------------
# Blend state
# ---------------------------------------------------------------------------


class BlendState(BaseModel):
    """Represents a Part blending with (assuming control of) the system.

    IFS: Blending occurs when a Part's state overwrites the Self's state,
    assuming control of I/O channels. The individual no longer observes
    the Part — they *become* it. ``blending_percentage`` tracks how much
    control the Part has taken.

    The ``occlusion_mask`` maps Self quality names (the 8 Cs) to reduction
    values. For example, ``{'calm': 0.9, 'clarity': 0.5}`` means this
    blend reduces Calm by 90% and Clarity by 50%. Qualities not in the mask
    fall back to the overall ``blending_percentage``.

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
            "Qualities not in the mask use blending_percentage as fallback."
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


# ---------------------------------------------------------------------------
# 8C Self-Energy Vector
# ---------------------------------------------------------------------------


class SelfEnergyVector(BaseModel):
    """The 8 Cs of Self-energy as a vector.

    IFS: The 8 Cs (Curiosity, Calm, Clarity, Compassion, Confidence,
    Courage, Creativity, Connectedness) define the quality of the system's
    processing capability when Self is present. Each quality ranges from
    0.0 (fully occluded) to 1.0 (fully accessible).

    Computational equivalent: a normalised feature vector representing
    the global system state. Individual qualities can be selectively
    reduced by blending Parts via ``BlendState.occlusion_mask``.
    """

    curiosity: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Openness to exploring Parts without agenda",
    )
    calm: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Groundedness — absence of reactivity",
    )
    clarity: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Ability to see the system clearly",
    )
    compassion: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Warmth toward Parts, especially burdened Exiles",
    )
    confidence: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Trust in Self's capacity to lead the system",
    )
    courage: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Willingness to approach pain and fear",
    )
    creativity: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Capacity for novel solutions and perspectives",
    )
    connectedness: float = Field(
        default=0.3, ge=0.0, le=1.0,
        description="Sense of connection to Parts and the wider world",
    )

    @property
    def composite(self) -> float:
        """Mean of all 8 qualities — the scalar Self-energy equivalent.

        This is the backward-compatible bridge to V1's scalar
        ``self_energy``. All V1 code that checks ``self_energy``
        now checks the composite of the 8C vector.
        """
        total = sum(getattr(self, q) for q in SELF_QUALITIES)
        return total / len(SELF_QUALITIES)

    @classmethod
    def uniform(cls, value: float) -> SelfEnergyVector:
        """Create a vector with all 8 qualities set to the same value.

        Used when initialising from a scalar ``self_energy`` value
        (backward compatibility with V1).
        """
        return cls(**{q: value for q in SELF_QUALITIES})

    def to_dict(self) -> dict[str, float]:
        """Export all 8 qualities as a dict."""
        return {q: getattr(self, q) for q in SELF_QUALITIES}


# ---------------------------------------------------------------------------
# SelfSystem
# ---------------------------------------------------------------------------


class SelfSystem(BaseModel):
    """The operating environment. Not an agent.

    IFS: Self is the system's ground state — always present, never damaged,
    only occluded by blending Parts.

    - ``self_potential`` represents the immutable core (always 1.0).
      **Treat as a constant — do not modify.**
    - ``self_energy`` is the composite (mean) of the 8C vector — what's
      currently accessible after blending effects. Recalculated
      automatically when Parts blend or unblend.
    - ``self_energy_vector`` is the full 8C breakdown (V2). Each quality
      can be independently occluded by blending Parts.

    Occlusion formula (per quality):

        ``quality = self_potential × (1 - occlusion)``

    where ``occlusion`` is the maximum of either the blend's specific
    mask value for that quality, or the blend's overall
    ``blending_percentage`` if no mask is specified. This replicates
    V1 behaviour when no ``occlusion_mask`` is provided.
    """

    self_potential: float = Field(
        default=1.0,
        description="The undamaged core — treat as constant (always 1.0)",
    )
    self_energy: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Composite (mean of 8C vector) — recalculated from blends",
    )
    self_energy_vector: SelfEnergyVector = Field(
        default_factory=SelfEnergyVector,
        description="V2: per-quality Self-energy breakdown (8 Cs)",
    )
    active_blends: list[BlendState] = Field(default_factory=list)
    session_log: list[LogEntry] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _sync_energy_and_vector(cls, data: Any) -> Any:
        """Sync ``self_energy`` and ``self_energy_vector`` at construction.

        If the caller provides ``self_energy`` but not ``self_energy_vector``,
        create a uniform vector matching the scalar (V1 compatibility).
        """
        if not isinstance(data, dict):
            return data

        has_vector = "self_energy_vector" in data
        has_energy = "self_energy" in data

        if has_energy and not has_vector:
            data["self_energy_vector"] = {
                q: data["self_energy"] for q in SELF_QUALITIES
            }

        return data

    @model_validator(mode="after")
    def _sync_composite(self) -> SelfSystem:
        """Ensure ``self_energy`` matches the vector composite after init.

        Uses a tolerance check to avoid floating-point drift when the
        vector was auto-created from a scalar value.
        """
        computed = self.self_energy_vector.composite
        if abs(computed - self.self_energy) > 1e-9:
            self.self_energy = computed
        return self

    def recalculate(self) -> None:
        """Recalculate the 8C vector and composite ``self_energy``.

        For each quality, finds the maximum occlusion across all active
        blends. If a blend has a specific ``occlusion_mask`` value for
        a quality, that value is used; otherwise the blend's overall
        ``blending_percentage`` is the fallback. This means V1 code
        (no masks) behaves identically — all qualities reduce uniformly.
        """
        if not self.active_blends:
            for quality in SELF_QUALITIES:
                setattr(self.self_energy_vector, quality, self.self_potential)
            self.self_energy = self.self_potential
            return

        for quality in SELF_QUALITIES:
            max_occlusion = max(
                b.occlusion_mask.get(quality, b.blending_percentage)
                for b in self.active_blends
            )
            setattr(
                self.self_energy_vector,
                quality,
                self.self_potential * (1.0 - max_occlusion),
            )

        self.self_energy = self.self_energy_vector.composite

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
