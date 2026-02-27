### Executive Summary

In Internal Family Systems (IFS) theory, the **Self** is conceptualized as an innate, undamaged, and constant core of the personality, characterized by qualities such as calmness, clarity, and compassion. Research indicates that the Self is **always fully present** ontologically; it does not fluctuate in its existence or inherent capacity. However, the **conscious access** to Self-energy fluctuates significantly based on the activity of "Parts" (subpersonalities). When Parts "blend" with the seat of consciousness to protect the system, they occlude the Self, much like clouds obscuring the sun.

Consequently, at the start of a therapeutic session—and by extension, the initialization of a computational simulation—the baseline state of **manifest Self-energy** is typically low to moderate, not maximum. The client (or simulated agent) usually begins in a "blended" state, dominated by protective Parts (Managers) or reactive Parts (Firefighters). Therefore, a robust computational model should initialize `Total_Self_Potential` as a constant maximum (100%), but `Available_Self_Energy` as a dynamic variable that starts at a lower baseline (e.g., 20–40%), inversely proportional to the activation levels of protective Parts. Modeling the initial state at maximum Self-energy would simulate an "unburdened" or "enlightened" system, which contradicts the clinical presentation of individuals seeking IFS therapy.

---

## 1. The Ontological Status of Self in IFS Theory

To determine the baseline for a simulation, one must first define the ontology of the Self within the IFS framework. The theory posits a dualistic relationship between the Self and the Parts, where the Self is not merely a "better" part, but a distinct level of entity and leadership.

### 1.1 The Constant Nature of Self

Dr. Richard Schwartz, the founder of IFS, and subsequent theorists assert that the Self is the essence of the individual—a seat of consciousness that remains inherently undamaged regardless of trauma or history [cite: 1, 2, 3]. Unlike Parts, which can be forced into extreme roles (burdens) by life experiences, the Self possesses immutable qualities often summarized as the "8 Cs": Calmness, Curiosity, Clarity, Compassion, Confidence, Creativity, Courage, and Connectedness [cite: 4, 5].

### 1.1 The Constant Nature of Self

Unlike Parts, which can be forced into extreme roles (burdens) by life experiences, the Self possesses immutable qualities often summarized as the "8 Cs": Calmness, Curiosity, Clarity, Compassion, Confidence, Creativity, Courage, and Connectedness [cite: 4, 5].

Crucially, IFS theory maintains that the Self does not need to be developed, built, or strengthened in the way a muscle is built. It is already fully formed and present from birth [cite: 5, 6]. The widely accepted analogy in IFS literature is that of the sun and clouds: the sun (Self) is always shining with full intensity, but it can be obscured by clouds (Parts) [cite: 3, 7]. Therefore, ontologically, the Self is **constant**.

### 1.2 Self-Energy vs. The Entity of Self

While the *Self* is the entity or seat of consciousness, **Self-energy** refers to the experiential manifestation or "field" of that entity [cite: 4, 8].
*   **Self:** The core leader, the "I" in the storm [cite: 9].
*   **Self-Energy:** The qualitative "vibe" or field of presence (compassion, calm) that radiates from the Self and can permeate the system [cite: 4, 8].

While the Self *entity* is constant, the amount of *Self-energy* available to the internal system fluctuates based on the configuration of the Parts. If a Manager part is tightly controlling the system to prevent pain, the flow of Self-energy is restricted or "occluded" [cite: 10, 11].

### 1.3 Implications for Modeling

In a computational model, this distinction suggests two separate variables:
1.  **`Global_Self_Constant`**: A static value representing the potential of the system (always 1.0 or 100%).
2.  **`Manifest_Self_Energy`**: A dynamic variable representing the current accessible energy, calculated as the Global Constant minus the "opacity" or "blending strength" of active Parts.

## 2. The Dynamics of Occlusion: Blending and Fluctuation

The fluctuation of Self-energy is the primary dynamic variable in an IFS session. Understanding the mechanics of "blending" is essential for programming the interaction logic of a simulation.

## 2. The Dynamics of Occlusion: Blending and Fluctuation

## 2. The Dynamics of Occlusion: Blending and Fluctuation

The fluctuation of Self-energy is the primary dynamic variable in an IFS session. Understanding the mechanics of "blending" is essential for programming the interaction logic of a simulation.

