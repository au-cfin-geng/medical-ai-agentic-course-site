# Role Switching for Research

Effective agentic research requires more than one way of thinking about the same problem. A developer builds a solution. A critic finds its flaws. A clinical translator explains what the solution means for a patient. These are not three different people — they are three different cognitive orientations that can be applied to the same research output, in sequence, by the same Claude session.

This page explains the concept of intentional role switching, when to use it in the lab missions, and how to execute it cleanly.

---

## Why Role Switching Matters

The output Claude produces is heavily shaped by the role framing you provide. The same underlying data — your error maps, your metric files, your study plan — produces systematically different outputs under different role prompts.

A **developer** prompt asks "what should I implement?" and produces code and implementation plans.

A **critic** prompt asks "what is wrong with this?" and produces objections, edge cases, and weaknesses.

A **clinical translator** prompt asks "what does this mean for a patient?" and produces plain-language explanations, practical implications, and honest limitations.

If you use only the developer role throughout a session, you get implementation — but you may not catch the scientific weaknesses in your approach, and you will not produce clinical-facing documentation. If you ask Claude to do all three simultaneously, you get a confused mixture. The discipline of role switching keeps each phase of the analysis clean and purposeful.

---

## The Developer to Critic Switch

The most common and most valuable role switch in this course is from developer to critic.

In Mission 3, you begin as a developer: Claude generates error map figures and produces the observation report. At the end of Mission 3, you have a failure hypothesis — a claim about why the worst-performing case fails and what change would improve it.

Before proceeding to Mission 4, switch to the critic role. Ask Claude to attack the hypothesis you just generated:

```
Now act as a skeptical peer reviewer.
Read reports/error_analysis.md and challenge the failure hypothesis.
Identify the three strongest objections:
1. Is the proposed cause mechanistically sound?
2. Is the proposed intervention actually testable with this dataset?
3. What alternative explanations exist that the hypothesis does not address?
Do not defend the hypothesis — only challenge it.
```

This is not an admission that the hypothesis is wrong. It is a diagnostic step. If the hypothesis survives this challenge, it is more credible. If the challenge reveals a significant weakness, you can revise the hypothesis before committing to a full training experiment in Mission 4.

The developer→critic switch adds perhaps fifteen minutes to a session. It can save hours of implementing and running an experiment based on a flawed hypothesis.

---

## Making Role Switches Explicit

A role switch is only effective if it is explicit in the prompt. A common failure mode is attempting to switch roles mid-prompt: "Implement the augmentation change and also critique the approach and summarize it for a clinical audience." This produces a confused output that is partly implementation, partly critique, and partly translation — none of it done well.

The correct approach is to complete the current task before switching:

1. Complete the implementation task to a verified output.
2. Start a new prompt that begins with the role declaration.
3. Give the new role a specific and bounded task.

The role declaration should appear as the first sentence of the prompt: "Act as a skeptical peer reviewer." or "You are now a clinical translator." This signals the reorientation clearly and prevents Claude from continuing in the previous role.

---

## The Mission 5 Three-Phase Sequence

Mission 5 — Design the Next Study — is the most complex role-switching sequence in the course. It uses three distinct roles in sequence within a single session.

**Phase 1 — Developer (study design):**
```
Act as a clinical researcher designing a follow-up study.
Read reports/error_analysis.md and reports/model_swap.md.
Draft a study plan for the next phase of this research.
The plan should include: research question, patient population, primary endpoint,
model architecture, evaluation protocol, and success criteria.
Write the draft to reports/challenge_plan.md.
```

**Phase 2 — Critic (adversarial review):**
```
Now act as a skeptical methods reviewer at a top medical imaging journal.
Read reports/challenge_plan.md.
Identify the 3 weakest assumptions in this study design.
For each weakness, state: (a) the specific assumption, (b) why it threatens
validity, (c) a specific change that would address it.
Do not defend the plan — only challenge it.
Write the critique to reports/study_critique.md.
```

**Phase 3 — Developer again (revision):**
```
Act as the study designer again.
Read reports/challenge_plan.md and reports/study_critique.md.
Revise challenge_plan.md to address the three weaknesses identified in the critique.
For each change, note in the document: "Revised in response to critique: [critique point]"
```

