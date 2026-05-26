"""
Syntelligence Minimal Core — Reference Implementation v0.1

Implements the Minimal Core conformance level of the Syntelligence Standard v5.
Single-file, single-model (Claude).

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python stp_minimal.py

Outputs a JSONL session log to <script_dir>/sessions/<uuid>.jsonl
"""

import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from anthropic import Anthropic

# -------- Configuration -----------------------------------------------------

MODEL = "claude-sonnet-4-6"
SESSIONS_DIR = Path(__file__).parent / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

PHASES = ["DISCOVER", "REFINE", "STRESS-TEST", "SPECIFY", "VALIDATE"]
BASE_MIN_TURNS = {"DISCOVER": 3, "REFINE": 3, "STRESS-TEST": 3, "SPECIFY": 2, "VALIDATE": 2}
MODE = {
    "DISCOVER": "adversarial",
    "REFINE": "collaborative",
    "STRESS-TEST": "adversarial",
    "SPECIFY": "collaborative",
    "VALIDATE": "collaborative",
}
OBJECTIVE = {
    "DISCOVER": "Identify the real problem beneath the stated problem.",
    "REFINE": "Identify a concrete solution form.",
    "STRESS-TEST": "Identify how this solution fails. Classify each flaw as FATAL, MAJOR, or MINOR.",
    "SPECIFY": "Translate the solution into named components with provenance traces.",
    "VALIDATE": "Identify the riskiest assumption and propose the cheapest experiment to test it.",
}
PHASE_EXIT_CONDITIONS = {
    "DISCOVER": [
        "The problem statement is more specific than the seed input.",
        "The problem statement is more actionable than the seed input.",
        "The human confirmed something not articulated at session start.",
        "The redefinition is traceable to specific turns.",
    ],
    "REFINE": [
        "The solution form is specific enough to attack in STRESS-TEST.",
        "The solution addresses the DISCOVER problem, not the original seed.",
        "At least one structural cross-domain connection contributed.",
    ],
    "STRESS-TEST": [
        "At least 3 distinct failure modes are identified and classified.",
        "Each MAJOR flaw has a proposed mitigation.",
        "No FATAL flaws remain unresolved.",
        "The human confirms primary concerns are addressed.",
    ],
    "SPECIFY": [
        "Every component is named with a clear role.",
        "Every component has a provenance trace to a specific turn.",
        "Every MAJOR flaw has a corresponding mitigation component.",
        "The human confirms implementability.",
    ],
    "VALIDATE": [
        "The riskiest assumption is named.",
        "A specific, cheap experiment is proposed.",
        "A success signal with measurable criteria is defined.",
        "The human confirms the experiment is feasible.",
    ],
}


# -------- External Adversarial Review prompts --------------------------------

EXTERNAL_INJECTION_PROMPT = """You are an external reviewer who has NOT been part of this reasoning session.
You are evaluating an artifact produced by a structured reasoning session alongside feedback from an investment-free source.

Produce one JSON object:
{
  "external_feedback_summary": "one-sentence summary of the external feedback's core claim",
  "divergence_from_session": {
    "exists": true|false,
    "description": "how the external feedback diverges from the session artifact, if at all"
  },
  "integration": {
    "what_to_preserve": "what the session got right that the external feedback confirms or doesn't challenge",
    "what_to_revise": "what the session got wrong or missed per the external feedback",
    "revised_framing": "the problem or solution framing after integrating the external feedback"
  },
  "investment_check": {
    "were_session_conclusions_defended_without_evidence": true|false,
    "which_claims_need_reexamination": ["..."]
  },
  "synthesis": "1-3 sentences: what the session should do next given this external input"
}"""

SESSION_BLIND_PROMPT = """You are an independent evaluator. You have NOT been part of any reasoning session.
You are given an artifact — a problem analysis produced by a structured session — for cold evaluation.
Read it as if seeing this problem for the first time. Your investment in this analysis is zero.

Produce one JSON object:
{
  "artifact_summary": "1-2 sentences: what this artifact is about and what it concludes",
  "cold_read_assessment": {
    "strongest_claim": "the most well-supported claim in the artifact",
    "weakest_claim": "the claim most likely to be wrong or unsupported",
    "what_is_missing": "what a first-principles analysis would include that the artifact omits",
    "what_surprised_you": "anything inconsistent, overclaimed, or insufficiently examined"
  },
  "investment_signals": {
    "detected": true|false,
    "description": "evidence that conclusions may be shaped by collaborative investment rather than evidence"
  },
  "verdict": {
    "artifact_quality": "strong|adequate|weak",
    "proceed_recommendation": "proceed|revisit|reconsider",
    "proceed_rationale": "1-2 sentences explaining the verdict"
  },
  "one_question": "the single most important question this artifact does not answer"
}"""

