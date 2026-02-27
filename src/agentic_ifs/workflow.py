"""The 6 Fs workflow, Trailheads, and FocusShift (U-Turn).

The 6 Fs is the standard IFS algorithm for engaging with Protectors
(Managers and Firefighters). It is the core "game loop" of V1.

Steps: Find → Focus → Flesh Out → Feel Toward → Befriend → Fear

The critical gate is **Feel Toward**: if ``self_energy`` is below
``COMPASSION_THRESHOLD``, a new Part has blended (the one feeling
negatively toward the target). That Part must be unblended first —
this is the recursive check that makes IFS clinically distinct.

This module also provides:
    - ``Trailhead`` / ``TrailheadLog``: entry points for a session
    - ``FocusShift``: the U-Turn marker (external → internal pivot)
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .dynamics import COMPASSION_THRESHOLD
from .graph import ProtectionGraph
from .self_system import LogEntry, SelfSystem


# ---------------------------------------------------------------------------
# Trailheads
# ---------------------------------------------------------------------------


class TrailheadType(str, Enum):
    """Classification of trailhead sensory modality.

    IFS: A trailhead can manifest as a body sensation (somatic),
    an internal image (visual), a voice or sound (auditory),
    or a thought/belief (cognitive).
    """

    SOMATIC = "somatic"
    VISUAL = "visual"
    AUDITORY = "auditory"
    COGNITIVE = "cognitive"


class Trailhead(BaseModel):
    """An entry point for a session — a signal that a Part is present.

    IFS: A trailhead is the sensation, image, emotion, or thought that
    indicates a Part is activated and available for engagement. It is
    the starting point for the 6 Fs process.

    Computational equivalent: EventLog entry / InterruptSignal.
    """

    id: UUID = Field(default_factory=uuid4)
    trailhead_type: TrailheadType
    intensity: float = Field(
        ge=0.0,
        le=1.0,
        description="Intensity of the signal (0.0–1.0)",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    description: str
    associated_part_id: UUID | None = Field(
        default=None,
        description="Populated after the FIND step identifies the Part",
    )


class TrailheadLog(BaseModel):
    """Ordered log of all trailheads observed in a session."""

    entries: list[Trailhead] = Field(default_factory=list)

    def add(self, trailhead: Trailhead) -> None:
        """Record a new trailhead."""
        self.entries.append(trailhead)

    def get_by_type(self, trailhead_type: TrailheadType) -> list[Trailhead]:
        """Filter trailheads by sensory modality."""
        return [t for t in self.entries if t.trailhead_type == trailhead_type]

    def get_by_part(self, part_id: UUID) -> list[Trailhead]:
        """Get all trailheads associated with a specific Part."""
        return [t for t in self.entries if t.associated_part_id == part_id]


# ---------------------------------------------------------------------------
# U-Turn (FocusShift)
# ---------------------------------------------------------------------------


class FocusShift(BaseModel):
    """U-Turn marker — the pivot from external trigger to internal Part.

    IFS: The U-Turn is the moment when attention shifts from "what happened
    to me" (my boss criticised me) to "what is happening inside me"
    (my Angry Part is activated). This pivot is foundational to IFS work.

    Computational equivalent: FocusShift event / meta-tag on session log.
    """

    from_subject: str = Field(description="The external trigger (e.g. 'My boss')")
    to_subject: str = Field(description="The Part now in focus (e.g. 'My Anger')")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    trailhead_id: UUID | None = Field(
        default=None,
        description="The trailhead that prompted this shift",
    )


# ---------------------------------------------------------------------------
# 6 Fs State Machine
# ---------------------------------------------------------------------------


class SixFsStep(str, Enum):
    """The six steps of the IFS Protector engagement algorithm.

    IFS (Anderson, Schwartz & Sweezy, 2017):
        1. Find — locate the Part
        2. Focus — direct attention to it
        3. Flesh Out — gather metadata (age, image, sensation)
        4. Feel Toward — check Self-energy presence (critical gate)
        5. Befriend — build relationship, update trust
        6. Fear — identify the Part's worst-case scenarios
    """

    FIND = "find"
    FOCUS = "focus"
    FLESH_OUT = "flesh_out"
    FEEL_TOWARD = "feel_toward"
    BEFRIEND = "befriend"
    FEAR = "fear"


class SixFsResult(BaseModel):
    """Result of executing a single step in the 6 Fs workflow.

    If ``unblend_required`` is set, the caller must unblend that Part
    before re-calling ``feel_toward``. This implements the recursive
    check: if you feel anger toward a Part, the anger is itself a Part.
    """

    step: SixFsStep
    target_part_id: UUID | None = None
    next_step: SixFsStep | None = None
    unblend_required: UUID | None = Field(
        default=None,
        description="Part to unblend before proceeding (feel_toward gate)",
    )
    notes: str = ""


class SixFsStateMachine:
    """Sequential state machine for Protector engagement (the 6 Fs).

    IFS: This is the standard algorithm for working with Managers and
    Firefighters. The facilitator (Self) moves through six steps to
    build a relationship with a protective Part and understand its fears.

    The critical gate is ``feel_toward()``: if ``self_energy`` is below
    ``COMPASSION_THRESHOLD``, a new Part has blended (the one feeling
    negatively toward the target). That Part must be unblended first.
    This recursive check prevents bypassing — it ensures Self is
    genuinely present before engaging.
    """

    def __init__(
        self,
        graph: ProtectionGraph,
        self_system: SelfSystem,
        log: TrailheadLog,
    ) -> None:
        self.graph = graph
        self.self_system = self_system
        self.log = log
        self._current_step: SixFsStep | None = None
        self._target_part_id: UUID | None = None

    @property
    def current_step(self) -> SixFsStep | None:
        """The step currently in progress, if any."""
        return self._current_step

    @property
    def target_part_id(self) -> UUID | None:
        """The Part currently being engaged."""
        return self._target_part_id

    def find(self, trailhead: Trailhead) -> SixFsResult:
        """Step 1: Locate the Part.

        IFS: Scan the system for the Part signalled by the trailhead.
        Associates the trailhead with the identified Part.

        Computational equivalent: ScanSystem → PartReference.
        """
        self._current_step = SixFsStep.FIND

        # If the trailhead already has an associated part, use it
        part_id = trailhead.associated_part_id

        # Log the trailhead
        self.log.add(trailhead)

        self.self_system.session_log.append(
            LogEntry(
                event_type="six_fs",
                description=f"FIND: Trailhead '{trailhead.description}' observed",
                part_id=part_id,
            )
        )

        return SixFsResult(
            step=SixFsStep.FIND,
            target_part_id=part_id,
            next_step=SixFsStep.FOCUS,
            notes=f"Trailhead: {trailhead.description} ({trailhead.trailhead_type.value})",
        )

    def focus(self, part_id: UUID) -> SixFsResult:
        """Step 2: Direct attention to the Part.

        IFS: Turn toward the Part with intention. This is the act of
        selecting it as the focus of engagement.

        Computational equivalent: SelectTarget(PartID).
        """
        if part_id not in self.graph.nodes:
            raise ValueError(f"Part {part_id} not in graph")

        self._current_step = SixFsStep.FOCUS
        self._target_part_id = part_id

        self.self_system.session_log.append(
            LogEntry(
                event_type="six_fs",
                description="FOCUS: Attention directed to Part",
                part_id=part_id,
            )
        )

        return SixFsResult(
            step=SixFsStep.FOCUS,
            target_part_id=part_id,
            next_step=SixFsStep.FLESH_OUT,
        )

    def flesh_out(self, part_id: UUID) -> SixFsResult:
        """Step 3: Gather metadata about the Part.

        IFS: Ask the Part about itself — its age, how it appears
        (image), where it's felt in the body, what it believes.

        Computational equivalent: QueryPart(PartID, attributes).
        """
        if part_id not in self.graph.nodes:
            raise ValueError(f"Part {part_id} not in graph")

        self._current_step = SixFsStep.FLESH_OUT
        part = self.graph.nodes[part_id]

        self.self_system.session_log.append(
            LogEntry(
                event_type="six_fs",
                description=f"FLESH_OUT: Part aged {part.age}, intent: '{part.intent}'",
                part_id=part_id,
            )
        )

        return SixFsResult(
            step=SixFsStep.FLESH_OUT,
            target_part_id=part_id,
            next_step=SixFsStep.FEEL_TOWARD,
            notes=f"Age: {part.age}, Intent: {part.intent}",
        )

    def feel_toward(self, part_id: UUID) -> SixFsResult:
        """Step 4: Check Self-energy presence — THE CRITICAL GATE.

        IFS: "How do you feel toward this Part?" If the answer is
        anything other than curiosity/compassion (e.g. anger, judgment,
        fear), then a *new* Part has blended — and must be worked with
        first. This recursive check is what makes IFS clinically distinct.

        If ``self_energy > COMPASSION_THRESHOLD``: proceed to Befriend.
        If ``self_energy <= COMPASSION_THRESHOLD``: return
        ``unblend_required`` with the most blended Part's ID.
        """
        if part_id not in self.graph.nodes:
            raise ValueError(f"Part {part_id} not in graph")

        self._current_step = SixFsStep.FEEL_TOWARD

        if self.self_system.self_energy > COMPASSION_THRESHOLD:
            # Self is present — proceed to Befriend
            self.self_system.session_log.append(
                LogEntry(
                    event_type="six_fs",
                    description=(
                        f"FEEL_TOWARD: Self-energy sufficient "
                        f"({self.self_system.self_energy:.2f} > {COMPASSION_THRESHOLD})"
                    ),
                    part_id=part_id,
                )
            )
            return SixFsResult(
                step=SixFsStep.FEEL_TOWARD,
                target_part_id=part_id,
                next_step=SixFsStep.BEFRIEND,
                notes="Self-energy sufficient — Self is present",
            )
        else:
            # A new Part has blended — find the most blended one
            interfering = self._identify_most_blended()
            self.self_system.session_log.append(
                LogEntry(
                    event_type="six_fs",
                    description=(
                        f"FEEL_TOWARD: Self-energy insufficient "
                        f"({self.self_system.self_energy:.2f} <= {COMPASSION_THRESHOLD})"
                        f" — unblend required"
                    ),
                    part_id=interfering,
                )
            )
            return SixFsResult(
                step=SixFsStep.FEEL_TOWARD,
                target_part_id=part_id,
                next_step=None,  # Caller must unblend first
                unblend_required=interfering,
                notes="Self-energy insufficient — another Part is blended",
            )

    def befriend(self, part_id: UUID) -> SixFsResult:
        """Step 5: Build relationship with the Part.

        IFS: Express appreciation for the Part's protective role.
        Update trust. Let the Part know that Self sees it and
        values its intention.

        Computational equivalent: UpdateTrust(PartID, +Increment).
        """
        if part_id not in self.graph.nodes:
            raise ValueError(f"Part {part_id} not in graph")

        self._current_step = SixFsStep.BEFRIEND
        part = self.graph.nodes[part_id]

        # Increment trust toward Self
        new_trust = min(part.trust_level + 0.1, 1.0)
        part.trust_level = new_trust

        self.self_system.session_log.append(
            LogEntry(
                event_type="six_fs",
                description=f"BEFRIEND: Trust updated to {new_trust:.2f}",
                part_id=part_id,
            )
        )

        return SixFsResult(
            step=SixFsStep.BEFRIEND,
            target_part_id=part_id,
            next_step=SixFsStep.FEAR,
            notes=f"Trust updated to {new_trust:.2f}",
        )

    def fear(self, part_id: UUID) -> SixFsResult:
        """Step 6: Identify the Part's worst-case scenarios.

        IFS: "What are you afraid would happen if you stopped doing
        your job?" The Part's fears reveal the Exile it protects and
        the burden it carries.

        Computational equivalent: GetFears(PartID) → list[Prediction].
        """
        if part_id not in self.graph.nodes:
            raise ValueError(f"Part {part_id} not in graph")

        self._current_step = SixFsStep.FEAR
        part = self.graph.nodes[part_id]

        # Find what this Part protects
        protected_exiles = [
            e for e in self.graph.edges
            if e.source_id == part_id
        ]

        self.self_system.session_log.append(
            LogEntry(
                event_type="six_fs",
                description=(
                    f"FEAR: Part protects {len(protected_exiles)} other Part(s)"
                ),
                part_id=part_id,
            )
        )

        return SixFsResult(
            step=SixFsStep.FEAR,
            target_part_id=part_id,
            next_step=None,  # 6 Fs complete for this Part
            notes=(
                f"Protects {len(protected_exiles)} Part(s). "
                f"Part intent: '{part.intent}'"
            ),
        )

    def _identify_most_blended(self) -> UUID | None:
        """Find the Part with the highest blending percentage.

        Used by ``feel_toward`` to identify which Part has taken over
        the seat of consciousness.
        """
        if not self.self_system.active_blends:
            return None
        most_blended = max(
            self.self_system.active_blends,
            key=lambda b: b.blending_percentage,
        )
        return most_blended.part_id
