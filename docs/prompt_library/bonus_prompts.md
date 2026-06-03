# Bonus and Advanced Prompts

These templates go beyond the mission brief. Use them if you finish early, want to deepen your understanding, or want to practise techniques that will be essential in your own research beyond this lab.

Each template here represents a more advanced agentic pattern — chaining, self-critique, cross-session continuity, and prompt engineering as a skill in itself.

---

## 1. Multi-Step Pipeline Orchestration Prompt

**When to use:** When you want to run a complete end-to-end pipeline (data inspection → training → evaluation → visualisation) as a single orchestrated sequence, with checkpointing at each stage.

**Why it works:** Orchestration prompts assign Claude the role of an executor who follows a defined sequence, verifies each step before proceeding, and stops with a clear error message if anything fails. This prevents a long cascade of steps where a silent failure in step 2 corrupts all subsequent results.

**Failure it prevents:** Running a 6-step pipeline and discovering at step 6 that step 2 produced empty output — having to debug backwards through all intermediate files. And finding this out after 4 hours of compute time.

**Customisation:** Adjust the step list to match your actual pipeline. Add `--dry-run` flags if your scripts support them, to verify the plan without executing it.

```
Act as a pipeline orchestrator. Execute the following steps in order.
Before each step, confirm the required inputs exist. If any step fails, stop immediately
and report: which step failed, the exact error message, and what to check.

Do not proceed to the next step until the current step has completed successfully.

Pipeline definition:
[PROJECT_ROOT]: [YOUR_PROJECT_ROOT]

Step 1: Data audit
  Command: python scripts/audit_data.py --data_dir data/ --output results/audit/
  Success criterion: results/audit/data_summary.csv exists and has > 0 rows
  If it fails: check that data/ directory contains NIfTI files

Step 2: Data loading test
  Command: python scripts/test_dataloader.py --data_dir data/ --batch_size 4
  Success criterion: script exits with code 0 and prints "All checks passed"

Step 3: Training (smoke test — 2 epochs only)
  Command: python scripts/train.py --data_dir data/ --output_dir results/smoke/ --epochs 2 --batch_size 4
  Success criterion: results/smoke/training_log.csv has exactly 2 rows (one per epoch)

Step 4: Full training
  [ONLY RUN IF I SAY "run full training" — wait for my confirmation after smoke test]
  Command: python scripts/train.py --data_dir data/ --output_dir results/training/ --epochs [N] --batch_size [B]
  Success criterion: results/training/best_model.pt exists

Step 5: Evaluation
  Command: python scripts/evaluate.py --checkpoint results/training/best_model.pt --data_dir data/ --output_dir results/eval/ --split test
  Success criterion: results/eval/metrics_per_case.csv has [N_TEST] rows

Step 6: Visualisation
  Command: python scripts/visualise.py --metrics results/eval/metrics_per_case.csv --output_dir results/figures/
  Success criterion: at least 3 PNG files exist in results/figures/

After all steps complete, print a pipeline summary:
| Step | Status | Output | Time |

Do not run Step 4 without my explicit approval. Pause after Step 3 and report.
```

---

## 2. Self-Critique Chain Prompt

**When to use:** When you want Claude to produce an output and immediately evaluate its own work — without you having to prompt the critique separately.

**Why it works:** Chaining production and critique in a single prompt forces Claude to hold two cognitive modes simultaneously: generator and evaluator. The critique is often more useful than the output itself because it surfaces the assumptions and weaknesses that were invisible during generation.

**Failure it prevents:** Accepting the first output Claude produces without any evaluation, which is the default behaviour if you do not explicitly ask for critique. First outputs are often overconfident and underspecified.

**Customisation:** Replace `[TASK_DESCRIPTION]` with any generative task. The critique criteria in section 2 should match the domain — adjust for code, scientific text, a study design, or a regulatory analysis.

```
I want you to generate an output and then immediately critique it.

Task: [TASK_DESCRIPTION]
(e.g. "Write a methods section describing our U-Net training procedure" or
"Implement a function that computes Dice score for BraTS regions")

Step 1 — Generate
Produce the output for the task above. Do your best. Do not add caveats or hedges yet.

Step 2 — Critique (switch roles: you are now a critic reviewing the work in Step 1)
Evaluate your own output on these dimensions:
a. Correctness: Is everything factually or technically accurate?
   List any claim or line of code you are less than 90% confident is correct.
b. Completeness: What is missing that a reader or user would need?
c. Assumptions: What assumptions did you make that I have not verified?
   List them explicitly.
d. Failure modes: Under what conditions would this output be wrong or fail?
e. What would make this output better? Name the single most important improvement.

Step 3 — Revised output (optional — I will ask for this separately)
Do not produce a revised output yet. Only produce Steps 1 and 2.
Then ask me: "Should I revise based on the critique?"

Format:
=== GENERATED OUTPUT ===
[output]

=== SELF-CRITIQUE ===
[critique structured by the 5 dimensions above]
```