### 2.1 The Mechanism of Blending

Blending occurs when a Part (subpersonality) takes over the seat of consciousness. When a Part blends, the individual no longer feels *separate* from the emotion or belief of that Part; they *become* it [cite: 12]. For example, instead of noticing a part that feels anger, the individual *is* angry.

In a blended state, the qualities of the Self (the 8 Cs) are blocked. The Part's extreme beliefs and emotions dominate the system's output. The "Sun" is hidden behind the "Clouds" [cite: 3, 10].
*   **Degree of Blending:** Blending is not binary (on/off). IFS acknowledges degrees of blending. A Part can eclipse the Self entirely (100% blended), or it can step back slightly, allowing a mixture of Self-energy and the Part's energy (e.g., 50% blended) [cite: 4, 13].
*   **Conscious Blending:** In some therapeutic maneuvers, a client may intentionally blend with a part to allow it to express itself, but this is done under the supervision of Self-energy [cite: 3].

### 2.2 Fluctuation of Access

Since Self-energy is occluded by Parts, and Parts react to internal and external stimuli (triggers), the *manifest* Self-energy genuinely fluctuates throughout a timeline.
*   **Trigger Event:** An external stressor activates a Protector Part (Manager).
*   **Reaction:** The Manager blends with the system to control the situation.
*   **Result:** Manifest Self-energy drops significantly.
*   **Intervention:** Through "unblending" techniques (insight, negotiation), the Part relaxes.
*   **Result:** Manifest Self-energy rises back toward the baseline or maximum [cite: 12, 13].

Therefore, in a simulation, Self-energy should be modeled as a **dependent variable** that fluctuates inversely to the activation/blending levels of the Parts.

### 2.2 Fluctuation of Access

*   **Intervention:** Through "unblending" techniques (insight, negotiation), the Part relaxes.
*   **Result:** Manifest Self-energy rises back toward the baseline or maximum [cite: 12, 13].

Therefore, in a simulation, Self-energy should be modeled as a **dependent variable** that fluctuates inversely to the activation/blending levels of the Parts.

## 3. The Baseline State: Start of a Session

To answer the user's question regarding the *initial state* of a simulation, we must look at the clinical reality of an IFS session before interventions occur.

### 3.1 The "Trailhead" and Initial Blending

IFS sessions typically begin with a "trailhead"—a problem, symptom, or reactive emotion that the client brings to the session [cite: 14]. The presence of a trailhead implies that Parts are already active and likely blended.
*   **Manager Dominance:** Most clients operate in daily life under the leadership of "Manager" parts (protectors that ensure safety and function). These managers often exclude Self-leadership to maintain control [cite: 6, 15].
*   **The "Anxious" Baseline:** Clients often arrive with anxiety, confusion, or overwhelm. These are not qualities of Self, but qualities of Parts. This indicates that at $t=0$, the Self is **not** fully present [cite: 11].
*   **Therapist as Auxiliary Self:** Because the client's Self-energy is often low or occluded at the start, the therapist must lend their own Self-energy to help the client's parts unblend [cite: 16, 17]. If the client were fully in Self at the start, therapy would largely be unnecessary for that moment.

### 3.2 Unblending as the First Step

The first procedural step in IFS is often "unblending" or assessing the state of the Self. The therapist checks for the "8 Cs." If the client reports feeling angry or afraid, the therapist knows a Part is blended. The goal is to reach a state where the client feels "calm" and "curious" toward the target part [cite: 14, 18].
This confirms that the *default* state at the start of work is a **mixed or blended state**, not a pure Self state.

### 3.2 Unblending as the First Step

The therapist checks for the "8 Cs." If the client reports feeling angry or afraid, the therapist knows a Part is blended. The goal is to reach a state where the client feels "calm" and "curious" toward the target part [cite: 14, 18].
This confirms that the *default* state at the start of work is a **mixed or blended state**, not a pure Self state.

### 3.3 Quantitative Evidence from IFS Scales

