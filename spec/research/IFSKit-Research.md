# Formalizing the Internal Family Systems (IFS) Model: A Proposal for IFSKit

**Key Points**
*   **Concept:** IFSKit is proposed as a Python library to simulate Internal Family Systems (IFS) therapy, modeling the mind not as a unitary entity but as a multi-agent system (MAS) composed of interacting sub-agents ("Parts") and a central coordinating principle ("Self").
*   **Framework:** **LangGraph** is identified as the optimal foundation due to its support for stateful, cyclic graphs and "human-in-the-loop" workflows, which mirror the recursive and relational nature of IFS therapy better than rigid role-based frameworks like CrewAI.
*   **Differentiation:** A critical distinction must be made between this proposed library and the existing "IFS Construction Kit" (often shortened to IFSKit) by Larry Riddle, which generates fractals [cite: 1, 2]. The proposed library would be novel in the domain of computational psychiatry and AI alignment.
*   **Theoretical Basis:** The architecture draws heavily on **Shard Theory**, **Global Workspace Theory (GWT)**, and the writings of researcher **Kaj Sotala**, who has extensively mapped IFS concepts to multi-agent reinforcement learning and AI alignment strategies [cite: 3, 4, 5, 6].
*   **Application:** The library would enable simulations of "unblending" (decoupling agent objective functions from the global executive state) and "unburdening" (rewriting traumatic priors/weights), offering a testing ground for AI safety (alignment via parts work) and digital therapeutic interventions.

---

## 1. Introduction

The convergence of computational neuroscience, artificial intelligence, and clinical psychology has opened new avenues for modeling human cognition. Internal Family Systems (IFS), a psychotherapeutic model developed by Richard Schwartz, posits that the mind is a system of discrete sub-personalities ("Parts") led by a core "Self" [cite: 7, 8]. While traditionally a clinical heuristic, IFS aligns remarkably well with modern "multi-agent models of mind" and modular reinforcement learning [cite: 3, 9].

## 1. Introduction

Internal Family Systems (IFS), a psychotherapeutic model developed by Richard Schwartz, posits that the mind is a system of discrete sub-personalities ("Parts") led by a core "Self" [cite: 7, 8]. While traditionally a clinical heuristic, IFS aligns remarkably well with modern "multi-agent models of mind" and modular reinforcement learning [cite: 3, 9].

This report outlines the architecture for **IFSKit** (a working title, distinct from the existing fractal software), an open-source Python library designed to formalize IFS as a computational architecture. By treating "Parts" as distinct agents with independent reward functions and "Self" as a global harmonization process, IFSKit aims to provide a testbed for research in **Computational Psychiatry** and **AI Alignment** (specifically Shard Theory) [cite: 6, 10].

This document details the mapping of psychological concepts to engineering primitives, proposes a concrete class hierarchy based on the LangGraph framework, and establishes the criteria for a contribution worthy of the *Journal of Open Source Software* (JOSS).

---

## 2. Conceptual Mapping: IFS Concepts to MAS Primitives

To engineer a computational version of IFS, abstract clinical terms must be translated into concrete Multi-Agent System (MAS) primitives. The following mapping relies on the premise that "Parts" function as specialized sub-agents or "shards" within a larger neural network or decision-making topology [cite: 5, 6].

### 2.1. The Taxonomy of Parts

In IFS, parts are categorized by their roles: Managers, Firefighters, and Exiles. In a MAS, these map to distinct agent behaviors and objective functions.

| IFS Concept | Computational/MAS Primitive | Functional Description |
| :--- | :--- | :--- |
| **Part** | **Sub-Agent / Policy Module** | A modular unit with a local objective function, a specific set of priors (memories), and a distinct output policy. In Shard Theory terms, a "shard" of value that bids for control of the motor/output cortex [cite: 6]. |
| **Manager** | **Preventative Control Agent** | An agent with a **loss-aversion** objective. It scans the environment for triggers (trailheads) that might activate an Exile. Its policy is *proactive* and rigid (e.g., "Always ensure X happens to avoid Y"). It uses inhibition signals to suppress Exile activation [cite: 8]. |
| **Firefighter** | **Reactive Interrupt Agent** | An agent with a high-priority **emergency override**. It is dormant until a "pain signal" (Exile activation) crosses a threshold. Its objective is immediate state change (distraction/damping) regardless of long-term utility (e.g., crashing the system to stop a process). It operates on a short time horizon [cite: 11]. |
| **Exile** | **Trauma-Bearing Node / Error Signal** | A frozen sub-network holding high-magnitude negative reward history (trauma). It is usually sequestered (inhibited) by Managers. When activated, it floods the Global Workspace with "pain" (negative utility signals) or distorted priors, forcing the system into a failure state [cite: 12, 13]. |
| **Self** | **Global Coordinator / Meta-Objective** | The emergent property of the system when no single Part is "blended" (hijacking control). Computational equivalents include the **Global Workspace** [cite: 14] or a meta-policy that optimizes for system-wide coherence (entropy reduction) rather than local agent rewards. It possesses "Self-energy" qualities like curiosity and calm [cite: 15]. |

