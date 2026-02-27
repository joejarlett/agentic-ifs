# Computational Architecture for Internal Family Systems: The IFSKit Library Specification

The Internal Family Systems (IFS) model, developed by Richard Schwartz, posits that the human mind is not a unitary entity but a dynamic, multiplicity-based system composed of discrete sub-personalities ("Parts") and a core, undamaged essence known as the "Self" [cite: 1, 2]. To translate this psychotherapeutic framework into a computational software library ("IFSKit"), one must map complex psychological dynamics onto rigorous data structures, state machines, and algorithmic processes. This report provides an exhaustive architectural blueprint for such a library, treating the psyche as a Multi-Agent System (MAS) subject to specific energy constraints, hierarchical logic, and feedback loops.

The proposed **IFSKit** is designed as an object-oriented, event-driven framework. It models the mind as a graph of interacting nodes (Parts) governed by a central attractor state (Self). The following sections detail the translation of every major IFS concept into computational primitives, defining the necessary data structures, state transitions, and observability metrics required for research and application.

---

## 1. Core Primitives: Parts Taxonomy and Class Hierarchy

In IFS, the fundamental unit of the psyche is the "Part." Computationally, a Part is an autonomous agent with local state, specific goals, and triggered behaviors. The taxonomy of Managers, Firefighters, and Exiles represents a class inheritance hierarchy with distinct operational parameters.

### 1.1 The `Part` Base Class

The generic `Part` represents any sub-personality. It encapsulates the basic properties shared by all internal entities: a narrative history, a set of beliefs, and a relationship to the Self.

*   **Computational Equivalent:** An Abstract Base Class (ABC) or Interface `IPart`.
*   **Data Structures:**
    *   `ID` (UUID): Unique identifier.
    *   `Narrative` (String/Log): The story the part tells about its origin.
    *   `Age` (Integer): The developmental age at which the part was frozen [cite: 3].
    *   `Intent` (String): The positive protective intent (even if the behavior is destructive) [cite: 1, 4].
    *   `TrustLevel` (Float 0.0-1.0): The degree to which the part trusts the Self.
*   **Essential for v1?** Yes.

### 1.1 The `Part` Base Class

    *   `Narrative` (String/Log): The story the part tells about its origin.
    *   `Age` (Integer): The developmental age at which the part was frozen [cite: 3].
    *   `Intent` (String): The positive protective intent (even if the behavior is destructive) [cite: 1, 4].
    *   `TrustLevel` (Float 0.0-1.0): The degree to which the part trusts the Self.
*   **Essential for v1?** Yes.

### 1.2 Managers (Proactive Protectors)

Managers are preemptive control systems. They scan the environment for triggers and enforce rules to prevent Exiles from being activated.

*   **Computational Equivalent:** A `Daemon` or `BackgroundService` running a continuous monitoring loop.
*   **Data Structures:**
    *   `Triggers` (List<Pattern>): Input patterns (external or internal) that initiate protective subroutines.
    *   `Strategies` (List<Behavior>): Pre-emptive actions (e.g., perfectionism, planning, criticizing).
    *   `Rigidity` (Float 0.0-1.0): Resistance to state change.
*   **State Transitions:**
    *   `IDLE` → `SCANNING` → `BLOCKING` (when a threat is detected).
*   **Observability:** Researchers would measure the frequency of `BLOCKING` events and the correlation between `Trigger` proximity and Manager activation.
*   **Essential for v1?** Yes.

### 1.3 Firefighters (Reactive Protectors)

Firefighters are interrupt handlers. They are activated only when the system encounters a critical error state (an Exile breaking through). They utilize extreme, often chaotic measures to extinguish emotional pain.

*   **Computational Equivalent:** An `Exception Handler` or `EmergencyOverride` system.
*   **Data Structures:**
    *   `PainThreshold` (Float): The level of affective intensity that triggers activation.
    *   `ExtinguishingBehaviors` (List<Action>): High-intensity outputs (e.g., binge eating, dissociation, rage) designed to numb or distract [cite: 1, 5].
    *   `RefractoryPeriod` (TimeSpan): Time required before the part can deactivate.
*   **State Transitions:**
    *   `DORMANT` → `ACTIVE` (triggered by Exile overflow) → `COOLDOWN`.
*   **Observability:** Measurement of "System Volatility"—the rapidity of the switch from Manager-control to Firefighter-chaos.
*   **Essential for v1?** Yes.

### 1.3 Firefighters (Reactive Protectors)

    *   `RefractoryPeriod` (TimeSpan): Time required before the part can deactivate.
*   **State Transitions:**
    *   `DORMANT` → `ACTIVE` (triggered by Exile overflow) → `COOLDOWN`.
*   **Observability:** Measurement of "System Volatility"—the rapidity of the switch from Manager-control to Firefighter-chaos.
*   **Essential for v1?** Yes.

