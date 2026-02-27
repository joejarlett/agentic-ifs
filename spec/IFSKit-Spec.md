# IFSKit — Formal Specification
## agentic-ifs v1.0 "Stabilization Release"

*Status: DRAFT — Awaiting author review*
*Author: Joe Jarlett*
*Last updated: 2026-02-27*

---

## 1. Purpose and Scope

`agentic-ifs` is a Python library that formalises **Internal Family Systems (IFS)** as a multi-agent computational architecture.

**What it is:**
- A research and simulation tool for exploring IFS dynamics computationally
- A foundation for builders working at the psychology/AI intersection
- A software implementation of the theoretical mappings explored by Kaj Sotala (Shard Theory / LessWrong alignment work)

**What it is not:**
- Clinical software (no MHRA, no DTAC, no clinical claims)
- A therapy delivery platform
- A replacement for IFS therapy or trained facilitation

**The key differentiator from other multi-agent frameworks:**
> This library optimises for **internal system homeostasis**, not **external task completion**.

---

## 2. Theoretical Foundation

Internal Family Systems (IFS), developed by Richard Schwartz, treats the human mind as a system of discrete sub-personalities ("Parts") governed by a core, undamaged essence ("Self").

Core IFS axioms that shape the architecture:
1. **Multiplicity is normal** — the mind is naturally a system of Parts, not a unitary entity
2. **All Parts have positive intent** — even destructive behaviours serve a protective purpose
3. **Self is never damaged** — Self-energy can be occluded but not destroyed
4. **The goal is not elimination** — Parts are not to be removed but to be unburdened and trusted

---

## 3. Core Architecture

### 3.1 The Central Design Decision: Self is Not an Agent

In standard multi-agent systems, everything is an agent. In IFSKit, **Self is the exception**.

Self = the system's operating environment — a global attractor state. When Self-energy is high, the system is stable and Parts can relax their protective roles. When Parts blend, they occlude Self-energy.

```
Self  →  SystemState (global context object, NOT an agent)
Parts →  Agents (autonomous, with local state and behaviours)
```

This is not an arbitrary design choice. It reflects the IFS axiom that Self is the ground from which all Parts emerge, not a peer participant.

### 3.2 Part Taxonomy

```
IPart (Abstract Base Class)
├── Manager      — proactive protector
├── Firefighter  — reactive protector
└── Exile        — burdened vulnerability
```

All Parts share a base identity (`IPart`). The subclasses have distinct activation patterns, data structures, and state machines.

---

## 4. Data Structures

### 4.1 `IPart` — Base Class

```python
class IPart(BaseModel):
    id: UUID
    narrative: str          # The story the part tells about its origin
    age: int                # Developmental age at which the part was frozen
    intent: str             # The positive protective intent
    trust_level: float      # 0.0–1.0: degree of trust in Self
    is_visible: bool = True # Whether accessible to consciousness
```

### 4.2 `Manager`

Proactive protector. Runs a continuous monitoring loop. Prevents Exiles from being activated.

**Computational equivalent:** Daemon / BackgroundService

```python
class Manager(IPart):
    triggers: list[Pattern]        # Input patterns that initiate protective subroutines
    strategies: list[Behavior]     # Pre-emptive actions (perfectionism, planning, criticism)
    rigidity: float                # 0.0–1.0: resistance to state change

    # State machine: IDLE → SCANNING → BLOCKING
    state: ManagerState = ManagerState.IDLE
```

**Observability:** Frequency of `BLOCKING` events; correlation between trigger proximity and activation.

### 4.3 `Firefighter`

Reactive protector. Activated when a Manager's blocking fails (Exile overflow). Uses extreme measures to extinguish emotional pain.

**Computational equivalent:** ExceptionHandler / EmergencyOverride

```python
class Firefighter(IPart):
    pain_threshold: float              # Affective intensity level that triggers activation
    extinguishing_behaviors: list[Action]  # High-intensity outputs (binge, dissociation, rage)
    refractory_period: timedelta       # Recovery time before deactivation

    # State machine: DORMANT → ACTIVE → COOLDOWN
    state: FirefighterState = FirefighterState.DORMANT
```

**Observability:** System Volatility — rapidity of switch from Manager-control to Firefighter-chaos.

### 4.4 `Exile`

Burdened vulnerability. Sequestered repository of unprocessed trauma. Carries high emotional charge.

**Computational equivalent:** EncryptedDataBlob / QuarantinedProcess