### 2.1. The Taxonomy of Parts

Computational equivalents include the **Global Workspace** [cite: 14] or a meta-policy that optimizes for system-wide coherence (entropy reduction) rather than local agent rewards. It possesses "Self-energy" qualities like curiosity and calm [cite: 15]. |

### 2.2. Dynamics and Processes

The interaction between parts is defined by specific dynamic states.

#### 2.2.1. Blending vs. Unblending

*   **Blending:** In engineering terms, this is **Priority Hijacking** or **Winner-Take-All** activation. A specific Part's local objective function temporarily becomes the system's *global* objective function. The "I" of the system becomes indistinguishable from the Part [cite: 16].
    *   *Implementation:* The `Part` agent writes its state directly to the global context, suppressing inputs from other agents.
*   **Unblending:** The process of **Decoupling**. The Part steps back from the executive control center (Global Workspace), allowing the Self (Meta-policy) to observe the Part as an object rather than being the subject [cite: 16].
    *   *Implementation:* Moving a Part's output from the "Action" channel to the "Observation" channel. The system can now query the Part's parameters without executing its policy.

#### 2.2.2. Trailheads and Triggers

*   **Trailhead:** A **Feature Vector** or environmental cue that has a high correlation with the activation of a specific Part.
*   **Triggering:** The specific condition where a `Manager` fails to filter a `Trailhead`, causing an `Exile` to activate, which subsequently triggers a `Firefighter` [cite: 17].

#### 2.2.3. Unburdening

*   **Unburdening:** The transformation of a Part's function. In computational terms, this is **Weight Re-initialization** or **Policy Update** based on a new set of priors provided by the Self. The agent retains its existence (computational resources) but releases its "burden" (maladaptive rigid constraints or extreme negative reward weights) [cite: 18].

---

## 3. Core Classes and Interfaces

The architecture should be modular, allowing users to define custom Parts while the System handles the dynamics of interaction.

## 3. Core Classes and Interfaces

The agent retains its existence (computational resources) but releases its "burden" (maladaptive rigid constraints or extreme negative reward weights) [cite: 18].

---

## 3. Core Classes and Interfaces

The architecture should be modular, allowing users to define custom Parts while the System handles the dynamics of interaction.

### 3.1. Class Hierarchy (Python Pseudo-code)

```python
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class InternalState(BaseModel):
    """The Global Workspace / Context of the System."""
    emotional_arousal: float = 0.0
    active_blends: List[str] = []  # IDs of parts currently blended
    memory_trace: List[Dict] = []
    self_energy_level: float = 0.0  # 0 to 1 scale (Curiosity, Calm, etc.)

class Part(BaseModel):
    """Base class for all IFS Parts (Sub-agents)."""
    id: str
    role: str  # 'Manager', 'Firefighter', 'Exile'
    intention: str  # The positive intent (e.g., "Keep the system safe")
    burden: Optional[str] = None  # The extreme belief/weight
    activation_threshold: float = 0.5

def perceive(self, state: InternalState) -> float:
        """Calculate activation level based on state triggers."""
        pass

def blend(self, state: InternalState) -> InternalState:
        """Hijack the state; apply local objectives to global state."""
        pass

def unburden(self, new_role: str):
        """Update the internal policy/burden."""
        self.burden = None
        self.role = new_role

class Manager(Part):
    """Proactive agent trying to control environment."""
    strategy: str  # e.g., "Perfectionism", "Planning"

def act(self):
        # Implementation of preemptive control logic
        pass

class Firefighter(Part):
    """Reactive agent for immediate distress reduction."""
    impulse: str  # e.g., "Binge", "Dissociate"

def react(self):
        # Implementation of extreme damping logic
        pass

class SelfSystem:
    """The central coordinator (not exactly an agent, but a mediator)."""

### 3.1. Class Hierarchy (Python Pseudo-code)

def act(self):
        # Implementation of preemptive control logic
        pass

class Firefighter(Part):
    """Reactive agent for immediate distress reduction."""
    impulse: str  # e.g., "Binge", "Dissociate"

def react(self):
        # Implementation of extreme damping logic
        pass

class SelfSystem:
    """The central coordinator (not exactly an agent, but a mediator)."""

def assess_coherence(self, parts: List[Part]) -> float:
        """Measure system harmony vs chaos."""
        pass

def facilitate_dialogue(self, part_a: Part, part_b: Part):
        """Enable message passing between disjoint parts."""
        pass
```