### 1.4 Exiles (Burdened Vulnerability)

Exiles are data repositories of unprocessed trauma, sequestered to prevent system instability. They carry high "energetic charges" (burdens).

*   **Computational Equivalent:** `EncryptedDataBlob` or `QuarantinedProcess`. They contain "hazardous" data (pain) that, if accessed without safeguards (Self-energy), causes a system crash (overwhelm).
*   **Data Structures:**
    *   `Burden` (Object): The specific trauma payload (see Section 6).
    *   `Visibility` (Boolean): Whether the part is accessible to consciousness.
    *   `EmotionalCharge` (Float 0.0-1.0): Intensity of the stored affect [cite: 3, 6].
*   **State Transitions:**
    *   `ISOLATED` → `LEAKING` (passive influence) → `FLOODING` (active overwhelm) → `UNBURDENED` (healed state).
*   **Essential for v1?** Yes.

---

## 2. The Core Operating System: Self and Self-Energy

The Self is not a part; it is the environment in which parts exist, or the "operating system" when it is functioning optimally. It is characterized by the 8 Cs and 5 Ps.

### 2.1 Self-Energy Quantified (The 8 Cs)

The "8 Cs" (Curiosity, Calm, Clarity, Compassion, Confidence, Courage, Creativity, Connectedness) [cite: 7, 8, 9] define the quality of the system's processing capability.

*   **Computational Equivalent:** A global `SystemState` vector or a `Context` object passed to all interactions.
*   **Data Structures:**
    *   `SelfVector` (Float[cite: 10]): A normalized vector representing the presence of each C.
        *   `Index 0`: Curiosity (0.0 to 1.0)
        *   `Index 1`: Calm (0.0 to 1.0)
        *   ...etc.
    *   `SelfEnergyTotal` (Float): A composite score derived from the vector magnitude.
*   **Measurement:**
    *   *Inputs:* Sentiment analysis of internal dialogue, Heart Rate Variability (HRV) metrics (somatic proxy) [cite: 11, 12].
    *   *Metric:* `SelfPreservationRatio`—the ratio of Self-energy to Part-activation intensity.
*   **Essential for v1?** Yes, as a scalar value. Vector breakdown is v2.

### 2.1 Self-Energy Quantified (The 8 Cs)

*   **Measurement:**
    *   *Inputs:* Sentiment analysis of internal dialogue, Heart Rate Variability (HRV) metrics (somatic proxy) [cite: 11, 12].
    *   *Metric:* `SelfPreservationRatio`—the ratio of Self-energy to Part-activation intensity.
*   **Essential for v1?** Yes, as a scalar value. Vector breakdown is v2.

### 2.2 The 5 Ps (Therapist/Facilitator Qualities)

The 5 Ps (Presence, Patience, Perspective, Persistence, Playfulness) [cite: 7, 13, 14] are active modifiers of the Self-Part relationship, particularly relevant for the "User" (therapist/facilitator) interacting with the library.

*   **Computational Equivalent:** `InteractionModifiers` or `PolicySettings` for the API.
*   **Data Structures:**
    *   `PatienceTimer` (TimeSpan): Computational delay allowing parts to respond without timeout.
    *   `Perspective` (Boolean): A flag toggling between "immersed" (blended) and "observer" (unblended) camera views in a sociogram.
*   **Essential for v1?** No. These are advanced interaction parameters for v2.

---

## 3. System Dynamics: Blending, Unblending, and Polarization

Dynamics describe how agents (Parts) interact with the environment (Self) and each other.

### 3.1 Blending and Unblending

Blending occurs when a Part's state overwrites the Self's state, assuming control of input/output channels [cite: 1, 4]. Unblending is the separation of these states.

*   **Computational Equivalent:** `Dependency Injection` vs. `System Overlay`. When blended, the Part *is* the `ActiveController`. When unblended, the Part is a `Delegate` or `Observer`.
*   **Data Structures:**
    *   `BlendingPercentage` (Float 0.0-1.0): How much of the I/O is controlled by the Part.
    *   `OcclusionMask`: A filter applied to the `SelfVector`. High blending reduces the available `SelfVector` values (e.g., high Anxiety Part blending reduces Calm to 0.0).
*   **State Transitions:**
    *   `UNBLENDED` (Part separate from Self) $\leftrightarrow$ `PARTIALLY_BLENDED` $\leftrightarrow$ `FULLY_BLENDED` (Hijack).
*   **Measurement:**
    *   Reaction time variance (blended parts often react faster/more rigidly).
    *   Linguistic markers (shifting from "I observe" to "I am").
*   **Essential for v1?** Yes, this is fundamental.

### 3.1 Blending and Unblending

*   **State Transitions:**
    *   `UNBLENDED` (Part separate from Self) $\leftrightarrow$ `PARTIALLY_BLENDED` $\leftrightarrow$ `FULLY_BLENDED` (Hijack).