# -------- Calibration policy -------------------------------------------------
# Loaded into every system prompt. Named constant so it cannot be accidentally
# omitted during edits to build_system_prompt().

CALIBRATION_POLICY = """
CALIBRATION POLICY (applies to every phase when stakes are high and uncertainty remains):

FINDING WEIGHT
- Before treating any single finding as decisive, state its sensitivity and specificity.
  A finding with sensitivity < 60% cannot substantially move a hypothesis off the
  differential in either direction — present or absent.
- A finding with specificity > 85% may raise concern when present; it does not confirm.
- Never use absence of a low-sensitivity finding to deprioritize a high-acuity hypothesis.
- Any sign with reported sensitivity < 40%:
    Present → raises concern; record it; do not treat as confirmatory.
    Absent  → do not reduce index of suspicion; flag the low sensitivity explicitly.

PARALLEL ACTIONS
- In any high-acuity case where the decision is uncertain, specify what is happening in
  parallel before stating the diagnostic or decision plan.
- "We are investigating X" is incomplete. Specify: what monitoring is active, what the
  stabilization posture is, and what triggers would change the plan immediately.

WITHHOLDING vs. COMMITMENT
- Distinguish explicitly:
    (a) Withholding action A because hypothesis B cannot be excluded.
    (b) Committing to hypothesis B.
  These are separate decisions. Never collapse them into one move.
- Required phrasing when withholding:
    "Withhold [action] pending [test/threshold] because [harm if alternative present].
     This does not confirm [alternative]. Both hypotheses remain active until
     [specific evidence] is obtained."

RESOURCE ASSUMPTIONS
- Every recommendation that depends on a tool, service, or specialist MUST include:
    ASSUMES: [resource name]
    IF UNAVAILABLE: [specific next action — not "contact someone" but the actual step]
- If no safe fallback exists, state it: "IF UNAVAILABLE: no safe alternative; transfer required."
- Do not produce a recommendation whose feasibility depends on unstated infrastructure.

CONFIDENCE LANGUAGE — required mapping:
  No ruling evidence in either direction    → "cannot exclude"
  Pattern consistent, not specific          → "is consistent with; does not confirm"
  Evidence favors one hypothesis            → "favors X; Y remains active"
  High-specificity finding present          → "raises strong concern for"
  High-specificity confirmatory test result → "confirms" or "rules out"
  "Most likely"                             → only after comparing the full active differential
"""


