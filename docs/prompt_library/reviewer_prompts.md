# Reviewer and Critic Prompts

Use these templates any time you want Claude to evaluate rather than produce. The Reviewer role is different from the Planner or Implementer — it must be critical, not constructive. A good reviewer finds problems. A good reviewer is not trying to be helpful in the usual sense.

These prompts are most valuable after you have produced something you are reasonably satisfied with — that is precisely when the tendency to miss problems is highest.

---

## 1. Code Review Prompt

**When to use:** After writing or receiving any script that will be used in the analysis — training loop, data loader, evaluation script, preprocessing code.

**Why it works:** This prompt assigns Claude the role of a peer code reviewer with specific expertise in three domains: software correctness, scientific reproducibility, and medical imaging conventions. Each domain surfaces different classes of bugs. Separating them prevents the reviewer from getting distracted by style issues and missing a Dice-label mapping error.

**Failure it prevents:** A training loop that appears to work but computes Dice on logits instead of probabilities, a preprocessing script that normalises with the wrong percentiles, or an evaluation that leaks test cases into the training split.

**Customisation:** Adjust the focus areas based on what you are reviewing. Add a fourth domain if relevant (e.g. "memory efficiency" for large-volume 3D training).

```
Act as a peer code reviewer with expertise in:
A. Software correctness (bugs, edge cases, error handling)
B. Scientific reproducibility (random seeds, logging, data splits)
C. Medical imaging conventions (NIfTI handling, label conventions, metric computation)

Review the code at [FILE_PATH].

For each domain, produce a structured list of findings:
- Severity: Critical / Major / Minor / Style
- Location: line number or function name
- Issue: what is wrong
- Evidence: why this is a problem (cite the specific line or pattern)
- Fix: what the correct version should be

Severity definitions:
- Critical: will produce wrong results silently (e.g. wrong label mapping)
- Major: will crash or prevent training from completing
- Minor: will not crash but may produce suboptimal results (e.g. missing augmentation seed)
- Style: does not affect results but reduces readability or maintainability

Domain A — Correctness:
Check for: off-by-one errors, incorrect tensor dimensions, wrong loss function for task,
wrong aggregation (batch mean vs case mean), NaN propagation, dtype mismatches,
in-place operations that corrupt gradients, incorrect mask application.

Domain B — Reproducibility:
Check for: use of random seed (all three: Python, NumPy, PyTorch), logging of hyperparameters,
saving of config before training starts, deterministic DataLoader (worker_init_fn),
train/val/test split defined before any processing, no data leakage across splits.

Domain C — Medical Imaging:
Check for: correct voxel spacing use in metric computation, correct BraTS label convention
(labels 0/1/2/4, not 0/1/2/3), Dice computed on 3D volume not 2D slices,
HD95 in mm (not voxels), correct handling of cases with absent tumour regions.

After the domain-specific lists, produce:
- A prioritised fix list (Critical first, then Major)
- A one-paragraph overall assessment: is this code ready to produce results for a paper?

Do not fix any issues yet. Only report.
```

---

## 2. Results Sanity Check Prompt

**When to use:** Immediately after receiving evaluation metrics, before drawing any conclusions.

**Why it works:** Results that look good are more dangerous than results that look bad. A surprisingly high Dice score is often a data leakage bug. A Dice of exactly 0.000 for every ET case is a label remapping error. This prompt asks Claude to interrogate the results for internal consistency, not just accept them.

**Failure it prevents:** Reporting a Dice of 0.95 to the group when it was computed on training cases accidentally included in the test set. Or reporting ET Dice of 0 without noticing that the model predicted the correct label index but the metric used the wrong class mapping.