Research using the *IFS Scale* and *Self-Leadership Scale* supports the view that average individuals (and particularly trauma populations) do not exist at maximum Self-leadership.
*   Scores on the Self-scale are distinct from scores on Parts scales (e.g., Anxious/Pessimistic, Addictive/Impulsive) [cite: 19].
*   High trauma correlates with lower access to Self and higher scores on extreme Parts [cite: 20, 21].
*   The existence of a spectrum of scores (1–5 Likert scale for frequency of Self qualities) proves that "maximum Self" is an ideal or a moment of high integration, not the statistical baseline [cite: 22, 23].

## 4. Computational Simulation Model Recommendations

Based on the theoretical and clinical evidence gathered, the following specifications are recommended for modeling the initial state and dynamics of an IFS internal system.

### 4.1 System Architecture

The simulation should be comprised of:
1.  **The Agent (System):** The container for all sub-entities.
2.  **The Self (Object/Singleton):**
    *   `Max_Capacity`: Constant (e.g., 100). Represents the "Undamaged Core."
    *   `Current_Access`: Variable (0–100). Represents "Self-Energy."
3.  **Parts (Array of Objects):**
    *   `Type`: Manager, Firefighter, Exile.
    *   `Activation_Level`: Variable (0–100). How triggered the part is.
    *   `Blending_Strength`: Variable (0–1.0). How much the part is obscuring the Self.

### 4.2 Initial State Configuration ($t=0$)

**Do not start Self-energy at Maximum.**
Starting at maximum implies an enlightened being or a completely unburdened system, which leaves no "work" for the simulation to perform.

### 4.2 Initial State Configuration ($t=0$)

### 4.2 Initial State Configuration ($t=0$)

**Do not start Self-energy at Maximum.**
Starting at maximum implies an enlightened being or a completely unburdened system, which leaves no "work" for the simulation to perform.

**Recommended Baseline:**
*   **Scenario: "Typical Therapy Client"**
    *   Initialize `Current_Access` (Self-Energy) at a **low-to-moderate baseline** (e.g., **20% to 40%**).
    *   Initialize at least one or two Manager parts with high `Blending_Strength` (e.g., "Inner Critic" or "Anxious Planner" active).
    *   This reflects the "occluded" state where the Sun is present but hidden behind clouds [cite: 3].

*   **Scenario: "Crisis/Triggered State"**
    *   Initialize `Current_Access` (Self-Energy) near **zero** (e.g., **5%**).
    *   Initialize a Firefighter part (e.g., "Rage" or "Dissociation") at maximum blending.
    *   This models the "Hijacked" state often seen in trauma responses [cite: 12].

### 4.3 The "Occlusion" Algorithm

The simulation must calculate `Current_Access` dynamically at every time step ($t$). The formula should reflect the IFS principle that Parts obscure the Self.

$$ \text{Self\_Energy}(t) = \text{Max\_Capacity} \times \left( 1 - \max(\text{Part}_1.\text{Blend}, \text{Part}_2.\text{Blend}, \dots) \right) $$

*Alternatively, a weighted sum could be used if multiple parts blend simultaneously, though IFS often focuses on one dominant part at a time.*

A more complex "Field" model [cite: 8] might suggest that Self-energy is a resource that Parts *consume* or *block*.
$$ \text{Self\_Energy}(t) = \text{Max\_Capacity} - \sum (\text{Part}_i.\text{Occlusion\_Factor}) $$

### 4.4 Simulation Dynamics (The Loop)

1.  **Input:** External Event (e.g., "Criticism from boss").
2.  **Trigger:** Exile (Wounded Child) feels pain.
3.  **Reaction:** Protector (Manager) activates to suppress Exile.
4.  **Blending:** Protector blends with System.
5.  **State Change:** `Current_Access` to Self drops. System behavior becomes rigid/defensive (Manager qualities).
6.  **Intervention (Simulation Goal):** "Unblending" function is called.
    *   Requires recognition of the Part.
    *   Requires separation (lowering `Blending_Strength`).
7.  **Restoration:** As `Blending_Strength` decreases, `Current_Access` returns to `Max_Capacity` (The Sun emerges).

### 4.4 Simulation Dynamics (The Loop)

System behavior becomes rigid/defensive (Manager qualities).
6.  **Intervention (Simulation Goal):** "Unblending" function is called.
    *   Requires recognition of the Part.
    *   Requires separation (lowering `Blending_Strength`).