*   **Measurement:**
    *   Reaction time variance (blended parts often react faster/more rigidly).
    *   Linguistic markers (shifting from "I observe" to "I am").
*   **Essential for v1?** Yes, this is fundamental.

### 3.2 Polarization

Polarization is a feedback loop where two Parts (usually Protectors) escalate their extreme roles in opposition to each other (e.g., a Perfectionist Manager vs. a Procrastinator Firefighter) [cite: 15, 16, 17].

*   **Computational Equivalent:** `Deadlock` or `Resource Contention` loop.
*   **Data Structures:**
    *   `PolarizationEdge` (Graph Edge): Connects `Part A` and `Part B`.
    *   `TensionLevel` (Float): The intensity of the conflict.
    *   `EscalationFunction` (Function): `f(A_activity) = k * B_activity`.
*   **State Transitions:**
    *   `STABLE` → `OSCILLATING` (rapid switching between parts) → `LOCKED` (paralysis).
*   **Observability:** Researcher observes negative correlation in activation times (when A is up, B is down) or simultaneous high-energy activation leading to system freeze.
*   **Essential for v1?** Yes.

### 3.3 Protective System Architecture

This describes the directed graph of protection. Managers and Firefighters are organized *around* Exiles.

*   **Computational Equivalent:** A Directed Acyclic Graph (DAG) or Dependency Graph.
*   **Data Structures:**
    *   `ProtectionList` (List<Reference>): A list of Exiles a specific Protector is guarding.
    *   `StrategyType`: Enum (Preemptive vs. Reactive).
*   **Logic:**
    *   `IF (Exile.Activation > Threshold) THEN (Firefighter.Execute())`
    *   `IF (Environment.Risk > Threshold) THEN (Manager.Execute())`
*   **Essential for v1?** Yes.

---

## 4. Operational Processes: The 6 Fs and Trailheads

The "6 Fs" [cite: 10, 18, 19, 20] constitute the standard algorithm for engaging with Protectors.

## 4. Operational Processes: The 6 Fs and Trailheads

Reactive).
*   **Logic:**
    *   `IF (Exile.Activation > Threshold) THEN (Firefighter.Execute())`
    *   `IF (Environment.Risk > Threshold) THEN (Manager.Execute())`
*   **Essential for v1?** Yes.

---

## 4. Operational Processes: The 6 Fs and Trailheads

The "6 Fs" [cite: 10, 18, 19, 20] constitute the standard algorithm for engaging with Protectors.

### 4.1 Trailheads

A trailhead is the entry point for a session—a somatic sensation, thought, or emotion that indicates a Part is present.

*   **Computational Equivalent:** `EventLog` entry or `InterruptSignal`.
*   **Data Structures:**
    *   `TrailheadType`: Enum (Somatic, Visual, Auditory, Cognitive).
    *   `Intensity`: Float.
    *   `Timestamp`: Time of occurrence.
*   **Essential for v1?** Yes.

### 4.2 The 6 Fs Algorithm

This is a sequential state machine used to unblend and build rapport with Protectors.

1.  **Find:** Locate the part.
    *   *Action:* `ScanSystem()` returning `PartReference`.
2.  **Focus:** Direct attention.
    *   *Action:* `SelectTarget(PartID)`.
3.  **Flesh Out:** Gather metadata.
    *   *Action:* `QueryPart(PartID, ["Age", "Image", "Sensation"])`.
4.  **Feel Toward:** Check for Self-energy.
    *   *Logic:* `IF (SelfVector.Compassion > Threshold) GOTO Befriend ELSE GOTO Unblend(InterferingPart)`.
    *   *Critical Check:* This step prevents bypassing. If the user feels "Anger" toward the part, a new Part (the Angry Part) is the active subject.
5.  **Befriend:** Build relationship.
    *   *Action:* `UpdateTrust(PartID, +Increment)`.
6.  **Fear:** Identify the worst-case scenario.
    *   *Action:* `GetFears(PartID)`. Returns `List<Prediction>`.
*   **Essential for v1?** Yes, this is the core "Game Loop" of the library.

---

## 5. The Unburdening Pipeline

Unburdening is the process of permanently releasing trauma, converting an Exile into an unburdened part [cite: 6, 21, 22].

### 5.1 Burdens and Legacy Burdens

Burdens are foreign data attached to a part. Legacy burdens are inherited, often linked to lineage or culture [cite: 3, 23, 24].

### 5.1 Burdens and Legacy Burdens

---

## 5. The Unburdening Pipeline

Unburdening is the process of permanently releasing trauma, converting an Exile into an unburdened part [cite: 6, 21, 22].

### 5.1 Burdens and Legacy Burdens

Burdens are foreign data attached to a part. Legacy burdens are inherited, often linked to lineage or culture [cite: 3, 23, 24].