---

## 3. Research Report Generation Prompt

**When to use:** At the end of the lab, to produce a structured 2-page research summary that documents what you did, what you found, and what you would do next.

**Why it works:** A research report is not a lab notebook transcript. It requires selecting and organising evidence to support a coherent narrative. This prompt assigns Claude the role of a research writer who structures the report according to standard scientific conventions, draws on your actual results, and flags where evidence is insufficient.

**Failure it prevents:** A report that describes every step you took in chronological order (a lab notebook) instead of the scientific argument your results support (a report). Also prevents a report that makes claims unsupported by the evidence collected during the lab.

**Customisation:** Fill in all the `[BRACKETS]` with your actual results. The more specific the evidence you provide, the more useful the report. Do not leave brackets unfilled — provide your actual values.

```
Act as a research writer. Generate a 2-page structured research summary based on the following evidence.

Evidence to use (fill in your actual values):
- Research question: [YOUR RESEARCH QUESTION]
- Dataset: BraTS [YEAR], [N_TRAIN] training, [N_VAL] validation, [N_TEST] test cases
- Model: 2D U-Net, [DESCRIBE ARCHITECTURE BRIEFLY]
- Best baseline result: Dice WT=[X], TC=[Y], ET=[Z] ± [SD]
- Best improved result (if applicable): Dice WT=[X], TC=[Y], ET=[Z] ± [SD]
- Key failure patterns: [FROM YOUR ERROR ANALYSIS — 2-3 specific findings]
- Root cause identified: [YOUR RCA CONCLUSION]
- Intervention tried: [WHAT YOU CHANGED IN MISSION 4]
- Outcome of intervention: [BETTER / WORSE / MIXED — with evidence]
- Proposed next study: [YOUR MISSION 5 DESIGN]

Generate a report with this structure:

# [PROJECT TITLE]
Authors: [YOUR NAMES]  |  Date: [DATE]  |  Course: PhD Medical AI Lab

## Abstract (100 words)
One-sentence background, one-sentence method, one-sentence result, one-sentence conclusion.

## Introduction (150 words)
Clinical context, research question, why it matters.

## Methods (250 words)
Dataset, preprocessing, model architecture, training, evaluation metrics.
Write in past tense, passive voice, reproducible level of detail.

## Results (200 words + one summary table)
Primary performance metrics. Comparison of baseline vs improved model if applicable.
Summary table: | Metric | Baseline | Improved | Delta | p-value |

## Error Analysis (150 words)
What the model fails on. Key failure patterns. Root cause finding.

## Discussion (200 words)
What the results mean. What they do not mean. Primary limitation. Next step.

## Conclusion (75 words)
What was demonstrated, what remains to be done.

Rules:
- Every performance claim must cite a specific number from the evidence provided
- Do not claim anything not in the evidence list above
- If evidence is insufficient to support a section, write [EVIDENCE NEEDED: describe what is missing]
  rather than fabricating content
```

---

## 4. "Teach Me" Prompt

**When to use:** Any time Claude produces an output you accepted but do not fully understand — a piece of code, a statistical result, an error message, a regulatory term.

**Why it works:** Asking Claude to teach rather than explain produces a different kind of response. Teaching requires assessing what the learner already knows, building from that point, and checking understanding. This prompt makes your understanding — not Claude's knowledge — the goal.

**Failure it prevents:** Using a model you do not understand in a clinical context. If you cannot explain how the loss function works, you cannot explain to a clinician why the model might fail on their cases. This is not just a pedagogical concern — it is a patient safety concern.

**Customisation:** Replace `[CONCEPT]` and `[CONTEXT]` with anything you encountered during the lab. The "check my understanding" step at the end is the most important part — do not skip it.

```
I accepted an output from you that I want to understand better, not just use.
Please teach me the following concept as if you are a tutor, not a textbook.

Concept: [CONCEPT — e.g. "why Dice loss is better than cross-entropy for class-imbalanced segmentation"]
Context where I encountered it: [e.g. "you recommended using DiceCELoss in the training loop"]
My current understanding (be honest): [e.g. "I know cross-entropy is a standard loss but I don't understand why it's bad for segmentation"]

Please teach me using this sequence:

1. Diagnose my understanding gap
   Based on what I said above, what do I need to understand first before I can understand [CONCEPT]?
   What prerequisite is missing?

2. Build the prerequisite (1-2 paragraphs)
   Explain the prerequisite in plain language, with one concrete analogy.

3. Explain the concept (2-3 paragraphs)
   Now explain [CONCEPT] building on the prerequisite.
   Use one concrete numerical example — not a formula, an actual calculation with numbers.
   Relate it back to brain tumour segmentation specifically.

4. Common misconception
   What do people usually get wrong about this? (Including me, based on what I said above.)

5. Check my understanding
   Ask me three questions that would reveal whether I have understood the concept.
   Do not answer them — I will answer, and then you can correct my understanding.

Do not use bullet points for the teaching sections. Use prose, as a tutor would speak.
```

