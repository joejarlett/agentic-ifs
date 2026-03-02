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

```python
from agentic_ifs import Session, Manager, Firefighter, Exile, Edge, EdgeType

session = Session(initial_self_energy=0.8)

# Define Parts
perfectionist = Manager(
    narrative="The Perfectionist — formed at age 12 after public failure",
    age=12,
    intent="Keep us safe from criticism",
    triggers=["criticism", "failure"],
    strategies=["over-preparation", "self-criticism"],
)

wounded_child = Exile(
    narrative="Wounded Child — carries shame from school failure",
    age=7,
    intent="Hold the pain so the system can function",
    emotional_charge=0.7,
)

# Add Parts and model relationships
session.add_part(perfectionist)
session.add_part(wounded_child)
session.add_edge(Edge(
    source_id=perfectionist.id,
    target_id=wounded_child.id,
    edge_type=EdgeType.PROTECTS,
))

# Run the 6 Fs workflow (Protector engagement)
from agentic_ifs import Trailhead, TrailheadType

trailhead = Trailhead(
    trailhead_type=TrailheadType.SOMATIC,
    intensity=0.6,
    description="Tightness in chest before presentation",
    associated_part_id=perfectionist.id,
)
result = session.find(trailhead)
result = session.focus(perfectionist.id)
result = session.flesh_out(perfectionist.id)
result = session.feel_toward(perfectionist.id)
result = session.befriend(perfectionist.id)
result = session.fear(perfectionist.id)

# Check system state
print(session.is_self_led)        # True
print(session.preservation_ratio) # Self-energy vs Part activation
```

See the [notebooks](#notebooks) for the full API walkthrough.

---

## Notebooks

Interactive walkthroughs rendered on GitHub — no setup required to read:

| Notebook | Topic |
|---|---|
| [01 — Parts and System](notebooks/01_parts_and_system.ipynb) | Creating Parts, modelling an internal system |
| [02 — Protection Graph](notebooks/02_protection_graph.ipynb) | Relationships, edges, Parts Map export |
| [03 — Six Fs Workflow](notebooks/03_six_fs_workflow.ipynb) | The 6 Fs state machine (Protector engagement) |
| [04 — Blending Dynamics](notebooks/04_blending_dynamics.ipynb) | Blending, unblending, Self-energy mechanics |
| [05 — Full Scenario](notebooks/05_full_scenario.ipynb) | End-to-end simulation with visualisation |
| [06 — LLM Dialogue](notebooks/06_dialogue.ipynb) | Making Parts speak with Gemini/Claude |
| [07 — Unburdening](notebooks/07_unburdening.ipynb) | The healing pipeline (Exile unburdening) |

---

## Architecture

### Part Classes

| Class | IFS Role | Computational Equivalent |
|---|---|---|
| `Manager` | Proactive protector | Daemon / BackgroundService |
| `Firefighter` | Reactive protector | ExceptionHandler / EmergencyOverride |
| `Exile` | Burdened vulnerability | EncryptedDataBlob / QuarantinedProcess |

### Core Components

| Module | Key Classes | Purpose |
|---|---|---|
| `parts` | `Manager`, `Firefighter`, `Exile`, `Burden` | Part data models, state enums, lineage |
| `self_system` | `SelfSystem`, `SelfEnergyVector`, `BlendState` | 8C Self-energy vector, blending/unblending |
| `graph` | `ProtectionGraph`, `Edge`, `PolarizationEdge` | Relationship graph and Parts Map export |
| `dynamics` | `is_self_led()`, `self_preservation_ratio()` | System health metrics, polarization detection |
| `workflow` | `SixFsStateMachine`, `Trailhead`, `FocusShift` | 6 Fs game loop, session entry points |
| `unburdening` | `UnburdeningStateMachine` | Exile healing pipeline |
| `dialogue` | `DialogueProvider`, `PartDialogue` | LLM Part dialogue (provider-agnostic) |
| `session` | `Session` | Convenience facade wiring all components |

---

## Releases

### V2 — "Healer Release" (current)

Adds the **healing pipeline** and **LLM Part dialogue**: unburdening state machine (Witnessing → Retrieval → Reparenting → Purging → Invitation), 8C Self-energy vector, 5 Ps interaction modifiers, auto-detect polarization, somatic body map, legacy burden lineage, Direct Access mode, and framework-agnostic LLM dialogue with optional Gemini and Anthropic integrations.

### V1 — "Stabilization Release"

**Protector work** foundation: Part classes, Self-energy scalar, Protection graph, 6 Fs state machine, blending mechanics, trailhead logging, Parts Map JSON export, Session facade.

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