*   **Computational Equivalent:**
    *   *Personal Burden:* `Malware` or `CorruptedData` attached to a process.
    *   *Legacy Burden:* `InheritedClassAttributes` or `GlobalVariables` passed down from a parent `System` (ancestor).
*   **Data Structures:**
    *   `BurdenType`: Enum (Personal, Legacy, Unattached, Societal).
    *   `Origin`: String (e.g., "Grandmother's famine trauma").
    *   `Content`: The limiting belief (e.g., "I am not enough").

### 5.2 Unburdening Stages (State Machine)

1.  **Witnessing:** The Self "downloads" the Exile's memory without being overwhelmed.
    *   *State:* `SYNCING`.
2.  **Retrieval:** Moving the Exile out of the trauma time/space.
    *   *State:* `RELOCATING`.
3.  **Unburdening Ritual:** The elemental release (fire, water, wind).
    *   *State:* `PURGING`.
    *   *Action:* `Part.Burden = NULL`.
4.  **Invitation:** Inviting new qualities.
    *   *Action:* `Part.Qualities.Add(NewQuality)`.
*   **Essential for v1?** No. This is v2 functionality due to its complexity and risk. v1 should focus on *stabilization* (Protectors).

---

### 6.1 Direct Access

Direct Access involves the therapist (or software agent) speaking directly to the Part, bypassing the client's Self if necessary [cite: 25, 26, 27].

*   **Computational Equivalent:** `RemoteProcedureCall (RPC)` or `RootAccess`. It allows external input to directly modify Part state without the internal `Self` proxy.
*   **Implementation:** A chat interface mode where the `User` role is "Therapist" and the `Responder` is explicitly locked to `Manager_01`.
*   **Essential for v1?** No (Advanced).

### 6.2 Parts Mapping (Sociogram)

Visualizing the internal system [cite: 28, 29, 30].

### 6.2 Parts Mapping (Sociogram)

It allows external input to directly modify Part state without the internal `Self` proxy.
*   **Implementation:** A chat interface mode where the `User` role is "Therapist" and the `Responder` is explicitly locked to `Manager_01`.
*   **Essential for v1?** No (Advanced).

### 6.2 Parts Mapping (Sociogram)

Visualizing the internal system [cite: 28, 29, 30].

*   **Computational Equivalent:** `Force-Directed Graph`.
    *   *Nodes:* Parts (sized by `Energy`).
    *   *Edges:* Relationships (Red = Polarized, Green = Allied, Blue = Protects).
    *   *Clusters:* Groupings of Managers/Firefighters around specific Exiles.
*   **Data Structures:** `AdjacencyMatrix` or `NodeList/EdgeList`.
*   **Essential for v1?** Yes, as a basic output (JSON export). 3D rendering is v2.

### 6.3 Somatic Expression

Mapping parts to body locations [cite: 31, 32, 33, 34].

*   **Computational Equivalent:** `BodyMap` coordinates.
*   **Data Structures:**
    *   `SensationLocation`: Vector (x, y, z) relative to body model.
    *   `SensationQuality`: String (e.g., "Tightness", "Heat").
*   **Essential for v1?** No (Advanced/v2).

### 6.4 The U-Turn

The conceptual pivot from focusing on the external trigger to the internal reaction.

*   **Computational Equivalent:** `FocusShift` event.
*   **Logic:** Detecting when `Subject` changes from "My Boss" (External) to "My Anger" (Internal).
*   **Essential for v1?** Yes, as a meta-tag for journal entries.

---

### Essential for v1 (The "Stabilization" Release)

*   **Class Definitions:** Part, Manager, Firefighter, Exile.
*   **Self Model:** Basic Self-Energy scalar.
*   **Graph:** Basic relationships (Protects, Polarized).
*   **Process:** The 6 Fs workflow (text-based).
*   **Dynamics:** Blending detection and manual Unblending.
*   **Trailheads:** Logging triggers.

### Advanced Features (The "Healer" Release)

*   **Unburdening Protocol:** Full witnessing and retrieval logic.
*   **Legacy Burdens:** Lineage data structures.
*   **Somatic Integration:** Body mapping.
*   **Direct Access:** Simulation mode.
*   **AI Integration:** Using LLMs to simulate Part dialogue based on the `Narrative` and `Strategies` attributes [cite: 35, 36].

### Advanced Features (The "Healer" Release)

### Advanced Features (The "Healer" Release)

*   **Unburdening Protocol:** Full witnessing and retrieval logic.
*   **Legacy Burdens:** Lineage data structures.
*   **Somatic Integration:** Body mapping.
*   **Direct Access:** Simulation mode.
*   **AI Integration:** Using LLMs to simulate Part dialogue based on the `Narrative` and `Strategies` attributes [cite: 35, 36].

---

## 8. Summary Table for Researchers