### 3.2. The `InternalSystem` Interface

This is the main engine that runs the simulation loop. It manages the "economy" of attention and control.

*   `step(input_stimulus)`: Processes one discrete time step.
*   `detect_blending()`: Identifies if any Part has exceeded the dominance threshold.
*   `apply_self_energy()`: Injects "Self" resources (Calm, Curiosity) to lower the activation of extreme Parts [cite: 15, 19].

---

## 4. Framework Selection: The Foundation

Based on the research into modern Python agent frameworks, **LangGraph** is the clear choice for IFSKit, though **AutoGen** has specific strengths for research.

### 4.1. Primary Recommendation: LangGraph

**LangGraph** (by LangChain) is explicitly designed for **stateful, multi-actor applications** built as graphs [cite: 20, 21, 22].

*   **Why it fits IFS:**
    *   **Cyclic Graphs:** Therapy and internal negotiation are *loops*, not straight lines. You talk to a Part, get a response, talk again, step back (unblend), and return. LangGraph supports cycles natively [cite: 23].
    *   **State Management:** IFS requires a persistent "Global Workspace" (Self) that Parts modify. LangGraph’s "State" schema that is passed between nodes is a perfect architectural match for the "Internal Family" system state [cite: 21].
    *   **Human-in-the-Loop:** LangGraph excels at pausing execution for human input. This is critical for IFSKit if used as a therapeutic aid, where a user must provide introspection before the simulation proceeds [cite: 24].

### 4.1. Primary Recommendation: LangGraph

LangGraph’s "State" schema that is passed between nodes is a perfect architectural match for the "Internal Family" system state [cite: 21].
    *   **Human-in-the-Loop:** LangGraph excels at pausing execution for human input. This is critical for IFSKit if used as a therapeutic aid, where a user must provide introspection before the simulation proceeds [cite: 24].

### 4.2. Alternatives and their Limitations

*   **AutoGen (Microsoft):** Excellent for *conversational* simulation between agents [cite: 24, 25]. If the goal is purely to simulate Parts arguing with each other in a chat window, AutoGen is superior. However, it lacks the fine-grained state control required to model "blending" (where the agent *becomes* the system) as effectively as LangGraph.
*   **CrewAI:** Focuses on "role-based teams" for getting work done (e.g., Researcher, Writer) [cite: 26, 27]. It assumes agents are cooperative tools. IFS Parts are often *adversarial* or *protectors*, often refusing to cooperate. CrewAI's rigid "process" structure is less suited for the psychological nuance of IFS.

### 4.3. The Verdict

Build IFSKit on **LangGraph**. The ability to define a `StateGraph` where nodes are `Parts` and edges are `Relationships` or `Triggers` provides the necessary engineering fidelity.

---

## 5. Minimum Viable Components for a JOSS-Worthy Contribution

To be accepted into the *Journal of Open Source Software* (JOSS), the software must show research utility, documentation, and ease of use [cite: 28].

### 5.1. The "JOSS Checklist" for IFSKit

1.  **Core Library (`ifskit`):**
    *   Implementation of `Part`, `Self`, and `System` classes using LangGraph.
    *   A pre-built library of common archetypes (e.g., `InnerCritic` (Manager), `Distractor` (Firefighter), `WoundedChild` (Exile)).
2.  **Simulation Engine:**
    *   A temporal loop allowing users to input "life events" (stimuli) and observe how the Parts react (e.g., "Critic blends in response to criticism").
3.  **Visualization Tools:**
    *   A method to generate a **Parts Map** (sociogram) showing alliances and polarizations between agents. (e.g., using NetworkX or Graphviz) [cite: 29].
4.  **Documentation:**
    *   Full API reference.
    *   **Tutorials:** "Simulating a Panic Attack," "Negotiating with an Inner Critic."
    *   **Scientific Background:** Explaining the mapping between IFS and MAS (as done in Section 2).
5.  **Testing Suite:**
    *   Unit tests for agent activation logic.
    *   Integration tests for the "Unburdening" process (ensuring state updates persist).

### 5.1. The "JOSS Checklist" for IFSKit

 **Documentation:**
    *   Full API reference.
    *   **Tutorials:** "Simulating a Panic Attack," "Negotiating with an Inner Critic."
    *   **Scientific Background:** Explaining the mapping between IFS and MAS (as done in Section 2).
