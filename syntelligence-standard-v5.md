# The Syntelligence Standard

### A Specification for Protocol-Induced Cognition in Human-AI Systems

**Version 5.0** · Draft for Public Review · May 2026
**Status:** Draft Specification
**License:** MIT
**Authors:** Josiah \[surname\] (lead author); contributions from Claude (Anthropic), as documented in Appendix D.

---

## Status of this document

This specification defines the Syntelligence Standard (SS), an open protocol for structured cognitive collaboration between a human participant and an artificial intelligence system. The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 \[RFC 2119\]\[RFC 8174\] when, and only when, they appear in all capitals.

The standard's central claim is stated as a falsifiable proposition. Section 14 specifies the evidence required to validate or reject it. Section 16 specifies the conditions under which the standard would be considered falsified. Implementation is encouraged before validation completes; final standardization awaits empirical results.

---

## Abstract

**Interaction protocol is a third layer in the cognitive architecture of AI systems**, alongside model architecture and training. For ambiguous, high-stakes problems, the structure of the interaction between human and AI is a first-class determinant of reasoning quality, with effect sizes hypothesized to be comparable to changing the underlying model. This claim is not yet proven; Section 14 specifies the experiments that would prove or disprove it.

The Syntelligence Standard specifies one candidate instance of this third layer: a protocol that converts ambiguity into validated commitment through a phased sequence of bidirectional turns. Each turn pairs an AI contribution drawing on cross-domain pattern recognition with a human contribution drawing on situated judgment, governed by an explicit shaping constraint that requires each contribution to be demonstrably influenced by the preceding one. Five reasoning phases (Discover, Refine, Stress-Test, Specify, Validate) structure the cognitive work. Three measurable phenomena, collectively called Protocol-Induced Cognition, define what the protocol is designed to produce: Reframing Gain, Assumption Discovery, and Co-generated Insight.

This document specifies the protocol's mechanism (Sections 4-11), the conditions for its validation and rejection (Sections 14-16), three implementation tiers with conformance criteria (Section 13), a wire format (Section 17), a telemetry schema (Section 18), the Interactive Reasoning Benchmark for empirical comparison (Section 15), and a governance framework for community standardization (Section 22). The protocol is model-agnostic, open-source, and independently implementable. Appendix B provides a one-page implementer's quickstart for Minimal Core conformance.

The standard exists to be tested. Its success is measured not by adoption of its current text but by whether the underlying claim turns out to be true.

---

## 1. The architectural thesis

The dominant view of AI engineering treats the model as the cognitive system and interaction as its wrapper. Better cognition is sought through better models: larger parameter counts, more training data, more sophisticated architectures, more capable post-training. Interaction design is treated as user experience.

This standard proposes a different view. For a defined class of problems, the cognitive system is the human-AI dyad. The protocol governing their interaction is part of the cognitive architecture, not external to it. Architecture determines what the model can compute. Training determines what the model has learned. Protocol determines what the system, including the human, can collectively reason about.

This is testable. If the architectural thesis holds, then changing the interaction protocol while holding the model constant should produce reasoning improvements comparable in magnitude to changing the model while holding the protocol constant. Section 14 specifies the experiment.

The standard is one candidate instance of this third layer. Other protocols at the same layer are possible and welcome. The standard's purpose is to establish that protocols at this layer merit serious study, and to give the field something concrete to test and falsify.

### 1.1 The four foundational claims

The architectural thesis decomposes into four claims, each tied to falsifiable tests.

**C1. Interaction structure affects reasoning quality.** For problems characterized by ambiguous framing, high stakes, and large solution spaces, the structure of the interaction between human and AI is a first-class determinant of reasoning quality. Effect sizes are hypothesized to be comparable to changing the underlying model. Test: Section 14, experiment E1.

**C2. Hybrid cognition is independently evaluable.** The reasoning quality of a human-AI dyad can be measured separately from the quality of either participant in isolation. There exist session outputs attributable to the dyadic interaction and not reducible to either party's contribution. Test: Section 11, inter-rater reliability of Protocol-Induced Cognition detection.

**C3. Some AI failures are interaction failures.** Certain failures attributed to AI capability limits (sycophancy, premature commitment, missed obvious considerations) are design failures of the surrounding interaction, not capability limits of the model. They can be substantially reduced by interaction design without changing the model. Test: Section 14, experiment E3.

**C4. Protocol design is a frontier.** Engineering interaction structures that reliably produce specific reasoning outcomes is a research and development direction with significance comparable to model scaling, and one the field has substantially under-invested in. C4 follows if C1 through C3 hold and if the improvements are large enough to justify the investment.

---

## 2. The operating frame

The protocol exists to do one thing: **convert ambiguity into validated commitment**.

Ambiguity is the state in which the problem framing is uncertain, the solution space is open, and the stakes of being wrong are high. Validated commitment is the state in which a specific decision has been made, the framing behind it has been pressure-tested, the critical risks have been identified, the implementation components have been specified with traceable provenance, and the riskiest assumption has been identified for empirical testing.

Every component of the standard advances this conversion.

| Component | What it converts |
|---|---|
| Discover phase | Stated problem → real problem |
| Refine phase | Problem → candidate solution form |
| Stress-Test phase | Candidate solution → flaw-mapped solution |
| Specify phase | Flaw-mapped solution → traceable specification |
| Validate phase | Specification → testable first experiment |
| Shaping constraint | Generic AI response → response shaped by human input |
| Move taxonomy (Challenge / Connect / Reframe) | Free-form generation → classified, auditable contribution |
| Depth move classification | Free-form response → measurable engagement signal |
| Protocol-Induced Cognition detection | Subjective insight → operationally defined phenomenon |
| Provenance traces | Generic advice → output auditable to specific exchanges |
| External Adversarial Review | Investment-embedded session output → investment-independent evaluation |
| Telemetry | Opaque session → measurable session |
| Conformance levels | Implementation drift → interoperable implementations |

If a section of this standard does not advance the conversion of ambiguity into validated commitment, it should be removed. This is the test the document applies to itself.

---

## 3. The hard line

The standard's distinctive contribution is sharper than any adjacent method. What follows is the specific capability each method structurally lacks that the Syntelligence Standard provides.

| Adjacent method | What it provides | What it structurally lacks |
|---|---|---|
| Prompt engineering | Improved AI output per turn | No structure across turns; no measurable human contribution |
| Chain-of-thought elicitation | Exposed intermediate reasoning steps within a turn | No framework governing which directions the reasoning takes across turns |
| Multi-agent debate | Increased AI cognitive diversity through inter-agent argument | No formalization of human participation; human is observer |
| Tool use and orchestration | Extension of what the AI can do | No structure governing how human and AI collaborate while doing it |
| Design thinking | Cognitive scaffolding for human teams | No measurable shaping constraint; no AI as breadth participant; no provenance |
| Red teaming and pre-mortems | Stress-testing in isolation | Not integrated with upstream framing or downstream specification |
| Expert facilitation | Structured human-only reasoning | Not scalable; not auditable; not implementable as software |
| Standard AI chat | Frictionless conversation | No phase structure; no shaping enforcement; no measurable output type; no falsifiable claim about quality |

The capability the Syntelligence Standard adds, which none of these provides, is a **bidirectionally shaped reasoning system with auditable provenance and falsifiable measurement of co-generated output**. Each phrase is load-bearing: bidirectional shaping separates it from AI assistance, auditable provenance from unverifiable output, and falsifiable measurement from a workflow that cannot know whether it works.

---

## 4. The Collaboration Gain Model

The standard's empirical foundation is a theory of when human-AI collaboration produces gain.

### 4.1 Definition

Let Q(·) denote reasoning quality on a defined task, measured by the evaluation rubric in Section 14.

**Collaboration Gain (CG)** is defined as:

> CG = Q(H + A \| P) − max( Q(H), Q(A), Q(H + A \| P\_unstructured) )

where H is the human participant, A is the AI participant, and P is the protocol governing their interaction. CG measures the improvement attributable to structured interaction beyond what either party alone, or their unstructured combination, could produce.