```
Act as a results auditor. Sanity-check the following evaluation results before I draw any conclusions.

Results file: [METRICS_CSV_PATH]
Training configuration: [CONFIG_JSON_PATH or brief summary]
Dataset: BraTS [YEAR], [N] test cases

Run the following checks and report PASS / WARN / FAIL for each:

1. Score range check
   - All Dice values are between 0.0 and 1.0 (inclusive)
   - All HD95 values are > 0 mm and < 200 mm (values > 150 mm are physically implausible for brain)
   - No metric value is exactly 0.000 for all cases (suggests a systematic bug)
   - No metric value is exactly 1.000 for all cases (suggests data leakage or a trivial test)

2. Region hierarchy check
   For each case: WT Dice should generally be >= TC Dice >= ET Dice
   (WT is the largest region, easiest to segment by volume)
   Flag any case where ET Dice > WT Dice + 0.1 (anatomically suspicious)

3. Baseline comparison
   Compare your results to published BraTS benchmarks:
   - BraTS 2020 winning method: WT ~0.89, TC ~0.85, ET ~0.82
   - A reasonable first baseline: WT ~0.80, TC ~0.70, ET ~0.65
   - An unlikely first baseline: WT > 0.92 (would require extensive tuning)
   Flag if your results are implausibly high (possible leakage) or implausibly low (possible bug)

4. Variance check
   - Compute standard deviation of each metric across cases
   - Flag if std < 0.05 (suspiciously uniform — possible batch evaluation error)
   - Flag if std > 0.25 (extremely high variance — possible data loading inconsistency)

5. Case count check
   - Count rows in the metrics CSV
   - Compare to expected number of test cases: [EXPECTED_TEST_CASES]
   - Flag if different

6. Correlation check
   - Compute correlation between dice_wt and tumour volume (from data_statistics.csv if available)
   - A very high correlation (r > 0.8) is expected for small-volume ET but suspicious for WT

Report: any FAIL or WARN result must be investigated before results are used.
Recommend: is it safe to proceed to analysis, or is there a red flag that needs resolving first?
```

---

## 3. Devil's Advocate Prompt

**When to use:** When you have reached a conclusion you believe in and are about to present it. Use this before any presentation, report, or peer discussion.

**Why it works:** Assigning Claude the explicit role of arguing against your conclusion forces it to surface the strongest counter-arguments. This is more useful than asking "what are the limitations?" — which produces a polite list. The devil's advocate must argue to win.

**Failure it prevents:** Presenting a conclusion that has an obvious flaw you missed because you were too close to the work. Peer reviewers and clinical collaborators will find it. Better to find it first.

```
Act as a devil's advocate. Your job is to argue as forcefully as possible against the following conclusion.
You are not trying to be balanced. You are trying to find the strongest possible objection.

My conclusion: [STATE YOUR CONCLUSION IN 1-3 SENTENCES]
Evidence I am using to support it: [LIST 2-4 PIECES OF EVIDENCE]
Context: brain tumour segmentation lab, BraTS dataset, U-Net model, [N] test cases

Your task:
1. Identify the single strongest objection to this conclusion. State it in one clear sentence.
2. Explain why this objection undermines the conclusion — not just weakens it.
3. Identify the weakest piece of evidence in my list. Why is it weak?
4. Propose an alternative explanation for my results that does not require my conclusion to be true.
5. What experiment or additional evidence would you demand before accepting this conclusion?

After your argument:
- Rate the strength of your objection: Decisive / Strong / Moderate / Weak
- If Decisive or Strong: tell me what I need to fix before presenting this conclusion
- If Moderate or Weak: tell me how I should acknowledge this limitation when presenting

Do not soften your argument. Do not end with reassurance. Argue hard.
```

---

## 4. Scientific Writing Review Prompt

**When to use:** When writing the Mission 6 summary or any report section where you make a claim about your model's performance or clinical relevance.

**Why it works:** Scientific claims must be grounded in specific evidence. This prompt asks Claude to trace every claim to its supporting data — and flag claims that are not supported. It also checks for common writing errors in medical AI papers (overclaiming clinical readiness, misusing statistical terminology).

