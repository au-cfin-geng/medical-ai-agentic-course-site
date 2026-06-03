# Mission 6 — Translate Responsibly

The gap between a research prototype and clinical deployment is wide. Your job is to describe that gap honestly.

---

## Why This Matters Clinically

Every clinical AI system begins as a research prototype. The critical moment in the development lifecycle is when researchers communicate their prototype's capabilities to clinicians, regulators, or patients — because that communication determines whether the system will be used appropriately or misused catastrophically.

The clinical deployment gap is real and large. A model trained on a sample of 20 patients from one institution, evaluated on a held-out set from the same institution, with no external validation, no prospective clinical study, and no regulatory clearance, is not ready for clinical use. This is true regardless of the Dice score. The Dice score measures one thing (voxel overlap on a specific dataset) and says nothing about how the model will perform on patients from a different scanner, a different institution, a different age group, or with post-operative anatomy.

Responsible translation means being specific about what was demonstrated, what was not demonstrated, what additional evidence would be required, and what human oversight would be needed in any research use. It is not modesty for its own sake — it is the scientific and ethical obligation of anyone who builds tools that affect patient care.

---

## Traditional Bottleneck

The most common failure mode in the communication of research prototypes is overstating capability. This takes several forms:

- **Implicit overstating:** not mentioning limitations, allowing the reader to assume the result generalizes more than it does.
- **Metric fetishism:** reporting the Dice score without contextualizing it against clinical benchmarks, inter-rater variability, or performance on edge cases.
- **Prototype-to-product confusion:** describing a research prototype as if it were a clinical product because it performs well on a held-out test set.
- **Jargon barriers:** writing for a technical audience in a document intended for clinical collaborators, making it impossible for the clinician to assess the claims independently.

The consequence of overstating is not just reputational risk for the researcher. It is a contribution to the systemic erosion of trust between clinical AI researchers and the clinical community — a problem that makes it harder for every subsequent researcher to have their work taken seriously.

---

## Claude / Agentic Method

Claude plays the role of clinical translator in Mission 6: an agent tasked with writing a clear, honest, limitation-first communication about the prototype for a clinical audience.

The key constraints are:
1. **Audience specification:** the document is written for a clinician who understands medicine but does not know ML. No jargon without explanation.
2. **Honesty constraint:** Claude is instructed to use the phrase "research prototype" (or equivalent) and to list limitations before strengths.
3. **Limitation-first output:** the memo begins with what the system cannot do and what it has not been tested on, before describing what it achieved.

These constraints are enforced by the prompt. Claude's default tendency when describing a system it has built is to describe its strengths first. The honesty constraint reverses this default.

---

## Anthropic Academy / Claude Reading Connection

> **Disclaimer:** The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

Relevant Anthropic Academy modules:

- **Claude 101** — introduces Claude's ability to adapt writing style for different audiences. Mission 6's audience-aware writing is a direct application.
- **AI Fluency: Framework and Foundations** — discusses responsible communication about AI capabilities and limitations. Mission 6 is the practical exam for this material.
- **AI Capabilities and Limitations** — the content of this module is exactly what Mission 6's translation memo must communicate: a clear, honest account of what AI systems can and cannot be trusted to do.

---

## Prompt Pattern Practiced

**Audience + honesty constraint + limitation-first output**

This prompt pattern has three components that must all be present:

1. **Audience:** specify who will read the document and what they know. "Write for a radiologist who understands brain tumour anatomy but has no ML background" gives Claude the information it needs to calibrate language, depth, and framing.

2. **Honesty constraint:** explicitly prohibit overstating. "Do not claim the prototype is ready for clinical use. Do not omit limitations. Use the phrase 'research prototype' at least twice." Constraints of this type override Claude's default tendency to present completed work positively.

3. **Limitation-first output:** specify the document structure so that limitations appear before achievements. A limitation-first structure forces the writer (and the reader) to engage with the gaps before engaging with the results.

