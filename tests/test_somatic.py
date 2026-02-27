"""Tests for agentic_ifs.somatic — BodyMap, somatic markers, and body locations."""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from agentic_ifs.somatic import (
    BodyLocation,
    BodyMap,
    BodyRegion,
    BodySide,
    SomaticMarker,
)


# ---------------------------------------------------------------------------
# Enum tests
# ---------------------------------------------------------------------------


class TestBodyRegion:
    def test_values(self) -> None:
        assert BodyRegion.HEAD == "head"
        assert BodyRegion.THROAT == "throat"
        assert BodyRegion.CHEST == "chest"
        assert BodyRegion.STOMACH == "stomach"
        assert BodyRegion.PELVIS == "pelvis"
        assert BodyRegion.LIMBS == "limbs"
        assert BodyRegion.BACK == "back"

    def test_count(self) -> None:
        assert len(BodyRegion) == 7


class TestBodySide:
    def test_values(self) -> None:
        assert BodySide.LEFT == "left"
        assert BodySide.CENTER == "center"
        assert BodySide.RIGHT == "right"

    def test_count(self) -> None:
        assert len(BodySide) == 3


# ---------------------------------------------------------------------------
# BodyLocation tests
# ---------------------------------------------------------------------------


class TestBodyLocation:
    def test_creation_with_defaults(self) -> None:
        loc = BodyLocation(region=BodyRegion.CHEST)
        assert loc.region == BodyRegion.CHEST
        assert loc.side == BodySide.CENTER
        assert loc.description == ""

    def test_creation_with_explicit_values(self) -> None:
        loc = BodyLocation(
            region=BodyRegion.HEAD,
            side=BodySide.RIGHT,
            description="Behind the right eye",
        )
        assert loc.region == BodyRegion.HEAD
        assert loc.side == BodySide.RIGHT
        assert loc.description == "Behind the right eye"

    def test_all_regions_accepted(self) -> None:
        for region in BodyRegion:
            loc = BodyLocation(region=region)
            assert loc.region == region

    def test_all_sides_accepted(self) -> None:
        for side in BodySide:
            loc = BodyLocation(region=BodyRegion.CHEST, side=side)
            assert loc.side == side


# ---------------------------------------------------------------------------
# SomaticMarker tests
# ---------------------------------------------------------------------------


class TestSomaticMarker:
    def test_creation(self) -> None:
        part_id = uuid4()
        marker = SomaticMarker(
            part_id=part_id,
            location=BodyLocation(region=BodyRegion.CHEST, side=BodySide.LEFT),
            sensation_quality="tightness",
            intensity=0.7,
        )
        assert isinstance(marker.id, UUID)
        assert marker.part_id == part_id
        assert marker.location.region == BodyRegion.CHEST
        assert marker.location.side == BodySide.LEFT
        assert marker.sensation_quality == "tightness"
        assert marker.intensity == 0.7

    def test_auto_generated_id(self) -> None:
        m1 = SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.STOMACH),
            sensation_quality="knot",
            intensity=0.5,
        )
        m2 = SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.STOMACH),
            sensation_quality="knot",
            intensity=0.5,
        )
        assert m1.id != m2.id

    def test_intensity_lower_bound(self) -> None:
        marker = SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.LIMBS),
            sensation_quality="tingling",
            intensity=0.0,
        )
        assert marker.intensity == 0.0

    def test_intensity_upper_bound(self) -> None:
        marker = SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.LIMBS),
            sensation_quality="burning",
            intensity=1.0,
        )
        assert marker.intensity == 1.0

    def test_intensity_below_zero_rejected(self) -> None:
        with pytest.raises(ValidationError):
            SomaticMarker(
                part_id=uuid4(),
                location=BodyLocation(region=BodyRegion.CHEST),
                sensation_quality="ache",
                intensity=-0.1,
            )

    def test_intensity_above_one_rejected(self) -> None:
        with pytest.raises(ValidationError):
            SomaticMarker(
                part_id=uuid4(),
                location=BodyLocation(region=BodyRegion.CHEST),
                sensation_quality="ache",
                intensity=1.1,
            )

    def test_round_trip_serialisation(self) -> None:
        marker = SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(
                region=BodyRegion.THROAT,
                side=BodySide.CENTER,
                description="Lump in the throat",
            ),
            sensation_quality="constriction",
            intensity=0.6,
        )
        json_str = marker.model_dump_json()
        restored = SomaticMarker.model_validate_json(json_str)
        assert restored.id == marker.id
        assert restored.part_id == marker.part_id
        assert restored.location.region == BodyRegion.THROAT
        assert restored.sensation_quality == "constriction"
        assert restored.intensity == 0.6