```python
class Exile(IPart):
    burden: Burden | None             # The trauma payload (see Section 6)
    emotional_charge: float           # 0.0–1.0: intensity of stored affect
    is_visible: bool = False          # Exiles are hidden by default

    # State machine: ISOLATED → LEAKING → FLOODING → UNBURDENED
    state: ExileState = ExileState.ISOLATED
```

**Observability:** Latent system charge (potential energy); frequency of LEAKING events.

### 4.5 `SelfSystem`

The operating environment. Not an agent. A global context object passed to all interactions.

```python
class SelfSystem(BaseModel):
    self_energy: float              # V1: simple scalar 0.0–1.0
    # V2: full 8C vector (Curiosity, Calm, Clarity, Compassion,
    #     Confidence, Courage, Creativity, Connectedness)

    active_blends: list[UUID]       # IDs of currently blended Parts
    session_log: list[LogEntry]     # Full interaction history
```

**Key metric:** `SelfPreservationRatio` — ratio of Self-energy to total Part activation intensity.

---

## 5. System Dynamics

### 5.1 Blending and Unblending

Blending occurs when a Part's state overwrites the Self's state, assuming control of I/O.

```python
class BlendState(BaseModel):
    part_id: UUID
    blending_percentage: float      # 0.0–1.0: how much I/O is Part-controlled
    occlusion_mask: dict[str, float]  # Reduces SelfSystem vector values
    # e.g., anxious Manager blending sets SelfSystem.calm → 0.0

# States: UNBLENDED ↔ PARTIALLY_BLENDED ↔ FULLY_BLENDED (hijack)
```

**Measurement:**
- Reaction time variance (blended parts react faster, more rigidly)
- Linguistic shift: "I observe…" → "I am…"

### 5.2 Polarization

A feedback loop where two Parts escalate in opposition.

**Computational equivalent:** Deadlock / Resource Contention

```python
class PolarizationEdge(BaseModel):
    part_a_id: UUID
    part_b_id: UUID
    tension_level: float            # 0.0–1.0
    escalation_fn: Callable         # f(A_activity) = k * B_activity

# States: STABLE → OSCILLATING → LOCKED (paralysis)
```

**Classic example:** Perfectionist Manager ↔ Procrastinator Firefighter. When one activates, the other escalates.

### 5.3 Protection Graph

The directed graph of Part relationships.

```python
class ProtectionGraph(BaseModel):
    nodes: dict[UUID, IPart]
    edges: list[Edge]               # Edge types: PROTECTS, POLARIZED, ALLIED

    def get_protectors_of(self, exile_id: UUID) -> list[IPart]: ...
    def get_polarized_pairs(self) -> list[PolarizationEdge]: ...
    def to_json(self) -> dict: ...  # Parts Map export
```

---

## 6. Burdens

Burdens are foreign data payloads attached to Exiles — limiting beliefs formed at the time of trauma.

```python
class Burden(BaseModel):
    burden_type: BurdenType     # Enum: PERSONAL | LEGACY | UNATTACHED | SOCIETAL
    origin: str                 # e.g., "Age 7, school failure"
    content: str                # The limiting belief: e.g., "I am not enough"
    emotional_charge: float     # 0.0–1.0

class BurdenType(Enum):
    PERSONAL = "personal"       # Direct personal trauma
    LEGACY = "legacy"           # Inherited (ancestral, family system)
    UNATTACHED = "unattached"   # Floating in the field, not clearly sourced
    SOCIETAL = "societal"       # Cultural/systemic (racism, gender norms, etc.)
```

**Note:** Unburdening (clearing the burden) is V2 scope. V1 supports burden storage and querying only.

---

## 7. The 6 Fs — Core Game Loop

The 6 Fs is the standard algorithm for engaging with Protectors. This is the primary workflow in V1.

```python
class SixFsStateMachine:
    """
    Sequential state machine for Protector engagement.
    IFS theory: Anderson, Schwartz & Sweezy (2017)
    """

    # States
    FIND      = "find"        # Locate the part (ScanSystem → PartReference)
    FOCUS     = "focus"       # Direct attention (SelectTarget)
    FLESH_OUT = "flesh_out"   # Gather metadata (QueryPart)
    FEEL_TOWARD = "feel_toward"  # Check Self-energy presence
    BEFRIEND  = "befriend"    # Build relationship (UpdateTrust)
    FEAR      = "fear"        # Identify worst-case scenarios (GetFears)
```

**The critical gate — Feel Toward:**

```python
def feel_toward(self, part_id: UUID, self_system: SelfSystem) -> NextStep:
    if self_system.self_energy > COMPASSION_THRESHOLD:
        return NextStep.BEFRIEND
    else:
        # A new Part has become active (the one feeling negatively toward the target)
        # Unblend the interfering Part first
        interfering_part = self.identify_active_blend(self_system)
        return NextStep.UNBLEND(interfering_part)
```