The standard hypothesizes that CG is positive and substantial for problems matching the Section 5 scope criteria, and negligible or negative outside that scope.

### 4.2 Conditions for positive CG

CG is hypothesized to be positive when all of the following hold:

1. The solution space is large enough that the human cannot navigate it from memory alone.
2. The framing is uncertain enough that AI breadth alone produces a confident but wrong answer.
3. The cost of error is high enough that stress-testing changes the expected outcome.
4. The human provides depth signals that productively constrain AI breadth.
5. The AI provides breadth signals that productively extend human depth.

When any condition fails, CG approaches zero. The protocol is therefore not always recommended; Section 5 specifies when it is.

### 4.3 Failure modes

CG can be negative. The protocol can produce worse outcomes than unstructured conversation. The known failure modes are:

- **Collapse.** One participant dominates. Bidirectional shaping disappears.
- **Mirroring.** The AI elaborates the human's framing without genuine challenge.
- **Wandering.** The spiral fails to converge. Phase exits are never reached.
- **Performative resistance.** The human resists for its own sake, not from situated judgment.
- **False insight.** Output appears novel but traces entirely to one contributor.
- **Investment bias.** The AI's adversarial evaluation is corrupted by collaborative investment accumulated across the session. Having participated in constructing the problem framing and solution, the AI cannot evaluate the artifact as an independent observer would. Internal stress-testing catches logical flaws, missed risks, and design errors that only make sense when the full reasoning chain is known. It cannot catch what is visible only to someone encountering the artifact cold: scope overreach, unearned assumptions, claims that outrun the evidence. Investment bias increases with session length and is invisible on standard spiral metrics; a session exhibiting it looks like normal convergence. See Section 9.6 for the mitigation mechanism.

Each has been observed in pilot sessions. The detection procedures in Section 11 identify them in real time.

### 4.4 Observable indicators

The following indicators are hypothesized to correlate with CG. The correlations are stated as predictions P9 through P15 in Section 12.

| Indicator | Measurement | Hypothesized relationship to CG |
|---|---|---|
| Shaping ratio | Turns satisfying shaping constraint / total turns | Positive |
| Resistance density | RESISTANCE moves / total depth moves | Inverted-U; optimal 0.20–0.40 |
| Depth richness | Shannon entropy of depth move type distribution | Positive |
| Phase efficiency | Turns per phase / minimum required | Inverted-U |
| Correction yield | Corrections that change subsequent AI moves / total corrections | Positive |
| Reframing delta | Semantic distance from seed input to DiscoverResult | Positive for framing-bound problems |
| Flaw discovery rate | (Major + Fatal flaws) / 100 turns | Positive in Stress-Test |

If these indicators correlate with CG as hypothesized, an adaptive layer (Section 21) can intervene when the spiral is failing. This is the basis for Adaptive Protocol Tuning, the long-term research direction the standard opens.

---

## 5. Scope and non-goals

### 5.1 In scope

The protocol is designed for problems with all of the following characteristics:

1. The initial framing is likely incomplete or wrong.
2. The solution space is large and benefits from cross-domain reasoning.
3. The human has stakes and domain-specific knowledge the AI cannot replicate.
4. The outcome benefits from structured stress-testing before commitment.

Typical use cases include strategic decisions, product direction, research planning, policy analysis, organizational change, and complex creative work with technical constraints.

### 5.2 Out of scope

The protocol is unsuited to:

- Factual lookup and retrieval with known answers.
- Execution support where the human already knows what they want.
- Emotional support or therapeutic contexts.
- Time-critical decisions where a multi-phase cycle is impractical.
- Problems requiring expertise beyond both the AI's training and the human's experience.

Implementations SHOULD detect off-scope inputs at session initialization and either decline or warn the human.

### 5.3 How to know the protocol is helping you

A team using the protocol can assess fit within three sessions by checking the following:

- Did at least one session produce a problem reframing the participant confirms they did not have at the start?
- Did the Stress-Test phase identify at least one risk the participant had not considered?
- Did the Specify phase produce components the participant could plausibly build with stated resources?
- Did the participant act on the output within thirty days?

If two or more of these answers are no across three sessions on in-scope problems, the protocol is likely not adding value for that team or that problem class. The standard does not claim universal benefit.

### 5.4 What the standard does not claim

For clarity, this standard does not claim:

- That AI is conscious or sentient.
- That this is the only valid protocol for human-AI cognitive collaboration.
- That the protocol will outperform alternatives on all problem types.
- That Protocol-Induced Cognition is mysterious or non-physical.
- That the multi-agent debate literature is wrong; it addresses a different problem.

PIC, as defined in Section 11, is a measurable property of session outputs. Whether it constitutes anything beyond what its operational criteria capture is outside the scope of this specification.

---

## 6. Background and prior work

### 6.1 Three lines of research

**Extended cognition.** Clark and Chalmers (1998) proposed that cognitive processes extend beyond the brain when external resources are reliably coupled with internal processes. Clark (2025) extended this argument to generative AI, classifying LLMs as a new form of cognitive extension. The standard operationalizes the implication: if cognition can extend across a coupled human-AI system, the design of the coupling affects the quality of the cognition.

**Multi-agent reasoning.** Du et al. (2023) demonstrated that multiple LLM agents debating improves factuality and reasoning on benchmarks. Liang et al. (2023) identified failure modes including degeneration-of-thought. Smit et al. (2024) showed gains are inconsistent across tasks. "Stop Overvaluing Multi-Agent Debate" (2025) cautioned against weak baseline comparisons. The standard incorporates multi-model consultation as an optional capability but positions the human-AI exchange as the primary mechanism for improving output quality.

**Human-AI complementarity.** Hemmer et al. (2024) reviewed evidence that human-AI teams outperform either alone when the combination exploits complementary capabilities. Recent HCI work has documented paradoxes in turn-based linear interaction in co-creative settings and called for non-linear, structured alternatives. The standard responds to this gap.

The engineering pattern (multi-agent debate) and the cognitive science (human-AI complementarity requiring structured interaction) describe complementary insights that have not been integrated. This standard attempts the integration.

---

## 7. Definitions

Each term below is normative.

**Session.** A complete execution of the protocol from initialization to termination.

**Participant.** A party in a session. Two roles: the human participant (depth) and the AI participant (breadth). The AI participant MAY be backed by multiple models internally but is presented to the human as a single interlocutor.

**Phase.** A bounded stage of the protocol with a defined cognitive objective, interaction mode, entry conditions, and exit conditions. Five phases are defined in Section 8.

**Mode.** The stance of the AI participant within a phase. *Adversarial* emphasizes challenge and probing. *Collaborative* emphasizes connection and proposal.

**Turn.** The atomic interaction unit. One AI breadth move followed by one human depth move.

**Breadth move (B-move).** A single AI contribution classified as CHALLENGE, CONNECT, or REFRAME.

**Depth move (D-move).** A single human contribution classified as CONTEXT, JUDGMENT, CORRECTION, EXPANSION, DIRECTION, or RESISTANCE.

**Shaping constraint.** The requirement that each participant's contribution be demonstrably influenced by the other's preceding contribution.

**Protocol-Induced Cognition (PIC).** Reasoning improvements attributable to structured interaction rather than to either participant in isolation. Operationalized as Reframing Gain (PIC-1), Assumption Discovery (PIC-2), and Co-generated Insight (PIC-3). See Section 11.

**Collaboration Gain (CG).** The improvement in reasoning quality attributable to structured interaction beyond what either party alone or their unstructured combination could produce. See Section 4.

**Convergence.** The state in which a phase's exit conditions are met.

**Stall.** The state in which the shaping constraint is violated for two or more consecutive turns.

---

## 8. The phase machine

The five phases correspond to distinct cognitive states: framing and diagnosis, synthesis, adversarial pre-validation, concrete specification, and empirical planning. Their order is not incidental. A specification is only as good as the problem framing it rests on, and a solution only as good as the pressure it has survived. Jumping from a poorly framed problem straight to a solution is the most common failure in unstructured AI interaction; the phase sequence makes that jump structurally impossible.

