"""Shared fixtures for agentic-ifs test suite."""

from __future__ import annotations

from datetime import timedelta

import pytest

from agentic_ifs import (
    Burden,
    BurdenType,
    Edge,
    EdgeType,
    Exile,
    Firefighter,
    Manager,
    PolarizationEdge,
    ProtectionGraph,
    SelfSystem,
    Trailhead,
    TrailheadLog,
    TrailheadType,
)


@pytest.fixture
def manager() -> Manager:
    """A sample Manager (Inner Critic)."""
    return Manager(
        narrative="The Inner Critic — formed at age 12 after school failure",
        age=12,
        intent="Keep us safe from criticism by being perfect first",
        triggers=["criticism from authority", "perceived failure"],
        strategies=["perfectionism", "over-preparation", "self-criticism"],
        rigidity=0.8,
    )


@pytest.fixture
def firefighter() -> Firefighter:
    """A sample Firefighter (Procrastinator)."""
    return Firefighter(
        narrative="The Procrastinator — shuts down when pressure is too high",
        age=14,
        intent="Protect from overwhelm by stopping all effort",
        pain_threshold=0.6,
        extinguishing_behaviors=["avoidance", "distraction", "numbing"],
        refractory_period=timedelta(hours=2),
    )


@pytest.fixture
def exile() -> Exile:
    """A sample Exile (Wounded Child)."""
    return Exile(
        narrative="The Wounded Child — carries shame from early school failure",
        age=7,
        intent="Hold the pain so the system can function",
        burden=Burden(
            burden_type=BurdenType.PERSONAL,
            origin="Age 7, school failure",
            content="I am not enough",
            emotional_charge=0.9,
        ),
        emotional_charge=0.7,
    )


@pytest.fixture
def self_system() -> SelfSystem:
    """A fresh SelfSystem at typical session defaults."""
    return SelfSystem()


@pytest.fixture
def populated_graph(manager: Manager, firefighter: Firefighter, exile: Exile) -> ProtectionGraph:
    """A ProtectionGraph with all three Part types and edges."""
    graph = ProtectionGraph()
    graph.add_part(manager)
    graph.add_part(firefighter)
    graph.add_part(exile)

    # Manager protects Exile
    graph.add_edge(Edge(
        source_id=manager.id,
        target_id=exile.id,
        edge_type=EdgeType.PROTECTS,
    ))

    # Firefighter protects Exile
    graph.add_edge(Edge(
        source_id=firefighter.id,
        target_id=exile.id,
        edge_type=EdgeType.PROTECTS,
    ))

    # Manager and Firefighter are polarized
    graph.add_polarization(PolarizationEdge(
        part_a_id=manager.id,
        part_b_id=firefighter.id,
        tension_level=0.7,
    ))

    return graph


@pytest.fixture
def trailhead_log() -> TrailheadLog:
    """An empty TrailheadLog."""
    return TrailheadLog()


@pytest.fixture
def sample_trailhead(exile: Exile) -> Trailhead:
    """A sample somatic trailhead."""
    return Trailhead(
        trailhead_type=TrailheadType.SOMATIC,
        intensity=0.6,
        description="Tightness in chest when boss gives feedback",
        associated_part_id=exile.id,
    )