5.  **Testing Suite:**
    *   Unit tests for agent activation logic.
    *   Integration tests for the "Unburdening" process (ensuring state updates persist).

---

## 6. Enabling New Research

IFSKit would allow researchers to ask questions that are currently impossible to test without ethical risks to human subjects.

### 6.1. AI Alignment & Safety (Shard Theory)

*   *Question:* Can an AI agent with "misaligned" shards (e.g., a paperclip-maximizing sub-agent) be realigned using "Internal Negotiation" rather than gradient descent retraining?
*   *Experiment:* Simulate an agent with a "Traumatized Shard" (Exile) and a "Protector Shard" (Manager). Test if "Self-led" dialogue (objective function rewrites) is more stable than forced suppression [cite: 6, 30].

### 6.2. Computational Psychiatry

*   *Question:* What is the topological tipping point where a "Protector" system becomes pathological (e.g., OCD)?
*   *Experiment:* Run Monte Carlo simulations of an IFS system with varying sensitivity thresholds for Managers. Determine the phase transition from "vigilance" to "paralysis" [cite: 31].

### 6.3. Digital Therapeutics

*   *Question:* Can a user's interaction with a customized "Externalized IFS Model" accelerate the "unblending" process in real therapy?
*   *Experiment:* Compare therapeutic outcomes between patients who map their parts in IFSKit vs. traditional journaling [cite: 29].

---

## 7. Target Audience

1.  **AI Alignment Researchers:** Specifically those working on **Shard Theory** (e.g., TurnTrout on LessWrong), **Multi-Agent RL**, and **Agent Foundations** [cite: 6].
2.  **Computational Psychiatrists:** Researchers attempting to model psychopathology using active inference or dynamical systems [cite: 31].
3.  **Digital Health Developers:** Creators of mental health chatbots (like Woebot or Wysa) looking for a more robust architectural model than simple decision trees [cite: 29, 32].
4.  **IFS Practitioners/Therapists:** Tech-savvy clinicians interested in visualizing client systems (though the tool is primarily computational).

## 7. Target Audience

3.  **Digital Health Developers:** Creators of mental health chatbots (like Woebot or Wysa) looking for a more robust architectural model than simple decision trees [cite: 29, 32].
4.  **IFS Practitioners/Therapists:** Tech-savvy clinicians interested in visualizing client systems (though the tool is primarily computational).

---

### 8.1. One-Line Description

> **IFSKit:** A Python framework for modeling the human mind as a multi-agent system, formalizing Internal Family Systems (IFS) therapy into a computational architecture for AI alignment and psychological simulation.

### 8.2. Draft README (Excerpt)

```markdown

# IFSKit: Computational Internal Family Systems

**Note:** If you are looking for the *IFS Construction Kit* for fractals by Larry Riddle, please visit [his site](https://larryriddle.agnesscott.org/ifskit/index.htm). This library is for *Internal Family Systems therapy* modeling.

## What is IFSKit?

IFSKit bridges the gap between **Computational Psychiatry**, **Multi-Agent Systems (MAS)**, and **AI Alignment**. It provides the primitives to build "Agents of Mind"—systems composed of competing and cooperating sub-agents ("Parts") harmonized by a central "Self" process.

## Why use IFSKit?

- **For AI Researchers:** Test **Shard Theory** and alignment strategies by simulating agents with internal conflict and "trauma."
- **For Therapists & Developers:** Build tools that visualize the "Internal Family," simulate "blending" dynamics, and model the "unburdening" of maladaptive behaviors.

## Core Concepts

- **Parts as Agents:** Define `Managers`, `Firefighters`, and `Exiles` with distinct policies and reward functions.
- **Stateful Blending:** Model how a single sub-agent can hijack the global executive function.
- **Self-Energy:** Implement meta-policies that regulate system entropy and facilitate internal negotiation.

## Built on LangGraph

IFSKit leverages the cyclic, stateful graph architecture of LangGraph to model the recursive nature of internal dialogue.

## Built on LangGraph

- **Stateful Blending:** Model how a single sub-agent can hijack the global executive function.
- **Self-Energy:** Implement meta-policies that regulate system entropy and facilitate internal negotiation.

## Built on LangGraph

IFSKit leverages the cyclic, stateful graph architecture of LangGraph to model the recursive nature of internal dialogue.

## Installation

`pip install computational-ifs` (Package name distinct to avoid conflict)
```

---

### 9.1. Existing "IFSKit" (Name Collision)