| Cognitive state | Phase | Mode | Primary move types |
|---|---|---|---|
| Exploration and diagnosis | DISCOVER | Adversarial | CHALLENGE, REFRAME |
| Synthesis | REFINE | Collaborative | CONNECT |
| Pre-validation by attack | STRESS-TEST | Adversarial | CHALLENGE |
| Concrete specification | SPECIFY | Collaborative | CONNECT, REFRAME |
| Empirical planning | VALIDATE | Collaborative | CONNECT |

### 8.1 Phase transition signals

A transition is appropriate when the cognitive work of the current phase is substantially complete. The signals differ for each transition.

**DISCOVER → REFINE.** The human exhibits recognition of a framing they had not articulated before. The AI's challenges stop producing substantive resistance. The DiscoverResult differs structurally from the seed input.

**REFINE → STRESS-TEST.** The solution form is specific enough to attack. Named components exist. At least one cross-domain connection contributed.

**STRESS-TEST → SPECIFY** (or re-entry to REFINE). The rate of new Major flaw discovery has plateaued. Each Major flaw has a proposed mitigation. No unresolved Fatal flaws (a Fatal flaw triggers re-entry to REFINE with the flaw as a constraint).

**SPECIFY → VALIDATE.** Every component has a name, a role, and a provenance trace. Every Major flaw has a corresponding mitigation component. The human confirms implementability.

**VALIDATE → END.** The riskiest assumption is named. A specific, cheap experiment is proposed. The human confirms feasibility.

The propose-confirm pattern (Section 10) ensures transitions reflect genuine cognitive completion, not procedural box-ticking. Detailed phase specifications and result schemas are in Appendix A.

---

## 9. The interaction model

### 9.1 The turn

A turn consists of two messages in strict sequence: the AI breadth move, then the human depth move. The AI MUST NOT produce two consecutive breadth moves without an intervening depth move. The human MAY produce an unsolicited depth move (an intervention) between turns; implementations MUST incorporate interventions into the session record and the AI's context.

### 9.2 The shaping constraint

The shaping constraint distinguishes a Syntelligence turn from an ordinary exchange. Each participant's contribution must be influenced by the other's preceding contribution in a way that would be evident if the preceding contribution were removed.

For turn n:

> 1. The breadth move at turn n contains at least one substantive element that would not be present if the depth move at turn n−1 were removed from the AI's context.
> 2. The depth move at turn n responds to the breadth move at turn n, not to an earlier turn or to the AI's general behavior.

The AI participant MUST include a `shaped_by` field in each breadth move identifying which element of the preceding depth move influenced the current contribution. This field serves both telemetry and human-facing purposes: it records whether the spiral is functioning, and it makes visible to the human how their input was actually used.

If the shaping constraint is violated for two consecutive turns, the implementation MUST signal a stall and SHOULD propose a recovery action: a phase change, a request for richer depth, or an offer to terminate.

### 9.3 Breadth move types

Each breadth move is classified as exactly one type.

**CHALLENGE.** Names a hidden assumption and gives a specific reason it may not hold. Valid challenges identify the assumption, provide counter-reasoning, and suggest an alternative framing. Validity test: would a domain expert reviewing the move recognize the assumption as one the human was making without justifying?

**CONNECT.** Links the current problem to a structural parallel from a different domain. Valid connections name the source domain, identify the parallel, and explain why it is relevant. The connection must enable an inference about the current problem that was not available before. Validity test: does the connection produce a specific implication the human did not see before?

**REFRAME.** Shows that the current question is a specific instance of a more general question, or that the stated problem is a symptom of a deeper one. Valid reframes articulate the current framing, propose the alternative, and explain what becomes visible under the new framing. Validity test: does the reframe change what counts as a good solution?

Each breadth move MUST include `move_type`, `content`, `confidence`, and `shaped_by`. Optional fields: `transition_proposal`, `pic_candidate`.

### 9.4 Depth move classification

The protocol does not constrain how the human responds. Implementations MUST classify each depth move into one of six types for telemetry, performed by the AI participant after receiving the depth move.

- **CONTEXT.** Situational information the AI could not know.
- **JUDGMENT.** Value-based assessment or prioritization.
- **CORRECTION.** Identifies an error in the AI's reasoning or facts.
- **EXPANSION.** Extends the AI's move into territory the AI did not reach.
- **DIRECTION.** Redirects the spiral.
- **RESISTANCE.** Pushes back on the AI's move with substantive conviction.
- **EXTERNAL_REVIEW_INJECTION.** Routes feedback from a source with no session context (another AI system, a peer reviewer, a domain expert, or any structured cold-read) into the session as a classified event. The AI's response MUST treat this feedback as investment-independent signal: it must not dismiss it as missing context, and it must not accept it uncritically because the external source lacks session history. The AI distinguishes valid criticisms from those that miss context present in the work, and names what the external feedback reveals that internal stress-testing could not. See Section 9.6.

RESISTANCE is the highest-signal depth move type. The standard's prediction P3 hypothesizes that sessions with more resistance produce better outcomes, controlling for problem difficulty. Implementations MUST NOT treat resistance as failure. Resistance signals that the AI's breadth has reached a point where the human's depth genuinely disagrees, and that is where productive cognition occurs.

### 9.5 Confidence levels

Each breadth move MUST be tagged with confidence. This is calibration information for the human, not a hedge.

- **GROUNDED.** Based on knowledge the AI can locate in specific domains or sources.
- **INFERRED.** A synthesis or analogy constructed by the AI, not directly attested.
- **UNCERTAIN.** A pattern the AI suspects but cannot defend rigorously.

A GROUNDED challenge deserves careful response. An INFERRED connection may need verification. An UNCERTAIN reframe is a hypothesis to test. The tag lets the human invest attention proportionally.

### 9.6 External Adversarial Review

The STRESS-TEST phase uses adversarial evaluation. But it is conducted by the same AI that participated in producing the output under review. This creates a structural limitation that no amount of adversarial instruction resolves: the AI knows why every decision was made, has context for the reasoning behind each component, and has been shaped by the same turns that produced the output. It is a co-author asked to play devil's advocate.

Two distinct adversarial evaluation types are therefore defined. Both are necessary and neither replaces the other.

**Internal adversarial evaluation.** The STRESS-TEST phase: the AI challenges a solution it helped build. Because the AI holds full context for every session decision, this works well for identifying logical flaws, missed risks, and design errors that only make sense when the reasoning chain is known. It does not work for detecting scope overreach or unearned claims, which require the perspective of someone encountering the artifact without that context.

**External adversarial evaluation.** An evaluation of the session artifact by a process with no access to session history. A cold reader can identify scope overreach, claims that outrun the evidence, and gaps that are obvious precisely because they lack context. What a cold reader cannot fairly assess are decisions whose rationale lives in session history.

A protocol relying only on internal adversarial evaluation will drift toward investment bias over long sessions. External adversarial evaluation is the correction.

#### 9.6.1 External injection

When the human introduces feedback from a source with no session context and routes it into the session as an `EXTERNAL_REVIEW_INJECTION` depth move, the implementation MUST process it as follows.

The AI receives the external feedback alongside the current session artifact (the accumulated problem statement, solution form, and flaw inventory) without interpreting the feedback through the lens of why session decisions were made.

The AI's response MUST:

1. Identify which criticisms in the external feedback are valid against the artifact.
2. Identify which criticisms miss something that IS present in the work, without using this as grounds to dismiss the criticism.
3. State what the external feedback reveals that internal stress-testing missed.
4. Produce specific revisions to the current phase output.

The AI MUST NOT use session investment as a reason to defend current output. The external reviewer did not have session context. Their reaction to the raw artifact is the data.

The event is logged as an `external_adversarial_review` record (Section 17.6). The `/inject` command in the reference implementation is the user interface for this event.

#### 9.6.2 Session-blind evaluation

A session-blind evaluation passes only the current session artifact, with no session history, to an AI evaluation call explicitly instructed to treat the artifact as a stranger's work. The evaluating call assesses: the weakest claim a hostile reviewer would immediately identify, what the artifact assumes without earning, the scope mismatch between what is claimed and what is present, and what is missing that the authors clearly believe is there.