# ---------------------------------------------------------------------------
# BodyMap tests
# ---------------------------------------------------------------------------


class TestBodyMapAdd:
    def test_add_single_marker(self) -> None:
        body_map = BodyMap()
        marker = SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.5,
        )
        body_map.add(marker)
        assert len(body_map.markers) == 1
        assert body_map.markers[0] is marker

    def test_add_multiple_markers(self) -> None:
        body_map = BodyMap()
        for i in range(5):
            body_map.add(SomaticMarker(
                part_id=uuid4(),
                location=BodyLocation(region=BodyRegion.CHEST),
                sensation_quality=f"sensation-{i}",
                intensity=i * 0.2,
            ))
        assert len(body_map.markers) == 5


class TestBodyMapGetByPart:
    def test_single_marker_for_part(self) -> None:
        body_map = BodyMap()
        target_part = uuid4()
        other_part = uuid4()

        body_map.add(SomaticMarker(
            part_id=target_part,
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.7,
        ))
        body_map.add(SomaticMarker(
            part_id=other_part,
            location=BodyLocation(region=BodyRegion.STOMACH),
            sensation_quality="knot",
            intensity=0.4,
        ))

        results = body_map.get_by_part(target_part)
        assert len(results) == 1
        assert results[0].part_id == target_part
        assert results[0].sensation_quality == "tightness"

    def test_multiple_markers_for_same_part(self) -> None:
        body_map = BodyMap()
        part_id = uuid4()

        body_map.add(SomaticMarker(
            part_id=part_id,
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.7,
        ))
        body_map.add(SomaticMarker(
            part_id=part_id,
            location=BodyLocation(region=BodyRegion.BACK, side=BodySide.RIGHT),
            sensation_quality="tension",
            intensity=0.5,
        ))

        results = body_map.get_by_part(part_id)
        assert len(results) == 2
        qualities = {m.sensation_quality for m in results}
        assert qualities == {"tightness", "tension"}

    def test_no_markers_for_part(self) -> None:
        body_map = BodyMap()
        body_map.add(SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.HEAD),
            sensation_quality="pressure",
            intensity=0.3,
        ))

        results = body_map.get_by_part(uuid4())
        assert results == []

    def test_empty_map_returns_empty(self) -> None:
        body_map = BodyMap()
        results = body_map.get_by_part(uuid4())
        assert results == []


class TestBodyMapGetByRegion:
    def test_single_region(self) -> None:
        body_map = BodyMap()
        body_map.add(SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.6,
        ))
        body_map.add(SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.STOMACH),
            sensation_quality="knot",
            intensity=0.4,
        ))

        results = body_map.get_by_region(BodyRegion.CHEST)
        assert len(results) == 1
        assert results[0].location.region == BodyRegion.CHEST

    def test_multiple_markers_in_region(self) -> None:
        body_map = BodyMap()
        body_map.add(SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.CHEST, side=BodySide.LEFT),
            sensation_quality="tightness",
            intensity=0.7,
        ))
        body_map.add(SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.CHEST, side=BodySide.RIGHT),
            sensation_quality="warmth",
            intensity=0.3,
        ))

        results = body_map.get_by_region(BodyRegion.CHEST)
        assert len(results) == 2

    def test_no_markers_in_region(self) -> None:
        body_map = BodyMap()
        body_map.add(SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.5,
        ))

        results = body_map.get_by_region(BodyRegion.PELVIS)
        assert results == []

    def test_empty_map_returns_empty(self) -> None:
        body_map = BodyMap()
        results = body_map.get_by_region(BodyRegion.HEAD)
        assert results == []


