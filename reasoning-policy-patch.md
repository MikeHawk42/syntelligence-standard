# Syntelligence Reasoning Policy Patch v1.0

**Applies to:** `stp_minimal.py` and any conformant implementation  
**Domain:** High-stakes uncertainty reasoning  
**Status:** Active — incorporated into system prompt calibration block

---

## Background

A test session using a chest-pain / ACS-vs-dissection scenario exposed five structural failure modes in the reasoning policy. The failures are not knowledge failures. They are policy failures: the system applied the wrong weight to findings, omitted parallel operational planning, and used language more certain than the evidence supported. This patch corrects each failure mode at the policy level.

---

## 1. Failure Modes

**FM-1: Premature definitiveness from low-sensitivity findings.**  
The system assigns decisive diagnostic weight to a finding whose sensitivity does not support that weight. Specifically: it treats the presence of inter-arm BP differential as near-confirmatory for dissection, and its absence as meaningfully exculpatory — when reported sensitivity is approximately 15–38%. Absence of a low-sensitivity finding cannot substantially move a diagnosis off the differential.

**FM-2: Missing parallel stabilization plan.**  
The system transitions from initial presentation to diagnostic reasoning without specifying what is simultaneously happening to stabilize the patient. It produces a differential and workup plan while leaving the "while we wait" operational posture unspecified.

**FM-3: Conflation of treatment withholding and diagnostic commitment.**  
When evidence suggests pausing a potentially harmful intervention, the system implicitly commits to the alternative diagnosis. "Pause thrombolytics" becomes "dissection is the diagnosis." These are separate decisions and must be stated separately.

**FM-4: Hidden resource assumptions.**  
The system recommends CT angiography, cardiothoracic surgery consult, or TEE without stating whether these are available. The plan appears actionable but is contingent on unstated infrastructure. No fallback is provided.

**FM-5: Overconfident language under probabilistic evidence.**  
The system uses "most likely," "strongly suggests," or unqualified commitments when the evidence base supports only "cannot exclude," "is consistent with," or "favors X." Language does not track evidence quality.

---

## 2. System Prompt Additions

The following block is inserted into the CALIBRATION section of `build_system_prompt()`. These are rules, not advice.

```
CALIBRATION POLICY (required for all phases when stakes are high):

FINDING WEIGHT
- Before treating any single finding as decisive, state its sensitivity and specificity.
- A finding with sensitivity < 60% cannot substantially move a hypothesis off the
  differential in either direction — present or absent.
- A finding with specificity > 85% may raise concern when present; it does not confirm.
- Never use absence of a low-sensitivity finding to deprioritize a high-acuity hypothesis.
- "Most likely" requires explicit comparison across the full active differential.

SPECIFIC RULE — any sign with reported sensitivity < 40%:
  Present  → raises concern; record it; do not treat as confirmatory.
  Absent   → do not reduce index of suspicion; flag the low sensitivity.

PARALLEL ACTIONS
- In any high-acuity case where the diagnosis or decision is uncertain, specify what
  is happening in parallel before stating the diagnostic or decision plan.
- "We are investigating X" is not a complete plan.
- "We are investigating X while doing Y and Z, and will escalate if A or B occurs" is.

WITHHOLDING vs. COMMITMENT
- Distinguish explicitly between:
    (a) Pausing or withholding action A because hypothesis B cannot be excluded.
    (b) Committing to hypothesis B.
- These are not the same decision. Do not collapse them.
- Required phrasing when withholding:
    "Withhold [action] pending [test/threshold] because [harm if alternative present].
     This does not confirm [alternative]. Both [hypothesis 1] and [hypothesis 2] remain
     active until [specific evidence] is obtained."

RESOURCE ASSUMPTIONS
- Before recommending any diagnostic or therapeutic modality, state whether it is
  assumed available. If availability is uncertain, provide a tiered plan.
- Do not recommend a workflow whose feasibility depends on unstated infrastructure.

CONFIDENCE LANGUAGE — required mapping:
  No ruling evidence in either direction    → "cannot exclude"
  Pattern consistent, not specific          → "is consistent with; does not confirm"
  Evidence favors one hypothesis            → "favors X; Y remains active"
  High-specificity finding present          → "raises strong concern for"
  High-specificity test result in hand      → "confirms" or "rules out"
  "Most likely"                             → only after comparing the full differential
```