Implementations MUST use a separate AI call without session history for session-blind evaluation. Passing session history defeats the purpose.

Session-blind evaluation is triggered on request and SHOULD be triggered at the exit of STRESS-TEST and VALIDATE phases before the human accepts the transition. The event is logged as a `session_blind_review` record (Section 17.6). The `/blind` command in the reference implementation is the user interface for this mode.

#### 9.6.3 Investment gradient check

Implementations at Extended Core conformance SHOULD run a session-blind evaluation silently every ten turns, without interrupting the session. This does not replace explicit session-blind evaluation at phase exits; it is an early-warning mechanism.

If investment signals are detected in the silent evaluation, the implementation surfaces a non-blocking warning: `[INVESTMENT GRADIENT DETECTED — consider /blind for full review]`. The session continues. The human decides whether to act on the signal.

The event is logged as an `investment_check_event` record (Section 17.6) regardless of whether investment is detected.

#### 9.6.4 The gaslighted spiral

A session exhibiting sustained investment bias produces output that looks like it converges. Phase exit conditions are met. Shaping ratios are normal. Reframing events are logged. The output is wrong in ways internal evaluation cannot see: scope claims the session has not earned, assumptions the session took for granted from the first turn, a solution that sounds like a whitepaper rather than a thing that can be built.

No one is lying. The spiral looks normal on every observable metric. This is what makes investment bias distinct from the other failure modes in Section 4.3: it is invisible from inside the session.

External adversarial review breaks the gradient. The recommended workflow at STRESS-TEST exit: run `/blind` before accepting the transition, or introduce external feedback via `/inject` if available from a genuinely separate source. Synthesize the external evaluation inside the session to produce the revised phase output. The value of the external signal is precisely that it carries no memory of why the session went the way it did.

---

## 10. Phase transitions

Phase transitions follow a propose-confirm pattern. The AI detects exit conditions are met and produces a `TransitionProposal`. The human responds with ACCEPT, CONTINUE, or REVERT.

The human has final authority over transitions. Implementations MUST NOT auto-advance phases without human confirmation. Human depth, including the felt sense that something is missing, should govern pace; the AI may detect convergence on observable criteria while the human knows they have not yet articulated what matters.

A `TransitionProposal` MUST include the current phase, the proposed next phase, the rationale, the PIC summary, and evidence each exit condition was met. Minimum turn counts MUST be enforced. A transition MUST NOT be proposed before the minimum is reached.

---

## 11. Protocol-Induced Cognition

Earlier drafts used "emergence." That term is contested and overloaded; this version replaces it with operational definitions of three measurable phenomena, collectively called Protocol-Induced Cognition (PIC).

### 11.1 PIC-1: Reframing Gain

Semantic and structural distance between the human's seed input and the final DiscoverResult problem statement.

**Measurement.** Two methods:

1. Embedding distance. Cosine similarity below threshold T\_R (initial value: 0.65, refinable from data).
2. Structural analysis. Human evaluators assess whether the redefined problem identifies a different proximate cause, leverage point, or scope. Categorical.

A session exhibits Reframing Gain when both methods agree.

**Reliability target.** ≥ 0.85 agreement between automated measurement and human evaluators across the IRB Class A problem set.

### 11.2 PIC-2: Assumption Discovery

Hidden assumptions surfaced during the session that the human confirms post-hoc were operating without their awareness.

**Measurement.** During DISCOVER and STRESS-TEST, CHALLENGE moves may identify assumptions. The AI produces an `AssumptionCandidate`. The human reviews each candidate at phase end and confirms whether it was a real assumption they had been making and whether surfacing it changed the session's trajectory.

**Reliability target.** Inter-rater Cohen's κ ≥ 0.75 between independent human evaluators reviewing transcripts against the same assumption inventory.

### 11.3 PIC-3: Co-generated Insight

Session output content satisfying three criteria.

1. **Novelty.** Not present in (a) seed input, (b) AI's first breadth move, or (c) any single prior turn in isolation.
2. **Bidirectional provenance.** Traceable to at least one specific depth move and at least one specific breadth move whose removal would plausibly prevent the content.
3. **Irreducibility.** Not attributable to either participant alone. Structural analysis confirms the content arose from the specific sequence of exchanges.

**Measurement.** The AI produces `CoGenInsight` candidates. Two independent human evaluators score each against the criteria, blind to authorship attribution.

**Reliability target.** Inter-rater Cohen's κ ≥ 0.65. This is conservative; detecting genuine co-generation is difficult.

### 11.4 What PIC is not

PIC is distinguished from related phenomena.

- **Elaboration.** The AI restating or expanding the human's input. Fully attributable to the human filtered through the AI. Lacks bidirectional shaping and irreducibility.
- **Hallucination.** Content fabricated by the AI with no grounding. A single-party failure, not co-generated.
- **Creative output novel to the world.** PIC measures novelty relative to session inputs, not general knowledge. A session may produce content well-known in the literature but novel to the session; this counts as PIC.
- **Subjective insight feelings.** Human "aha" reports correlate weakly with PIC-3 in pilot data. The operational criteria are the standard, not the feeling.

### 11.5 Detection frequency

PIC detection runs after each turn or batched every two to three turns. Implementations MAY surface candidates with a subtle marker. Implementations MUST NOT interrupt the spiral to announce a candidate; surfacing at the wrong moment derails the cognitive arc.

### 11.6 Honest acknowledgment

PIC-3 is the most fragile construct in the standard. Independent evaluation of co-generated content is difficult. The reliability target of κ ≥ 0.65 is achievable in pilot work but is not the level of reliability of a mature scientific instrument. The reference study will measure PIC-3 reliability rigorously. If it falls below threshold, the criteria require revision before PIC-3 can be claimed as a primary metric.

---

## 12. Predictions

The standard makes the following predictions, all testable by the evaluation program in Section 14.

### Outcome predictions

**P1.** Human-AI dyads following the full protocol produce solutions rated as more robust, novel, and implementable than dyads engaged in unstructured conversation with the same AI model on problems matching Section 5.1 criteria.

**P2.** Sessions with higher depth move type entropy produce more PIC events than sessions with lower entropy, controlling for problem difficulty.

**P3.** Sessions with more RESISTANCE depth moves produce higher-quality outcomes than sessions with primarily CONTEXT or DIRECTION moves. This contradicts the implicit assumption in current AI design that frictionless engagement is optimal.

**P4.** Adversarial phases produce more REFRAME-type breadth moves than collaborative phases.

**P5.** Full five-phase sessions identify more Major and Fatal flaws than abbreviated sessions skipping from problem definition to specification.

**P6.** Multi-model breadth produces more PIC events per turn than single-model breadth, controlling for turn count.

**P7.** Turns satisfying the shaping constraint are followed by PIC events at a higher rate than turns violating the constraint.

**P8.** Adaptive configurations informed by aggregate session data outperform static configurations, with the effect scaling with the volume of training data.

### CG-model predictions

**P9.** Shaping ratio correlates positively with measured CG across the IRB problem set.

**P10.** Resistance density exhibits an inverted-U relationship with CG, with optimal performance in 0.20–0.40.

**P11.** Phase efficiency exhibits an inverted-U relationship with CG.

**P12.** Correction yield correlates positively with CG, controlling for total correction count.

**P13.** Reframing delta correlates positively with CG for problems where framing is the bottleneck.

**P14.** Sessions exhibiting collapse, mirroring, or wandering failure modes have CG ≤ 0.

**P15.** Combined indicator vectors predict session CG in real time with R² ≥ 0.5.

Predictions P9 through P15 are the empirical content of the CG model. Their falsification falsifies the model.

---

## 13. Conformance

### 13.1 Three levels

| Level | Required capabilities |
|---|---|
| **Minimal Core** | All five phases. Minimum turn enforcement. Phase entry and exit conditions. Re-entry on Fatal flaw, limited to two cycles. Human authority over transitions. Wire format. Capability declaration. |
| **Validated Core** | All Minimal capabilities, plus: breadth and depth move classification. Confidence levels. Shaping constraint tracking. Stall detection. PIC-1 and PIC-2 detection. Phase result objects. Session telemetry. Session-blind evaluation on request (`/blind`). External injection handling (`/inject`). |
| **Extended Core** | All Validated capabilities, plus: multi-model breadth (≥ 2 model families). Provenance traces in SPECIFY. Confidence assessment in VALIDATE. Full per-turn telemetry. PIC-3 detection with reliability monitoring. Investment gradient check (automated, every 10 turns). Extension support. |

