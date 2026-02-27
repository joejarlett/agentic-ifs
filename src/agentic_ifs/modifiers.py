"""The 5 Ps — interaction modifiers for the IFS facilitator.

IFS (Schwartz): The 5 Ps describe the qualities of an effective IFS
facilitator (therapist or Self-led individual). They are not Part qualities
(those are the 8 Cs of Self) — they are **how** the facilitator engages
with the system.

- **Presence**: being fully here with the Part
- **Patience**: allowing the Part to move at its own pace
- **Perspective**: maintaining observer stance (not merging with the Part)
- **Persistence**: staying with the process even when Parts resist
- **Playfulness**: bringing lightness and warmth to the interaction

Computationally, the 5 Ps are API-level modifiers that affect how the
6 Fs workflow and unburdening pipeline behave. They tune thresholds,
increments, and variance — making the simulation more nuanced.
"""

from __future__ import annotations

import random

from pydantic import BaseModel, Field


class FivePs(BaseModel):
    """The 5 Ps of IFS facilitation as interaction modifiers.

    Each P is a float from 0.0 (absent) to 1.0 (fully present). Default
    0.5 represents a competent but not masterful facilitator.

    These modifiers affect the simulation engine:

    - ``presence``: multiplier on Self-energy checks — amplifies available
      Self when the facilitator is fully present.
    - ``patience``: scales ``COMPASSION_THRESHOLD`` down — a patient
      facilitator can work with lower Self-energy.
    - ``perspective``: controls log detail level — high perspective means
      the facilitator maintains observer stance and logs more metadata.
    - ``persistence``: scales trust increment in ``befriend()`` — a
      persistent facilitator builds trust more effectively.
    - ``playfulness``: introduces variance in trust increments — a playful
      facilitator brings spontaneity.
    """

    presence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description=(
            "Being fully here with the Part. "
            "Amplifies effective self_energy for threshold checks."
        ),
    )
    patience: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description=(
            "Allowing the Part to move at its own pace. "
            "Reduces COMPASSION_THRESHOLD for feel_toward gate."
        ),
    )
    perspective: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description=(
            "Maintaining observer stance (not merging with the Part). "
            "Controls log detail level."
        ),
    )
    persistence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description=(
            "Staying with the process even when Parts resist. "
            "Scales trust increment in befriend step."
        ),
    )
    playfulness: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description=(
            "Bringing lightness and warmth to the interaction. "
            "Introduces variance in trust increments."
        ),
    )

    def effective_threshold(self, base_threshold: float) -> float:
        """Compute the effective compassion threshold.

        High ``patience`` lowers the gate, allowing the facilitator to
        work with Parts even when Self-energy is moderate. High
        ``presence`` means less threshold reduction is needed.

        Formula: ``threshold × (1 - patience × 0.3)``

        At patience=0.0: full threshold (no adjustment).
        At patience=1.0: threshold reduced by 30%.
        """
        return base_threshold * (1.0 - self.patience * 0.3)

    def effective_self_energy(self, self_energy: float) -> float:
        """Compute effective Self-energy for threshold checks.

        High ``presence`` amplifies the available Self-energy, modelling
        the IFS principle that a fully present facilitator can access
        more Self even when the system is partially blended.

        Formula: ``self_energy × (1 + presence × 0.2)``

        At presence=0.0: no amplification.
        At presence=1.0: 20% boost.

        Capped at 1.0.
        """
        return min(self_energy * (1.0 + self.presence * 0.2), 1.0)

    def trust_increment(self, base_increment: float = 0.1) -> float:
        """Compute trust increment for the befriend step.

        ``persistence`` scales the base increment up — a persistent
        facilitator builds trust more effectively. ``playfulness``
        adds random variance, modelling the IFS observation that
        playful engagement often unlocks Parts more quickly.

        At persistence=0.0: half the base increment.
        At persistence=1.0: 1.5× the base increment.

        Playfulness adds ±20% variance at playfulness=1.0.
        """
        scaled = base_increment * (0.5 + self.persistence)
        if self.playfulness > 0.0:
            variance = self.playfulness * 0.2 * base_increment
            scaled += random.uniform(-variance, variance)
        return max(scaled, 0.01)  # Never negative or zero