| IFS Concept | Computational Primitive | Observable Metric |
| :--- | :--- | :--- |
| **Part** | Autonomous Agent / Class Instance | Activation frequency, Resource consumption |
| **Self** | Global System State / Attractor | Stability of the system (low volatility) |
| **Blending** | Control Overlay / Masking | Reduction in 8C variable scores |
| **Polarization** | Deadlock / Negative Feedback Loop | Inverse correlation of activity between 2 nodes |
| **Burden** | Malformed Data Payload | System interrupts / "Pain" signals |
| **Manager** | Daemon / Cron Job | Preemptive trigger response time |
| **Firefighter** | Exception Handler | Spike in entropy / chaotic output |
| **Exile** | Encrypted/Sequestered Storage | Latent system charge (potential energy) |

This specification provides the foundational architecture for **IFSKit**, a library capable of modeling the complex, systemic nature of the human psyche as described by Internal Family Systems theory. By rigorous application of these data structures, researchers can simulate internal dynamics, track therapeutic progress, and potentially develop AI-assisted therapeutic tools.

**Sources:**
1. [ifs-institute.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH_BPRtnv9u4bpglsNLDjPAzqpGl8xpJmIst3CMI17o1PE1IWJV81FrdGI2wFAbtK73rUlQSesL8F_KO4JJHScBGZb51f4c7orMj6k6yGL1pnecnvmmlnLCpqhgXmK54V1nrSdQkT53ryuMZ5cU48g5w3LPQdf8CEVQToKErDEUOfjQTcW4_68=)
2. [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEWQNj5QSzrNc20ljHF1MEWXttDUGbCG7s2trcFZ3bMmDcyH6QohDTmtV94o3RykaB69E7dLlrcT77qxxY9DakDImSQw2CQUIFsBaQGsNywnRVpp3VNSSLjr2x-zgxxJM5AVB8k-qUyfJomiZOuJSg0)
3. [lucasforstmeyer.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEu9xGjRG3Ne0EqkKX2EPgXFL91KbHSUtc8vmRgMMTcq9d5tek5872W0VjGoULv3exGyWgbj7lDiYlt4JJKICCMrh3AmPA4P5vr-q6b5DrsmTdJcuAsXQMGw_q-1ZPYpFBbf9jTV8vjzMBSy86rfHyyZK1RYJSHeEOWFd6vEQ==)
4. [internalfamilysystems.pt](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHbpTozJ62Bjr4VUYZXElYU32dBtakEtYYh7lUwRF9s6ZgE8tFnCTcAqN_bQQOZfth1vptrYgD9UsY9rxcNZP5r5nJIZY6T2eOicjJtK-4rNWRrXwX4TJOA_HHbp-LGgOr9hLycIAwMvtYQePRlEQILG2d6VfCHK96LeW514c-E5ozoUHDu-bNdFTVRm6bq3XGtUPol)
5. [casuallyluxe.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFgnYzyRFWQQEisWsc15_zaFHBu1QUzidpg2VwpKK4b8C9wSQCT8PQTtHx86wwyDiHUS_0TdP1U63gWMaPWaSNU38l4FMk0Z3mXb43G3Rl7MKSporARe-HdiLij8QGlcUm8)
6. [ifsguide.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFtNVwXc4FrovzHF4l5_3w9icgdYqVIhHfs2sGScpXxpu9uuewAei4b3J0ACYGM_8jUsewOwmdL39qUKP_cRpdP1dtfrFDrvSQ4Km_rpO4SIrwXr5maYCav47CeDq_f4mfbuqKxHPnEsjEIRfc2Uw==)
7. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEryteJcLHUCqhV0SFsWR3BWBSJf-OENwdyOctZjCpYFgaw9PwdCwIwn9zOcxJCJcZvZzF5mw0ClHzBzid3SVyhiQ8LY5vi0XQtBB56N_zANA-OdrjBTO6kPQag_zHoQ1TV-S47To4Nipj8oSVuOLgh28-DGsO1VSgWp0Bi_bcPYmQNgTFupY7kexinnUBLHgh-HzI6qWcu)

## 8. Summary Table for Researchers

[medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEryteJcLHUCqhV0SFsWR3BWBSJf-OENwdyOctZjCpYFgaw9PwdCwIwn9zOcxJCJcZvZzF5mw0ClHzBzid3SVyhiQ8LY5vi0XQtBB56N_zANA-OdrjBTO6kPQag_zHoQ1TV-S47To4Nipj8oSVuOLgh28-DGsO1VSgWp0Bi_bcPYmQNgTFupY7kexinnUBLHgh-HzI6qWcu)