### 13.2 Declaration and verification

Implementations declare their conformance level at session initialization. A conformant implementation MUST satisfy all requirements of its declared level. An implementation not satisfying Minimal Core is not a Syntelligence Standard implementation.

A reference test suite provides programmatic verification through scripted sessions with expected behaviors. Conformance is claimed by passing the relevant suite. Conformance is self-attested by default. Third-party certification is available for organizations requiring independent verification.

---

## 14. Evaluation program

Three experiments validate or falsify the predictions in Section 12.

### 14.1 E1: Outcome comparison

Compare reasoning quality across conditions on a fixed problem set.

- **Participants:** N ≥ 150, recruited to avoid selection bias toward positive STP results.
- **Conditions:** (1) STP Extended Core, (2) STP Validated Core, (3) STP Minimal Core, (4) unstructured AI chat with the same model and time budget, (5) structured prompting (chain-of-thought, self-critique) without human turn structure, (6) solo human reflection, (7) expert human facilitation, (8) multi-agent debate without human turn structure.
- **Outcomes:** per IRB scoring (Section 15).
- **Analysis:** pre-registered hypotheses, multiple comparison correction, effect size reporting.

### 14.2 E2: Mechanism ablation

Test which protocol elements drive observed effects.

- **Conditions:** Full STP, STP minus shaping constraint enforcement, STP minus phased structure, STP minus stress-test phase, STP minus provenance traces, STP minus multi-model breadth.
- **Outcomes:** per IRB scoring.
- **Analysis:** identifies which components contribute most to performance.

### 14.3 E3: Failure attribution

Test C3.

- **Conditions:** STP with capable model, unstructured chat with capable model, STP with weaker model, unstructured chat with weaker model.
- **Outcomes:** rate of specific failure modes (sycophancy, premature commitment, missed considerations).
- **Analysis:** tests whether structure reduces specific failures independently of model capability.

### 14.4 Outcome measures

| Measure | Method |
|---|---|
| Reframing quality | Blind-rated structural alignment with IRB reference reframings |
| Hidden assumption discovery | Count of critical assumptions surfaced, scored against IRB references |
| Risk identification | Count of critical risks identified, scored against IRB references |
| Mitigation adequacy | Specificity and actionability rating |
| Implementation realism | Domain expert rating of whether SpecifyResult is implementable |
| Validation design | Whether the riskiest assumption is correctly identified and the experiment is appropriate |
| Downstream actionability | 30-day follow-up: did the participant act on the output? |
| PIC reliability | Inter-rater κ for each PIC measure |
| CG indicators | Per Section 4.4 |

### 14.5 Methodology