7.  **Restoration:** As `Blending_Strength` decreases, `Current_Access` returns to `Max_Capacity` (The Sun emerges).

### 5.1 Self-Like Parts

The simulation must distinguish between **True Self** and **Self-Like Parts**.
*   **Self-Like Parts:** Managers that *imitate* the Self. They may appear calm or competent but lack true compassion or curiosity (they are often strategic or controlling) [cite: 24, 25].
*   **Modeling:** A simulation might falsely report "High Control" as "High Self" if not careful. Self-like parts should still count as *blended* states, occluding the True Self.

### 5.2 The "Observer" vs. "Energy"

Some interpretations of IFS distinguish between the "Observer" (mindfulness) and "Self-Energy" (the active healing force).
*   The simulation might model the **Observer** as a passive state (awareness of parts) and **Self-Energy** as an active resource (healing of parts). Accessing the Observer is often the first step to accessing Self-Energy [cite: 26].

### 5.3 Initial State in "Unburdened" Systems

If the simulation is intended to model a "Self-led" person (the goal of therapy), then the initial state would start with Self-energy at a high value (e.g., 80-90%). In this state, Parts are present but do not blend; they offer input/advice to the Self rather than taking over [cite: 2, 9].
*   *Note:* Even in Self-led systems, 100% presence 24/7 is considered rare or an ideal. Fluctuation is normal as life challenges trigger old burdens [cite: 1].

## Conclusion

In IFS theory, the **Self** is an immutable constant (the Sun), but **Self-energy** is a fluctuating resource dependent on the level of "cloud cover" (Parts blending).

For a computational simulation:
1.  **Ontology:** Model the Self as a permanent object with maximum potential.
2.  **Phenomenology:** Model the *available* Self-energy as a variable that fluctuates inversely with Part activation.
3.  **Initialization:** Start the simulation with **low-to-moderate Self-energy** (reflecting a typical blended state) rather than maximum Self-energy. This provides the necessary initial conditions to simulate the dynamic process of "unblending" and restoring balance, which is the core mechanic of the IFS model.

## Conclusion

3.  **Initialization:** Start the simulation with **low-to-moderate Self-energy** (reflecting a typical blended state) rather than maximum Self-energy. This provides the necessary initial conditions to simulate the dynamic process of "unblending" and restoring balance, which is the core mechanic of the IFS model.

### References

[cite: 27] Four Corners Wellbeing. (2024). All parts are welcome: The life-changing power of Internal Family Systems.
[cite: 13] Therapy with Alessio. (2021). Self in IFS Therapy: What it is, what are the 8 C's and the 5 P's of Self.
[cite: 1] Aspire Counseling. (2025). What Is the Self in IFS Therapy?
[cite: 9] IFS Institute. (n.d.). Evolution of The Internal Family Systems Model.
[cite: 4] Therapy with Alessio. (2021). What is Self and Self-energy in IFS Therapy?
[cite: 5, 28] IFS EMDR Therapy Group. (2025). Understanding Self in IFS Therapy: The 8 C's and 5 P's.
[cite: 16] Aglow Counseling. (2024). Speaking from Self-Energy: The Vital Role of Self-Energy in Every Stage of IFS Therapy.
[cite: 6] Louis Laves-Webb. (2025). Understanding Core Concepts of IFS.
[cite: 2] IFS Institute. (n.d.). Internal Family Systems Model Outline.
[cite: 26] Reddit. (2024). Confused about Self and Self Energy.
[cite: 17] Medium. (2025). A Guide to Self-Energy.
[cite: 8] Parts and Self. (2025). An Hypothesis to Unify IFS.
[cite: 20] DeLand, L. (n.d.). Journal for Self Leadership. Internal Family Systems Scale.
[cite: 24] Reddit. (2024). How to know you've met Self Energy?
[cite: 25] IFS Institute. (n.d.). IFS Scale Research.
[cite: 21] IFS Scale. (n.d.). Self Scale.
[cite: 29] IFS Guide. (2024). What is SELF in IFS?
[cite: 22] Steinhardt, M. (2024). Development and Validation of Self-Leadership Scale.
[cite: 23] Psi Chi Journal. (2020). Self-Leadership Scale.
[cite: 19] IFS Scale. (n.d.). Subscales.
[cite: 12] Fearlessly Inspired Solutions. (n.d.). The Power of Unblending in IFS Therapy.
[cite: 3] IFS with Sanni. (2025). How to Access Self IFS.
[cite: 7] Act Right Now. (2023). The Power of Self-Energy in IFS.
[cite: 10] Sentience Counselling. (2025). Understanding Internal Family Systems and Parts.
[cite: 14] IFS Guide. (2025). A Detailed Walkthrough of an IFS Session.
[cite: 15] Louis Laves-Webb. (2025). What to Expect in Your First IFS Therapy Session.
[cite: 18] Sage Soul. (2023). Understanding Blended Parts in IFS.
[cite: 30] Life Architect. (2021). An IFS Therapy Session.
[cite: 11] Thrive Psychotherapy. (2025). The 8 Cs of Self-Leadership IFS.