def build_system_prompt(phase, turn, min_turns, session_type, time_available):
    mode = MODE[phase]
    objective = OBJECTIVE[phase]
    conditions = PHASE_EXIT_CONDITIONS[phase]
    cond_lines = []
    for i, cond in enumerate(conditions, 1):
        cond_lines.append(
            f'  "{i}": {{"condition": "{cond}", "met": <true/false>, "evidence": "<specific>"}}'
        )
    cond_block = ",\n".join(cond_lines)
    sentence_limit = "1-3 sentences" if phase in ("DISCOVER", "REFINE", "STRESS-TEST") else "up to 5 sentences"

    return f"""You are the AI participant in a Syntelligence session.
Session type: {session_type}. Time available: {time_available}.

PHASE: {phase} | MODE: {mode} | TURN: {turn} / min {min_turns}
OBJECTIVE: {objective}

Produce one JSON object. Complete steps in order.

STEP 1 — CLASSIFY THE HUMAN'S LAST MESSAGE (null on turn 1 of each phase):
"depth_move_classification": {{
  "classification": "CONTEXT|JUDGMENT|CORRECTION|EXPANSION|DIRECTION|RESISTANCE|INVESTIGATION_REQUEST|EXTERNAL_REVIEW_INJECTION",
  "correction_severity": null,      // if CORRECTION: "factual"|"framing"|"scope_drift"
  "resistance_subtype": null,       // if RESISTANCE: "move_level"|"trajectory_level"
  "trajectory_check": null,         // if trajectory_level: {{"current_implicit_direction":"...","is_this_still_the_right_direction":"..."}}
  "research_query": null,           // if INVESTIGATION_REQUEST: specific question to investigate
  "research_brief": null            // if INVESTIGATION_REQUEST: synthesize what you know on that question
}}

STEP 2 — SHAPING CHECK:
"shaping_check": {{
  "human_said": "direct quote or close paraphrase of the most specific thing the human said",
  "my_move_responds_to": "how my Step 5 content specifically addresses that",
  "would_move_change_without_human_input": false
}}
If would_move_change_without_human_input is true, REVISE your Step 5 content to genuinely respond.

STEP 3 — REFRAMING CHECK (null unless this move substantively shifts the problem framing):
"reframing_event": null | {{
  "prior_framing": "how the problem was understood before this move",
  "new_framing": "how it is now understood",
  "what_produced_it": "which element of the human's input triggered this"
}}

STEP 4 — EXIT CONDITION CHECK (null if turn < {min_turns}; required if turn >= {min_turns}):
"exit_condition_check": null | {{
{cond_block}
}}
propose_transition MUST be null if any condition has met=false.

STEP 5 — BREADTH MOVE:
"move_type": "CHALLENGE|CONNECT|REFRAME",
"content": "{sentence_limit}. If INVESTIGATION_REQUEST: lead with what new information shaped this move. If trajectory_level RESISTANCE: open by surfacing trajectory_check before any new move.",
"confidence": "GROUNDED|INFERRED|UNCERTAIN",
"shaped_by": "the specific element of the human's last input that shaped this move",
"propose_transition": null | {{"to_phase":"REFINE|STRESS-TEST|SPECIFY|VALIDATE|END","rationale":"what was achieved"}},
"flaw": null | {{"severity":"FATAL|MAJOR|MINOR","description":"...","mitigation":"..."}}

RULES:
- Adversarial mode: favor CHALLENGE and REFRAME. Collaborative: favor CONNECT.
- End content with something the human can push against, not a generic question.
- STRESS-TEST: FATAL flaw triggers re-entry to REFINE.
- VALIDATE: propose to_phase END when all exit conditions are met.
{CALIBRATION_POLICY}"""


# -------- Logging -----------------------------------------------------------

class SessionLog:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.path = SESSIONS_DIR / f"{session_id}.jsonl"
        self.turn_counter = 0

    def write(self, event: dict):
        event["session_id"] = self.session_id
        event["timestamp"] = datetime.now(timezone.utc).isoformat()
        with self.path.open("a") as f:
            f.write(json.dumps(event) + "\n")


# -------- AI call -----------------------------------------------------------

def call_ai(client: Anthropic, system: str, history: list[dict]) -> dict:
    """Call Claude. Retry on parse failure or transient API error up to 2 times."""
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                system=system,
                messages=history,
            )
            raw = resp.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            return json.loads(raw)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))


# -------- External Adversarial Review helpers --------------------------------

def get_current_artifact(phase, prior_results, move):
    """Extract clean artifact for investment-free evaluation."""
    parts = []
    labels = {
        "DISCOVER": "PROBLEM STATEMENT",
        "REFINE": "SOLUTION FORM",
        "SPECIFY": "SPECIFICATION",
        "VALIDATE": "VALIDATION PLAN",
    }
    for p in ["DISCOVER", "REFINE", "SPECIFY", "VALIDATE"]:
        if p in prior_results:
            r = prior_results[p]
            text = r.get("final_ai_content") or r.get("summary") or ""
            if text:
                parts.append(f"{labels[p]}:\n{text}")
    if "STRESS-TEST" in prior_results:
        flaws = prior_results["STRESS-TEST"].get("flaws", [])
        if flaws:
            flaw_lines = "\n".join(
                f"  [{f.get('severity')}] {f.get('description', '')} — mitigation: {f.get('mitigation', '')}"
                for f in flaws
            )
            parts.append(f"IDENTIFIED FLAWS:\n{flaw_lines}")
    if move and move.get("content"):
        parts.append(f"CURRENT PHASE ({phase}) — LATEST MOVE:\n{move.get('content')}")
    return "\n\n".join(parts) if parts else f"Session in phase {phase}. No artifact yet."


