"""Tests for agentic_ifs.modifiers — FivePs interaction modifiers."""

from __future__ import annotations

import pytest

from agentic_ifs.modifiers import FivePs


class TestFivePsDefaults:
    def test_default_values(self) -> None:
        ps = FivePs()
        assert ps.presence == 0.5
        assert ps.patience == 0.5
        assert ps.perspective == 0.5
        assert ps.persistence == 0.5
        assert ps.playfulness == 0.5

    def test_custom_values(self) -> None:
        ps = FivePs(presence=0.9, patience=0.1, persistence=0.8)
        assert ps.presence == 0.9
        assert ps.patience == 0.1
        assert ps.persistence == 0.8

    def test_validation_bounds(self) -> None:
        with pytest.raises(Exception):
            FivePs(presence=1.5)
        with pytest.raises(Exception):
            FivePs(patience=-0.1)


class TestEffectiveThreshold:
    def test_zero_patience_no_change(self) -> None:
        ps = FivePs(patience=0.0)
        assert ps.effective_threshold(0.5) == pytest.approx(0.5)

    def test_max_patience_reduces_by_30_percent(self) -> None:
        ps = FivePs(patience=1.0)
        assert ps.effective_threshold(0.5) == pytest.approx(0.35)

    def test_half_patience(self) -> None:
        ps = FivePs(patience=0.5)
        # 0.5 * (1 - 0.5 * 0.3) = 0.5 * 0.85 = 0.425
        assert ps.effective_threshold(0.5) == pytest.approx(0.425)


class TestEffectiveSelfEnergy:
    def test_zero_presence_no_change(self) -> None:
        ps = FivePs(presence=0.0)
        assert ps.effective_self_energy(0.5) == pytest.approx(0.5)

    def test_max_presence_boosts_by_20_percent(self) -> None:
        ps = FivePs(presence=1.0)
        assert ps.effective_self_energy(0.5) == pytest.approx(0.6)

    def test_capped_at_one(self) -> None:
        ps = FivePs(presence=1.0)
        assert ps.effective_self_energy(0.95) == pytest.approx(1.0)


class TestTrustIncrement:
    def test_zero_persistence_halves_increment(self) -> None:
        ps = FivePs(persistence=0.0, playfulness=0.0)
        assert ps.trust_increment(0.1) == pytest.approx(0.05)

    def test_max_persistence_scales_up(self) -> None:
        ps = FivePs(persistence=1.0, playfulness=0.0)
        assert ps.trust_increment(0.1) == pytest.approx(0.15)

    def test_default_persistence(self) -> None:
        ps = FivePs(persistence=0.5, playfulness=0.0)
        # 0.1 * (0.5 + 0.5) = 0.1
        assert ps.trust_increment(0.1) == pytest.approx(0.1)

    def test_never_zero(self) -> None:
        ps = FivePs(persistence=0.0, playfulness=0.0)
        assert ps.trust_increment(0.0) >= 0.01

    def test_playfulness_adds_variance(self) -> None:
        ps = FivePs(persistence=0.5, playfulness=1.0)
        results = {ps.trust_increment(0.1) for _ in range(50)}
        # With playfulness=1.0, should get some variance
        assert len(results) > 1