**Failure it prevents:** A report that states "the model performs well" without citing a Dice value, or "the model could assist clinicians" without any evidence of clinical comparative performance, or "our results are statistically significant" without a valid statistical test.

```
Act as a scientific writing reviewer for a medical AI publication.
Review the following text section for claim validity and language precision.

Text to review:
"""
[PASTE YOUR TEXT HERE]
"""

Supporting evidence available:
- Evaluation metrics: [METRICS_SUMMARY]
- Dataset: [DATASET DESCRIPTION]
- Comparator: [WHAT YOU COMPARED AGAINST, OR "none"]
- Statistical tests performed: [LIST OR "none"]

For each claim in the text, evaluate:

1. Claim identification: quote the claim exactly
2. Evidence check: does the evidence listed above support this specific claim?
   SUPPORTED / PARTIALLY SUPPORTED / UNSUPPORTED
3. Language check: is the language appropriately hedged for the evidence level?
   - "The model achieves X" — requires specific evidence, appropriate if supported
   - "The model may improve" — appropriate for hypotheses, problematic if presented as fact
   - "The model is ready for clinical use" — requires regulatory approval and prospective trials
4. Overclaiming check: flag any statement that implies:
   - Clinical readiness without prospective validation
   - Causation when only correlation is shown
   - Generalisation beyond the test population
   - Statistical significance as clinical significance

Red flag phrases (flag automatically if present):
- "state of the art" — requires systematic comparison to all recent methods
- "clinically viable" — requires prospective clinical trial
- "accurately predicts" — requires calibration analysis
- "outperforms radiologists" — requires reader study

Produce a line-by-line annotation. For each flagged item, suggest a corrected version.
At the end: what is the one change that would most improve the scientific integrity of this text?
```

---

## 5. Peer Reviewer Simulation Prompt

**When to use:** Before any formal presentation (end-of-day showcase, written report), to experience the hardest likely questions first.

**Why it works:** Simulating a critical peer reviewer forces you to encounter the hardest version of the questions you will face. If you can answer the simulated reviewer's questions, you are prepared. If you cannot, you know what work remains.

**Failure it prevents:** Walking into a showcase without a coherent answer to "but what happens when you apply this to a different hospital's scanner?" or "why did you choose this architecture over a simpler baseline?"

```
Act as a sceptical peer reviewer at a top medical AI conference (e.g. MICCAI, NeurIPS Medical Imaging track).
You have received the following abstract describing a student lab project.

Abstract:
"""
[PASTE YOUR ABSTRACT OR RESULT SUMMARY HERE]
"""

Write a realistic peer review. Include:

1. Summary (2 sentences): what the authors claim and what they have done
2. Strengths (2-3 bullet points): what is genuinely good about this work
3. Weaknesses (4-6 bullet points, ordered by severity):
   - Major weaknesses first (would prevent acceptance at a real venue)
   - Minor weaknesses second (would require revision)
4. Questions for the authors (3-5 questions the reviewer demands answers to)
5. Overall recommendation: Accept / Major Revision / Reject — with one-sentence justification

Reviewer persona: you are rigorous, fair, and not hostile — but you hold the work to the standard
of a real publication. You will not accept "future work" as a substitute for missing evidence.
You are particularly attentive to:
- Train/test contamination
- Lack of external validation
- Metric selection appropriateness
- Overclaiming clinical relevance

After the review, step out of character and add:
"To prepare for this review: [list 3 specific things the student should address before the showcase]"
```

---

## Quick Reference

| Template | Role | Best Used When |
|---|---|---|
| Code Review | Peer reviewer (3 domains) | After writing any script |
| Results Sanity Check | Results auditor | Before drawing any conclusions |
| Devil's Advocate | Opponent | When confident in a conclusion |
| Scientific Writing Review | Publication reviewer | When writing claims about performance |
| Peer Reviewer Simulation | Conference reviewer | Before showcase or report submission |
