# Syntelligence Pilot Study Protocol

### A 10-session pilot to determine whether the protocol produces value before committing to a larger study

**Status:** Pre-registered pilot. Run before collecting data. Commit to the analysis plan before recruiting.

---

## Why pre-commit before running

The pilot's purpose is to find out whether the protocol does anything useful. The standard failure mode of small studies is post-hoc interpretation: "session 3 went badly because the user wasn't engaged, session 7 doesn't count because the problem was wrong for the protocol, session 9 was a hit." This is how projects survive evidence that should have killed them.

This protocol pre-commits to:

1. What problems count as in-scope.
2. What the session must produce to count as a positive outcome.
3. What thresholds across the ten sessions count as success, ambiguous, or failure.
4. What the pilot will conclude before any sessions are run.

The cost of pre-committing is that some sessions will be excluded for legitimate reasons. The benefit is that the result, whatever it is, is interpretable.

---

## Recruitment

### Who

Ten participants, recruited from network. Each brings one real problem they are actually trying to solve and would otherwise think about alone or with unstructured AI chat. Not contrived problems. Not problems pre-shaped to fit the protocol.

### Inclusion criteria for the problem

A problem qualifies if the participant can answer yes to all of the following before the session:

1. "I have been thinking about this for at least a week and haven't reached a decision."
2. "If I decide wrong, there are consequences I would care about."
3. "I don't fully know what the right framing of the problem is."
4. "Acting on the wrong solution would cost me time, money, relationships, or opportunity."

These four questions are asked at recruitment and the answers are logged. Problems that fail any criterion are excluded from the analysis but the session can still be run if useful.

### Exclusion criteria

Exclude anyone who:

- Has previously been told about Syntelligence in detail. (Avoids demand characteristics.)
- Is in crisis (emotional, financial, medical). The adversarial phases are inappropriate.
- Wants help with a technical execution task. Out of scope per Section 5.

Aim for at least three problems in genuinely different domains. If all ten are "should I quit my job" or "how do I grow my startup," the pilot tells you nothing about generalization.

---

## Pre-session

For each participant, log before the session:

1. **The problem statement** (verbatim, in their words). One to three sentences.
2. **Their best current thinking** (what they would do if they had to decide today, with reasoning).
3. **What they have already tried** (what tools, conversations, methods they've used on this problem).
4. **Inclusion-criteria answers** (the four yes/no above).
5. **Self-rated confidence in their current best thinking**, 1-10.

This pre-session record is the baseline. Everything the protocol produces will be compared against it.

---

## During the session

The session is run with the Minimal Core reference implementation (`stp_minimal.py`). The session log is preserved (the JSONL file). No additional in-session metrics are collected from the participant; the protocol should not be evaluated by interrupting it.

Sessions run until either: all five phases complete, two re-entries are exhausted, or the participant ends early. There is no time limit. Pilot expectation: 30-90 minutes per session.

---

## Immediately post-session

Within five minutes of session end, before the participant has time to rationalize, ask the following six questions. Record verbatim answers.

1. **The reframing question.** "How would you state your problem now, in your own words? Don't look at the session transcript. Just say what you think the problem is." Compare against pre-session problem statement.

2. **The novelty question.** "Was there any point in the session where you saw something you genuinely had not seen before? If yes, what?" Answer is either: yes with specific content, yes but vague, or no.

3. **The risk question.** "What risks did the session surface that you weren't already worried about?" Count specific risks named.

4. **The action question.** "What do you plan to do next, specifically?" Note whether the action is more specific than the pre-session "best current thinking."

5. **The confidence question.** Self-rated confidence in current best thinking, 1-10. Compare against pre-session.

6. **The counterfactual question.** "Do you think you could have reached this point in 60 minutes of unstructured ChatGPT or Claude conversation?" Answer is yes / unsure / no.

---

## 30-day follow-up

Email or message each participant 30 days after the session. Single question:

> "Did you take any action based on the session output? If yes, what happened?"

Three possible answers: yes-acted-and-it-helped, yes-acted-but-it-didn't-help-or-too-soon-to-tell, no-didn't-act.

---

## Pre-committed analysis

Before running any sessions, commit to the following thresholds for evaluating the pilot.

### Per-session classification

A session is classified as one of three outcomes, decided by these rules:

**POSITIVE outcome** — session is classified positive if ALL of the following hold:
- Post-session problem statement differs meaningfully from pre-session problem statement (judged by an independent reader as "yes, this is a different problem" or "this is the same problem at a deeper level"). Operationalized: independent reader who is not the experimenter rates the change 3+ on a 1-5 scale of "how different is the post-session framing."
- Participant answers "yes with specific content" to the novelty question.
- Participant names at least one risk in the risk question that was not in their pre-session record.
- The counterfactual question is answered "no" or "unsure" (i.e., they do not think they could have reached this with unstructured chat).

**NULL outcome** — session is classified null if two or three of the four conditions above hold. The protocol produced something but not clearly more than unstructured AI conversation would have.

**NEGATIVE outcome** — session is classified negative if fewer than two of the four conditions hold, OR if the participant explicitly states the session was unhelpful, OR if the session ended early due to participant frustration.

### Pilot-level interpretation

Across the ten sessions, the following pre-committed thresholds determine the pilot's conclusion.

**Strong positive signal — proceed to larger study.** At least 6 of 10 sessions classified POSITIVE, AND at least 4 of those 6 act on the output within 30 days, AND at least 2 different problem domains are represented in the positives.

**Weak positive signal — refine and re-pilot.** 4-5 of 10 classified POSITIVE. The protocol is doing something but the failure modes need investigation before scaling. Identify what distinguished positive from null sessions; revise the spec or implementation; run a second pilot.

**Null result — the protocol does not yet produce reliable value.** Fewer than 4 sessions classified POSITIVE. Before continuing, the standard should be revised to address what failed. Public publication of null result is required by the standard's governance commitments.

**Negative result — the protocol may produce worse outcomes than the alternative.** 3 or more sessions classified NEGATIVE. The architectural thesis is in trouble. The standard should be revised significantly or abandoned. Publish negative result.

These thresholds are not predictions. They are commitments. Whatever the results, the conclusion follows from the rules above, not from interpretation.

---

## What the pilot does not test

The pilot cannot test:

- Whether the protocol beats expert human facilitation. (Would require recruiting facilitators.)
- Whether the protocol beats multi-agent debate. (Would require building the debate baseline.)
- Whether the protocol generalizes across domains. (10 sessions is too few; aim for breadth but acknowledge limitation.)
- Whether Adaptive Protocol Tuning would help. (Requires aggregate data from many sessions.)
- Inter-rater reliability of PIC-3 detection. (Requires multiple trained evaluators.)

The pilot tests only one thing: whether the protocol produces something a real user, on a real problem, considers more valuable than what they'd get from unstructured AI conversation. That is the minimum bar. If this bar fails, the larger study is premature.

---

## Researcher discipline

Run the pilot honestly. The following practices reduce experimenter bias:

1. **Do not coach participants** during the session. The protocol should work without you helping the participant interpret it. If they ask what they should do, tell them "respond however feels natural."
2. **Do not select the problem for them.** Take whatever they bring, as long as it meets inclusion criteria.
3. **Do not exclude post-hoc.** If a session goes badly, it counts. The only reason to exclude is if the inclusion criteria turn out to have been miscoded.
4. **Run the analysis with someone else.** Have an independent reader classify outcomes without knowing your hypothesis. Pre-commit to using their classification, not yours.
5. **Publish before the next version.** Whatever happens, write up the results before producing v6 of the standard. The temptation to revise the standard "to reflect what we learned" before the world sees the results is the path to indefensible work.

---

## Timeline

This pilot can be run in 6-8 weeks:

- Week 1-2: Recruit participants, schedule sessions.
- Week 3-5: Run the 10 sessions.
- Week 6: Post-session interviews complete; problem-statement comparisons done; sessions classified by independent reader.
- Week 10: 30-day follow-ups complete.
- Week 11: Pilot writeup published.

If results are positive, larger study can be designed in week 12.

---

## Cost

- API costs: 10 sessions × ~$2 per session = ~$20.
- Participant compensation: optional but recommended. $50/session × 10 = $500.
- Researcher time: ~40-60 hours total across recruitment, sessions, interviews, writeup.

The cost of running this pilot is much smaller than the cost of building infrastructure, writing v6 of the standard, or seeking funding based on unverified claims.

---

## What the pilot writeup should contain

Regardless of result, the writeup contains:

1. The protocol used (this document).
2. Participant demographics and problem domains (anonymized).
3. Per-session outcome classification with reasoning.
4. Two or three full session transcripts (with consent), redacted for sensitive content.
5. The 30-day follow-up results.
6. Honest discussion of what failed, what surprised, and what the pilot cannot conclude.
7. The conclusion that follows from the pre-committed thresholds.
8. The next step that follows from the conclusion.

Publish on the Syntelligence project page alongside the standard. Link from the v5 spec.

---

*The pilot is not designed to prove the standard works. It is designed to give the standard a chance to fail honestly before more is built on it. That is what makes any subsequent positive result credible.*