8. [ifsemdrtherapy.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5xiestWE3JqGlNGpDA13HF4pG_V3AV4p7JHdivYu_WqFzLqbFOV2UfUJ1BUrUgbpxK0QVr9rgGYiLFHv5Zq7gjc86hsb9Vbv1X01i7Loc-1X88B5nnk6W85KXyA6i61uN9bRm3PS-GRhBvzOLeQDg3CWvwasDVeOq0fWbIof_9zblsIYbJj_TZPxfYQw88ld92l0=)
9. [therapywithalessio.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGPI-Eud0Q3zdxGn7u4rR4m-lQ93BgNeO1ae8wGexr87q9FPu0lbBH9qu6SQq5kW7e7rsGo_cTI7baNhGwONBysTRtgwz2j4Ao_e-EXgRUSc1XtVnnRBP-tuArK1AdU8YKn2o2KBN28StxtzkDDfXd8GWCgYFWg5V0Z4ddYcOaTxBJQUJDcaszJJqEd6TXFq6-M-LwsorGiHIAnT9MqzeguZUg59Uod)
10. [rocklandrecoverybh.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFkkBjy7Dxwems2SW0wGsMofTU4gQppEqMK-hfhLZLBkIJMNjJzwhJy7jt1TJImKxF5E1vLwtFrRi_AhGJrVu6dfmr2UuB2azqlY9erDXfmHrbdHDJyIU5lH2Fg0eCx-ssUbYn3rk6JBBe6pk8g8Un47QXBAknsfnZiO46IKsIdSefOn-54qJjD9LYRfN40kxJ6-kP8IaTobQ==)
11. [gettherapybirmingham.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGmSbEfcbVQG9GuN-AJeVrkcigOCz0_sF6UQ_HFmNsx4b1naygeMXvH8CYolWfGNZHjF6fAlXpR8RDL-RoVA4LhQx2NxqLjuPitrTC-NraM0QJg5FJg2yU4k-lwANc7whSfqnyDYEFW00MZ-YEqFL9spncnEF81NkIkKdW71J07r1vf_BFCj4VsT0A2)
12. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFUZsOJp1rUgybzaPW67dZyINL5VSS9MB_vMFWwm8QEbYjnGqIaAK_x0vsQ8piw8S2GEUAnyhpyF57YwxCXs-fP-fxuFw68Bs0kWx90WbNTp8KjScfK3pURuc-MZbgHxtG8V1xY1uBFOH7pWsvMRLCgvscQjEafQbyiw1L6ij7nccwri_DIb9gA8GcwQdxOPzKz02OIH4d93lEUBNfru57McZ7GkpaN44McxRsfNv9buo4BLyiCAgrCwzclLFGIzOeIdU31hXvOoEWhQOzdWBU=)
13. [louislaves-webb.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGnodYsBgc7l7mRvaxjK5lJTcN4rcpMPozTKjRhiEdv9rE3bl5rQ3ujo5TTZhzt6S8FxzbhiwzEHxwgjSDnWp-FpSslQXQUSs7sBWbyljyuyGKR9NPFlOkCaPZhEn7smcjAT4E9bAiY54zTU_6Dg6GL_W4=)

## 8. Summary Table for Researchers

[louislaves-webb.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGnodYsBgc7l7mRvaxjK5lJTcN4rcpMPozTKjRhiEdv9rE3bl5rQ3ujo5TTZhzt6S8FxzbhiwzEHxwgjSDnWp-FpSslQXQUSs7sBWbyljyuyGKR9NPFlOkCaPZhEn7smcjAT4E9bAiY54zTU_6Dg6GL_W4=)

14. [everythingifs.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH1XhKGGTXUpDeZTcT_gGZNgXGo4o6321Twn6laQHv4VXEDjucqMoRzQFhOhKyHsNmmCKKi6ktaaJiIMzI8JOywL4L8feBW-AtWNTyw4FTEOyLflmpMMY8qJ3tU9tVmYYVJDkRsa0dQ110-MsvLXCgJNSMB5dhGBXqYsSaD6hakgQ==)
15. [stroudtherapy.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFpY5wVW3dxKw6iGFWmYE8710rxEkhVMROIneQpHCbLfor2MPI5VMo9nq-oPlfjckB8Aq1j1taHIrUhsdLry8g91cUnoMwqmG9PRABvIM8hr5qHPCMSDJHDUXerYeu9QD9lHNNREWeUsEAb_dZY)
16. [ifsguide.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGGg9Rx1Pv7Ymn2UkWeymBSOox5MxjJBsNOVV53b8BDju5sC80yXFWIu2EK3E44og4GCWxrTEEfSSryn0nUdAeK_XqD5Ti3E86OI_KxD9UxnMYmQVCkr73RFJIZvUSBCyWjdr9Zwo2__w==)
17. [seancuthbert.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF2iiGqA4YXU8P5xtGpu8vomC2tme1JKRU9p9yTMsVBmE_ptnH25_BfIYTxGgWsIC2RWEnQpFXq2mXPnTafPxMJiLB3g4vL5vOHTw6INVdO_j3hCfgD6v2KxuBcSVaLlN0yz1hF2nEtznWT9D8C6zRAUMuAQ7osfnmfH7wmUQXPTZB2sIcmvEe0TbozTgc4SFIsN6nl6Nx5KaDmG8damEULwA==)
18. [therapywithalessio.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHreW-4zb02XQupiA0u9JovKMHOQ4ZFZpLJ4RnVkxUZgBMu84IczyN_ycdcZp7n1gx7R6MLLUQjSWDsXXK5g8sc1vcsgBEndVS21kylvwPBs_CqZTt1Gn3FLIsN88XCnp0q9HXJFQfJXHOM3mu_YuyjZjvU2VXj81YjuvJtnqIDfdMaBU-stT_zbKK7sx_2RxioQUMUqmvAw0vT)
19. [ifsguide.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFCZbwq65XZRKnla7CEeVTpAThYCCZFCVv5h7Svjy0KQk14YhhwB8T7k58WiESwAkaD_2TTqLY9aZ9HD6KsAb37X5vd6EcYDe9GA4FTJkH-ny6zFfQi9CZliT7RN9VlYZhUZCblG53qXoAV_2E84CIwJkPg3a9R63If80eIljZttOJDthXtOtlFBFxorg==)
20. [intensivetherapyretreat.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuboLMlXWI_XpHijpfkjBlQHkL2utEULRjGfzm_1ua5W4SBhYS5l85BpyEIMv9xrXRtHQOKV55hcRHI3h9VY-1q5XFdwbyyIq_qq57sk72Oe96kAySSpbF9sc0gRtHWdud6jBJCBeRlFc=)

