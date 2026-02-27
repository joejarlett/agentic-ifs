"""Part classes and supporting enums for Internal Family Systems.

This module defines the core data structures for IFS Parts — the autonomous
sub-personalities that make up the internal system. Each Part has a positive
protective intent, even when its behaviours are destructive.

IFS taxonomy:
    - Manager: proactive protector (Daemon/BackgroundService)
    - Firefighter: reactive protector (ExceptionHandler/EmergencyOverride)
    - Exile: burdened vulnerability (EncryptedDataBlob/QuarantinedProcess)

All Parts share a common base (IPart) and are distinguished by the ``part_type``
discriminator field, enabling correct Pydantic v2 serialisation via PartUnion.
"""

from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Annotated, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# State enums
# ---------------------------------------------------------------------------


class ManagerState(str, Enum):
    """State machine for Manager Parts.

    IFS: Managers continuously scan for threats to the system. They transition
    from idle monitoring to active scanning to blocking when a threat is detected.

    ``IDLE`` → ``SCANNING`` → ``BLOCKING``
    """

    IDLE = "idle"
    SCANNING = "scanning"
    BLOCKING = "blocking"


class FirefighterState(str, Enum):
    """State machine for Firefighter Parts.

    IFS: Firefighters are dormant until a Manager's blocking fails and an
    Exile's pain overflows. They activate with extreme measures, then enter
    a refractory cooldown period.

    ``DORMANT`` → ``ACTIVE`` → ``COOLDOWN``
    """

    DORMANT = "dormant"
    ACTIVE = "active"
    COOLDOWN = "cooldown"


class ExileState(str, Enum):
    """State machine for Exile Parts.

    IFS: Exiles are sequestered by Protectors. Their state can change
    through two distinct pathways:

    **Pathological breakthrough** (defences fail):
    ``ISOLATED`` → ``LEAKING`` → ``FLOODING``

    **Therapeutic healing** (Self retrieves intentionally):
    ``ISOLATED`` → ``RETRIEVED`` → ``UNBURDENED``

    LEAKING and FLOODING are *uncontrolled* — Exile material breaks through
    despite Protectors. RETRIEVED is *intentional* — Self goes back to the
    trauma scene and brings the Exile forward into present safety.
    """

    ISOLATED = "isolated"
    LEAKING = "leaking"
    FLOODING = "flooding"
    RETRIEVED = "retrieved"
    UNBURDENED = "unburdened"


class BurdenType(str, Enum):
    """Classification of burden origin.

    IFS distinguishes burdens by their source — personal experience, inherited
    family patterns, culturally transmitted beliefs, or unattached/ambient
    energies in the field.
    """

    PERSONAL = "personal"
    LEGACY = "legacy"
    UNATTACHED = "unattached"
    SOCIETAL = "societal"


# ---------------------------------------------------------------------------
# Burden
# ---------------------------------------------------------------------------


class Burden(BaseModel):
    """Trauma payload attached to an Exile.

    IFS: A burden is a limiting belief or extreme feeling taken on at the
    time of a wounding experience. It is *foreign* to the Part — not the
    Part's true nature, but something imposed on it.

    ``emotional_charge`` is the **stored** intensity — how much potential
    pain is locked in the payload. Compare with ``Exile.emotional_charge``
    which is the **current** activation intensity affecting the system now.
    """

    burden_type: BurdenType
    origin: str = Field(description="Origin context, e.g. 'Age 7, school failure'")
    content: str = Field(description="The limiting belief, e.g. 'I am not enough'")
    emotional_charge: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Stored intensity of the burden (0.0–1.0)",
    )
    lineage: list[str] = Field(
        default_factory=list,
        description="Lineage chain for legacy burdens, e.g. ['grandmother', 'mother', 'self']",
    )

    @property
    def generation_depth(self) -> int:
        """Number of generations in the lineage chain.

        Returns 0 if no lineage is specified (personal burden).
        """
        return len(self.lineage)


# ---------------------------------------------------------------------------
# Base Part
# ---------------------------------------------------------------------------