### References

[cite: 14] IFS Guide. (2025). A Detailed Walkthrough of an IFS Session.
[cite: 15] Louis Laves-Webb. (2025). What to Expect in Your First IFS Therapy Session.
[cite: 18] Sage Soul. (2023). Understanding Blended Parts in IFS.
[cite: 30] Life Architect. (2021). An IFS Therapy Session.
[cite: 11] Thrive Psychotherapy. (2025). The 8 Cs of Self-Leadership IFS.

**Sources:**
1. [aspirecounselingmo.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEn853DGtOkIlPAN4hUDoE-BeVCHJr-L3TpUSNHlIdhcdlLZmPQ3vzJjUng2qfyw09GqBDbo6SQDlFSfLO69WCTo-XgEP-7YYHQPrnZHh116tG47_VQfQuQaOLa41YOO5lScVl9a05dA72vgyJ8WVlIEt44tu9TyLvj)
2. [ifs-institute.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5afZA6IG82-N0sy0r722O16_YAZFg4ZBvhzDTL9-jnKOzEUxQptMS3OTNGXSwGycLYS1Dpa2Ci4SDZkB8Ff5fS1swjz2udPCKS71f57PCiC4ZMetzgiSvhYL3LTeXCLNU0Pi9p5gJ_GWEMh8Uk9jXPIStUDdE1eZWeOcMK3D0TCQjsMFPOEQy)
3. [ifswithsanni.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFRx3vjPDoTZ1gU7fCDc5jHaTW1vOaLfN4flinsUAzZWtQZ7XDyUvV1uggcHfROao9yLJ_x8jvd0XOVkNlvNcwzrK1Nlbkgj0htSdRfU1IHcF8Ez_UMQQtQX8rHpSxjK-HlOjAzcFYVRu9S-gufPA==)
4. [therapywithalessio.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQETO3FsHbWVYKrnEdyt-0pGKAxZ_g7VsQjjRZHHuWk1CC648k0FC2iisIwegMwBdObuYb1cI230ICpMu2CPD6yDotRG27TmVm1Vjv7Es5RXXJ30_B3taK6dgMeCYlKtPf9js2jqKgfZ5X-kW5UmAX5bKwK-d0rxYv_uvNztOL6J7HdNJnS8XryM3g8izjoZM21KaF7YdwUvlqAe6j_ud-owCggapPE=)
5. [ifsemdrtherapy.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEPcI3S0Q0DG6R1RdJh-qqhDwcHNT9gi5mZY1yGjx3QAJMicEdalHiGUJTrXbq7otqdA8NKbsKbxbF3yDHXuQgGtOcbnSiPaf7iZjIt6CUp9jEVLilgUQhhP2pWF3q1829t-hoZituz4hjUMuwKci7Nlhtd31xCUiYokjTXhYvW6obMi799ZSxnt9TDJLQecow2NRVS)
6. [louislaves-webb.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFTW-yUvvz_lcxArRzL63JsAMfMSkEd3iFTXal-SEVMDlasSf4f2-tqbyDwWVtVq-MhTCfj59SHXvnLK_-JbZXYcaWlCxijnYRY9AM80s0EaT3-MEuG6iImGTOlMYHYo_OBzSAY2GA9l5PW14v4K-VQD7DVw58iamjjdg==)
7. [actrightnow.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_oaon0tqYL59UcDcZhmfJsXu2AjdDi7Fa2atZM-9b_yrX3HSPElLmccNZ1qmOjHbJpKbQr5Ksloed7z5jEb_DotX0DERFo_5NKurzmUkKOVbhBvlxtKHp6gPJGhwb43QpLtr50ztGV3RMLQ0M4sivcN8VtB8Brz_nBw==)