---

## 5. Cross-Session Continuity Prompt

**When to use:** At the END of a session (before closing Claude Code), to prepare for the next session. Also use it to update your CLAUDE.md.

**Why it works:** Claude will not remember this session. If you do not create a structured handover document, you will spend 15-20 minutes at the start of the next session reconstructing context. This prompt produces that document in under 2 minutes.

**Failure it prevents:** Starting the next session with "where were we?" and asking Claude to read through everything from scratch — which is slow and error-prone because Claude may misinterpret the files it reads without the context you carry in your head.

```
We are about to end this session. Generate a structured handover document so the next session
can continue efficiently.

Please produce the following:

1. Session summary (5 bullet points maximum)
   What was accomplished this session? Be specific — cite file names, metric values, decisions made.

2. Current state
   - Last completed action: [what is the most recent thing that finished and produced output?]
   - Output files created: [list with paths]
   - Model/checkpoint state: [which checkpoint is the best right now, and where is it?]
   - Known working commands: [commands that ran successfully this session]

3. Open issues
   - What was started but not finished?
   - What failed and was not resolved?
   - What decision was deferred?

4. Next session starting point
   - The first prompt to paste at the start of the next session: [write it out in full]
   - The first command to run: [specific shell command]
   - The first question to answer: [what needs to be decided before work continues?]

5. CLAUDE.md update (if needed)
   - Does anything in CLAUDE.md need updating based on this session?
   - If yes, write the specific lines to add or change.

Save this document to [PROJECT_ROOT]/session_handover_[DATE].md
Then read it back and confirm it is complete enough that someone who was not in this session
could pick up the work in under 5 minutes.
```

---

## 6. Prompt Iteration Prompt

**When to use:** When a prompt you wrote produced a disappointing output and you want to improve the prompt rather than just retry.

**Why it works:** Most prompt failures come from structural issues — wrong role assignment, missing constraints, underspecified output format — not from the model's capability. This meta-prompt treats prompt engineering as a skill with learnable principles, not trial and error.

**Failure it prevents:** Spending time rephrasing the same prompt randomly, hoping for a better result. The iteration prompt diagnoses why the prompt failed and produces a structurally improved version.

```
I wrote a prompt that produced a disappointing output. Help me improve the prompt itself,
not just retry it.

My original prompt:
"""
[PASTE YOUR ORIGINAL PROMPT HERE]
"""

The output I received (paste or describe):
"""
[DESCRIBE WHAT CLAUDE PRODUCED]
"""

What I actually wanted (be specific):
"""
[DESCRIBE THE OUTPUT YOU NEEDED — NOT THE PROMPT, THE DESIRED OUTPUT]
"""

Please diagnose the prompt and produce an improved version:

1. Diagnosis (one sentence per issue)
   - Role: Was a role assigned? Was it the right role for this task?
   - Context: Was enough background provided? What was missing?
   - Objective: Was the goal stated unambiguously?
   - Constraints: Were there constraints on format, length, scope, or approach?
   - Output specification: Was the expected output format described precisely?
   - Verification: Was there a way to check whether the output was correct?

2. Root cause
   Which ONE issue above is most responsible for the poor output?

3. Improved prompt
   Write the improved prompt in full.
   Highlight (with inline comments or bold) the specific changes you made and why each change addresses the root cause.

4. Predicted improvement
   What specifically will be different about the output if I use the improved prompt?
   What could still go wrong?

After improving the prompt, I will run it and report back.
```

---

## Quick Reference

| Template | Advanced Pattern | When It Pays Off |
|---|---|---|
| Pipeline Orchestration | Sequential verification with stop conditions | Long multi-step pipelines |
| Self-Critique Chain | Generate-then-critique in one prompt | High-stakes outputs (code, reports) |
| Research Report | Evidence-grounded structured writing | End-of-lab showcase, future publications |
| "Teach Me" | Tutor mode with understanding check | After accepting any output you don't fully understand |
| Cross-Session Continuity | Handover documentation | End of every session |
| Prompt Iteration | Meta-level prompt debugging | When a prompt consistently underperforms |