There is a prominent piece of software called **IFS Construction Kit** by Larry Riddle, used for generating fractals (Iterated Function Systems) [cite: 1, 2].
*   **Differentiation:** Your library must explicitly distinguish itself. Consider naming the PyPI package `computational-ifs` or `agentic-ifs` while keeping the project name "IFSKit" (with a disclaimer).

### 9.2. Theoretical Prior Work

*   **Kaj Sotala (Multiagent Models of Mind):** Sotala has written extensively on mapping IFS to global workspace theory and AI agents. IFSKit would be the *software implementation* of his theoretical blog posts on LessWrong/Alignment Forum [cite: 3, 4, 5].
*   **Psychopathia Machinalis:** A taxonomy of AI dysfunctions. IFSKit offers the *remediation* architecture for the pathologies described in this framework [cite: 33].
*   **Woebot / Wysa:** Existing therapeutic chatbots use CBT (Cognitive Behavioral Therapy) and are generally closed-source and rigid [cite: 32]. IFSKit differentiates by being **open-source**, **IFS-based** (parts work vs. cognitive reframing), and **architecturally modular** (agent-based).

### 9.3. Technical Differentiator

Most current agent systems (CrewAI, AutoGen) optimize for *external task completion* (e.g., "Search the web and write a report"). IFSKit optimizes for *internal system homeostasis* (e.g., "Resolve the conflict between the Agent A and Agent B to reduce global anxiety"). This inward-facing objective function is the key innovation.

### 9.3. Technical Differentiator

### 9.3. Technical Differentiator

Most current agent systems (CrewAI, AutoGen) optimize for *external task completion* (e.g., "Search the web and write a report"). IFSKit optimizes for *internal system homeostasis* (e.g., "Resolve the conflict between the Agent A and Agent B to reduce global anxiety"). This inward-facing objective function is the key innovation.

**Sources:**
1. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQElSAcsRg6RfeCtzCifmBDE8Q3JP1edm_hlb4sZWHhS2c_le-iYLK69O-ZKCL7WmABndzMXYqrVKV7M7_YCOHaHA6XP47t90rd3WvxFHIl3pB80SZFq)
2. [agnesscott.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHFgMkwYUvoAiUTC46FRHpd4w_jvMYM5mbkBLWQ0QzIQEMylIt1d5VxObzmcJFGoXUJr9f8S_Rzgb9xynmOAqow4m1xPAI5bnWnEYzk59hE3FiQT7PxgPdqalhS7-bOO2aw-hkY3422mzgFRWvFFG4j2tOgvCFY)
3. [lesswrong.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGtStQaWRSt0mp6EbBGWDuLFds4Ek6juX2-jJZv6z2fID7XKqRMHfo8qGnG9ITUf-qeC3whj82yL8155ddlejaeYh4d9nZsMziVmJZDzxOJU2UUSz9SeTX6Mhuwyf1tSyRW6NXAbXfSWdbw6Hci_hw_4rFovmZra_XJWNj5cvCg9QNfhrabP20kgBdUZhUI6ethaot0WeKxcv4Ww04holsebgU=)
4. [lesswrong.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrsoZMgroY2AiJ5T2KyzUGs3pybHm7bzxWtlTBFDl7IXnL4SpQ3lEHKtO_0iyz9_hOU4DItbEOC4fPdcYz85xWCHOe01yzE443Ewctdd6AWLuPIUxz6PZVH8Wh7ze6TGIYBfv3-tIvBFBnmWPEkfIhcx98YOICqZ-jyoSdI8TYlQHqMRpuzlevmiBPcBgN1e7BG3T17Og=)
5. [greaterwrong.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFr6HPSER6uY4llxhhZss7DY6Xqw4CKC66Jg0Giyy4jYfD9wSM3-yL-DF6FtCpdL3TwVOMffY_0egQhpVhykYQEUrUVob7-H-Vq_9hA1o-WqPT0XtGieNsza_JrcHQhzuJwA3IP6L3aZf-prgM0Mqhpl9O570LkBlZ3SrGevZxnroSDFHbrXcdfdKvShpUXKLv8d71eljRV2XM=)
6. [alignmentforum.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF-KkriOYIMs_uc_Ivn_4MAh3MUGiBXLdtQRAsG0ucVyGp8TQ_VMqtNBfKej7ViUpuwNEXfdvRSHa-i4kk3OHlqZfuet-MvxXAZq5uIK1P-I2DdMcHK390xLlr-jqa9eiI3LmRSJwSNSFXHVyBAtEYDMdoX7sd9D0LvqVVRAZEE0Jwi9PMxNFCImnPDQQ==)
7. [ifs-institute.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE4NGDb_J7TkONT0CuYw0fGhd8rFA5rRCSfI6W1ssbtXLYPhb4ZoGgrX_ob8uGXIV1uRImknHhK0dWPRpfi0GWUPvzzOwS9M4KyNSVmTrwQjfvvGTBNE6zuO_qJHNobC1ARSH1vyc7gvU4MG1TesnquxllOYjsjIh8XaMPhxwb1g6AeKGjZTb4=)

