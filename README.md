# agentic-ifs

**Internal Family Systems as multi-agent computational architecture.**

`agentic-ifs` is a Python library that formalises the [Internal Family Systems (IFS)](https://ifs-institute.com) therapeutic model as a software architecture.

IFS treats the mind as a system of discrete sub-personalities ("Parts") governed by a core, undamaged essence ("Self"). This library provides rigorous data structures, state machines, and simulation primitives for researchers and builders working at the psychology/AI intersection.

---

## The Central Insight

Unlike standard multi-agent frameworks, `agentic-ifs` optimises for **internal system homeostasis**, not external task completion.

Parts are not tools calling APIs. They are agents with protective intentions, emotional charges, and relationships to each other and to Self.

**Self is not an agent.** Self is the system's operating environment — a global attractor state.

---

## Installation

```bash
pip install agentic-ifs
```

For development:

```bash
git clone https://github.com/joejarlett/agentic-ifs.git
cd agentic-ifs
pip install -e ".[dev]"
```

Requires Python 3.11+.

---

## Quick Start

### Create Parts and model a system

```python
from agentic_ifs import (
    Session, Manager, Firefighter, Exile,
    Edge, EdgeType, Trailhead, TrailheadType,
)

# Create a session (default self_energy=0.3 — typical session start)
session = Session(initial_self_energy=0.8)

# Define Parts
perfectionist = Manager(
    narrative="The Perfectionist — formed at age 12 after public failure",
    age=12,
    intent="Keep us safe from criticism",
    triggers=["criticism", "failure"],
    strategies=["over-preparation", "self-criticism"],
    rigidity=0.7,
)

numbing = Firefighter(
    narrative="The Numb-er — activates when shame overwhelms",
    age=14,
    intent="Stop the pain when it overflows",
    pain_threshold=0.6,
    extinguishing_behaviors=["dissociation", "scrolling"],
)

wounded_child = Exile(
    narrative="Wounded Child — carries shame from school failure",
    age=7,
    intent="Hold the pain so the system can function",
    emotional_charge=0.7,
)

# Add Parts to the system
session.add_part(perfectionist)
session.add_part(numbing)
session.add_part(wounded_child)

# Model relationships
session.add_edge(Edge(
    source_id=perfectionist.id,
    target_id=wounded_child.id,
    edge_type=EdgeType.PROTECTS,
))
session.add_edge(Edge(
    source_id=numbing.id,
    target_id=wounded_child.id,
    edge_type=EdgeType.PROTECTS,
))
```

### Run the 6 Fs workflow

The 6 Fs is the standard IFS algorithm for engaging with Protectors:

```python
# Step 1: Find — locate a Part via a trailhead (entry signal)
trailhead = Trailhead(
    trailhead_type=TrailheadType.SOMATIC,
    intensity=0.6,
    description="Tightness in chest before presentation",
    associated_part_id=perfectionist.id,
)
result = session.find(trailhead)
print(result.next_step)  # SixFsStep.FOCUS

# Step 2-6: Walk through the engagement
result = session.focus(perfectionist.id)
result = session.flesh_out(perfectionist.id)
result = session.feel_toward(perfectionist.id)

if result.unblend_required:
    # Another Part has blended — unblend it first
    session.unblend(result.unblend_required)
    result = session.feel_toward(perfectionist.id)

result = session.befriend(perfectionist.id)   # Trust increases
result = session.fear(perfectionist.id)        # 6 Fs complete
```

### Check system metrics

```python
# Is Self currently leading the system?
print(session.is_self_led)            # True (self_energy > 0.5)

# Self-preservation ratio (Self-energy vs total Part activation)
print(session.preservation_ratio)

# Export the Parts Map for visualisation (D3.js, Gephi, Cytoscape)
import json
parts_map = session.export_parts_map()
print(json.dumps(parts_map, indent=2))
```

### Use blending mechanics

```python
from agentic_ifs import BlendState

# A Part blends — Self-energy drops
session.blend(BlendState(
    part_id=perfectionist.id,
    blending_percentage=0.7,
))
print(session.self_system.self_energy)  # 0.3 (1.0 * (1 - 0.7))
print(session.is_self_led)              # False

# Unblend — Self-energy recovers
session.unblend(perfectionist.id)
print(session.self_system.self_energy)  # 1.0
```

### Composable core (advanced)

The `Session` facade is optional. You can use the components directly:

```python
from agentic_ifs import (
    ProtectionGraph, SelfSystem, TrailheadLog,
    SixFsStateMachine, is_self_led, self_preservation_ratio,
)

graph = ProtectionGraph()
self_system = SelfSystem(self_energy=0.5)
log = TrailheadLog()
workflow = SixFsStateMachine(graph=graph, self_system=self_system, log=log)

# Full control over each component
```

---

## API Overview

### Part Classes

| Class | IFS Role | Computational Equivalent |
|---|---|---|
| `Manager` | Proactive protector | Daemon / BackgroundService |
| `Firefighter` | Reactive protector | ExceptionHandler / EmergencyOverride |
| `Exile` | Burdened vulnerability | EncryptedDataBlob / QuarantinedProcess |

All Parts inherit from `IPart` and use a `part_type` discriminator for correct Pydantic v2 serialisation.

### Core Components

| Module | Key Classes | Purpose |
|---|---|---|
| `parts` | `Manager`, `Firefighter`, `Exile`, `Burden` | Part data models and state enums |
| `self_system` | `SelfSystem`, `BlendState` | Self-energy, blending/unblending |
| `graph` | `ProtectionGraph`, `Edge`, `PolarizationEdge` | Relationship graph and Parts Map export |
| `dynamics` | `is_self_led()`, `self_preservation_ratio()` | System health metrics |
| `workflow` | `SixFsStateMachine`, `Trailhead`, `FocusShift` | 6 Fs game loop, session entry points |
| `session` | `Session` | Thin convenience facade |

---

## V1 Scope — "Stabilization Release"

V1 focuses on **Protector work** (Managers and Firefighters). Exile unburdening is V2.

**V1 includes:** Part classes with full data structures, Self-energy scalar, Protection graph, 6 Fs state machine, blending mechanics, trailhead logging, Parts Map JSON export, U-Turn as FocusShift.

**Deferred to V2:** Unburdening pipeline, 8C Self-energy vector, LLM simulation of Part dialogue, auto-detect polarization, Direct Access mode, 3D Parts Map rendering.

See [spec/IFSKit-Spec.md](spec/IFSKit-Spec.md) for the full architectural specification.

---

## Not Clinical Software

This library is for research, simulation, and philosophical exploration. It is not intended for clinical use, therapy delivery, or crisis support.

---

## Author

[Joe Jarlett](https://joejarlett.co.uk) — Bristol-based AI engineer and MSc psychologist.

## Theoretical Predecessor

[Kaj Sotala](https://www.lesswrong.com/users/kaj_sotala) mapped IFS to multi-agent reinforcement learning and AI alignment theory (Shard Theory). `agentic-ifs` is the software implementation of that theoretical work.

---

## Licence

MIT
