# agentic-ifs — Claude Instructions

## What This Project Is

`agentic-ifs` is an open-source Python library that formalises **Internal Family Systems (IFS)** therapy as a **multi-agent computational architecture**.

IFS, developed by Richard Schwartz, treats the mind as a system of discrete sub-personalities ("Parts") governed by a core, undamaged essence ("Self"). This library provides rigorous data structures and simulation primitives for researchers and builders working at the psychology/AI intersection.

**This is not clinical software.** It is a research, simulation, and philosophical exploration tool. It is not intended for clinical use, therapy delivery, or crisis support.

**PyPI package name:** `agentic-ifs`
**GitHub:** github.com/joejarlett/agentic-ifs

---

## About the Author

**Joe Jarlett** — Bristol-based AI engineer and MSc psychologist.
- MSc Psychological Sciences (Brunel, 2025) + Psychosynthesis Diploma
- 10 years as CTO (Nimble Elearning)
- Trained in IFS, ACT, and Psychosynthesis frameworks
- Building GroundedNinja — a psychology-grounded AI platform

Joe's role on this project: **domain expert and architect**. He specifies what to build and validates that it reflects authentic IFS theory. Agents write the code.

---

## Key Theoretical Predecessor

**Kaj Sotala** mapped IFS to multi-agent reinforcement learning and AI alignment theory in blog posts on LessWrong and the Alignment Forum (Shard Theory). That is theoretical/conceptual work.

`agentic-ifs` is the **software implementation** — runnable Python code, not blog posts.

The key differentiator from standard multi-agent frameworks:
> This library optimises for **internal system homeostasis**, not **external task completion**.

Parts are not tools calling APIs. They are agents with protective intentions, emotional charges, and relationships to each other and to Self.

---

## Architecture Overview

### The Central Insight

**Self is not a Part.** Self is the system's operating environment — a global attractor state. When Self-energy is high, the system is stable. When Parts blend, they occlude Self-energy.

This maps to: `Self` = global `SystemState` vector, NOT an agent class.

### Part Taxonomy (Class Hierarchy)

```
IPart (Abstract Base)
├── Manager      — proactive protector (Daemon/BackgroundService)
├── Firefighter  — reactive protector (ExceptionHandler)
└── Exile        — burdened vulnerability (QuarantinedProcess)
```

### Core Computational Mappings

| IFS Concept | Computational Primitive |
|---|---|
| Part | Autonomous Agent / Class Instance |
| Self | Global System State / Attractor |
| Blending | Control Overlay / OcclusionMask on SelfVector |
| Unblending | Decouple Part from I/O controller |
| Polarization | Deadlock / Negative Feedback Loop |
| Burden | Malformed Data Payload (CorruptedData) |
| Trailhead | EventLog entry / InterruptSignal |
| 6Fs workflow | Sequential State Machine (the "game loop") |
| Parts Map | AdjacencyMatrix / Force-directed graph JSON |

### Key Architectural Decisions

| Decision | Resolution |
|---|---|
| Session design | Composable core + thin `Session` facade that delegates |
| SelfSystem model | Two fields: `self_potential=1.0` (constant) + `self_energy=0.3` (dynamic) |
| Self-energy default | 0.3 — typical person arriving at session with Managers running |
| Occlusion formula | `self_energy = self_potential * (1 - max_blend)` |
| Polarization | Explicit `PolarizationEdge` + auto-detect heuristic (V2) |
| Strategy types | `list[str]` for triggers, strategies, behaviors. LLM-friendly |
| Pydantic serialisation | `PartUnion` discriminated union via `part_type: Literal[...]` on each subclass |
| Blend/unblend location | Instance methods on `SelfSystem` only — not duplicated in `dynamics.py` |
| Timestamps | `datetime.now(timezone.utc)` everywhere (not deprecated `utcnow`) |
| 8C Self-energy | Vector of 8 Cs; scalar `self_energy` is backward-compatible computed mean |
| DialogueProvider | `typing.Protocol`, not ABC — duck typing, no inheritance required |
| LLM providers | Optional extras (`pip install ".[google]"` or `".[anthropic]"`) — core stays dependency-free |
| Unburdening | Separate state machine parallel to 6 Fs; keeps workflow.py focused on Protectors |

---

## Current Status — V2 "Healer Release"