### 9.3. Technical Differentiator

[ifs-institute.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE4NGDb_J7TkONT0CuYw0fGhd8rFA5rRCSfI6W1ssbtXLYPhb4ZoGgrX_ob8uGXIV1uRImknHhK0dWPRpfi0GWUPvzzOwS9M4KyNSVmTrwQjfvvGTBNE6zuO_qJHNobC1ARSH1vyc7gvU4MG1TesnquxllOYjsjIh8XaMPhxwb1g6AeKGjZTb4=)

8. [ifs-institute.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEjwuYfkIJ52U5MDpOc8Zg8K2fFAhSYgULfTAM8Erb6C8bMm13QQ_phX8Pfb54kyhkpOEaf8dPbBNoMPWOH-WXm73VCc7ez1gpEIcdXhlRT-KYIeu_OAqyu3H1J32N7wgRrZ2BmX1OUa5aiXftgfPz0AMI5D4uN6cuMRK62Ot_GzeTsRt-1DAr5Kh4WT506OAUjL7SKtX937NZg6rDOxQtEua4=)
9. [pnas.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHdqBXyCPXWN5WRxLKijrmePSgD66uU4H9ZUPcsawkmvS3tzZZVcnomwDrfcz1ICWZzxBNS4b6B3nL0_fL9VUvlpunKivV6xbS4hf-3KU8Q249CXivCLWZ4GMeTSr7zBWrPWSOCbQ==)
10. [psychopathia.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExGTkkZ_RJ--KKg6J2YolygdPwIzaA2ZVSTYlAPPCnFh8-xEE99AtG-Ar6_qiOe_tqP1lEF_NXEGA2HthqltBZY1_XE0--mo5A5MwGQ9w5yK2vF-pUznHSfAK7Onel_xMbPi1PAJs3imQF)
11. [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGbUQNjcN3DNfaMethym0mfDixCQyuAXQSAfLjY-ji2D_UPma6_MjRZtswyA7qL1MLTncJ3xa3E6Wr6FCxNVhi9bNgailUHCin6xyqHA9rHEAjicn0jRU3rlkWwLnaPl3KqFOz0pz8oREQbNYJYnpNn)
12. [nih.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEh_XW0SNsSXFfpCRiQDiI3VczXbhVCtpLZpAXuFVZ3TkSiM4WkHteuC-YpkHKenRabJtf2_9toAJx52AEqPFvLP1xWIJkE8RkEM1aKzjhoYWIVSTtSaZflANU0i2UUX0tNvLaGxu6q)
13. [lesswrong.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFuc2sD3EyG7-UchPebYqSJZU3SCfGz5tiMnpn0u9G-9s5nrA4sZKXyPZN2l0MZUf6Qz_7wb5oO5MiBeh3WV-QuGZJp-632JXITD4X2s_K9jRaCo-KuIdG4k66vVbgc1ez9s2y3YMpn85BbC_1VuBFML5ql61j2)
14. [lesswrong.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEub_v6zez3QHUNzB3gWMs0zCZEbt_-dCpOHdTT9UjSU6QTTuhv1F_erNAtQjhhqu815fyxnSQgDmRcQKFH4O1CTvPolFfrWwNFhczl1ksXmwFI6dlNqx-LTr-pLDscrcSLwxVBJjrqL7LpnIrfPMtCPQybARUwen5fwf9WxkHrboO5C5gCrIOTG6iaJygcNItuU7HHoyFc2l9VmTsaGtc=)

### 9.3. Technical Differentiator

[lesswrong.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEub_v6zez3QHUNzB3gWMs0zCZEbt_-dCpOHdTT9UjSU6QTTuhv1F_erNAtQjhhqu815fyxnSQgDmRcQKFH4O1CTvPolFfrWwNFhczl1ksXmwFI6dlNqx-LTr-pLDscrcSLwxVBJjrqL7LpnIrfPMtCPQybARUwen5fwf9WxkHrboO5C5gCrIOTG6iaJygcNItuU7HHoyFc2l9VmTsaGtc=)