This recursive check is what makes IFS clinically distinct from other models. If the user feels anger or judgment toward a Part, that anger is itself a Part — and must be worked with first.

---

## 8. Trailheads

Entry points for a session — the sensation, image, emotion, or thought that signals a Part is present.

```python
class Trailhead(BaseModel):
    id: UUID
    trailhead_type: TrailheadType   # SOMATIC | VISUAL | AUDITORY | COGNITIVE
    intensity: float                 # 0.0–1.0
    timestamp: datetime
    description: str
    associated_part_id: UUID | None  # Populated after FIND step

class TrailheadLog(BaseModel):
    entries: list[Trailhead]

    def add(self, trailhead: Trailhead) -> None: ...
    def get_by_type(self, t: TrailheadType) -> list[Trailhead]: ...
```

---

## 9. The U-Turn

The conceptual pivot from external trigger to internal reaction.

```python
class FocusShift(BaseModel):
    """
    Marks the moment attention pivots from external (My Boss) to internal (My Anger).
    Used as a meta-tag on session log entries.
    """
    from_subject: str               # The external trigger
    to_subject: str                 # The Part now in focus
    timestamp: datetime
    trailhead_id: UUID | None       # The trailhead that prompted the shift
```

---

## 10. Parts Map Export

V1 exports the internal system as a JSON graph (for use with force-directed visualisation tools such as D3.js, Gephi, or Cytoscape).

```python
def export_parts_map(graph: ProtectionGraph) -> dict:
    """
    Returns a JSON-serialisable dict with nodes and edges.
    Node size = Part.emotional_charge
    Edge colour: PROTECTS=green, POLARIZED=red, ALLIED=blue
    """
    return {
        "nodes": [...],   # {id, label, type, charge, state}
        "edges": [...]    # {source, target, type, tension}
    }
```

---

## 11. V1 Implementation Checklist

### Core models (parts.py)
- [ ] `IPart` abstract base class
- [ ] `Manager` with ManagerState enum
- [ ] `Firefighter` with FirefighterState enum
- [ ] `Exile` with ExileState enum
- [ ] `Burden` and `BurdenType` enum

### Self system (self_system.py)
- [ ] `SelfSystem` with `self_energy` scalar
- [ ] `BlendState` model
- [ ] `blend()` and `unblend()` methods
- [ ] `OcclusionMask` application to SelfSystem

### Graph (graph.py)
- [ ] `Edge` and `EdgeType` enum
- [ ] `PolarizationEdge` with escalation function
- [ ] `ProtectionGraph` with add/query methods
- [ ] `to_json()` / `export_parts_map()`

### Dynamics (dynamics.py)
- [ ] `BlendState` tracking
- [ ] Blending/unblending state transitions
- [ ] Polarization detection
- [ ] `SelfPreservationRatio` calculation

### Workflow (workflow.py)
- [ ] `SixFsStateMachine` with all 6 states
- [ ] `feel_toward()` Self-energy gate with recursive unblend
- [ ] `Trailhead` and `TrailheadLog`
- [ ] `FocusShift` / U-Turn marker

### Package
- [ ] `__init__.py` with clean public API
- [ ] `pyproject.toml` (Python 3.11+, Pydantic v2, MIT licence)
- [ ] `README.md`
- [ ] pytest test suite for each module

---

## 12. Open Questions for Author Review

These need Joe's input before implementation:

1. **5 Ps placement** — Are the 5 Ps (Presence, Patience, Perspective, Persistence, Playfulness) V1 validation constraints on the facilitation context, or V2 API interaction modifiers?

2. **Self-energy initialisation** — What should the default `self_energy` scalar be at system start? 0.5 (neutral) or 1.0 (full Self, Parts not yet active)?

3. **Polarization detection** — Should the library auto-detect polarization from the escalation pattern, or require explicit declaration of polarized pairs?

4. **Session concept** — Should V1 have an explicit `Session` object wrapping a `ProtectionGraph` + `SelfSystem` + `TrailheadLog`, or keep these composable without a session wrapper?

---

## 13. References

- Schwartz, R. (1994). *Internal Family Systems Therapy*. Guilford Press.
- Anderson, F., Sweezy, M. & Schwartz, R. (2017). *Internal Family Systems Skills Training Manual*.
- Sotala, K. (2019–2023). IFS/Shard Theory mapping posts. LessWrong / Alignment Forum.
- Research background: `spec/research/IFSKit-Research.md`, `spec/research/IFSKit-Concept-Mapping.md`