## 8. Summary Table for Researchers

[intensivetherapyretreat.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuboLMlXWI_XpHijpfkjBlQHkL2utEULRjGfzm_1ua5W4SBhYS5l85BpyEIMv9xrXRtHQOKV55hcRHI3h9VY-1q5XFdwbyyIq_qq57sk72Oe96kAySSpbF9sc0gRtHWdud6jBJCBeRlFc=)

21. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGyVntWuPOXttGpA3lwafKn-z1o147skTnAQN4kqSrqRErJh0G8DUGGucgn18jOx0y1pd1sCPaEA2aI6fHri0Hf56H2_XjF2Boz-nXmNvBcHQowbS3Dbv97vGxF-7iq4PLLPLSb8fGMBSiOmR6VYAbVQ9fNvj4xdGlKySKIjl4iOzu7bg==)
22. [therapywithalessio.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQElCSbx_sp0ZJG_RnnXTyk2T8CZowSW_3z6nGtDnAAqq-pQLcD8hXtggcg1BbYlYHlx-g53ztNgbotpm8hBTTwRki0aMvjhcULOE44KgkPnBAVdVu1KspFTFemVk124qBekUyQlwlsLg2-8cjSZnHRrR9Go)
23. [everythingifs.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHBTS8rr2VfjJZvwp2LpUeFg8mC8i17qn6e2hoUeiL8RDXGuosV31lW4xmNaLtEVmkIcZ1z02p5oR_zaYvrUC5GoQzqnW-gW7IvrfHacYSgr3HuyZ60XYP0LasrQDNFrF-ksGIRIRcMkQZKNZGdg_BKPt76GQgso3c4ibT7uruU3Em185ngmLHdZ_nm7jXL2ofV5BcbgSjTc6KYPtBPok1fxSAtsg==)
24. [partsofmetherapy.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGFqNH5HwkoD_vwF_pczjzHWvkGrGHQxcmH-Tmf1Tb_wVYPwuE7xHY-tu6SYZBeQOriNFWCOMEFw5yPdFAYHl8HUZAn__P2hpZT-Bc5pqFLzPBYpbUw4auw7c7VrJh53K-JhlciHTmhpVDw03yNmTfpP94=)
25. [silversparrowcards.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFF0_nPO2bGpn35_t78ZkrIpMmulolW2odyyqK__zhyAiHZOd321a38SAYx_kZb5ooU1fIerp9rVLATggIwgOvNtlcWIouewBUNg1-J7Xu70bk_fmq6dvDitwLoQlOfRNvfjFjgOeD2ykMBaWvHKtA0Il1XYzVkqROm-mlp5q_1K8JekrbV5NEiUzeh1Q==)
26. [kendhalhart.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFV0ENMoRdhbLOgHZy5Dg-stRsuqsKvrktf-TkgJe0RoJzuEIFHKiVlApvacm9BDS6R7wv0MCrKLYyy-kttLxYKBuZg5w4jqlaX-D4PGAcPn8PsqkvsV_a4KWv7ChTGHNM12A==)
27. [teachablecdn.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEVDsr3cwbHheFvzu21879i80rINsWaGePgkpHGkKYgNrwjdVeS1jsa4WnDr2pPt3AjY-cSG2EKopsLTroJyEdAW82GdrnEhKPGMxq_FR7KcM5d4TYX6NeShwOPeBUh45UHYZZAW90FyHd83Wha2qOl0yJvUIeN0R8H6UAzg4KHV--E536o0cZ9U7rGN_zt_IS-pYZsWzj3dLw2ngLLTCMz4MbxG5LL)

