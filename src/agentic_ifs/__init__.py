"""agentic-ifs: Internal Family Systems as multi-agent computational architecture.

This library formalises IFS therapy as a multi-agent system for research,
simulation, and philosophical exploration. It optimises for **internal system
homeostasis**, not external task completion.

**Not clinical software.** Not intended for clinical use, therapy delivery,
or crisis support.

Quick start::

    from agentic_ifs import Session, Manager, Exile

    session = Session()
    session.add_part(Manager(
        narrative="The Perfectionist",
        age=12,
        intent="Keep us safe from criticism",
        triggers=["criticism", "failure"],
        strategies=["over-preparation", "self-criticism"],
    ))
"""

__version__ = "0.2.0"

# --- Parts and enums ---
from .parts import (
    Burden,
    BurdenType,
    Exile,
    ExileState,
    Firefighter,
    FirefighterState,
    IPart,
    Manager,
    ManagerState,
    PartUnion,
)

# --- Self system ---
from .self_system import (
    SELF_QUALITIES,
    BlendState,
    LogEntry,
    SelfEnergyVector,
    SelfSystem,
)

# --- Graph ---
from .graph import Edge, EdgeType, PolarizationEdge, ProtectionGraph

# --- Dynamics ---
from .dynamics import (
    COMPASSION_THRESHOLD,
    detect_polarization,
    is_self_led,
    self_preservation_ratio,
)

# --- Workflow ---
from .workflow import (
    FocusShift,
    SixFsResult,
    SixFsStateMachine,
    SixFsStep,
    Trailhead,
    TrailheadLog,
    TrailheadType,
)

# --- Unburdening (V2) ---
from .unburdening import (
    UnburdeningElement,
    UnburdeningResult,
    UnburdeningStateMachine,
    UnburdeningStep,
)

# --- Modifiers (V2) ---
from .modifiers import FivePs

# --- Somatic (V2) ---
from .somatic import BodyLocation, BodyMap, BodyRegion, BodySide, SomaticMarker

# --- Dialogue (V2) ---
from .dialogue import (
    DialogueContext,
    DialogueMessage,
    DialogueProvider,
    PartDialogue,
    build_part_system_prompt,
)

# --- Session ---
from .session import Session

__all__ = [
    # Parts
    "IPart",
    "Manager",
    "ManagerState",
    "Firefighter",
    "FirefighterState",
    "Exile",
    "ExileState",
    "Burden",
    "BurdenType",
    "PartUnion",
    # Self system
    "SelfSystem",
    "SelfEnergyVector",
    "SELF_QUALITIES",
    "BlendState",
    "LogEntry",
    # Graph
    "ProtectionGraph",
    "Edge",
    "EdgeType",
    "PolarizationEdge",
    # Dynamics
    "COMPASSION_THRESHOLD",
    "self_preservation_ratio",
    "is_self_led",
    "detect_polarization",
    # Workflow
    "SixFsStateMachine",
    "SixFsStep",
    "SixFsResult",
    "Trailhead",
    "TrailheadLog",
    "TrailheadType",
    "FocusShift",
    # Unburdening
    "UnburdeningStep",
    "UnburdeningElement",
    "UnburdeningResult",
    "UnburdeningStateMachine",
    # Modifiers
    "FivePs",
    # Somatic
    "BodyRegion",
    "BodySide",
    "BodyLocation",
    "SomaticMarker",
    "BodyMap",
    # Dialogue
    "DialogueProvider",
    "DialogueContext",
    "DialogueMessage",
    "PartDialogue",
    "build_part_system_prompt",
    # Session
    "Session",
]