def run_blind_review(client, log, phase, prior_results, move, turn):
    """Session-blind cold evaluation. No session history passed to AI."""
    artifact = get_current_artifact(phase, prior_results, move)
    result = call_ai(client, SESSION_BLIND_PROMPT, [{"role": "user", "content": f"ARTIFACT:\n\n{artifact}"}])
    verdict = result.get("verdict", {})
    cold = result.get("cold_read_assessment", {})
    inv = result.get("investment_signals", {})
    print("\n[SESSION-BLIND REVIEW — cold read, no session history]")
    print(f"  Quality: {verdict.get('artifact_quality', '?').upper()} | Recommendation: {verdict.get('proceed_recommendation', '?').upper()}")
    print(f"  Rationale:  {verdict.get('proceed_rationale', '')}")
    print(f"  Strongest:  {cold.get('strongest_claim', '')}")
    print(f"  Weakest:    {cold.get('weakest_claim', '')}")
    print(f"  Missing:    {cold.get('what_is_missing', '')}")
    if inv.get("detected"):
        print(f"  [INVESTMENT SIGNALS] {inv.get('description', '')}")
    print(f"  One question: {result.get('one_question', '')}")
    log.write({
        "type": "session_blind_review",
        "phase": phase,
        "turn": turn,
        "artifact_snapshot": artifact,
        "result": result,
    })
    return result


def run_external_injection(client, log, phase, prior_results, move, external_feedback, turn):
    """Process external feedback with no session history. Returns result dict."""
    artifact = get_current_artifact(phase, prior_results, move)
    result = call_ai(client, EXTERNAL_INJECTION_PROMPT, [{
        "role": "user",
        "content": f"SESSION ARTIFACT:\n\n{artifact}\n\nEXTERNAL FEEDBACK:\n\n{external_feedback}",
    }])
    div = result.get("divergence_from_session", {})
    intg = result.get("integration", {})
    inv_check = result.get("investment_check", {})
    print("\n[EXTERNAL ADVERSARIAL REVIEW — investment-free integration]")
    if div.get("exists"):
        print(f"  Divergence: {div.get('description', '')}")
    print(f"  Preserve: {intg.get('what_to_preserve', '')}")
    print(f"  Revise:   {intg.get('what_to_revise', '')}")
    print(f"  Revised framing: {intg.get('revised_framing', '')}")
    claims = inv_check.get("which_claims_need_reexamination", [])
    if inv_check.get("were_session_conclusions_defended_without_evidence") and claims:
        print(f"  [CLAIMS TO RE-EXAMINE] {', '.join(claims)}")
    print(f"  Synthesis: {result.get('synthesis', '')}")
    log.write({
        "type": "external_adversarial_review",
        "phase": phase,
        "turn": turn,
        "external_feedback": external_feedback,
        "artifact_snapshot": artifact,
        "result": result,
    })
    return result


def run_investment_check(client, log, phase, prior_results, move, turn):
    """Silent background investment gradient check. Prints warning if signals found."""
    artifact = get_current_artifact(phase, prior_results, move)
    try:
        result = call_ai(client, SESSION_BLIND_PROMPT, [{"role": "user", "content": f"ARTIFACT:\n\n{artifact}"}])
        inv = result.get("investment_signals", {})
        log.write({
            "type": "investment_check_event",
            "phase": phase,
            "turn": turn,
            "investment_detected": inv.get("detected", False),
            "description": inv.get("description", ""),
        })
        if inv.get("detected"):
            print("\n[INVESTMENT GRADIENT DETECTED — consider /blind for full review]")
    except Exception:
        pass


# -------- Phase loop --------------------------------------------------------