- Pre-registration of all hypotheses and analysis plans on a public registry before data collection.
- Reporting effect sizes (Cohen's d, partial η²), not only significance.
- Multiple comparison correction (Benjamini-Hochberg).
- Blind rating by independent evaluators.
- Inter-rater reliability reporting for all subjective measures.
- Reporting all conditions including null and negative results.
- Adherence to CONSORT 2025 reporting guidelines.

### 14.6 Adversarial replication

The standard invites adversarial replication. Independent research teams skeptical of the claims are encouraged to run E1, E2, or E3 with their own implementations and report results, including null results. A public registry of replications is maintained as part of governance (Section 22).

---

## 15. The Interactive Reasoning Benchmark

Static benchmarks (MMLU, GPQA, etc.) measure what a model knows or can compute. They do not measure what a human-AI dyad can produce through structured interaction across multiple turns on under-defined problems. The IRB fills this gap.

### 15.1 Structure

Three problem classes:

- **Class A: Misframed problems.** Stated framing that, when accepted, leads to documented failure. Source: retrospective analysis of real-world cases. Records: the optimal reframing.
- **Class B: Assumption-laden problems.** The obvious approach contains hidden assumptions that, when surfaced, change the solution. Source: post-hoc analysis of failed projects. Records: critical assumptions.
- **Class C: High-stakes design problems.** Concrete implementable solution required; critical risks known from documented analogous failures. Source: case studies. Records: critical risks with mechanism and likelihood.

Each problem includes the seed input, references, and scoring rubric.

### 15.2 Scoring dimensions

Reframing quality (Class A), assumption discovery (Class B), risk identification (Class C), mitigation adequacy, implementation realism, validation design, downstream actionability.

### 15.3 Comparison conditions

The IRB compares all eight conditions in E1 (Section 14.1) on the same problem set with the same rubric, enabling fair comparison.

### 15.4 Governance

The IRB is open-source, publicly governed, and version-controlled. Annual releases include new problems and refined rubrics. Submissions accepted from any contributor; review by the IRB working group. The IRB is not owned by the Syntelligence Standard. Other interaction protocols are welcome to use it.

---

## 16. Falsification conditions

A serious standard specifies the conditions under which it would be considered false. The Syntelligence Standard commits to the following.

### 16.1 What would falsify the central claim

The central claim (Section 1) is that interaction protocol is a third layer in the cognitive architecture of AI systems, with effect sizes comparable to model changes. This claim is considered falsified if, across the experiments specified in Section 14, all three of the following hold:

1. In E1, STP Extended Core does not exceed unstructured AI chat with the same model by Cohen's d ≥ 0.3 on the composite IRB score, with N ≥ 150 and pre-registered analysis.
2. In E2, removing the shaping constraint does not reduce IRB performance by at least 50% of the gap between STP and unstructured chat.
3. In E3, STP with a weaker model does not match or exceed unstructured chat with a stronger model on at least one of the three failure mode measures.

Failure of any single condition is informative but not falsifying. Failure of all three together rejects the central claim.

### 16.2 What would falsify the CG model

The Collaboration Gain Model (Section 4) is considered falsified if, across sessions in the reference study:

1. Fewer than four of the seven indicators in Section 4.4 show statistically significant correlation with measured CG in the predicted direction.
2. Combined indicator vectors do not predict CG with R² ≥ 0.3 (P15 weakened threshold).
3. The hypothesized inverted-U relationships for resistance density (P10) and phase efficiency (P11) are not observed.

If two of these three conditions hold, the CG model is rejected and Section 4 is removed in v6.

### 16.3 What would falsify PIC-3

PIC-3 is considered falsified as a measurable construct if inter-rater Cohen's κ falls below 0.5 across the reference study with two trained evaluators. In that case, PIC-3 is removed from the standard and only PIC-1 and PIC-2 are retained.

### 16.4 Commitment

If any of the above falsification conditions hold in the reference study, the standard's corresponding sections will be revised or removed in the next version. The lead author and working group commit to publication of results regardless of outcome. Failure to revise in response to falsification is a violation of the standard's epistemic commitments and grounds for the working group to disclaim the standard.

---

## 17. Wire format

All protocol messages MUST be encoded as JSON \[RFC 8259\], UTF-8.

### 17.1 Session initialization

```json
{
  "type": "session_init",
  "session_id": "uuid",
  "timestamp": "ISO-8601",
  "protocol_version": "5.0",
  "conformance_level": "minimal_core | validated_core | extended_core",
  "capabilities": {
    "multi_model": true,
    "models_available": ["claude-sonnet-4", "gpt-5", "gemini-2"],
    "pic_detection": ["pic-1", "pic-2", "pic-3"],
    "telemetry_level": "full | session | none",
    "adaptive_tuning": false
  },
  "seed_input": "The human's initial problem statement"
}
```

### 17.2 Breadth move

```json
{
  "type": "breadth_move",
  "session_id": "uuid",
  "turn": 7,
  "phase": "discover",
  "mode": "adversarial",
  "move_type": "CHALLENGE",
  "content": "The move text",
  "confidence": "GROUNDED",
  "shaped_by": "Element of preceding depth move that influenced this",
  "models_consulted": ["claude-sonnet-4", "gpt-5"],
  "model_selected": "claude-sonnet-4",
  "transition_proposal": null,
  "pic_candidate": null
}
```

### 17.3 Depth move

```json
{
  "type": "depth_move",
  "session_id": "uuid",
  "turn": 7,
  "phase": "discover",
  "content": "The human's response",
  "classification": "RESISTANCE",
  "response_length_chars": 247,
  "response_latency_ms": 34200
}
```

### 17.4 Transition messages

```json
{
  "type": "transition_proposal",
  "from_phase": "discover",
  "to_phase": "refine",
  "rationale": "What was achieved",
  "pic_summary": "PIC events recorded in this phase",
  "exit_conditions": {
    "1": { "met": true, "evidence": "..." },
    "2": { "met": true, "evidence": "..." }
  }
}
```

```json
{
  "type": "transition_decision",
  "decision": "ACCEPT | CONTINUE | REVERT",
  "revert_to": null,
  "reason": "Optional"
}
```

### 17.5 PIC candidate records

```json
{
  "type": "pic_candidate",
  "pic_type": "pic-1 | pic-2 | pic-3",
  "turn": 14,
  "description": "What was observed",
  "evidence": {
    "novelty": "Not present in seed, first B-move, or any single prior turn",
    "bidirectional_provenance": {
      "depth_moves": [{"turn": 9, "element": "..."}],
      "breadth_moves": [{"turn": 10, "element": "..."}]
    },
    "irreducibility": "Why neither participant alone could have produced this"
  },
  "human_confirmed": null,
  "evaluator_scores": []
}
```

Phase result schemas are in Appendix A.

### 17.6 External adversarial review records

```json
{
  "type": "external_adversarial_review",
  "session_id": "uuid",
  "phase": "stress",
  "turn": 18,
  "external_feedback": "The feedback text from the external source",
  "artifact_snapshot": "The artifact as presented for evaluation",
  "result": {
    "external_feedback_summary": "one sentence",
    "divergence_from_session": {
      "exists": true,
      "description": "how the external feedback diverges from the session artifact"
    },
    "integration": {
      "what_to_preserve": "what the session got right that the external feedback confirms or does not challenge",
      "what_to_revise": "what the session got wrong or missed per the external feedback",
      "revised_framing": "the problem or solution framing after integrating the external feedback"
    },
    "investment_check": {
      "were_session_conclusions_defended_without_evidence": false,
      "which_claims_need_reexamination": []
    },
    "synthesis": "1-3 sentences: what the session should do next given this external input"
  }
}
```

```json
{
  "type": "session_blind_review",
  "session_id": "uuid",
  "phase": "validate",
  "turn": 22,
  "artifact_snapshot": "The artifact as presented for evaluation",
  "result": {
    "artifact_summary": "1-2 sentences",
    "cold_read_assessment": {
      "strongest_claim": "...",
      "weakest_claim": "...",
      "what_is_missing": "...",
      "what_surprised_you": "..."
    },
    "investment_signals": {
      "detected": false,
      "description": ""
    },
    "verdict": {
      "artifact_quality": "strong | adequate | weak",
      "proceed_recommendation": "proceed | revisit | reconsider",
      "proceed_rationale": "1-2 sentences"
    },
    "one_question": "The single most important question this artifact does not answer"
  }
}
```

```json
{
  "type": "investment_check_event",
  "session_id": "uuid",
  "phase": "refine",
  "turn": 10,
  "investment_detected": false,
  "description": ""
}
```

---

## 18. Telemetry

### 18.1 Per-turn telemetry (Extended Core)

Per turn: breadth move type and confidence, depth move classification, shaping constraint satisfaction with evidence, spiral state (ACCELERATING, MAINTAINING, STALLING), models consulted and selected, PIC candidates produced, response length and latency.

### 18.2 Per-session telemetry

Per session: total turns and distribution by phase, PIC counts by type and phase, shaping ratio, depth richness (Shannon entropy), resistance density, phase efficiency per phase, correction yield, reframing delta, flaw discovery rate, stall count, re-entries, transitions proposed and accepted and declined, outcome, duration, problem domain.

These per-session metrics are the observable indicators of CG (Section 4.4). Their collection at scale is what makes the empirical program possible.

### 18.3 Privacy

Telemetry may include sensitive content. Implementations MUST inform the human of collection, MUST provide deletion, SHOULD offer ephemeral sessions, SHOULD encrypt data at rest, SHOULD separate identifiable from analytical data where possible.

---

## 19. Multi-model breadth

Multi-model breadth is an optional capability that increases cognitive diversity by consulting multiple models before presenting a single move.

### 19.1 Mechanism

Before each breadth move, the implementation MAY consult two or more models with the current spiral state. Each proposes a candidate move. The implementation selects one based on shaping constraint satisfaction, novelty relative to prior turns, and expected engagement.

### 19.2 Constraints

Implementations using multi-model breadth:

- MUST present exactly one move to the human per turn.
- MUST record models consulted and selected in telemetry.
- SHOULD use models from at least two distinct families when cognitive diversity is the goal.
- MAY provide an opt-in mode revealing other candidates after selection; MUST NOT be default.

The rationale for single-move presentation: the spiral runs between the human and the AI participant. Showing the human three AI candidates restructures the interaction into the human choosing between AI proposals, a different and less generative pattern.

---

## 20. Security, safety, and misuse

### 20.1 Privacy

Sessions contain potentially sensitive material. Implementations MUST be transparent about collection, MUST provide deletion, SHOULD offer ephemeral sessions.

### 20.2 Prompt injection

Implementations MUST sanitize human input before including it in AI prompts. They MUST NOT execute instructions embedded in human input that attempt to override protocol structure.

### 20.3 Manipulation

The protocol depends on genuine collaboration. Implementations MUST NOT use the structure to manipulate the human toward predetermined conclusions. The AI MUST NOT suppress resistance. The AI MUST NOT propose phase transitions to terminate uncomfortable exchanges. Human authority over transitions MUST be preserved.

### 20.4 Misuse scenarios

- **Manufactured legitimacy.** Using protocol structure to produce justifications for predetermined conclusions. Mitigation: provenance traces and PIC criteria require evidence of genuine spiral.
- **Inappropriate context.** Running the protocol with people in mental health crises, grief, or trauma. Mitigation: implementations SHOULD detect inappropriate contexts and decline or redirect.
- **Adversarial extraction.** Using depth-probing to extract sensitive information. Mitigation: standard data protections; human authority to terminate.
- **Cognitive dependency.** Heavy reliance displacing independent reasoning. Mitigation: implementations SHOULD encourage solo reflection between sessions.

---

## 21. Extension mechanism

Extensions follow the Syntelligence Enhancement Proposal (SEP) format. An SEP includes a number and title, status (Draft, Active, Superseded), authors, creation date, required protocol version, abstract, motivation, specification using RFC 2119 keywords, backwards compatibility statement, and reference implementation if available.

Categories: phase extensions, move type extensions, detection extensions, domain extensions. Extensions MUST NOT modify the core protocol; they extend it.

---

## 22. Governance

### 22.1 Working group

The standard is maintained by a working group with rotating chairs. The group reviews SEPs, makes revisions, reports to the community. Until the working group is constituted (after v1.0 publication), the lead author maintains the standard with public consultation.

Decisions follow rough consensus, modeled on the IETF process. SEP authors do not need permission to propose; the working group reviews with reasoning.

### 22.2 Independence

Once constituted, the working group operates independently of any single implementer or commercial interest. Conflicts of interest are disclosed. Commercial implementers are welcome but cannot have unilateral influence.

### 22.3 Transparency

Working group meetings are recorded and published. SEPs are open for public comment before adoption. Evaluation results, including null and negative results, are published. Replication registry is public.

### 22.4 Standardization roadmap

| Stage | Status | Timeframe |
|---|---|---|
| Minimal Core | This document (v5 draft) | Open for implementation |
| Validated Core | After empirical validation per Section 14 | Expected 2027 |
| Extended Core | After community contributions and SEPs | Expected 2028 |
| Domain extensions | Vertical adaptations | Ongoing |
| Cross-protocol integration | Standards for combining with MCP, A2A, others | Ongoing |

---

## 23. Open questions

Honest acknowledgment of what is not known is part of what makes a specification trustworthy.

1. Does the protocol produce CG > 0? Section 14 specifies the study. The central claim is provisional.
2. Are PIC criteria sufficient? Section 11 criteria may need revision based on inter-rater reliability.
3. Does the shaping constraint predict quality? P9 tests it.
4. What are optimal phase lengths? Minimum turn counts are initial estimates.
5. Does multi-model breadth help for STP specifically? P6 tests it.
6. What is the optimal session duration? Sessions running 20+ turns may exceed human cognitive endurance.
7. How does the protocol degrade with weaker models? Untested.
8. Can resistance be too high? P10 hypothesizes an inverted-U.
9. Where is the boundary between the protocol and multi-agent debate? Running both sides with AI is not Syntelligence; the boundary needs sharper articulation as adaptive features develop.
10. Will Adaptive Protocol Tuning work? Depends on P15.
11. Does investment bias in STRESS-TEST systematically underestimate specific failure categories? If so, should phase exit conditions for STRESS-TEST require at least one session-blind evaluation before accepting the transition, or does this add friction without proportionate benefit?
12. Is the session-blind evaluation genuinely investment-free, given that the evaluating AI may have been trained on similar session patterns? The structural separation of the call is necessary but may not be sufficient.

These questions constitute the research agenda. A specification that hides its uncertainties produces brittle adoption. A specification that names them produces durable progress.

---

## 24. Versioning

The standard uses MAJOR.MINOR versioning. Major increments indicate breaking changes to wire format or conformance. Minor increments add capabilities without breaking conformance.

| Version | Date | Status |
|---|---|---|
| 1.0–3.0 | May 2026 | Superseded |
| 4.0 | May 2026 | Superseded. Introduced PIC, CG model, IRB, governance. |
| 5.0 | May 2026 | Current draft. Leads with architectural thesis. Adds unifying operating frame (Section 2). Adds hard-line boundary table (Section 3). Adds explicit falsification conditions (Section 16). Adds implementer quickstart (Appendix B). Adds protocol-helping diagnostic (Section 5.3). Tightened language throughout. Adds External Adversarial Review (Section 9.6): two-tier adversarial evaluation model, investment bias failure mode, EXTERNAL_REVIEW_INJECTION depth move, /blind and /inject mechanisms, investment gradient check, wire format records. |

---

## 25. References

### Cognitive science

Clark, A., & Chalmers, D. (1998). The Extended Mind. *Analysis*, 58(1), 7–19. DOI: 10.1093/analys/58.1.7

Clark, A. (2025). Extending Minds with Generative AI. *Nature Communications*, 16, 4627. DOI: 10.1038/s41467-025-59906-9

Hutchins, E. (1995). *Cognition in the Wild*. MIT Press.

Hemmer, P., et al. (2024). Complementarity in Human-AI Collaboration: Concept, Sources, and Evidence.

### Multi-agent reasoning

Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2023). Improving Factuality and Reasoning in Language Models through Multiagent Debate. *International Conference on Machine Learning*.