**Status: V2 implemented.** 199 tests, mypy clean, ruff clean.

V1 ("Stabilization Release") covered **Protector work** — the 6 Fs, blending, Parts Map. V2 adds the **healing pipeline** and **LLM Part dialogue**.

**V1 (complete):**
- `IPart`, `Manager`, `Firefighter`, `Exile` classes with discriminated union
- `SelfSystem` with two-variable Self model (potential + energy)
- Protection graph: Protects/Polarized/Allied edges
- **6 Fs as the core game loop** — sequential state machine
- Blending mechanics: `BlendingPercentage` + `OcclusionMask`
- Trailhead logging and FocusShift (U-Turn)
- Parts Map as JSON export (graph data for D3.js, Gephi, Cytoscape)
- `Session` convenience facade

**V2 (complete):**
- **8C Self-Energy Vector** — `SelfEnergyVector` model with per-quality occlusion; scalar `self_energy` is backward-compatible mean
- **Unburdening Pipeline** — `UnburdeningStateMachine` (Witnessing → Retrieval → Purging → Invitation → Complete)
- **5 Ps Interaction Modifiers** — `FivePs` model tuning compassion threshold, trust increments, Self-energy checks
- **LLM Part Dialogue** — `DialogueProvider` protocol + `PartDialogue` orchestrator; optional Gemini and Anthropic integrations
- **Direct Access Mode** — therapist speaks directly to Part, bypassing Self-energy check
- **Auto-Detect Polarization** — `detect_polarization()` heuristic; returns suggestions, doesn't auto-modify graph
- **Somatic BodyMap** — `BodyMap`, `SomaticMarker`, `BodyLocation` for mapping Parts to body regions
- **Legacy Burden Lineage** — `Burden.lineage` for inherited/ancestral burdens; `Exile.invited_qualities` for post-unburdening

---

## Folder Structure

```
agentic-ifs/
├── CLAUDE.md               # This file — agent instructions
├── LICENSE                 # MIT
├── README.md               # Project overview and quick start
├── pyproject.toml          # Package config (pydantic, pytest, mypy, ruff)
├── spec/                   # Living specification documents
│   ├── IFSKit-Spec.md      # Formal spec (master document)
│   ├── v1-scope.md         # V1 detailed scope
│   └── research/           # Raw research documents from gnkb
│       ├── Ecosystem-Gaps-PsychAI.md
│       ├── IFSKit-Research.md
│       ├── IFSKit-Concept-Mapping.md
│       └── IFS-Self-Energy-Baseline.md
├── src/
│   └── agentic_ifs/
│       ├── __init__.py     # Full public API surface with __all__
│       ├── parts.py        # IPart, Manager, Firefighter, Exile, Burden, enums, PartUnion
│       ├── self_system.py  # SelfSystem, SelfEnergyVector, BlendState, LogEntry
│       ├── graph.py        # ProtectionGraph, Edge, EdgeType, PolarizationEdge, to_json()
│       ├── dynamics.py     # is_self_led(), self_preservation_ratio(), detect_polarization()
│       ├── workflow.py     # SixFsStateMachine, Trailhead, TrailheadLog, FocusShift
│       ├── session.py      # Session convenience facade (wires all components)
│       ├── modifiers.py    # V2: FivePs interaction modifiers
│       ├── unburdening.py  # V2: UnburdeningStateMachine (Exile healing pipeline)
│       ├── somatic.py      # V2: BodyMap, SomaticMarker, BodyLocation
│       ├── dialogue.py     # V2: DialogueProvider protocol, PartDialogue orchestrator
│       └── integrations/   # V2: Optional LLM provider implementations
│           ├── __init__.py
│           ├── google.py   # GeminiDialogueProvider
│           └── anthropic.py # AnthropicDialogueProvider
└── tests/
    ├── conftest.py         # Shared fixtures
    ├── test_parts.py       # Part instantiation, enums, PartUnion, lineage
    ├── test_self_system.py # Blend/unblend, 8C vector, recalculate
    ├── test_graph.py       # Graph operations, to_json, get_shared_exiles
    ├── test_dynamics.py    # Metrics, thresholds, polarization detection
    ├── test_workflow.py    # 6 Fs happy path, feel_toward gate
    ├── test_session.py     # Session delegation, V2 wiring
    ├── test_modifiers.py   # V2: FivePs thresholds, trust increments
    ├── test_unburdening.py # V2: Full unburdening pipeline
    ├── test_somatic.py     # V2: BodyMap, markers, queries
    └── test_dialogue.py    # V2: Mock provider, speak_as, direct_access
```