15. [psychology.org.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHfcZ1plUT9_KqW-BKdhcGISN34R-PoWJ9vVbbCnmo9Xg0PGioJja5L8l6F3v_QzAKPdb0MZTOdGKTgQbmpZOuSMNpNEoETHn-LIs1B-oEhjwGoLXznl1CaVROV_zI-Jr1VBcIP8xPEwJA04daWx3R7jOAr-cnOwgV3Y7sB5pbc1wePA5q6Ul18skSydyERMQJqDq-3-0XCSjIeq85FeVJT)
16. [lesswrong.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH1nRJLJrtbc5zfo2wO97S5Bkoj5xCuR7PMJ4lG5VPPa5pAaz861okZpXy9tRxQ4zRBE01IVHMWB2ZLYPVoUXu1wHGaCkZ8XFMvPYHVEtqlrymzB4NyCl9E6oqR8z-IYElzV9SarKhLOlHVwPoFR7gstBSWijqy3v-hf7VLKF0NUlcpGkQeULRjixBt-0HKUjNWPAff8w==)
17. [riazcounseling.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGizRrmIcCfQA3tULP1yJAxvBMlJxzenygqSf1xPsLsFr5XrBfNgsCmn5uZLta19uAGH5LcKAr-qMnrZcSZsOi9Gil5vHUcGM7d9B9iKIwbQN5JhXGox7Y8FEPnSl-z_aiGfYB1KPPJp646ogWMDGgC7nmaruxq7ZZI6e3kHClWYJX0E7v20qdfcQ13j9TKg5IGe6tZZsim0wM=)
18. [simplepractice.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHjHwhR4Pu9MmdWMzzkdbRqw_ME0JxXEukjz8OPuudwqqrRRt0KdjbKhgvQPAs9_U-9FTZlfzT447h2TfKQRJ-xjwi7oilQXw2pnBYTzhYXvMAdk113QOniMAouXKBIM2Sf6JHYSIL8Us9Ej9w0IPXcKNPOKdOpYg==)
19. [iptrauma.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF29edyHWf6MsZ4J5M2r6rUbIWgXzuT_srwzISn8jy23hgjCXXOehOOLoDreibQV_IEETXhvstjNt6zoQZefpdYt1yMugH7V5ohAg7IJ0UrHgAGSqs7hbA6aXlFi9P3WrtZdawFp9oZvz-W_TlA0Dut1uU0hwEz8-R_eB3hnL__aPMWAdXRhHXneZB7xekrimD6cXUd4loFF536g6ihRQ==)
20. [peliqan.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH0tlvVXZZggy8SDcrCJes_RIN8h44izb0B1aixtPU1dVjB4BPQlzSMULuO1v1KENhK_EZ8nEvVicAxwjutWiUwjoQaJky42mx5aMB9KVhKgv27y04HrYAShR8CBcJ3iLTteA==)

### 9.3. Technical Differentiator

[peliqan.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH0tlvVXZZggy8SDcrCJes_RIN8h44izb0B1aixtPU1dVjB4BPQlzSMULuO1v1KENhK_EZ8nEvVicAxwjutWiUwjoQaJky42mx5aMB9KVhKgv27y04HrYAShR8CBcJ3iLTteA==)

21. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE5yFo8IxGmqdQx75ciiLaBByyhPNwwvGY6hVMe0EUXfRO746VYqfcmTaCLtakf7zD9DRgH2QTO5U_kdQJpUgGWuWELE8YS-QJJoU-5Ze3ROQABYbvW3FC-L0mtLvhRL2H6OBxpt7PJ6_ZgRa2q647r5q-ycwHC-zOtXpCVTX1HCko5pYI1tYvm7M6bAxI4LhvLem54VUpvbtlaz8wbEsFU27YJaZZfEbvN4174bSKu56Jc)
22. [openagents.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGfhxtBqtfo8JeUvakBx9hK6h8NVjMtzCUVcYcPWHzia95dW-_VjtLtpFdOEu5NqwmYF2fiBYEHicC1MaREnaRu94Cqi2FD4G2EwIck7ZEodY_kBSNJ8cP_l29jMCJAjAq6D2-nnGp3cFsQ6LPA4WfdURpSSc5UyAxPjFX-h_J6tMpm_23csvAe1QE=)
23. [aithority.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDxWCjMEft0ZhsJKaep0b0stcCmDYgBJ_JrM8kMt0l19GO3eGWz_KRXD8SgavnnG9WoItpv51jbK5ZYkQLP6UruAoHziKTRYGL3KiHR58ijw2o2-546nFeiCcrV3Hn5wha5oRwk1dEXuZxKwq1AuVMmEEYvCL0rDTNSj8ZTZO7k3G3PB3KPiyPrr96InLciIdRcn5H5gHnsmiByOGv_R-CV5GMTkCmFoQ=)
24. [aiagentskit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEpEVg3azqOG0-T9w4_iKGLyPZqkHbMtPrJJf4xCwixe3LsWPJyUt-JjXezXaeNenocktgAzIjjfn3dh5YO9tGhKz4AO8X6EM5ghe509X94quLlwMq_bB15PMDkJzv5NUBJdDBTUkQCGHgXee00tTEra8jCdg==)
25. [getathenic.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFQSFiHe2RoOWXwaH_z2-clotKQrLSQrBumNIXwB74lSpBQ5edM5T_BtkAHSGOVmodofRpGwbJ-2h9eU86J-_kFX1L4V7TK877KhAPk2V7xGexgWqD9XpOdHwfde3T_yE8xGS6O4wVDtxQKQ36FH6dvNvXNhh4JJN72UCuY8tIA9w==)
26. [truefoundry.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGRrjPQXaKMyQ0gqXpuN91zih6c0huwbPglqkLWiBpUJLcntcgk2pixqeQCjwSk71pxJKuelZOVXvFXTqHuLtz8e3_1DAvkXbAYfAOzlepaaYylJ6cVBdHrFJx-wsQDnzTvW2Oa9hhFgc4=)
27. [3pillarglobal.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHGWyzU-CLpiEbrMHFuZLcViUKt8v300VaL_FdslwYUneNWSK_efkEV0Pkqam869spVogvHEgldWfSrczVDV9i4bVb5RjgSeeCU2aTKadPNGQaoCAiBhPvOpgtx-44gcQ5XnkOkbZoOBgjANAT7jy_A4RGaf8gDOQTcbdmi7gKns8g=)

### 9.3. Technical Differentiator

[3pillarglobal.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHGWyzU-CLpiEbrMHFuZLcViUKt8v300VaL_FdslwYUneNWSK_efkEV0Pkqam869spVogvHEgldWfSrczVDV9i4bVb5RjgSeeCU2aTKadPNGQaoCAiBhPvOpgtx-44gcQ5XnkOkbZoOBgjANAT7jy_A4RGaf8gDOQTcbdmi7gKns8g=)

28. [riojournal.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGyWXyLX_J3NY1oy1DNlcvzbJvPbG8s-orOcOPDHuGLBdJoCRbtjRd5NIsLirqBDIGQ7F0qMPP-lVye8-U9Wk2PYcL7zpMcihHVCPxO_WVZP0fVOEjbN4yFM8FX)
29. [partsandself.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEWT11rfx-kkZ3nzCjcc0XbMvlSJpdK52e5pw0yaJhgQFUsVH5MwMxB02gO6uuL9VKlEpje58Fcjq1gCWDpZeddSd0wNqDCyBHXNVE3chh2GQzlSojS68gn2XdoY-oaIG-DIGqqU1R6ETQgQjoycxakvHgqIr2U5ZFQRquwx17Lg-5-WBALXfvC1D30X_J6oIHxQIR5uRTM-filbRaIugUQhXMS)
30. [astralcodexten.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFMyZzQIjkpfBkcK164I5B6_FmArm9AZPb2JCMB5MKXoPmYusS-6FTkuK5CgZU2oLNFgbM-VHBmOpuFyddh_Pi9mI-glA8RtXlLcejAQomn4UZwS_Z2EA4fh3mW9Tt8PAb0lRRYeL82onD-CTn1s_HPOs5-z5ba)
31. [researchgate.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH2Wl13nO6qYV3lnB_JO-R21LwTFgQ_q8jl6qA4VbkQs1RmFov3253qexHdlXYfi1-O_maqoNfu0bK6Do1Jao3uDijclbVun4OJW-tB9BMkIsJ4zoTMkVdA77_-wPCZzR-whHFiFJ82BSSF5WaTsJxC6c4rCavDEbTjdcuFwvdyBIXMwNoPuNAtSX-ghSHkY4-7tKpgwnm30ZDaII2--bQ=)
32. [arxiv.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEo1BYWcYVhSPEiRMTujgNFfAXrGqJh-44OuDezp0oAv7surP-yvlxQpkpkcRv9_tIgLYIkLQiGLHSh4xCPDpUlCJ2llndPuqCPrhmUiMDdFVI28bB8x5Ax)
33. [psychopathia.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHBKY5mM8K4HqPhjttnPGtasYqPg2JffAXx3AUrnQ1NjQC0_i6DouZa_H5wpAqIIPU9XAFAN3aNRRwW4Fly37nQmbr3hsMhwjgwSY35mzeNMhg=)