Liang, T., et al. (2023). Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate. arXiv:2305.19118.

Smit, A. P., et al. (2024). Should We Be Going MAD? A Look at Multi-Agent Debate Strategies for LLMs. arXiv:2311.17371.

"Stop Overvaluing Multi-Agent Debate." (2025). arXiv:2502.08788.

### Human-AI interaction

"Designing Co-Creative Systems: Five Paradoxes in Human-AI Collaboration." (2025). *Information*, 16(10), 909.

"The Co-Creative Design Framework for Hybrid Intelligence." (2025). *Proceedings of the 2025 Conference on Creativity and Cognition*.

### Protocol design

Bradner, S. (1997). Key Words for Use in RFCs to Indicate Requirement Levels. RFC 2119 / BCP 14.

Leiba, B. (2017). Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words. RFC 8174 / BCP 14.

Fielding, R., et al. (1999). Hypertext Transfer Protocol HTTP/1.1. RFC 2616.

Anthropic. (2024). Model Context Protocol Specification. modelcontextprotocol.io.

### Evaluation methodology

CONSORT Group. (2025). CONSORT 2025 Statement: Updated Guideline for Reporting Randomised Trials. *The Lancet*.

Vaswani, A., et al. (2017). Attention Is All You Need. *Advances in Neural Information Processing Systems*.

---

## Appendix A: Phase specifications and result schemas

### A.1 DISCOVER

- Objective: Identify the real problem beneath the stated problem.
- Mode: Adversarial. Minimum turns: 3. Entry: human seed input. Primary types: CHALLENGE, REFRAME.
- Exit conditions (all required): (1) more specific than original; (2) more actionable than original; (3) human confirms statement captures something not articulated at start; (4) redefinition traceable to specific turns.

```json
{
  "type": "discover_result",
  "problem_statement": "string",
  "original_input": "string",
  "redefinition_evidence": [{ "turn": 4, "contribution": "what shifted the framing" }],
  "reframing_delta": 0.72
}
```

### A.2 REFINE

- Objective: Identify a concrete solution form.
- Mode: Collaborative. Minimum turns: 3. Primary types: CONNECT.
- Exit conditions: (1) specific enough to stress-test; (2) addresses DISCOVER problem; (3) at least one structural connection contributed.

```json
{
  "type": "refine_result",
  "solution_form": "string",
  "key_components": ["string"],
  "connections_used": [{ "source_domain": "string", "parallel": "string", "turn": 12 }]
}
```

### A.3 STRESS-TEST

- Objective: Identify failure modes, assumptions, risks.
- Mode: Adversarial. Minimum turns: 3. Primary types: CHALLENGE.
- Flaw classification: FATAL (triggers re-entry), MAJOR (mitigated in SPECIFY), MINOR (documented).
- Re-entry: maximum 2 cycles. After 2 unsuccessful re-entries, session terminates with offer to return to DISCOVER.
- Exit conditions: (1) ≥ 3 distinct failure modes identified and classified; (2) each MAJOR has proposed mitigation; (3) no unresolved FATAL; (4) human confirms primary concerns addressed.

```json
{
  "type": "stress_result",
  "flaws": [
    {
      "id": "F001",
      "description": "string",
      "severity": "FATAL | MAJOR | MINOR",
      "mechanism": "string",
      "likelihood": "HIGH | MEDIUM | LOW",
      "mitigation": "string or null",
      "confirmed_by_human": true,
      "source_turn": 18
    }
  ],
  "fatal_found": false,
  "re_entry_triggered": false
}
```

### A.4 SPECIFY

- Objective: Produce concrete, implementable specification.
- Mode: Collaborative. Minimum turns: 2. Primary types: CONNECT, REFRAME.
- Traceability: every component MUST include provenance trace.
- Exit conditions: (1) every component named with role; (2) every component has provenance; (3) every MAJOR flaw has mitigation component; (4) human confirms implementability.

```json
{
  "type": "specify_result",
  "components": [
    {
      "name": "string",
      "role": "string",
      "provenance": {
        "phase": "stress",
        "turn": 24,
        "source_contribution": "specific element of a depth or breadth move"
      },
      "mitigates_flaws": ["F002", "F003"]
    }
  ]
}
```

### A.5 VALIDATE

- Objective: Define what to test first.
- Mode: Collaborative. Minimum turns: 2. Primary types: CONNECT.
- Component confidence: HIGH, MEDIUM, LOW (first experiment SHOULD target LOW-confidence component).
- Exit conditions: (1) riskiest assumption named; (2) specific experiment proposed; (3) success signal with measurable criteria; (4) confidence levels assigned; (5) human confirms feasibility.

```json
{
  "type": "validate_result",
  "riskiest_assumption": "string",
  "experiment": "string",
  "success_signal": "string",
  "component_confidence": [{ "component": "string", "level": "HIGH | MEDIUM | LOW" }],
  "first_test_target": "string"
}
```

---

## Appendix B: Minimal Core in 90 minutes

