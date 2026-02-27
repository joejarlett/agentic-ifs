"""The Unburdening Pipeline — the therapeutic process for Exiles.

Unburdening is the process of permanently releasing a Burden from an Exile,
transforming it from a carrier of unprocessed trauma to a free, unburdened
Part. This is the core healing process in IFS therapy.

The pipeline runs AFTER Protector work (the 6 Fs) has been completed —
Protectors must give permission before the system can access the Exile.

Stages: Witnessing → Retrieval → Reparenting → Purging → Invitation

Each stage requires Self-energy above ``COMPASSION_THRESHOLD`` — the same
gate that operates in the 6 Fs. If Self-energy drops (a Part blends),
unburdening pauses until the interfering Part is unblended.
"""

from __future__ import annotations

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from .dynamics import COMPASSION_THRESHOLD
from .graph import ProtectionGraph
from .parts import Exile, ExileState
from .self_system import LogEntry, SelfSystem


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class UnburdeningStep(str, Enum):
    """Stages of the unburdening pipeline.

    IFS: Unburdening follows a five-stage ritual after Protectors have
    stepped back. Each stage deepens the relationship between Self and
    the Exile, culminating in the release of the Burden and the invitation
    of new qualities.

    ``WITNESSING`` → ``RETRIEVAL`` → ``REPARENTING`` → ``PURGING`` → ``INVITATION`` → ``COMPLETE``
    """

    WITNESSING = "witnessing"
    RETRIEVAL = "retrieval"
    REPARENTING = "reparenting"
    PURGING = "purging"
    INVITATION = "invitation"
    COMPLETE = "complete"


class UnburdeningElement(str, Enum):
    """The elemental medium through which a Burden is released.

    IFS: During the purging stage, the Exile chooses an element to carry
    the burden away. This is a somatic/imaginative ritual — the client
    visualises the burden being consumed by fire, washed away by water,
    blown away by wind, absorbed by earth, or dissolved by light.

    In clinical IFS, the element is traditionally chosen by the Exile,
    not by Self or the facilitator. In simulation, the researcher
    represents the Exile's choice via the API.
    """

    FIRE = "fire"
    WATER = "water"
    WIND = "wind"
    EARTH = "earth"
    LIGHT = "light"


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------


class UnburdeningResult(BaseModel):
    """Result of executing a single step in the unburdening pipeline.

    Parallel to ``SixFsResult``. If ``unblend_required`` is set, the
    caller must unblend that Part before re-attempting the current step.
    This implements the same Self-energy gate used in the 6 Fs.
    """

    step: UnburdeningStep
    exile_id: UUID
    next_step: UnburdeningStep | None = None
    unblend_required: UUID | None = Field(
        default=None,
        description="Part to unblend before proceeding (Self-energy gate)",
    )
    notes: str = ""


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


