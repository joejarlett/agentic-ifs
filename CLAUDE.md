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

---

## V1 Scope — "Stabilization Release"

V1 focuses on **Protector work** (Managers and Firefighters). This is the stable foundation; Exile/unburdening work is V2.

**V1 includes:**
- `Part`, `Manager`, `Firefighter`, `Exile` classes with full data structures
- `Self` as a scalar `SelfEnergy` float (not full 8C vector — that's V2)
- Protection graph: Protects/Polarized/Allied edges
- **6 Fs as the core game loop** — sequential state machine
- Blending mechanics: `BlendingPercentage` + `OcclusionMask`
- Trailhead logging
- Parts Map as JSON export (graph data only, not rendered visualization)
- U-Turn as `FocusShift` meta-tag

**V1 excludes (V2 scope):**
- Unburdening pipeline (Witnessing → Retrieval → Purging → Invitation)
- Legacy Burden lineage data structures
- Somatic integration / BodyMap coordinates
- Direct Access mode (RPC to Part bypassing Self)
- LLM simulation of Part dialogue
- 8C Self-energy vector breakdown
- 3D/visual Parts Map rendering

---

## Folder Structure

```
agentic-ifs/
├── CLAUDE.md               # This file — agent instructions
├── LICENSE                 # MIT
├── README.md               # Project overview (to be written)
├── pyproject.toml          # Package config (to be written)
├── spec/                   # Living specification documents
│   ├── IFSKit-Spec.md      # Formal spec (master document)
│   ├── v1-scope.md         # V1 detailed scope
│   └── research/           # Raw research documents from gnkb
│       ├── Ecosystem-Gaps-PsychAI.md
│       ├── IFSKit-Research.md
│       └── IFSKit-Concept-Mapping.md
├── src/
│   └── agentic_ifs/
│       ├── __init__.py
│       ├── parts.py        # Part, Manager, Firefighter, Exile
│       ├── self_system.py  # SelfSystem, SelfEnergy
│       ├── graph.py        # ProtectionGraph, adjacency
│       ├── dynamics.py     # Blending, Unblending, Polarization
│       ├── workflow.py     # 6Fs state machine
│       └── trailheads.py   # TrailheadLog
├── tests/
└── docs/
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
2. Framework-agnostic core — **no LangGraph dependency** in V1. Pure Python simulation loop
3. Optional LangGraph integration can be in a separate `agentic_ifs.integrations.langgraph` module
4. MIT licence
5. All public API should have docstrings that explain both the computational and IFS-theoretical meaning
6. Tests in `tests/` using pytest

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

> Note: Documents uploaded via content have `title: "Untitled Document"` in gnkb — this is a platform limitation. Use the local filenames and IDs above as the canonical reference. All future research should use `gnkb research create` which sets titles correctly.

**Research pattern for this project:**
All new research questions (IFS theory, architecture decisions, open questions) should go into this collection, not the job-search Jobs collection.

---

*Last updated: 2026-02-27*