---

## Agent Working Instructions

### For spec agents

1. The primary spec document lives at `spec/IFSKit-Spec.md` — that is the source of truth for what to build
2. Raw research in `spec/research/` is background; the spec synthesises it
3. When speccing, always ask: does this mapping feel true to IFS theory? The code must serve the psychology, not the other way around
4. Joe has trained in IFS — if something feels architecturally convenient but psychologically wrong, flag it

### For dev agents

1. Python 3.11+, typed (Pydantic v2 for data models)
2. Framework-agnostic core — no framework dependency. Pure Python simulation loop
3. LLM integrations are optional extras in `agentic_ifs.integrations/` — core stays dependency-free beyond Pydantic
4. MIT licence
5. All public API should have docstrings that explain both the computational and IFS-theoretical meaning
6. Tests in `tests/` using pytest
7. `PartUnion` discriminated union for `dict[UUID, PartUnion]` — Pydantic v2 requires `part_type: Literal[...]` on each subclass
8. `blend()` / `unblend()` are instance methods on `SelfSystem` only — do not duplicate in `dynamics.py`
9. Use `datetime.now(timezone.utc)` — not `datetime.utcnow()` (deprecated in 3.11+)
10. `Exile.emotional_charge` = current activation; `Burden.emotional_charge` = stored intensity — keep docstrings clear
11. `DialogueProvider` is a `typing.Protocol` — any object with `generate_part_response()` is valid, no inheritance
12. `self_energy` (scalar) must always remain backward-compatible — it is the mean of the 8C vector

### For documentation agents

1. Docs must be readable by both psychologists (who know IFS but not code) and engineers (who know code but not IFS)
2. Every class and method docstring should have the IFS meaning alongside the technical meaning
3. JOSS (Journal of Open Source Software) publication is a target — maintain that standard

---

## Key Constraints

- **Not clinical software** — no MHRA, no DTAC, no clinical claims
- **Philosophical and research use** — appropriate for researchers, therapists exploring the model, AI/psych intersection builders
- **Framework-agnostic** — the core library should not require any specific agent framework
- **Joe is the IFS authority** — if in doubt about theoretical fidelity, ask

---

## Knowledge Base (gnkb)

Research for this project is stored in a dedicated gnkb collection.

**Collection:** Agentic IFS
**Collection ID:** `6fdf5f3b-e2b8-46e7-9813-1129c60cc0ad`

`gnkb` is a global CLI. Key commands:

```bash
# Search the collection
gnkb documents search query="<text>" collectionId="6fdf5f3b-e2b8-46e7-9813-1129c60cc0ad"

# List all documents in collection
gnkb documents list collectionId="6fdf5f3b-e2b8-46e7-9813-1129c60cc0ad"

# Trigger new deep research into the collection
gnkb research create collectionId="6fdf5f3b-e2b8-46e7-9813-1129c60cc0ad" prompt="<research question>" execute=true

# Check research job status
gnkb research list collectionId="6fdf5f3b-e2b8-46e7-9813-1129c60cc0ad"

# Download a completed research document
gnkb documents download <documentId> path=spec/research/<filename>.md
```

**Current documents in collection:**
| Local file | gnkb ID | Note |
|---|---|---|
| `spec/research/IFSKit-Research.md` | `b91ec8c2` | Architecture research — LangGraph rec, Sotala predecessor, name collision |
| `spec/research/IFSKit-Concept-Mapping.md` | `43022da5` | Full IFS concept → computational primitive mapping, V1/V2 split |
| `spec/research/Ecosystem-Gaps-PsychAI.md` | `55b75e75` | Why this gap exists — ecosystem analysis confirming IFSKit as the missing piece |
| `spec/research/IFS-Self-Energy-Baseline.md` | — | Self-energy baseline research — validates two-variable model, 0.3 default, crisis states |

**Research pattern for this project:**
All new research questions (IFS theory, architecture decisions, open questions) should go into this collection, not the job-search Jobs collection.

---

*Last updated: 2026-02-27*