class UnburdeningStateMachine:
    """Sequential state machine for the Exile unburdening pipeline.

    IFS: Unburdening is the core healing process in IFS. After Protectors
    have stepped back (via the 6 Fs), Self can access the Exile directly.
    The five stages — Witnessing, Retrieval, Reparenting, Purging,
    Invitation — form the ritual that releases the Burden and transforms
    the Exile.

    Each stage gates on ``self_energy > COMPASSION_THRESHOLD``. If a Part
    blends during unburdening (which is common — Protectors often panic
    when Exile material surfaces), the pipeline pauses until the
    interfering Part is unblended.

    The pipeline enforces that all steps target the same Exile — you
    cannot witness one Exile and then retrieve a different one.

    Usage::

        machine = UnburdeningStateMachine(graph, self_system)
        r1 = machine.witness(exile.id)
        r2 = machine.retrieve(exile.id)
        r3 = machine.reparent(exile.id, "I needed someone to say I was safe")
        r4 = machine.purge(exile.id, UnburdeningElement.WATER)
        r5 = machine.invite(exile.id, ["playfulness", "lightness"])
    """

    def __init__(
        self,
        graph: ProtectionGraph,
        self_system: SelfSystem,
    ) -> None:
        self.graph = graph
        self.self_system = self_system
        self._current_step: UnburdeningStep | None = None
        self._target_exile_id: UUID | None = None

    @property
    def current_step(self) -> UnburdeningStep | None:
        """The step currently in progress, if any."""
        return self._current_step

    @property
    def target_exile_id(self) -> UUID | None:
        """The Exile currently being unburdened."""
        return self._target_exile_id

    # -------------------------------------------------------------------
    # Validation helpers
    # -------------------------------------------------------------------

    def _validate_exile_id(self, exile_id: UUID) -> None:
        """Ensure subsequent steps target the same Exile that was witnessed.

        Raises:
            ValueError: If ``exile_id`` does not match the Exile that was
                witnessed at the start of this pipeline.
        """
        if self._target_exile_id is not None and exile_id != self._target_exile_id:
            raise ValueError(
                f"Cannot switch Exile mid-pipeline — "
                f"witnessing targeted {self._target_exile_id}, "
                f"but {exile_id} was passed"
            )

    # -------------------------------------------------------------------
    # Pipeline steps
    # -------------------------------------------------------------------

    def witness(self, exile_id: UUID) -> UnburdeningResult:
        """Stage 1: Witnessing — Self downloads the Exile's memory.

        IFS: Self sits with the Exile and witnesses what happened to it.
        The Exile tells its story — the original wounding event — and Self
        receives it without being overwhelmed. This is the first time the
        Exile has been truly *seen* by someone who can hold the pain.

        The critical requirement is Self-presence: Self must be able to
        hold the Exile's experience with compassion rather than reactivity.
        If ``self_energy`` is below ``COMPASSION_THRESHOLD``, a Protector
        has blended and must be unblended first.

        Computational equivalent: ReadPayload(ExileID) with authentication
        check (Self-energy gate).

        Raises:
            ValueError: If ``exile_id`` is not in the graph.
            ValueError: If the Exile has no burden to witness.
        """
        # Self-energy gate
        if self.self_system.self_energy <= COMPASSION_THRESHOLD:
            interfering = self._identify_most_blended()
            self.self_system.session_log.append(
                LogEntry(
                    event_type="unburdening",
                    description=(
                        f"WITNESSING: Self-energy insufficient "
                        f"({self.self_system.self_energy:.2f} <= {COMPASSION_THRESHOLD})"
                        f" — unblend required"
                    ),
                    part_id=interfering,
                )
            )
            return UnburdeningResult(
                step=UnburdeningStep.WITNESSING,
                exile_id=exile_id,
                next_step=None,
                unblend_required=interfering,
                notes="Self-energy insufficient — another Part is blended",
            )

        # Validate Exile exists in graph
        if exile_id not in self.graph.nodes:
            raise ValueError(f"Exile {exile_id} not in graph")

        part = self.graph.nodes[exile_id]
        if not isinstance(part, Exile):
            raise ValueError(f"Part {exile_id} is not an Exile")

        # Exile must have a burden to witness
        if part.burden is None:
            raise ValueError(
                f"Exile {exile_id} has no burden — nothing to witness"
            )

        self._current_step = UnburdeningStep.WITNESSING
        self._target_exile_id = exile_id

        burden_content = part.burden.content

        self.self_system.session_log.append(
            LogEntry(
                event_type="unburdening",
                description=(
                    f"WITNESSING: Self witnesses Exile's burden: '{burden_content}'"
                ),
                part_id=exile_id,
            )
        )

        return UnburdeningResult(
            step=UnburdeningStep.WITNESSING,
            exile_id=exile_id,
            next_step=UnburdeningStep.RETRIEVAL,
            notes=f"Burden witnessed: '{burden_content}'",
        )

    def retrieve(self, exile_id: UUID) -> UnburdeningResult:
        """Stage 2: Retrieval — move the Exile out of the trauma scene.

        IFS: The Exile is stuck in the original time and place of the
        wounding. Retrieval means going back to that scene, taking the
        young Part by the hand, and bringing it into present safety.
        The Exile is no longer isolated in the past — it is now present
        with Self in the here-and-now.

        After retrieval, the Exile's state moves to ``RETRIEVED`` — this
        is an intentional, therapeutic state (Self brought the Exile
        forward), distinct from ``LEAKING``/``FLOODING`` which are
        pathological breakthrough states.

        Computational equivalent: Extract process from quarantine into
        active memory space.

        Raises:
            ValueError: If ``witness()`` has not been called first.
            ValueError: If ``exile_id`` doesn't match the witnessed Exile.
        """
        # Step order enforcement
        if self._current_step != UnburdeningStep.WITNESSING:
            raise ValueError("Cannot retrieve before witnessing")

        # Exile consistency check (Issue 4)
        self._validate_exile_id(exile_id)

        # Self-energy gate
        if self.self_system.self_energy <= COMPASSION_THRESHOLD:
            interfering = self._identify_most_blended()
            self.self_system.session_log.append(
                LogEntry(
                    event_type="unburdening",
                    description=(
                        f"RETRIEVAL: Self-energy insufficient "
                        f"({self.self_system.self_energy:.2f} <= {COMPASSION_THRESHOLD})"
                        f" — unblend required"
                    ),
                    part_id=interfering,
                )
            )
            return UnburdeningResult(
                step=UnburdeningStep.RETRIEVAL,
                exile_id=exile_id,
                next_step=None,
                unblend_required=interfering,
                notes="Self-energy insufficient — another Part is blended",
            )

        part = self.graph.nodes[exile_id]
        assert isinstance(part, Exile)

        # Move Exile out of isolation into present safety (therapeutic state)
        part.state = ExileState.RETRIEVED

        self._current_step = UnburdeningStep.RETRIEVAL

        self.self_system.session_log.append(
            LogEntry(
                event_type="unburdening",
                description="RETRIEVAL: Exile moved from trauma scene to present safety",
                part_id=exile_id,
            )
        )

        return UnburdeningResult(
            step=UnburdeningStep.RETRIEVAL,
            exile_id=exile_id,
            next_step=UnburdeningStep.REPARENTING,
            notes="Exile retrieved from trauma scene — now accessible",
        )

    def reparent(
        self,
        exile_id: UUID,
        what_was_needed: str,
    ) -> UnburdeningResult:
        """Stage 3: Reparenting — Self gives the Exile what it needed.

        IFS: After retrieval, Self asks the Exile: "What did you need
        back then that you didn't get?" The Exile expresses its unmet
        need — comfort, protection, acknowledgement, safety — and Self
        provides it. This is the relational repair that makes unburdening
        meaningful rather than procedural.

        Only after the Exile has received what it needed does the burden
        become ready to release. Without this step, purging is mechanical.

        Computational equivalent: Provide missing input data to a
        quarantined process before attempting payload deletion.

        Parameters
        ----------
        exile_id:
            UUID of the Exile being reparented.
        what_was_needed:
            What Self provides to the Exile — a description of the
            unmet need being fulfilled (e.g. "I needed someone to tell
            me I was safe", "I needed to be held", "I needed protection").

        Raises:
            ValueError: If ``retrieve()`` has not been called first.
            ValueError: If ``exile_id`` doesn't match the witnessed Exile.
        """
        # Step order enforcement
        if self._current_step != UnburdeningStep.RETRIEVAL:
            raise ValueError("Cannot reparent before retrieval")

        # Exile consistency check
        self._validate_exile_id(exile_id)

        # Self-energy gate
        if self.self_system.self_energy <= COMPASSION_THRESHOLD:
            interfering = self._identify_most_blended()
            self.self_system.session_log.append(
                LogEntry(
                    event_type="unburdening",
                    description=(
                        f"REPARENTING: Self-energy insufficient "
                        f"({self.self_system.self_energy:.2f} <= {COMPASSION_THRESHOLD})"
                        f" — unblend required"
                    ),
                    part_id=interfering,
                )
            )
            return UnburdeningResult(
                step=UnburdeningStep.REPARENTING,
                exile_id=exile_id,
                next_step=None,
                unblend_required=interfering,
                notes="Self-energy insufficient — another Part is blended",
            )

        self._current_step = UnburdeningStep.REPARENTING

        self.self_system.session_log.append(
            LogEntry(
                event_type="unburdening",
                description=(
                    f"REPARENTING: Self provides what the Exile needed: "
                    f"'{what_was_needed}'"
                ),
                part_id=exile_id,
            )
        )

        return UnburdeningResult(
            step=UnburdeningStep.REPARENTING,
            exile_id=exile_id,
            next_step=UnburdeningStep.PURGING,
            notes=f"Reparenting: '{what_was_needed}'",
        )

    def purge(
        self,
        exile_id: UUID,
        element: UnburdeningElement,
    ) -> UnburdeningResult:
        """Stage 4: Purging — the elemental release of the Burden.

        IFS: The Exile chooses an element — fire, water, wind, earth, or
        light — to release the burden. The client visualises the burden
        leaving the Exile's body and being consumed, washed away, blown
        away, absorbed, or dissolved by the chosen element.

        This is the moment of transformation. The burden is not the Exile's
        true nature — it was imposed on the Exile at the time of wounding.
        Purging separates the burden from the Part.

        After purging, ``exile.burden`` is set to ``None`` and
        ``exile.emotional_charge`` is reduced to 0.1 (residual — Parts
        keep their story, they just lose the overwhelming charge).

        Computational equivalent: Delete corrupted data payload; reduce
        activation intensity to residual.

        Raises:
            ValueError: If ``reparent()`` has not been called first.
            ValueError: If ``exile_id`` doesn't match the witnessed Exile.
        """
        # Step order enforcement
        if self._current_step != UnburdeningStep.REPARENTING:
            raise ValueError("Cannot purge before reparenting")

        # Exile consistency check
        self._validate_exile_id(exile_id)

        # Self-energy gate
        if self.self_system.self_energy <= COMPASSION_THRESHOLD:
            interfering = self._identify_most_blended()
            self.self_system.session_log.append(
                LogEntry(
                    event_type="unburdening",
                    description=(
                        f"PURGING: Self-energy insufficient "
                        f"({self.self_system.self_energy:.2f} <= {COMPASSION_THRESHOLD})"
                        f" — unblend required"
                    ),
                    part_id=interfering,
                )
            )
            return UnburdeningResult(
                step=UnburdeningStep.PURGING,
                exile_id=exile_id,
                next_step=None,
                unblend_required=interfering,
                notes="Self-energy insufficient — another Part is blended",
            )

        part = self.graph.nodes[exile_id]
        assert isinstance(part, Exile)

        # Release the burden via the chosen element
        part.burden = None
        part.emotional_charge = 0.1  # Residual — the story remains

        self._current_step = UnburdeningStep.PURGING

        self.self_system.session_log.append(
            LogEntry(
                event_type="unburdening",
                description=(
                    f"PURGING: Burden released via {element.value} — "
                    f"emotional charge reduced to residual"
                ),
                part_id=exile_id,
            )
        )

        return UnburdeningResult(
            step=UnburdeningStep.PURGING,
            exile_id=exile_id,
            next_step=UnburdeningStep.INVITATION,
            notes=f"Burden purged via {element.value}",
        )

    def invite(
        self,
        exile_id: UUID,
        new_qualities: list[str],
    ) -> UnburdeningResult:
        """Stage 5: Invitation — the Exile takes on new qualities.

        IFS: After the burden is released, there is an empty space where
        the burden used to be. The Exile is invited to choose new qualities
        to fill that space — playfulness, lightness, curiosity, safety,
        joy. These qualities are the Exile's *true nature*, which was
        obscured by the burden.

        After invitation, the Exile's state moves to ``UNBURDENED`` — it
        is now a free Part, no longer carrying trauma.

        Computational equivalent: Write new payload (positive qualities)
        to freed memory; transition process state to UNBURDENED.

        Raises:
            ValueError: If ``purge()`` has not been called first.
            ValueError: If ``exile_id`` doesn't match the witnessed Exile.
        """
        # Step order enforcement
        if self._current_step != UnburdeningStep.PURGING:
            raise ValueError("Cannot invite before purging")

        # Exile consistency check
        self._validate_exile_id(exile_id)

        # Self-energy gate
        if self.self_system.self_energy <= COMPASSION_THRESHOLD:
            interfering = self._identify_most_blended()
            self.self_system.session_log.append(
                LogEntry(
                    event_type="unburdening",
                    description=(
                        f"INVITATION: Self-energy insufficient "
                        f"({self.self_system.self_energy:.2f} <= {COMPASSION_THRESHOLD})"
                        f" — unblend required"
                    ),
                    part_id=interfering,
                )
            )
            return UnburdeningResult(
                step=UnburdeningStep.INVITATION,
                exile_id=exile_id,
                next_step=None,
                unblend_required=interfering,
                notes="Self-energy insufficient — another Part is blended",
            )

        part = self.graph.nodes[exile_id]
        assert isinstance(part, Exile)

        # Invite new qualities to fill the space left by the burden
        part.invited_qualities = new_qualities
        part.state = ExileState.UNBURDENED

        self._current_step = UnburdeningStep.COMPLETE

        self.self_system.session_log.append(
            LogEntry(
                event_type="unburdening",
                description=(
                    f"INVITATION: Exile takes on new qualities: "
                    f"{', '.join(new_qualities)}"
                ),
                part_id=exile_id,
            )
        )

        return UnburdeningResult(
            step=UnburdeningStep.INVITATION,
            exile_id=exile_id,
            next_step=None,
            notes=f"Qualities invited: {', '.join(new_qualities)}",
        )

    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------

    def _identify_most_blended(self) -> UUID | None:
        """Find the Part with the highest blending percentage.

        Used by the Self-energy gate to identify which Part has taken
        over the seat of consciousness and must be unblended before
        unburdening can continue.
        """
        if not self.self_system.active_blends:
            return None
        most_blended = max(
            self.self_system.active_blends,
            key=lambda b: b.blending_percentage,
        )
        return most_blended.part_id