### References

[actrightnow.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_oaon0tqYL59UcDcZhmfJsXu2AjdDi7Fa2atZM-9b_yrX3HSPElLmccNZ1qmOjHbJpKbQr5Ksloed7z5jEb_DotX0DERFo_5NKurzmUkKOVbhBvlxtKHp6gPJGhwb43QpLtr50ztGV3RMLQ0M4sivcN8VtB8Brz_nBw==)

8. [partsandself.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE-362qz1yigBLTCsulXXCCdh8n6GUyZ460t7Fmt19lCDtUrE3yRdFvFcelQTI7ihJYhuO9QNaPe9NX6TXiITKqOsqmJ_qZZ-7wvL0yAjp4YXCk1xILkcrEPY6M4kR3RU12gdhZnI1px08c)
9. [ifs-institute.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExXq4sTfyK_qQz77qw13uVoWNkk0mw2L_GOmT8XmRpsVqk2yxagT-YGnCUSFENnD664beRixzv84OpGnX6Y9Aj2Sn50jXQp_pod2Fg1z-xvO_1oUfs1bhDw-vPL_OSg-y6emTGwOsNUO7mP0b9nI94jslZKOoVGx3a3si8jZE7ZfjGOASteoeMJj1ONrQblOoi_Rp1UiOwS1F9Gopc5TMvKtcy)
10. [sentiencecounselling.ca](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGIAzFw96kfSSNQouF5S7XvP6a-psi80oeBXgcjJ1ZBtXjr5H1BwRjfCeTFG0fxEN8aWQPSq8EPaxgMa_-b-N7Je6uLdc64lX-m42KOdcOd4kpiIHHkWXKXvNBprzJ6gaL9T7Ws1UKwhnxMWtEciPucqiZXhdQTdbDAXIpIwaZLJ21PaaEdrg==)
11. [thrivepsychotherapynyc.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGTS8GGYwnktkdimByRCU7nLhkIWuBGZ-Odsn5idEqGuFXZ1ZjpT5HAUsPAQeXnYzwCyyMp6vrSM2ulRMKXPdhBsZdyrDjdotMeKE4jSyjiMn24JN3W0Q7sjdCb3SqSp8QBVEOXCM9OU1EDfU691kTq9F59yRE=)
12. [fearlesslyinspiredsolutions.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFxXH363aN0w27N2aeIoAJx_pOCIYtuNFD6DwyQbInSfcfVcPDo8jjqfgkH6qO3yCdxgmzrXcQgQ4QkSHBnISwnFvE8aXpljvAoWwcfrt2md0uF5Q0ijXn08thvcpuUxZC5Yzv-SrSbUWbCD-GHmJXeyJ_YWZtk0f_WoiZWPdEMj5RLmr2R)
13. [therapywithalessio.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFHlrzOEQWvx-rLZ12mf0WTYObcv2PtgxiU4tctu9E8KaQjYlCY6b2RrYQUbraZPu0t-XTYxy-cSDSHr3UBPncoRsMi3XXid6kegvTVC4iuASfcU-5_9JdwxTlzW31y-P4QM-scysWPHqEVsETE5CjXgM3yn-TixfOa5XeedTmbRpHQy1GRdPG2llt-sxJiokIVlIAp8TkWlrEvKiq1d5p3gxsgNSOgcw==)
14. [ifsguide.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFxGyh-NizjAozUSj-HzGnp8nplMx9UcEv29zrmmoNlKo8Ssa3wR5R37heCO4QcxHEQtAl5FVmhKWKzVYhNQrJf8V731Tczv5eoIsLxLbHjFvjvXbFyasD77foYk-93PxnLPtCCDy24Iphw_cl8TzmyXe9b55M-Y6aOBqZa5ICP7JRJ2xcDKbAufBvaabp_eV3Xhg29)

### References