## 8. Summary Table for Researchers

[teachablecdn.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEVDsr3cwbHheFvzu21879i80rINsWaGePgkpHGkKYgNrwjdVeS1jsa4WnDr2pPt3AjY-cSG2EKopsLTroJyEdAW82GdrnEhKPGMxq_FR7KcM5d4TYX6NeShwOPeBUh45UHYZZAW90FyHd83Wha2qOl0yJvUIeN0R8H6UAzg4KHV--E536o0cZ9U7rGN_zt_IS-pYZsWzj3dLw2ngLLTCMz4MbxG5LL)

28. [creately.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQELjmMD_GmkcL8LO5spJeH_5MyC_dFHx_DfMMLufcAF5VWs-QoTadAl2id2VXYPTKEHywZoi2erPfRIYwRgMXgKuzNNlJRsIXeyFVl48b0Rx39a4Bt8XGZZXlL_uXMXfIIVPHQVmEUQRBOKcPVT5F_vYA==)
29. [lifearchitect.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF04Anm4DppecgmGdTemPYT0O7NBm7f6zTt4qLXS8Ynycxm42pNw3SurH6J-zoxTh5PnkaQNT7A6YjL60UNRKr554SCTt3GM2Km9AgQy5ai-gFofsEztCULITcZ4x_NuszoryjDDyEAyPUBYapPQQS0AemC3YXt)
30. [supanote.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDpFRKu8rHwn0uQbhdDIeGDfOrPF2SRl1Ao4FPoRYXiJMPe9NqO3By8XQvtVK7-mYEY6_3jGYWgnnqaG0ggwLU41U-zHvRl5wQg53zZYAvdSeRwDg07idzrWqdxhBssGlVK9z94Urf6ePqK899DW_Ak7wApg==)
31. [ifsguide.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFUYbGSMdTSThIIsAFRmTbZ0Acak1lx4OFq8RFtgCntlicGNijegDUmmQq-xMoxQAun5L63BJf32fFQi6kjpaKTeLjCq2VJYAAA5vPgydAVgUUtyyWr9yXqiIgw-S-UxCcWeUTe900V_Y9gyaTY0Bk=)
32. [sonacollective.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEL319qT-9zTJ_rgdfBvwOGX4lMiIJ0Izuiub7yFoPKg_4dlxJFM-vJP8H7YuOJKByQv-XZwVAhDoZwCcUHvu7EYA96UkF7_CfhC2VVukXuEzRHuZgQPg4ZIvQhuW_DVx46wtWlZbaKRHlAqHxlQRntKUH1gteK_kbc)
33. [therapycenterhouston.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHTDChkNuI1aKjfVP9LWynIAkwNR25InZtB3ptwyfF-KbrBxyEpKZ3FoaB4fEVsR-FR7uCsA2aAu-xyFtglcVZRMIHC4ns20tqryRHfDS8CO5570jtxy0049htg6nmBTItLL_VMlzSHURJgqgbyN1JHu-4Lxdi7oUywg961xg==)
34. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEp8tnSr_Pf0sA5Yym8zHcq9eXKKKADoRgxIPb1wgk8Z6X_7b80myf2NNBwwNwFBP4Yp15AOEQTXdMqWbZFUIaoHEjhLnBu4AruaQUsJsKDCPsc6xwEPTdyhnahQjIMYmeI819-gB_MOJJ5jcaY897o8Rffm9i62r_HDkEA4i4--ld67uI=)

## 8. Summary Table for Researchers

[medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEp8tnSr_Pf0sA5Yym8zHcq9eXKKKADoRgxIPb1wgk8Z6X_7b80myf2NNBwwNwFBP4Yp15AOEQTXdMqWbZFUIaoHEjhLnBu4AruaQUsJsKDCPsc6xwEPTdyhnahQjIMYmeI819-gB_MOJJ5jcaY897o8Rffm9i62r_HDkEA4i4--ld67uI=)

35. [partsandself.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEjjOtSbTeJehHJ6uSLChUN78mYiJg-Fcij4Cag7kHvV637FHE-_osZtocTC4AaANntqRWWlpafOO9gwBCvwbIHB_l9lvf_yb6NWCsdXtIiB1knXkbFUJ7POeAsEM43gzAIDgjm_Wu4EBvo3UT3oDInePu1xwml0S7DSn4atn3K7bLMfk9EWEyzs_ecHjF6iCEE9Y_OAytfljITmwUEQfRZynSS)
36. [allbein.gs](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHsKYZFKR5CHof4MMqKBpHJJk1YXJzyqIabwnczCJbzVKq2iWwKeg23RcR7W23zyIK5m-xzP_Dujh_P4ksdxgsa0_h5RIoJsCVDRwu8)