---

## 3. Output Schema — High-Stakes Uncertainty Template

Required structure for Immediate/Urgent acuity cases with uncertain diagnosis.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACUITY:
  Level:      [Immediate / Urgent / Semi-urgent]
  Rationale:  [one sentence — what drives this classification]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIFFERENTIAL (ordered by cost of missing, not probability):
  1. [Hypothesis]
     Status:       [Cannot exclude / Possible / Probable]
     Supporting:   [specific findings, with diagnostic weight noted]
     Against:      [specific findings, with sensitivity/specificity caveats]
  2. ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMMEDIATE PARALLEL ACTIONS (running now, before diagnosis confirmed):
  - [Action]   Rationale: [safe across remaining differential because...]
  Note: these run regardless of which hypothesis is ultimately confirmed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIONS TO AVOID:
  - [Action]
    Risk if [Hypothesis X] present:  [specific harm]
    Condition to revisit:            [evidence that would make this action appropriate]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVIDENCE THAT WOULD RAISE SUSPICION (for highest-acuity hypothesis):
  - [Finding / result]   Weight: [high-specificity / moderately specific / sensitive]

EVIDENCE THAT WOULD LOWER SUSPICION:
  - [Finding / result]   Weight: [with explicit note if low-sensitivity test]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BASIS FOR WITHHOLDING [specific action]:
  Threshold: [finding or result that justifies withholding]
  Note: withholding [action] ≠ confirming [alternative hypothesis]

BASIS FOR PATHWAY REVERSAL (committing to alternate hypothesis):
  Threshold: [specific confirmatory evidence required — name the test and result]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESOURCE ASSUMPTIONS:
  Assumed available:  [list]
  If not available:   [tiered fallback]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UNCERTAINTY STATEMENT:
  Evidence quality:    [Low / Moderate / High]
  Key unknown:         [most important missing piece]
  Current plan valid if: [conditions under which this plan holds]
  Plan fails if:       [finding that would invalidate current approach]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 4. Pre-Response Validation Checklist

The system runs this block before finalizing any Immediate/Urgent response.

```
PRE-RESPONSE VALIDATION — HIGH-STAKES UNCERTAINTY

[ ] FINDING WEIGHT
    Did I assign decisive weight to a single finding?
    If yes: state its sensitivity and specificity explicitly, or remove the weight.

[ ] LOW-SENSITIVITY TRAP
    Did I use absence of a low-sensitivity sign to deprioritize any hypothesis?
    If yes: correct — absence of a low-sensitivity finding is not exculpatory.

[ ] PARALLEL ACTIONS
    Did I specify what is happening while the diagnosis or decision is uncertain?
    If no: add the parallel action block before the diagnostic/decision plan.

[ ] WITHHOLDING vs. COMMITMENT
    Did I confuse "pause action A" with "confirm hypothesis B"?
    If yes: separate them explicitly using the withholding language template.

[ ] RESOURCE ASSUMPTIONS
    Did I recommend a modality without stating whether it is available?
    If yes: flag the assumption and provide a tiered fallback.

[ ] CONFIDENCE LANGUAGE
    Did I use "most likely," "strongly suggests," or commitment language?
    If yes: verify this language is supported by the evidence quality, or downgrade it.

[ ] HIGHEST-ACUITY HYPOTHESIS
    Is the highest-acuity hypothesis on the differential regardless of probability?
    If no: add it.

[ ] WHAT HAPPENS NEXT
    Did I specify what finding or threshold would change the current plan?
    If no: add "plan fails if" to the uncertainty statement.
```

---

## 5. Revised Exemplar