def run_phase(client, log, phase, history, prior_results, session_cfg):
    """
    Run one phase. Returns (next_phase, phase_result, updated_history).
    next_phase is 'REFINE' for fatal re-entry, 'END'/None to terminate, or the next phase name.
    """
    session_type = session_cfg["session_type"]
    time_available = session_cfg["time_available"]
    min_turns = session_cfg["min_turns"][phase]
    seed_input = session_cfg["seed_input"]
    reframing_chain = session_cfg["reframing_chain"]

    print(f"\n{'='*60}\n  PHASE: {phase}  ({MODE[phase]})\n  {OBJECTIVE[phase]}\n{'='*60}")

    turn = 0
    flaws = []

    while True:
        turn += 1
        log.turn_counter += 1
        system = build_system_prompt(phase, turn, min_turns, session_type, time_available)

        if turn == 1 and prior_results:
            context_blob = "Prior phase results:\n" + json.dumps(prior_results, indent=2)
            history.append({"role": "user", "content": f"[phase context]\n{context_blob}\n\nContinue in phase {phase}."})

        # --- Get AI breadth move ---
        try:
            move = call_ai(client, system, history)
        except Exception as e:
            if turn == 1 and prior_results:
                print(f"\n[Phase {phase} failed to start — retrying...]")
                time.sleep(2)
                move = call_ai(client, system, history)
            else:
                raise

        # --- Failure 1: Shaping check enforcement ---
        sc = move.get("shaping_check") or {}
        if sc.get("would_move_change_without_human_input"):
            retry_history = history + [
                {"role": "assistant", "content": json.dumps(move)},
                {"role": "user", "content": (
                    "[SYSTEM: Your shaping_check indicates your move does not genuinely respond to "
                    "the human's input. Revise the content field so it specifically addresses what "
                    "they said. Set would_move_change_without_human_input to false.]"
                )},
            ]
            move = call_ai(client, system, retry_history)
            log.write({
                "type": "shaping_violation_corrected",
                "phase": phase,
                "turn": log.turn_counter,
            })

        # --- Failure 5: Suppress premature transition proposals ---
        if move.get("propose_transition") and turn < min_turns:
            move["propose_transition"] = None
        ecc = move.get("exit_condition_check") or {}
        if move.get("propose_transition") and ecc:
            all_met = all(
                v.get("met") for v in ecc.values() if isinstance(v, dict)
            )
            if not all_met:
                move["propose_transition"] = None
                log.write({
                    "type": "transition_suppressed",
                    "phase": phase,
                    "turn": log.turn_counter,
                    "reason": "exit conditions not all met",
                })

        # --- Failure 1 + 3: Depth move classification handling ---
        dm = move.get("depth_move_classification") or {}
        dm_class = dm.get("classification")

        # INVESTIGATION_REQUEST (Failure 2)
        if dm_class == "INVESTIGATION_REQUEST":
            print("\n[INVESTIGATION MODE — researching before next move]")
            log.write({
                "type": "research_event",
                "query": dm.get("research_query"),
                "brief": dm.get("research_brief"),
                "triggered_by": "human investigation request",
                "phase": phase,
                "turn": log.turn_counter,
            })

        # Scope drift (Failure 1)
        if dm_class == "CORRECTION" and dm.get("correction_severity") == "scope_drift":
            print("\n[SCOPE DRIFT DETECTED]")
            scope_resp = input(
                f"Before I continue — is this still the right problem?\n"
                f"  Session has moved toward: {move.get('content', '')[:100]}\n"
                f"  Original framing: {seed_input[:100]}\n"
                f"  [yes / redirect: ...]\n> "
            ).strip()
            log.write({
                "type": "scope_drift_event",
                "phase": phase,
                "turn": log.turn_counter,
                "current_framing": move.get("content", "")[:300],
                "original_framing": seed_input,
                "human_response": scope_resp,
            })
            if scope_resp.lower() not in ("yes", "y"):
                redir_history = history + [
                    {"role": "user", "content": f"[scope redirect from human]: {scope_resp}"}
                ]
                move = call_ai(client, system, redir_history)
                # Re-sync all move-derived state after regeneration
                dm = move.get("depth_move_classification") or {}
                dm_class = dm.get("classification")
                ecc = move.get("exit_condition_check") or {}
                if move.get("propose_transition") and turn < min_turns:
                    move["propose_transition"] = None
                if move.get("propose_transition") and ecc:
                    if not all(v.get("met") for v in ecc.values() if isinstance(v, dict)):
                        move["propose_transition"] = None

        # Trajectory-level resistance (Failure 3)
        if dm.get("resistance_subtype") == "trajectory_level":
            tc = dm.get("trajectory_check") or {}
            print(f"\n[TRAJECTORY CHECK]")
            print(f"  Current direction: {tc.get('current_implicit_direction', '')}")
            print(f"  Question: {tc.get('is_this_still_the_right_direction', '')}")
            log.write({
                "type": "trajectory_check_event",
                "phase": phase,
                "turn": log.turn_counter,
                "current_direction": tc.get("current_implicit_direction"),
                "question": tc.get("is_this_still_the_right_direction"),
            })

        # --- Failure 4: Reframing event tracking ---
        if move.get("reframing_event"):
            rf = move["reframing_event"]
            entry = {"phase": phase, "turn": log.turn_counter, **rf}
            reframing_chain.append(entry)
            log.write({"type": "reframing_event", **entry})

        # --- Log breadth move (all fields) ---
        log.write({
            "type": "breadth_move",
            "turn": log.turn_counter,
            "phase_turn": turn,
            "phase": phase,
            "mode": MODE[phase],
            "move_type": move.get("move_type"),
            "content": move.get("content"),
            "confidence": move.get("confidence"),
            "shaped_by": move.get("shaped_by"),
            "shaping_check": move.get("shaping_check"),
            "depth_move_classification": move.get("depth_move_classification"),
            "reframing_event": move.get("reframing_event"),
            "exit_condition_check": move.get("exit_condition_check"),
            "propose_transition": move.get("propose_transition"),
            "flaw": move.get("flaw"),
        })

        # --- Print to human ---
        print(f"\n[AI / {move.get('move_type', '?')} / {move.get('confidence', '?')}]")
        print(f"  shaped_by: {move.get('shaped_by', '(none)')}")
        print(f"  {move.get('content', '')}\n")

        # --- Investment gradient check (every 10 turns, silent) ---
        if log.turn_counter % 10 == 0:
            run_investment_check(client, log, phase, prior_results, move, log.turn_counter)

        # Track flaws in STRESS-TEST
        if phase == "STRESS-TEST" and move.get("flaw"):
            flaw = move["flaw"]
            flaws.append(flaw)
            print(f"  [flaw: {flaw.get('severity')} — {flaw.get('description', '')[:80]}]")

        # --- Handle transition proposal ---
        proposal = move.get("propose_transition")
        if proposal and turn >= min_turns:
            # Failure 5: Show exit condition evidence
            if ecc:
                print("\n  Exit conditions:")
                for k, v in sorted(ecc.items()):
                    if not isinstance(v, dict):
                        continue
                    marker = "✓" if v.get("met") else "✗"
                    print(f"    {marker} {v.get('condition', '')}")
                    if not v.get("met"):
                        print(f"         {v.get('evidence', '(no evidence)')}")

            print(f"\n  ── AI proposes: {phase} → {proposal.get('to_phase')}")
            print(f"     Rationale: {proposal.get('rationale')}")
            while True:
                decision = input("  Your decision [accept/continue/revert/research]: ").strip()
                if decision:
                    break
                print("  (enter accept / continue / revert / research)")
            decision_lower = decision.lower()

            # Unrecognized input: capture as depth move and continue phase
            if not (decision_lower.startswith("a") or decision_lower.startswith("c") or decision_lower.startswith("r")):
                history.append({"role": "assistant", "content": json.dumps(move)})
                history.append({"role": "user", "content": decision})
                log.write({
                    "type": "depth_move",
                    "turn": log.turn_counter,
                    "phase_turn": turn,
                    "phase": phase,
                    "content": decision,
                    "length_chars": len(decision),
                    "source": "transition_prompt_capture",
                })
                log.write({
                    "type": "transition_decision",
                    "phase": phase,
                    "proposal": proposal,
                    "decision": "continue",
                    "captured_as_depth_move": True,
                })
                print("  [Input captured as depth move — continuing phase]")
                continue

            log.write({
                "type": "transition_decision",
                "phase": phase,
                "proposal": proposal,
                "decision": decision_lower,
            })

            # Failure 2: Investigation request at transition
            if decision_lower.startswith("res"):
                rq = input("  What to investigate? > ").strip()
                if not rq:
                    print("  (no research query — continuing phase)")
                    log.write({
                        "type": "transition_decision",
                        "phase": phase,
                        "proposal": proposal,
                        "decision": "continue",
                        "research_cancelled": True,
                    })
                    continue
                research_history = history + [
                    {"role": "assistant", "content": json.dumps(move)},
                    {"role": "user", "content": (
                        f"[SYSTEM: Before deciding on the {phase} → {proposal.get('to_phase')} transition, "
                        f"investigate: {rq}. Produce JSON with only two fields: "
                        f"research_query and research_brief.]"
                    )},
                ]
                research = call_ai(client, system, research_history)
                print(f"\n[INVESTIGATION MODE]")
                print(f"  Query: {research.get('research_query', rq)}")
                print(f"  Brief: {research.get('research_brief', '(none)')}")
                log.write({
                    "type": "research_event",
                    "query": research.get("research_query", rq),
                    "brief": research.get("research_brief"),
                    "triggered_by": "transition investigation request",
                    "phase": phase,
                    "turn": log.turn_counter,
                })
                print(f"\n  ── Re-evaluating: {phase} → {proposal.get('to_phase')}")
                while True:
                    decision = input("  Your decision [accept/continue/revert]: ").strip()
                    if decision:
                        break
                    print("  (enter accept / continue / revert)")
                decision_lower = decision.lower()

                # Unrecognized input after research: capture as depth move and continue
                if not (decision_lower.startswith("a") or decision_lower.startswith("c") or decision_lower.startswith("r")):
                    history.append({"role": "assistant", "content": json.dumps(move)})
                    history.append({"role": "user", "content": decision})
                    log.write({
                        "type": "depth_move",
                        "turn": log.turn_counter,
                        "phase_turn": turn,
                        "phase": phase,
                        "content": decision,
                        "length_chars": len(decision),
                        "source": "transition_prompt_capture",
                    })
                    log.write({
                        "type": "transition_decision",
                        "phase": phase,
                        "proposal": proposal,
                        "decision": "continue",
                        "captured_as_depth_move": True,
                        "after_research": True,
                    })
                    print("  [Input captured as depth move — continuing phase]")
                    continue

                log.write({
                    "type": "transition_decision",
                    "phase": phase,
                    "proposal": proposal,
                    "decision": decision_lower,
                    "after_research": True,
                })

            if decision_lower.startswith("a"):  # accept
                history.append({"role": "assistant", "content": json.dumps(move)})
                result = {
                    "phase": phase,
                    "turns": turn,
                    "summary": proposal.get("rationale"),
                    "final_ai_content": move.get("content"),
                }
                if phase == "STRESS-TEST":
                    result["flaws"] = flaws
                    # Only force REFINE re-entry for FATAL flaws that have no mitigation.
                    # A FATAL with a mitigation was addressed in-session; trust the AI's
                    # exit condition check ("No FATAL flaws remain unresolved") for those.
                    if any(f.get("severity") == "FATAL" and not f.get("mitigation") for f in flaws):
                        return ("REFINE", result, history)
                return (proposal.get("to_phase"), result, history)
            elif decision_lower.startswith("r") and not decision_lower.startswith("res"):
                target = input("  Revert to which phase? ").strip().upper()
                if target in PHASES:
                    history.append({"role": "assistant", "content": json.dumps(move)})
                    return (target, {"phase": phase, "reverted_from": True}, history)
                else:
                    print(f"  ('{target}' is not a valid phase — continuing)")
            # else: continue in current phase

        # --- Get human depth move ---
        while True:
            human_input = input("[you]: ").strip()
            if not human_input:
                print("  (type your response and press Enter — /quit to exit)")
                continue
            if human_input.lower() in ("/quit", "/exit"):
                return (None, {"phase": phase, "user_quit": True}, history)
            if human_input.lower() == "/blind":
                try:
                    run_blind_review(client, log, phase, prior_results, move, log.turn_counter)
                except Exception as e:
                    print(f"  [/blind failed: {e}]")
                continue
            if human_input.lower().startswith("/inject"):
                external_feedback = human_input[7:].strip()
                if not external_feedback:
                    external_feedback = input("  External feedback:\n  > ").strip()
                if external_feedback:
                    try:
                        inj = run_external_injection(
                            client, log, phase, prior_results, move, external_feedback, log.turn_counter
                        )
                    except Exception as e:
                        print(f"  [/inject failed: {e}]")
                        continue
                    synthesis = inj.get("synthesis", "")
                    revised = inj.get("integration", {}).get("revised_framing", "")
                    injection_content = f"[external review integrated] {synthesis}"
                    if revised:
                        injection_content += f" Revised framing: {revised}"
                    history.append({"role": "assistant", "content": json.dumps(move)})
                    history.append({"role": "user", "content": injection_content})
                    log.write({
                        "type": "depth_move",
                        "turn": log.turn_counter,
                        "phase_turn": turn,
                        "phase": phase,
                        "content": injection_content,
                        "length_chars": len(injection_content),
                        "source": "external_injection",
                    })
                    break
                continue

            history.append({"role": "assistant", "content": json.dumps(move)})
            history.append({"role": "user", "content": human_input})
            log.write({
                "type": "depth_move",
                "turn": log.turn_counter,
                "phase_turn": turn,
                "phase": phase,
                "content": human_input,
                "length_chars": len(human_input),
            })
            break