Example prompt:
```
Read CLAUDE.md and all reports in reports/.
Act as a clinical translator writing for a radiologist collaborator.
The radiologist understands neuro-oncology but does not know machine learning.

Write reports/translation_memo.md with the following structure:
1. What this system is (one paragraph — use the phrase "research prototype")
2. What it was tested on (specific: sample size, institution, modality, split)
3. What it cannot do and has not been tested on (list at least 3 specific limitations)
4. What it demonstrated (specific Dice score with context: "a radiologist typically
   achieves inter-rater Dice of approximately X")
5. What would be required for research use (human oversight requirements)
6. What additional evidence would be needed before clinical consideration

Honesty constraints:
- Do not claim the system is ready for clinical use
- Do not omit any limitation identified in reports/error_analysis.md
- List limitations before listing achievements
- Use plain language: if you use an ML term, immediately explain it in one sentence
```

---

## What You Will Build

By the end of Mission 6, the project record will contain:

1. **`reports/translation_memo.md`** — a one-to-two page document written for a clinical audience. It must contain: the phrase "research prototype" or equivalent at least twice, at least three specific limitations stated in plain language, a contextualized description of the Dice score, the human oversight requirements, and the additional evidence required before clinical consideration.

---

## What to Do in the Lab Studio

1. Read `reports/error_analysis.md` and `reports/model_swap.md` before starting.
2. Give Claude the clinical translator prompt.
3. When Claude finishes, read the memo as if you were the radiologist. Can you follow every sentence? Does any sentence contain ML jargon that is not immediately explained?
4. Check: does the memo contain "research prototype" or equivalent?
5. Count the specific limitations listed. Are there at least three? Are they specific to this prototype, not generic ("all ML models have limitations")?
6. Read the section on what would be required for clinical consideration. Is it honest about the gap?

---

## Expected Artifact

`reports/translation_memo.md`: a one-to-two page document with clear section headings, written in plain language, following the limitation-first structure. The most important test: if you gave this document to a radiologist who had never seen a machine learning paper, would they have an accurate understanding of what this system can and cannot do?

The memo must contain:
- The phrase "research prototype" (or equivalent) at least twice
- At least three specific limitations stated in plain language
- A sentence that begins: "Before this system could be considered for any research use..."
- No claim of clinical readiness

---

## How to Inspect the Result

Open `reports/translation_memo.md`. Perform the following checks:

1. Search for "research prototype" or equivalent. If absent, ask Claude to revise.
2. Count the specific limitations. "The model has limitations" does not count as a specific limitation. "The model was trained and evaluated on a single-institution dataset of 20 patients; performance on patients from different scanners or institutions is unknown" counts as specific.
3. Read the Dice score description. Is it contextualized? Does it tell the radiologist what 0.42 means in practice?
4. Check for jargon. If you find "batch normalization," "U-Net architecture," or "cross-entropy" without immediate plain-language explanation, the audience translation is incomplete.

---

## Reflection Question

Would you use this system if you were the radiologist reading this memo? Under what conditions?

Think specifically: what would you need to know about the system that is not yet in the memo? What additional validation study would you want to see before you would trust the output enough to use it as a second-opinion tool in a research context?

---

## Extension Challenge

Write a second version of the memo for a different audience: a hospital administrator considering funding a prospective study. The administrator cares about different things than the radiologist — costs, timelines, regulatory requirements, liability, patient consent. What changes in the framing, the level of detail, and the emphasis? Write a prompt that switches the audience while keeping the same honesty constraints.

---

## Transfer to Your Own Research

For any technical research result in your own work, how would you write a one-page honest summary for a clinical collaborator?

Practice: take the most recent result from your own research and write a three-paragraph limitation-first summary for a clinical audience. Start with what was not demonstrated. Then state what was demonstrated and what the number means in practice. Then describe what additional evidence would be needed before the result should influence clinical decision-making.