class TestBodyMapRemovePartMarkers:
    def test_remove_single_marker(self) -> None:
        body_map = BodyMap()
        part_id = uuid4()
        other_part = uuid4()

        body_map.add(SomaticMarker(
            part_id=part_id,
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.7,
        ))
        body_map.add(SomaticMarker(
            part_id=other_part,
            location=BodyLocation(region=BodyRegion.STOMACH),
            sensation_quality="knot",
            intensity=0.4,
        ))

        body_map.remove_part_markers(part_id)
        assert len(body_map.markers) == 1
        assert body_map.markers[0].part_id == other_part

    def test_remove_multiple_markers_for_part(self) -> None:
        body_map = BodyMap()
        part_id = uuid4()

        body_map.add(SomaticMarker(
            part_id=part_id,
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.7,
        ))
        body_map.add(SomaticMarker(
            part_id=part_id,
            location=BodyLocation(region=BodyRegion.BACK),
            sensation_quality="tension",
            intensity=0.5,
        ))
        body_map.add(SomaticMarker(
            part_id=uuid4(),
            location=BodyLocation(region=BodyRegion.HEAD),
            sensation_quality="pressure",
            intensity=0.3,
        ))

        body_map.remove_part_markers(part_id)
        assert len(body_map.markers) == 1
        assert body_map.markers[0].sensation_quality == "pressure"

    def test_remove_nonexistent_part_is_noop(self) -> None:
        body_map = BodyMap()
        existing_part = uuid4()
        body_map.add(SomaticMarker(
            part_id=existing_part,
            location=BodyLocation(region=BodyRegion.CHEST),
            sensation_quality="tightness",
            intensity=0.5,
        ))

        body_map.remove_part_markers(uuid4())
        assert len(body_map.markers) == 1

    def test_remove_from_empty_map_is_noop(self) -> None:
        body_map = BodyMap()
        body_map.remove_part_markers(uuid4())
        assert len(body_map.markers) == 0


class TestBodyMapSerialisation:
    """Test that the BodyMap round-trips through JSON correctly."""

    def test_round_trip(self) -> None:
        part_id = uuid4()
        body_map = BodyMap()
        body_map.add(SomaticMarker(
            part_id=part_id,
            location=BodyLocation(
                region=BodyRegion.CHEST,
                side=BodySide.LEFT,
                description="Upper left chest near heart",
            ),
            sensation_quality="tightness",
            intensity=0.8,
        ))
        body_map.add(SomaticMarker(
            part_id=part_id,
            location=BodyLocation(region=BodyRegion.THROAT),
            sensation_quality="constriction",
            intensity=0.4,
        ))

        json_str = body_map.model_dump_json()
        restored = BodyMap.model_validate_json(json_str)

        assert len(restored.markers) == 2
        assert restored.markers[0].part_id == part_id
        assert restored.markers[0].location.region == BodyRegion.CHEST
        assert restored.markers[0].location.side == BodySide.LEFT
        assert restored.markers[0].sensation_quality == "tightness"
        assert restored.markers[1].location.region == BodyRegion.THROAT

    def test_empty_map_round_trip(self) -> None:
        body_map = BodyMap()
        json_str = body_map.model_dump_json()
        restored = BodyMap.model_validate_json(json_str)
        assert restored.markers == []


class TestBodyMapIntegrationWithParts:
    """Test BodyMap with Part fixtures from conftest."""

    def test_map_markers_to_real_parts(self, manager, exile) -> None:
        body_map = BodyMap()

        body_map.add(SomaticMarker(
            part_id=manager.id,
            location=BodyLocation(
                region=BodyRegion.HEAD,
                side=BodySide.CENTER,
                description="Pressure behind the forehead",
            ),
            sensation_quality="pressure",
            intensity=0.6,
        ))
        body_map.add(SomaticMarker(
            part_id=exile.id,
            location=BodyLocation(
                region=BodyRegion.STOMACH,
                description="Deep knot in the gut",
            ),
            sensation_quality="heaviness",
            intensity=0.9,
        ))

        manager_markers = body_map.get_by_part(manager.id)
        assert len(manager_markers) == 1
        assert manager_markers[0].sensation_quality == "pressure"

        exile_markers = body_map.get_by_part(exile.id)
        assert len(exile_markers) == 1
        assert exile_markers[0].sensation_quality == "heaviness"

    def test_remove_unburdened_part(self, exile) -> None:
        """IFS: when an Exile unburdens, its somatic markers dissolve."""
        body_map = BodyMap()

        body_map.add(SomaticMarker(
            part_id=exile.id,
            location=BodyLocation(region=BodyRegion.STOMACH),
            sensation_quality="heaviness",
            intensity=0.9,
        ))
        body_map.add(SomaticMarker(
            part_id=exile.id,
            location=BodyLocation(region=BodyRegion.CHEST, side=BodySide.LEFT),
            sensation_quality="ache",
            intensity=0.7,
        ))
        assert len(body_map.get_by_part(exile.id)) == 2

        body_map.remove_part_markers(exile.id)
        assert body_map.get_by_part(exile.id) == []
        assert len(body_map.markers) == 0