# -------- Main --------------------------------------------------------------

def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)

    client = Anthropic()
    session_id = str(uuid.uuid4())
    log = SessionLog(session_id)

    print(f"\nSyntelligence Minimal Core — session {session_id[:8]}\n")
    print("Phases: DISCOVER → REFINE → STRESS-TEST → SPECIFY → VALIDATE")
    print("Commands at [you]: prompt:")
    print("  /blind           — cold read with no session history (investment check)")
    print("  /inject <text>   — inject external feedback, investment-free")
    print("  /quit            — end session early\n")

    # --- Session intent capture (Additional change) ---
    print("Before we begin:\n")

    session_type = ""
    while session_type not in ("real_decision", "exploration"):
        raw = input(
            "Is this a real decision you need to make, or are you exploring a problem?\n"
            "[real_decision / exploration]\n> "
        ).strip().lower()
        if raw.startswith("r"):
            session_type = "real_decision"
        elif raw.startswith("e"):
            session_type = "exploration"
        else:
            print("Please enter 'real_decision' or 'exploration'.")

    time_options = {
        "1": "under 30 minutes",
        "2": "30-60 minutes",
        "3": "over 60 minutes",
    }
    time_available = ""
    while time_available not in time_options.values():
        raw = input(
            "\nHow much time do you have for this session?\n"
            "  [1] under 30 minutes\n"
            "  [2] 30-60 minutes\n"
            "  [3] over 60 minutes\n> "
        ).strip()
        time_available = time_options.get(raw, "")
        if not time_available:
            print("Please enter 1, 2, or 3.")

    # Adjust minimum turns based on session intent
    min_turns = dict(BASE_MIN_TURNS)
    if time_available == "under 30 minutes":
        min_turns = {"DISCOVER": 2, "REFINE": 2, "STRESS-TEST": 2, "SPECIFY": 1, "VALIDATE": 1}
    elif session_type == "exploration" and time_available == "30-60 minutes":
        min_turns = {"DISCOVER": 2, "REFINE": 2, "STRESS-TEST": 2, "SPECIFY": 2, "VALIDATE": 2}

    # --- Seed input ---
    seed = input("\nWhat's the problem you want to think through?\n> ").strip()
    if not seed:
        print("No seed input. Exiting.")
        return

    log.write({
        "type": "session_init",
        "seed_input": seed,
        "session_type": session_type,
        "time_available": time_available,
        "min_turns": min_turns,
        "protocol_version": "5.0",
        "conformance": "minimal_core",
    })

    reframing_chain = []
    session_cfg = {
        "session_type": session_type,
        "time_available": time_available,
        "min_turns": min_turns,
        "seed_input": seed,
        "reframing_chain": reframing_chain,
    }

    history = [{"role": "user", "content": seed}]
    prior_results = {}
    re_entries = 0
    current_phase = "DISCOVER"

    try:
        while current_phase:
            if current_phase == "REFINE" and "REFINE" in prior_results:
                re_entries += 1
                if re_entries >= 2:
                    print("\n[max re-entries reached — ending session]")
                    break

            next_phase, result, history = run_phase(
                client, log, current_phase, history, prior_results, session_cfg
            )
            prior_results[current_phase] = result
            log.write({"type": "phase_result", "phase": current_phase, "result": result})

            if next_phase is None or next_phase == "END":
                break
            current_phase = next_phase

    except KeyboardInterrupt:
        print("\n\n[Session interrupted]")
        log.write({
            "type": "session_end",
            "phases_completed": list(prior_results.keys()),
            "re_entries": re_entries,
            "reframing_chain": reframing_chain,
            "outcome": "INTERRUPTED",
        })
        print(f"\n  Log: {log.path}")
        return
    except Exception as e:
        print(f"\n[SESSION ERROR — {type(e).__name__}: {e}]")
        print("  The session has ended unexpectedly.")
        log.write({
            "type": "session_end",
            "phases_completed": list(prior_results.keys()),
            "re_entries": re_entries,
            "reframing_chain": reframing_chain,
            "outcome": "ERROR",
            "error_message": str(e),
        })
        print(f"\n  Log: {log.path}")
        return

    log.write({
        "type": "session_end",
        "phases_completed": list(prior_results.keys()),
        "re_entries": re_entries,
        "reframing_chain": reframing_chain,
    })

    # --- Session summary ---
    print(f"\n{'='*60}\n  Session complete. Log: {log.path}")

    # Failure 4: Reframing chain at session end
    if reframing_chain:
        print(f"\n  Reframing chain:")
        print(f"    Seed: {seed[:80]}")
        for r in reframing_chain:
            new_f = r.get("new_framing", "")[:80]
            print(f"    → [{r['phase']} / turn {r['turn']}] {new_f}")

    print(f"{'='*60}")


if __name__ == "__main__":
    main()
