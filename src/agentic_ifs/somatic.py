"""Somatic BodyMap — mapping IFS Parts to body locations.

IFS therapy frequently uses somatic awareness as an entry point for
Parts work. Parts manifest as body sensations — tightness in the chest,
a knot in the stomach, heat in the face, heaviness in the limbs. These
felt-sense locations are called **somatic markers** or **trailheads**.

When a therapist asks "Where do you feel that in your body?", they are
asking the client to identify a SomaticMarker. The BodyMap collects all
known markers, enabling the system to track which Parts live where in
the body.

This is a V2 module. V1 logged somatic trailheads as free text; V2
formalises the body as a structured coordinate space.

Computational mapping:
    - BodyRegion / BodySide: discrete spatial coordinates
    - SomaticMarker: a (Part, Location, Quality, Intensity) tuple
    - BodyMap: indexed collection of SomaticMarkers
"""

from __future__ import annotations

from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Spatial enums
# ---------------------------------------------------------------------------


class BodyRegion(str, Enum):
    """Major body region where a Part's sensation is felt.

    IFS: Therapists work with broad anatomical zones, not precise
    coordinates. These regions cover the most commonly reported
    somatic locations in Parts work.

    HEAD includes face, scalp, and jaw. THROAT covers the neck and
    vocal area. CHEST is the ribcage and heart space. STOMACH is the
    abdominal area. PELVIS is the lower abdomen and hips. LIMBS covers
    arms, hands, legs, and feet. BACK spans the full posterior torso.
    """

    HEAD = "head"
    THROAT = "throat"
    CHEST = "chest"
    STOMACH = "stomach"
    PELVIS = "pelvis"
    LIMBS = "limbs"
    BACK = "back"


class BodySide(str, Enum):
    """Lateral position of the sensation.

    IFS: Some Parts are felt distinctly on one side of the body.
    A protective Part might create tension on the left side of the
    chest, while another manifests on the right shoulder. CENTER
    is the default for midline sensations.
    """

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


# ---------------------------------------------------------------------------
# Location and marker models
# ---------------------------------------------------------------------------


class BodyLocation(BaseModel):
    """A specific location in the body where a Part is felt.

    IFS: "Where do you feel that in your body?" is one of the most
    important questions in IFS therapy. The answer — "a tightness in
    my upper left chest" — gives a BodyLocation with region, side,
    and free-text description.

    The ``description`` field allows natural-language detail beyond
    the structured region/side coordinates (e.g. "just below the
    sternum", "behind the right eye").
    """

    region: BodyRegion
    side: BodySide = Field(
        default=BodySide.CENTER,
        description="Lateral position (defaults to CENTER for midline sensations)",
    )
    description: str = Field(
        default="",
        description="Free-text detail, e.g. 'upper left chest', 'behind the right eye'",
    )


class SomaticMarker(BaseModel):
    """A Part's felt-sense presence in the body.

    IFS: A somatic marker is the bridge between cognitive understanding
    of a Part and embodied experience of it. When a client can locate
    a Part in the body and describe its quality ("it feels like a
    heavy stone in my stomach"), the therapeutic work deepens
    significantly.

    ``sensation_quality`` captures the felt-sense texture — words like
    "tightness", "heat", "heaviness", "buzzing", "hollowness", "ache".
    ``intensity`` is the strength of the sensation on a 0.0 to 1.0
    scale, where 0.0 is imperceptible and 1.0 is overwhelming.
    """

    id: UUID = Field(default_factory=uuid4)
    part_id: UUID = Field(
        description="The Part this somatic sensation belongs to",
    )
    location: BodyLocation
    sensation_quality: str = Field(
        description="Felt-sense texture, e.g. 'tightness', 'heat', 'heaviness'",
    )
    intensity: float = Field(
        ge=0.0,
        le=1.0,
        description="Strength of sensation (0.0 imperceptible – 1.0 overwhelming)",
    )


# ---------------------------------------------------------------------------
# BodyMap collection
# ---------------------------------------------------------------------------


class BodyMap(BaseModel):
    """Collection of all somatic markers in the internal system.

    IFS: The body map is a holistic picture of where Parts live in
    the body. In a session, a therapist might build this map
    incrementally — first noticing tightness in the chest (a Manager),
    then heaviness in the stomach (an Exile), then heat in the face
    (a Firefighter). The BodyMap holds all these markers and supports
    querying by Part or by body region.

    Computational equivalent: an indexed collection with filtered views
    over a flat list of SomaticMarker entries.
    """

    markers: list[SomaticMarker] = Field(default_factory=list)

    def add(self, marker: SomaticMarker) -> None:
        """Append a somatic marker to the map.

        IFS: A new body sensation has been noticed and associated
        with a Part. This is often the first step in establishing
        a relationship with a Part — "I notice a tightness in my
        chest, and it belongs to the Critic."
        """
        self.markers.append(marker)

    def get_by_part(self, part_id: UUID) -> list[SomaticMarker]:
        """Return all somatic markers belonging to a specific Part.

        IFS: A single Part may be felt in multiple body locations.
        The Inner Critic might create tension in the jaw *and*
        tightness in the shoulders. This method collects all of
        a Part's somatic footprint.
        """
        return [m for m in self.markers if m.part_id == part_id]

    def get_by_region(self, region: BodyRegion) -> list[SomaticMarker]:
        """Return all somatic markers in a given body region.

        IFS: "What else do you notice in your chest?" — this query
        surfaces all Parts that are somatically present in a region,
        regardless of which Part they belong to.
        """
        return [m for m in self.markers if m.location.region == region]

    def remove_part_markers(self, part_id: UUID) -> None:
        """Remove all somatic markers for a given Part.

        IFS: When a Part unburdens, its somatic signature often
        dissolves — the tightness releases, the heaviness lifts.
        This method clears all body-level traces of the Part.
        """
        self.markers = [m for m in self.markers if m.part_id != part_id]