This three-phase sequence is peer review in a single session. You play the role of both author and reviewer, with Claude executing both roles. The result is a study plan that has been stress-tested against its own weaknesses before it is shown to anyone else.

---

## The Mission 6 Technical to Clinical Switch

Mission 6 requires the sharpest role switch in the course: from technical analyst to clinical translator. The same Dice score — a number between 0 and 1 — means different things to an ML researcher and to a clinical radiologist.

To an ML researcher, "Dice 0.67" means the model's segmentation overlaps with ground truth at a coefficient of 0.67, a moderate result that exceeds some baselines and trails others. To a clinical radiologist, "Dice 0.67" is meaningless without translation: does the model catch the tumour? Where does it fail? What should I trust it to do, and what should I not?

The role switch is not just a vocabulary change — it requires a change in what is foregrounded and what is backgrounded. The ML researcher foregrounds the number. The clinical translator foregrounds the implication.

```
Act as a clinical AI communicator writing for a radiologist audience.
Read outputs/metrics/model_swap_comparison.json and reports/model_swap.md.

Write a clinical summary memo (reports/clinical_memo.md) that:
- Does not use the words: epoch, loss function, tensor, batch, architecture, weights
- States in plain language what the model can and cannot do
- Names at least 3 specific failure modes that a radiologist should know about
- Is explicit about the limitations of the teaching-data evaluation
- Does not claim any clinical readiness
- Ends with a clear statement of what human oversight is required

Do not overstate what was demonstrated. The model was evaluated on teaching data only.
```

This prompt changes the vocabulary constraint, the audience model, and the honesty requirement simultaneously. Without all three, the clinical memo will revert to technical language (without the vocabulary constraint), miss the clinical perspective (without the audience model), or overstate the findings (without the honesty requirement).

---

## Multi-Perspective Exercise

One of the most effective learning exercises in the course is to ask the same research question to three different roles and compare the answers. This exposes how much role framing shapes the output.

**Example question:** "Is our brain tumour segmentation model ready to be useful in a clinical setting?"

- **Developer role:** "Based on the evaluation results, the model achieves a Dice score of 0.67 on the teaching dataset. The primary failure mode is boundary segmentation in low-contrast cases. The next development step would be..."
- **Skeptical Reviewer role:** "No. The model has been evaluated on a teaching dataset that does not represent the full range of clinical presentations. The sample size is insufficient for statistical confidence. The failure mode in low-contrast cases is clinically significant..."
- **Clinical Translator role:** "The model shows that AI can identify large, well-contrasted brain tumours in the teaching cases. It tends to miss the boundaries of smaller lesions. Before it would be useful in a clinic, it would need to be tested on a much larger and more diverse set of patients, with a radiologist confirming every output..."

Three different answers to the same question. All of them are useful. None of them is complete without the others. The scientific picture requires all three perspectives.

---

## When NOT to Switch Roles

Role switching mid-implementation causes confusion. If Claude is in the middle of writing a training script, switching to a critic role mid-prompt will interrupt the implementation and produce a half-finished script alongside a critique.

Complete the current task before switching. This is the rule: one role per task, one task per prompt segment, one verification per output. When a task is complete and the output is verified, switch roles for the next task.

!!! note "The transition prompt"
    Use a clear transition phrase to signal a role switch: "Now that the implementation is complete and I have verified the output, I want to switch your role." This explicit transition prevents Claude from treating the role switch as a continuation of the previous task.

!!! warning "Role ambiguity in long sessions"
    In sessions longer than roughly 20-30 exchanges, Claude's adherence to an initial role declaration weakens. If you started the session as a developer, Claude may drift toward mixing developer and critic outputs as the session lengthens. If you notice Claude producing unsolicited critique during an implementation task, re-state the role explicitly: "Continue as the developer role. Do not critique — only implement."

!!! example "The three-question diagnostic"
    When you are unsure which role to use next, ask these three questions: (1) Do I need something built? Use Developer. (2) Do I need to understand what I have? Use Data Inspector or Visual Debugger. (3) Do I need to identify what might be wrong? Use Skeptical Reviewer. (4) Do I need to explain this to a non-technical audience? Use Clinical Translator.