[ifsguide.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFxGyh-NizjAozUSj-HzGnp8nplMx9UcEv29zrmmoNlKo8Ssa3wR5R37heCO4QcxHEQtAl5FVmhKWKzVYhNQrJf8V731Tczv5eoIsLxLbHjFvjvXbFyasD77foYk-93PxnLPtCCDy24Iphw_cl8TzmyXe9b55M-Y6aOBqZa5ICP7JRJ2xcDKbAufBvaabp_eV3Xhg29)

15. [louislaves-webb.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQETLidOX4NpMgGykgBTHgd2hIwpvfbEMKQjQrPn-oTCux6nVTlof9kHZ10tgWT05kMvaXUgNtrCdaSoJ2ow0ozNI2rE7XrltAoFmPMWO4MO3l7xx42TFICWd8ycnw5S2ghJyidF8Cy3mZQqHCJ0_WJHOXY7NC2XzS2Hw4qhcWyqCA==)
16. [aglowcounseling.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEs9fuE9jAsW_y4sci9iPKvyZiQ0tRsQNnOhzQlHwALZb-HLbVANKCpHGBqXUWAdBiiIO6JG00jSZggUs_4AOVxxw3lz65S2AHWQFwyPq57Lrx9MCj0ykysWdR-fEdyOaZdq06Ktk5Ghn-GMCb82SlccnUJU3ta9cyGJllDVj3cnCqH7_aM2HBzyWWv8886fzhLcilRa40EDRNkMLL3U5_BX8rfpksPSta8ioPOWCtc4A==)
17. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEGGQ9j11XGjY-B_71DiSkf9Zx7cSUH0zuJqcyFZTdoB1AU_TY469A7GSXRxF_xP08QBYIqvyktT2Cgsv-5gmDW30s6k1DLf6kMmBMLW-0ug1UNEFnvz0zukIH0Q6wVjA12Kp1gXedbRwufxv7mgBEauc31KwYNTLN3C8xanXpmr2bE)
18. [sagesoul.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEdbKZ7o5lY8kU76N9FqQxEInKUjD5yzcRCujUHi_9anX1-SIh_uYxf8gh6H7y_H246NTTej85QW5i_o-axY4P9i2CqnO5q9YA7XI_Uu84aTrV-fp1_Pov5ZQAGsjFTtsytEmmY7qhcKQC3p6bV-sY1iilusurR)
19. [ifs-scale.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0YvV0Viozw_IW_a6iMrA2haHK6bL0ce1QwUtlq5uShG9mhYxEFcKmJLKH6umXd-JCwtm-2vk9rblqdgKsP5S5nXmqQ-qbPljyHv1oFzH2lM4evpAZudzV6zw=)
20. [foundationifs.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEFCbJhNP-TU00HFjeLkHhkHqDJ2tpzdvVDIuKoktWNW1oBQEjiP9WjsUv5O39tyTkfomVOQJG-mxdP7d-xIB6YOnxxBke32aAT76nsHLapvzde0T2tw7bODb2NGwQ4xNGPeoOrCAY5yDod-1-0BGHC0s1kvSg5tq0AWJLNVjeRGQ1j5VK0ohRmug==)
21. [ifs-scale.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlzZe65JUI7pARRWnNfb4ktGCCaQ8jXqdDIpQxRtxEe6tSEGvpwPzEGkoT_p6wXLVbnbVTL4hxQIrCYFSrwUYqVDTrJd8J0PGjpQwWBacmZvDLXWo4vSD0rcGT)

### References

[ifs-scale.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlzZe65JUI7pARRWnNfb4ktGCCaQ8jXqdDIpQxRtxEe6tSEGvpwPzEGkoT_p6wXLVbnbVTL4hxQIrCYFSrwUYqVDTrJd8J0PGjpQwWBacmZvDLXWo4vSD0rcGT)