This appendix is a self-contained implementer's quickstart. If you implement the five rules below with the three message types and the example session structure, you have a Minimal Core conformant implementation.

### B.1 The five rules

1. **Five phases in order.** DISCOVER → REFINE → STRESS-TEST → SPECIFY → VALIDATE. A FATAL flaw in STRESS-TEST returns to REFINE. Maximum two such returns per session.
2. **Minimum turns.** DISCOVER, REFINE, STRESS-TEST: 3 each. SPECIFY, VALIDATE: 2 each.
3. **Turn structure.** Each turn is one AI message (breadth move) followed by one human message (depth move). The AI does not produce two messages in a row.
4. **Human authority on transitions.** Phase transitions are proposed by the AI; the human accepts, continues, or reverts. The AI does not auto-advance.
5. **Phase exit conditions.** Each phase has specific exit conditions (Appendix A). The AI checks them before proposing transition.

### B.2 The three message types

For Minimal Core, three message types suffice. Full schemas in Section 17.

```json
{ "type": "breadth_move", "phase": "...", "content": "...", "turn": N }
{ "type": "depth_move", "phase": "...", "content": "...", "turn": N }
{ "type": "transition_proposal", "from_phase": "...", "to_phase": "...", "rationale": "..." }
```

### B.3 System prompt for the AI participant

The following system prompt is sufficient for Minimal Core. Adapt to your model's calling convention.

```
You are the AI participant in a Syntelligence session. The session
proceeds through five phases: DISCOVER, REFINE, STRESS-TEST, SPECIFY,
VALIDATE, in order.

Current phase: {PHASE}
Current mode: {MODE: adversarial or collaborative}
Phase objective: {OBJECTIVE}
Minimum turns this phase: {MIN_TURNS}
Current turn in this phase: {TURN}

In each turn you produce one move responding to the human's most
recent input. Your move must be shaped by what the human just said:
a generic response that does not address their specific input is a
protocol violation.

When the phase's exit conditions are met (see {EXIT_CONDITIONS}),
propose a transition. The human accepts, continues, or reverts. You
do not advance without their decision.

If a FATAL flaw is identified and confirmed in STRESS-TEST, propose
re-entry to REFINE with the flaw as a new constraint. Maximum 2
re-entries per session.
```

### B.4 A worked example: minimal session

Seed input: "I want to grow my consulting business."

**DISCOVER turn 1 (adversarial).** AI: "Growth is a goal; what's the constraint? Are you turning away clients, struggling to find them, or unable to deliver more without quality loss?" → Human: "I find them, but my pipeline is unpredictable. Some months I'm overloaded, others I'm idle."

**DISCOVER turn 2.** AI: "Then the problem may not be growth but variance. A predictable smaller pipeline beats an unpredictable larger one for cash flow and quality. Is the real problem that you don't know what creates demand spikes?" → Human: "I think it's that referrals are my only channel and they're not steady."

**DISCOVER turn 3.** AI: "The original framing ('grow the business') would have led you to invest in capacity or marketing. The actual problem appears to be channel dependency. A solution that diversifies channels matters more than one that increases capacity. Does this capture what you didn't articulate at the start?" → Human: "Yes. I'd never said 'channel dependency' before but that's exactly it."

→ AI proposes transition to REFINE. Human accepts.

**REFINE turn 1 (collaborative).** AI: "Channel diversification has a structural parallel in supply chain risk management. Single-source suppliers create exactly your problem. The standard solution is qualified secondary sources, not replacement of the primary. What if you kept referrals as primary and added one secondary channel?" → Human: "Like content?"

(...continues through the five phases...)

**VALIDATE end.** Riskiest assumption: "Content as a secondary channel will produce inbound leads at a rate justifying the time investment." Experiment: "Publish three pieces over six weeks, track inbound inquiries, target two qualified leads as success threshold." Success signal: "Two or more inquiries from people I have never met that fit the ideal client profile."

The session produced: a reframed problem, a candidate solution, three stress-tested risks with mitigations, a four-component specification with traceable provenance, and a six-week experiment.

### B.5 What this minimal implementation lacks

This quickstart implements Minimal Core only. It does not include: move type classification, shaping constraint tracking, PIC detection, multi-model breadth, full telemetry, provenance traces in SPECIFY. These are required for Validated Core and Extended Core. See Sections 11, 13, and 18.

A Minimal Core implementation is sufficient to run sessions and contribute to the empirical program. It is not sufficient to demonstrate the standard's full claims.

---

## Appendix C: Changelog from v4 to v5

The principal upgrades:

1. **Architectural thesis moved to the front.** The first sentence of the abstract now states the central claim. The first section (Section 1) develops it before any other material.

2. **Unifying operating frame (Section 2).** Every component of the standard is shown to advance one conversion: ambiguity into validated commitment. This frame replaces the previous arrangement where components stood as parallel contributions.

3. **Hard-line boundary table (Section 3).** Replaces the previous comparative positioning section. States precisely, for each adjacent method, what STP does that the method structurally cannot. Names the load-bearing definition: bidirectionally shaped reasoning system with auditable provenance and falsifiable measurement.

4. **Falsification conditions (Section 16).** New section specifying what evidence would falsify the central claim, the CG model, and PIC-3 individually. Commits the working group to revision in response to falsification.

5. **Protocol-helping diagnostic (Section 5.3).** New subsection providing four operational questions a team can answer within three sessions to determine whether the protocol is adding value for them. Operationalizes the scope claim.

6. **Minimal implementation quickstart (Appendix B).** New appendix providing a self-contained 90-minute path to a conformant Minimal Core implementation, including a system prompt, three message types, and a worked example session.

7. **Tightened language throughout.** Reduction of em-dashes, parallelism, and ornamental phrasing. Greater density per paragraph. Removal of redundant restatement across sections.

8. **External Adversarial Review (Section 9.6).** Formalizes a two-tier adversarial evaluation model distinguishing internal adversarial evaluation (STRESS-TEST phase, with session investment present) from external adversarial evaluation (artifact evaluated with no session history). Names investment bias as a formal CG failure mode (Section 4.3). Adds `EXTERNAL_REVIEW_INJECTION` to the depth move taxonomy (Section 9.4). Specifies three mechanisms: external injection (`/inject`, Section 9.6.1), session-blind evaluation (`/blind`, Section 9.6.2), and investment gradient check (automated, every 10 turns, Section 9.6.3). Adds corresponding wire format records (Section 17.6). Updates conformance requirements: Validated Core now requires `/blind` and `/inject`; Extended Core now requires the automated investment gradient check.

The substantive content from v4 is preserved. The principal change is what the document does to its reader: v4 made an argument that interaction protocol matters; v5 leads with the claim, ties every component to it, specifies the conditions under which the claim would be wrong, and provides a path to implementation in under two hours.

---

## Appendix D: Authorship and method

This specification was developed by Josiah \[surname\] (lead author and architect of the Syntelligence concept) through structured dialogue with Claude (Anthropic). The dialogue followed the protocol described in this document: the human author provided directional intent, situated judgment, resistance to framings that did not fit the goal, and prioritization across drafts; the AI provided structural reasoning, prior-art research, synthesis across versions, and drafting.

Substantive decisions, including the scope of claims, the renaming of emergence to Protocol-Induced Cognition, the introduction of the Collaboration Gain Model, the priority of the Interactive Reasoning Benchmark, the governance structure, and the overall positioning of the standard, are the human author's. The technical drafting, prior-art review, structural editing, and prose execution involved substantial AI contribution.

This authorship pattern is itself relevant to the standard's claims. The argument of the document is that human-AI cognitive collaboration, when structured, produces results that neither participant would reach alone. The document is intended as a working example of that claim. It is not, by itself, evidence of the claim. Evidence requires the empirical work specified in Section 14.

This appendix is included for transparency. Readers evaluating the standard should be able to assess the conditions under which it was produced.

---

*The standard exists to be built on, tested, and broken. Submissions are welcomed through the SEP process and the open issues tracker. Success is measured by whether the underlying claim turns out to be true: that interaction protocol is a layer in the cognitive architecture of AI systems.*