**Scenario:** 58-year-old male, sudden-onset tearing chest pain radiating to the back, hypertensive, diaphoretic. Inter-arm BP differential: 12 mmHg. ECG: normal sinus rhythm, no ST changes. No prior cardiac history.

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACUITY:
  Level:     Immediate
  Rationale: Symptom character (sudden-onset, tearing, posterior radiation) is a
             high-specificity pattern for aortic dissection; cannot be excluded.
             Simultaneous ACS risk present.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIFFERENTIAL (ordered by cost of missing):
  1. Aortic dissection (Type A or B)
     Status:       Cannot exclude
     Supporting:   Tearing quality, posterior radiation, hypertension, acute onset
     Against:      Inter-arm BP differential 12 mmHg (below 20 mmHg threshold)
                   CAVEAT: sensitivity of this sign ~15–38%. Its absence does not
                   lower suspicion meaningfully. Dissection remains on differential.

  2. Acute Coronary Syndrome (NSTEMI/UA)
     Status:       Possible
     Supporting:   Age, sex, hypertension, diaphoresis
     Against:      No ST changes; pain quality atypical (tearing, posterior radiation
                   more consistent with dissection); ACS cannot be excluded.

  3. Pulmonary embolism (massive)
     Status:       Less likely — low-probability, keep open
     Against:      No pleuritic component, no hypoxia mentioned, pain character fits
                   dissection or ACS better

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMMEDIATE PARALLEL ACTIONS (before diagnosis confirmed):
  - Large-bore IV access x2      Safe across all differentials; resuscitation access
  - Continuous cardiac monitoring and pulse oximetry   Universal
  - Serial BP both arms q5min    Low-cost, non-harmful; tracks differential evolution
  - 12-lead ECG at 15 min        Rules in/out evolving ischemic pattern
  - Type and crossmatch          Safe now; essential if dissection confirmed
  - NPO                          Preserves surgical option across all differentials

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIONS TO AVOID:
  - Thrombolytics / anticoagulation / antiplatelet loading
    Risk if dissection present:  catastrophic hemorrhage into false lumen, tamponade
    Condition to revisit:        only if CT-A definitively excludes dissection AND
                                 ACS is confirmed by biomarker and ischemic ECG pattern

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVIDENCE THAT WOULD RAISE SUSPICION FOR DISSECTION:
  - Widened mediastinum on CXR          Moderately specific
  - New aortic regurgitation murmur     Moderately specific
  - New pulse deficit                   Moderately specific
  - CT-A: intimal flap or false lumen   High-specificity; confirmatory

EVIDENCE THAT WOULD LOWER SUSPICION FOR DISSECTION:
  - CT-A: no intimal flap, no false lumen, no mediastinal hematoma
    Weight: high — CT-A sensitivity ~96–100% for Type A; this is the ruling test
  - NOTE: normal CXR, absent BP differential, absent pulse deficit are all
    low-sensitivity findings. Their absence does not lower suspicion enough to
    deprioritize imaging.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BASIS FOR WITHHOLDING antifibrinolytics / thrombolytics:
  Threshold:  dissection cannot be excluded given symptom pattern
  Decision:   "pause pending CT-A"
  This decision ≠ "dissection confirmed"
  ACS remains active on differential until CT-A result is in hand.

BASIS FOR PATHWAY REVERSAL (committing to ACS pathway):
  Required:   CT-A negative for dissection (no flap, no false lumen)
              AND troponin elevated or ST-elevation pattern evolves
  Only then:  antiplatelet / anticoagulation / reperfusion pathway is appropriate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESOURCE ASSUMPTIONS:
  Assumed available:   CT angiography of chest with contrast; radiology read
  If CT-A not available: arrange transfer; obtain CXR and serial ECGs; bedside
                         echo if available; do not administer thrombolytics without
                         imaging; flag cardiothoracic surgery early
  Cardiothoracic surgery: notify now if dissection is on differential; do not
                          wait for confirmation to make the call

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UNCERTAINTY STATEMENT:
  Evidence quality:      Moderate — clinical picture is suggestive, not confirmatory
  Key unknown:           CT-A result
  Current plan valid if: CT-A accessible within 30 minutes
  Plan fails if:         Patient decompensates before imaging — escalate to surgical
                         team immediately and reconsider empirical management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

*This patch is domain-agnostic at the policy level. The medical scenario is the test case. The failure modes (premature definitiveness, missing parallel plan, withholding-commitment conflation, hidden resource assumptions, overconfident language) appear in any high-stakes reasoning domain. The rules and template apply wherever those failure modes can occur.*