22. [journalofselfleadership.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFBb8X0A6gqsyakY0Ol7HM9URfAJrtWZeSombIBKHBRU77vnSJkd0KftIG8-7kHp_qUUF6Yjmj9Y6VYiHM05KMm7zyIzGd4SfKFxgbj4W_F2m_JxFyjFDhs-i6VRC8SVzm2paugBXFPf6EWFtcfAh20vYfuiMz9YuClwDw5fkNKsiWrSNXHhKgvPreZ7Wlr9-LFT25cPC6DloAq-Q==)
23. [ymaws.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHMyJfevOE0ThSjvJk6hOotDI6L1d-bEKWQ5BERSDWpHkLgIEejx3oEZ4blQupQOJwll3nFWWL9X0RW3EkBdfCkKWGNcjDC6iAEXZ1BAz541C9DaBUPux4-PLztnPJM09FfDP-a2ONz-0YfGS3X8P2xa6sli50Z_5wdqH7IDe87kQ5EEocXiQ==)
24. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGtsL_e_wf4doQ8MPO7_Sa7uIGSw_aLCOQE7TXREPBVFYhAlsW2yTFXE_PSSd84oW1CNn-kLbOpEvt3Y1G0eBMZIvgn1qFz_P4Y4OI3s1H2xq7BQA7hLVcZSZmUxzuawhZn4KvxI4QEz3In-EgOWZpYsmQlXt5dywDyPgL7Hm7fkI0iFPiEktzm4UXSFcneP4dIc4PoUIzFAQ==)
25. [ifs-institute.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFMA7KV1P9lGXVh_6Rln9bv_BIAUnKPPDGTxegzORqITJ1tsLaluEHs6QoSY91nZQJDKSfK6JvtC3pq6Js-Tce33nlvH9kPkVAakd8u9fQfxNQepSAMlIneqb9e6fBnaNYL1sDdE5tG5ZvVkB0=)
26. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFBMIJFn9TBN2LxpfJMhgbk_IjjLPl-fdKYI6b3Z7KEO3HEkFGJdK2Vb_jU_uhekITlh4evoAK2NWRIyeWNlXtLIAnfbjmTAJzYW0GngQUqs_qojQBYIgEM8kiI9CnpM8LBUbIQWgOI2HbRaehY3tDRoz_3PDoFPfPSzPnCZI3es3CN327SOouuD4HgoYQ96BIJN3AK-Y_rcWvl)
27. [fourcornerswellbeing.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExWKJo8jrpqhAhVoe1Ne8CzJ4pELLXxKwz-pXTj0cdQ_Rbd3snqG2klZTPSyVaxm2Hl2kLRlY-501XOYENFKvDbrkWb1694IDq9zKlqKmNVlhCBAZPPuIrmJ1MUZy6GHihItgtG86jzY66CDz23_iC87h-39-Spe42sZ4R-7h1_kedEwYXiQ9lQhi5sghYQgcA1PFx4oBRS-aWxl4aj3RBR5Bl5cM57-h6U_m6mhLzbKGtAPqj)

28. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG8QClzUlkqFlziO5kWhFq31u3wEO44DT3Ep5XpRX66e_TfNsshGM0SguGI7CR2m9ziM-f89dtotdFc7fcxWJEYMe82OvvuiZDEC1MOysjrxWPiOoRF99y8Q08nHh_B6q_gTv8y-YM5-pRflh7V_LbQjn-IumdcILQ4uu0lgcHZPaCbMpWqfVgZk3ReynlKY0_A6-2gZlsjgg==)
29. [ifsguide.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHRCSWmC8_VPRaay7KiWNOgxeTjCyMh0hmY4dpQXmqjXx-b3woeQkcihgYk8VUOXf6w_vY0inVLwKRtyjaefzRTHAJFKvZ36ju564QKrlKPExp8q3YC67-g3gLlD6jnTq8e)
30. [lifearchitect.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6GJA3__Q7EEoKf7Sm7Ap9DanjqZ4BaarqDv55kFVqCpgseL2BZV5-ov4HJKGFHTwaU5QAiQ_FT0M-2Eb_-mjqs7_OHoHHiRxwuqwCgW8zmwpNVgtzHnVfZBBaA_AUwp3m9mf83kGrHUUbrBI=)

### References

[lifearchitect.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6GJA3__Q7EEoKf7Sm7Ap9DanjqZ4BaarqDv55kFVqCpgseL2BZV5-ov4HJKGFHTwaU5QAiQ_FT0M-2Eb_-mjqs7_OHoHHiRxwuqwCgW8zmwpNVgtzHnVfZBBaA_AUwp3m9mf83kGrHUUbrBI=)