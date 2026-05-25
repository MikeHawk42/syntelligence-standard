# Syntelligence

AI is good at a narrow band of things. It retrieves, summarizes, generates first drafts. It can answer a question faster than any person alive.

What it is bad at is the harder kind of thinking: whether you are solving the right problem, what assumption you have been making so long you stopped noticing it, how an idea fails before you have committed to it. These are also the things that matter most when the stakes are high.

The reason is structural. In any unstructured conversation with an AI, the AI generates and you react. The AI shapes the frame; you respond to it. The breadth the AI brings — its pattern-matching across everything it has read — never gets corrected by the depth you bring: your years of context, constraint, and situated judgment. The two don't combine. They alternate.

Syntelligence is a protocol that fixes the structure.

---

## How it works

Human intelligence is deep. AI intelligence is broad. The protocol gives both a job.

The AI's job is to produce one move per turn — a challenge, a connection, or a reframe — and to make that move demonstrably shaped by what you just said. Not a generic response. A response that would be different if your previous message did not exist. If it cannot pass that test, it tries again.

Your job is to push back, correct, redirect, or deepen — whatever the move warrants. Not to agree. The protocol treats resistance as the highest-signal input you can give.

The session runs through five phases in sequence. You cannot skip forward.

**DISCOVER.** The AI's job is not to help. It is to challenge whether the problem you stated is the problem you actually have.

**REFINE.** The AI's job is to build — to connect your problem to structural solutions from other domains and produce a concrete direction.

**STRESS-TEST.** The AI's job is to attack what was just built. Every flaw is classified: fatal, major, or minor. A fatal flaw sends you back to Refine.

**SPECIFY.** The AI's job is to make the solution concrete — named components, each traceable to specific exchanges in the session. Nothing generic.

**VALIDATE.** The AI's job is to identify the riskiest assumption in the specification and propose the cheapest possible experiment to test it.

The session ends with a logged output: a reframed problem, a stress-tested solution, a specification with provenance, and a first experiment. Not a summary. A set of things you can act on.

---

## What we do not yet know

The claim behind this protocol is that interaction structure is a third cognitive layer in AI systems, alongside model architecture and training. If the claim holds, changing the protocol while holding the model constant should produce reasoning improvements comparable in magnitude to changing the model.

This claim has not been proven. A 10-session pilot study with pre-registered success criteria is running now to find out. The protocol is published before the results are in because the design is either worth testing or it is not, and the only way to know is to test it.

The pilot result — positive, null, or negative — will be published in full before any further development begins.

---

## Run a session

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python stp_minimal.py
```

Bring a real problem you have been thinking about for at least a week. The session takes 30–90 minutes.

Two commands worth knowing:

`/blind` — passes the current session output to a separate AI call with no session history. A cold read from something that has no investment in what was built. Useful before accepting a phase transition.

`/inject <feedback>` — routes external feedback (from another AI, a colleague, a document) through an investment-free evaluation. Useful when you want a signal from outside the session.

---

## What's in this repository

| File | Description |
|------|-------------|
| `syntelligence-standard-v5.md` | The full v5 specification |
| `stp_minimal.py` | Minimal Core reference implementation |
| `pilot-protocol.md` | Pre-registered 10-session pilot study |

The specification defines the protocol precisely, with falsification conditions — the specific evidence that would require the central claim to be withdrawn. The reference implementation is a single Python file. The pilot protocol commits to success thresholds before data collection begins.

---

## Status

`v5.0.0-draft` — pilot not yet run. Do not build on this for production use until the pilot publishes.

---

*This document was produced by the process it describes.*
