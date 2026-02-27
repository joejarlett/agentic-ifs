"""System dynamics utilities — metrics and thresholds.

This module provides read-only utility functions that operate on
``SelfSystem`` and ``ProtectionGraph`` state. It does **not** contain
blend/unblend logic — that lives as instance methods on ``SelfSystem``.

Key concepts:
    - ``COMPASSION_THRESHOLD``: the minimum ``self_energy`` required for
      Self-led engagement with a Part (the critical gate in the 6 Fs).
    - ``self_preservation_ratio``: how much Self-energy is available
      relative to total Part activation intensity.
    - ``is_self_led``: whether the system is currently above the
      compassion threshold.
"""

from __future__ import annotations

from .graph import ProtectionGraph
from .self_system import SelfSystem

COMPASSION_THRESHOLD: float = 0.5
"""Minimum ``self_energy`` for Self-led engagement.

IFS: The "Feel Toward" step in the 6 Fs checks whether the facilitator
(Self) can approach the target Part with curiosity and compassion. If
``self_energy`` is below this threshold, another Part has blended and
must be unblended first.
"""


def self_preservation_ratio(
    self_system: SelfSystem,
    graph: ProtectionGraph,
) -> float:
    """Ratio of Self-energy to total Part activation intensity.

    IFS: This metric captures the balance of power between Self and
    the Parts. A high ratio means Self is in the lead; a low ratio
    means Parts are dominating the system.

    Returns 1.0 if there are no Exiles (no activation to measure against),
    or if total activation is zero.
    """
    exiles = graph.get_exiles()
    if not exiles:
        return 1.0

    total_activation = sum(e.emotional_charge for e in exiles)
    if total_activation == 0.0:
        return 1.0

    return min(self_system.self_energy / total_activation, 1.0)


def is_self_led(self_system: SelfSystem) -> bool:
    """Whether the system is currently Self-led.

    Returns ``True`` if ``self_energy`` exceeds ``COMPASSION_THRESHOLD``,
    meaning Self has enough presence to approach Parts with curiosity
    and compassion rather than reactivity.
    """
    return self_system.self_energy > COMPASSION_THRESHOLD