class IPart(BaseModel):
    """Abstract base for all IFS Parts (sub-personalities).

    IFS: A Part is an autonomous sub-personality with its own perspective,
    feelings, memories, and goals. All Parts have positive protective intent,
    even when their behaviours are destructive.

    This class should not be instantiated directly — use ``Manager``,
    ``Firefighter``, or ``Exile``.
    """

    id: UUID = Field(default_factory=uuid4)
    part_type: str = Field(description="Discriminator for Pydantic union deserialisation")
    narrative: str = Field(description="The story the Part tells about its origin")
    age: int = Field(description="Developmental age at which the Part was frozen")
    intent: str = Field(description="The positive protective intent")
    trust_level: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Degree of trust in Self (0.0–1.0)",
    )
    is_visible: bool = Field(
        default=True,
        description="Whether accessible to consciousness",
    )


# ---------------------------------------------------------------------------
# Concrete Part types
# ---------------------------------------------------------------------------


class Manager(IPart):
    """Proactive protector. Runs continuous monitoring to prevent Exile activation.

    IFS: Managers are preemptive control systems — they scan the environment
    for triggers and enforce rules (perfectionism, planning, criticism) to
    keep the system safe. They operate like daemons or background services.

    Computational equivalent: Daemon / BackgroundService.
    """

    part_type: Literal["manager"] = "manager"
    triggers: list[str] = Field(
        default_factory=list,
        description="Input patterns that initiate protective subroutines",
    )
    strategies: list[str] = Field(
        default_factory=list,
        description="Pre-emptive actions (e.g. perfectionism, over-preparation)",
    )
    rigidity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Resistance to state change (0.0–1.0)",
    )
    state: ManagerState = ManagerState.IDLE


class Firefighter(IPart):
    """Reactive protector. Activated when Manager blocking fails (Exile overflow).

    IFS: Firefighters use extreme, often chaotic measures to extinguish
    emotional pain — binge eating, dissociation, rage, substance use.
    They are interrupt handlers, activated only in emergency.

    Computational equivalent: ExceptionHandler / EmergencyOverride.
    """

    part_type: Literal["firefighter"] = "firefighter"
    pain_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Affective intensity level that triggers activation (0.0–1.0)",
    )
    extinguishing_behaviors: list[str] = Field(
        default_factory=list,
        description="High-intensity outputs (e.g. binge, dissociation, rage)",
    )
    refractory_period: timedelta = Field(
        default=timedelta(minutes=30),
        description="Recovery time before deactivation",
    )
    state: FirefighterState = FirefighterState.DORMANT


class Exile(IPart):
    """Burdened vulnerability. Sequestered repository of unprocessed trauma.

    IFS: Exiles carry the pain, shame, fear, and loneliness from wounding
    experiences. They are hidden by Protectors (Managers and Firefighters)
    to prevent the system from being overwhelmed.

    ``emotional_charge`` is the **current** activation intensity — how much
    the system is being affected right now. Compare with
    ``Burden.emotional_charge`` which is the **stored** intensity in the
    trauma payload.

    Computational equivalent: EncryptedDataBlob / QuarantinedProcess.
    """

    part_type: Literal["exile"] = "exile"
    burden: Burden | None = Field(
        default=None,
        description="The trauma payload (limiting belief + stored charge)",
    )
    emotional_charge: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Current activation intensity (0.0–1.0)",
    )
    is_visible: bool = Field(
        default=False,
        description="Exiles are hidden by default",
    )
    invited_qualities: list[str] = Field(
        default_factory=list,
        description=(
            "Qualities invited in after unburdening (V2). "
            "e.g. ['playfulness', 'curiosity', 'lightness']"
        ),
    )
    state: ExileState = ExileState.ISOLATED


# ---------------------------------------------------------------------------
# Discriminated union type
# ---------------------------------------------------------------------------

PartUnion = Annotated[
    Manager | Firefighter | Exile,
    Field(discriminator="part_type"),
]
"""Discriminated union of all concrete Part types.

Use this for dict values and list elements that may hold any Part subtype.
Pydantic v2 will correctly deserialise JSON back to the right class based
on the ``part_type`` field.
"""
