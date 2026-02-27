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

from .graph import PolarizationEdge, ProtectionGraph
from .parts import Firefighter, Manager
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


# ---------------------------------------------------------------------------
# V2: Polarization detection
# ---------------------------------------------------------------------------

_LOW_TRUST_THRESHOLD: float = 0.4
"""Trust level below which a Protector is considered rigidly defensive.

Used by ``detect_polarization()`` as a heuristic: Parts with low trust
in Self tend to escalate their strategies, increasing the likelihood
of polarization with other low-trust Protectors guarding the same Exile.
"""


def detect_polarization(
    graph: ProtectionGraph,
    trust_threshold: float = _LOW_TRUST_THRESHOLD,
) -> list[PolarizationEdge]:
    """Suggest polarized pairs from graph structure (V2).

    IFS: Polarization occurs when two Protectors (typically a Manager and
    a Firefighter) escalate in opposition — e.g. a Perfectionist Manager
    tightens control while a Procrastinator Firefighter shuts down harder.

    This heuristic detects *potential* polarization by looking for:

    1. A Manager and a Firefighter that both protect the same Exile
    2. Both have ``trust_level`` below ``trust_threshold`` (rigid, defensive)

    Returns a list of suggested ``PolarizationEdge`` objects. These are
    **suggestions only** — the researcher should review and confirm before
    adding them to the graph.

    Parameters
    ----------
    graph:
        The protection graph to analyse.
    trust_threshold:
        Maximum ``trust_level`` for a Protector to be considered rigid.
        Default 0.4.
    """
    suggestions: list[PolarizationEdge] = []
    already_polarized = {
        (pe.part_a_id, pe.part_b_id) for pe in graph.polarization_edges
    } | {
        (pe.part_b_id, pe.part_a_id) for pe in graph.polarization_edges
    }

    managers = [
        p for p in graph.nodes.values()
        if isinstance(p, Manager) and p.trust_level < trust_threshold
    ]
    firefighters = [
        p for p in graph.nodes.values()
        if isinstance(p, Firefighter) and p.trust_level < trust_threshold
    ]

    for mgr in managers:
        for ff in firefighters:
            if (mgr.id, ff.id) in already_polarized:
                continue

            shared = graph.get_shared_exiles(mgr.id, ff.id)
            if shared:
                tension = 1.0 - min(mgr.trust_level, ff.trust_level)
                suggestions.append(
                    PolarizationEdge(
                        part_a_id=mgr.id,
                        part_b_id=ff.id,
                        tension_level=round(tension, 2),
                    )
                )

    return suggestions
