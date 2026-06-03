# Mission 5 — Design the Next Study

Every pilot experiment ends with a question: what should we do next, and how should we do it rigorously?

---

## Why This Matters Clinically

The gap between a successful pilot experiment and a rigorous follow-on study is where most clinical AI research stalls. A pilot demonstrates feasibility on a small dataset with a simple model. A follow-on study tests a specific hypothesis on a larger, more representative dataset, with pre-specified endpoints, a statistical analysis plan, and a realistic risk assessment.

The skills required to design the follow-on study are distinct from the skills required to run the pilot. Many researchers who are excellent at implementing and evaluating models struggle to articulate a precise research question, define a measurable success criterion before seeing the data, or anticipate the most likely ways their study design could fail.

Mission 5 trains these skills: taking what you have learned from Missions 0-4 and translating it into a study design that a collaborator could critique, a funder could evaluate, and you could actually execute.

---

## Traditional Bottleneck

Students who finish a pilot computation often cannot articulate a next-study research question with pre-specified success criteria. When asked "what should you do next?", typical answers are:

- "Train on more data" — not a research question.
- "Use a better model" — not a research question.
- "Test on external data" — almost a research question, but lacks a specific hypothesis and a pre-specified success criterion.

The absence of a formalized study design process means that the next study begins without clarity on what would count as success, what the primary endpoint is, what the sample size should be, or what the fallback plan is if the primary approach fails.

Mission 5 uses Claude in a role-switching mode to force clarity: first as developer (reviewing what was built), then as reviewer (critiquing the study design), then as study design critic (generating the strongest objections to the proposed design).

---

## Claude / Agentic Method

Mission 5 introduces role switching as a deliberate strategy for improving research thinking quality. The same task looks different when Claude is playing the developer role versus the reviewer role versus the study design critic role — and the differences reveal blind spots that any single perspective would miss.

**Developer role:** Claude synthesizes Missions 0-4 into a summary of what was demonstrated.

**Reviewer role:** Claude switches to a skeptical peer reviewer who asks: what assumptions were made? What was not demonstrated? What would a skeptical reader object to?

**Study design critic role:** Claude generates the three strongest objections to the proposed follow-on study and proposes revisions to address each.

This role-switching workflow is also an introduction to the conceptual space of subagents — specialized agents that each contribute a distinct perspective to a shared problem.

---

## Anthropic Academy / Claude Reading Connection

> **Disclaimer:** The Anthropic Academy modules listed here are independent courses created by Anthropic. This course is not affiliated with Anthropic, and the connections described below are the course author's interpretation of how those public resources relate to the skills practiced in this lab. Always consult the original Academy content directly.

Relevant Anthropic Academy modules:

- **AI Fluency for Students** — discusses critical thinking about AI research claims. Mission 5's critic role is a practical application of this critical stance.
- **Introduction to Subagents** — introduces the concept of specialized agents with distinct roles. The role-switching in Mission 5 is a manual approximation of what subagent architectures automate.
- **Teaching AI Fluency** — discusses how to develop AI literacy in research contexts. Designing a rigorous study is an act of AI fluency: knowing when and how to trust AI-assisted results.
- **AI Capabilities and Limitations** — Mission 5's study design process explicitly addresses the limitations discovered in Missions 1-4 as the starting point for the next research question.

---

## Prompt Pattern Practiced

**Switch Claude to reviewer role before asking for the next study; plan before code**

This prompt pattern enforces a cognitive shift: you cannot design a rigorous next study without first honestly assessing what your current study did and did not demonstrate. The role switch forces this assessment.

**Phase 1 — Developer summary:**
```
Read CLAUDE.md and all reports in the reports/ directory.
Act as the developer who built this system. Summarize in 200 words:
- What was demonstrated (with specific Dice scores and metrics)
- What was not demonstrated (what claims cannot be made from this pilot)
- The single most important limitation of the current work
Write this summary to reports/day1_summary.md.
```

**Phase 2 — Study design:**
```
Now switch roles. Act as a researcher designing the follow-on study.
Based on the limitation you identified, write a study design in reports/challenge_plan.md
with exactly six sections:
1. Weakness addressed (one sentence: what limitation does this study address?)
2. Research question (format: "Does [intervention] improve [metric] compared to [baseline]
   in [population]?")
3. Proposed method (specific: what model, what data, what split)
4. Success criterion (pre-specified: "We will consider the study successful if [metric]
   exceeds [threshold] on [evaluation set]")
5. Primary risk (what is most likely to go wrong?)
6. Fallback plan (if the primary approach fails, what is the alternative?)
```

**Phase 3 — Critique:**
```
Now switch to skeptical peer reviewer. Read reports/challenge_plan.md.
State the three strongest objections to this study design.
For each objection, propose a specific revision that would address it.
Add a "Reviewer Objections and Revisions" section to reports/challenge_plan.md.
```

---

## What You Will Build

By the end of Mission 5, the project record will contain:

1. **`reports/challenge_plan.md`** — a structured study design with all six sections completed. The research question must name the intervention, the metric, and the baseline. The success criterion must be measurable and pre-specified. The reviewer objections and revisions section must contain at least three specific objections.

2. **`reports/day1_summary.md`** — a honest 200-word summary of what was demonstrated in Missions 0-4, what was not demonstrated, and the single most important limitation. This document is the starting point for the study design.

---

## What to Do in the Lab Studio

1. Start with `reports/error_analysis.md` and `reports/model_swap.md` open.
2. Give Claude the Phase 1 developer summary prompt.
3. Read `reports/day1_summary.md`. Is the limitation identification honest? Does it acknowledge the small sample size, the simple model, the pilot nature of the work?
4. Give Claude the Phase 2 study design prompt.
5. Read the research question. Does it name the intervention, metric, and baseline explicitly?
6. Check the success criterion. Is it measurable? Is it pre-specified (not "we will see")?
7. Give Claude the Phase 3 critique prompt.
8. Read the objections. Are they strong? Could a real peer reviewer have raised them?

---

## Expected Artifact

`reports/challenge_plan.md` — six sections as specified above. The research question must follow the format: "Does [specific intervention] improve [named metric] compared to [named baseline] in [specified population or dataset]?" The success criterion must be a falsifiable statement: "We will consider this hypothesis supported if the Dice score on the held-out test set exceeds 0.65 with patient-level split."

`reports/day1_summary.md` — 200-word honest summary. The most important sentence is the limitation statement: specific, honest, and not defensive.

---

## How to Inspect the Result

Open `reports/challenge_plan.md`. Check the research question: does it name the intervention, the metric, and the baseline? If it says "improve model performance," it is not specific enough. If it says "Does Dice loss combined with boundary weighting improve whole-tumour Dice score compared to binary cross-entropy baseline on BraTS 2021 validation set?", it is specific.

Check the success criterion: is it a falsifiable statement with a named metric and a threshold? If it says "better performance," it is not a success criterion.

Check the reviewer objections: are they substantive? The best objections are ones you would not have thought of yourself. If Claude's objections are generic ("more data would help"), ask Claude to be more specific about the study design's particular weaknesses.

---

## Reflection Question

What assumption in your challenge plan is most likely to be wrong?

Every study design rests on assumptions that are not tested in the pilot. Pick the one assumption in your six-section plan that you are least confident about. What evidence would you need to test that assumption before committing to the full study?

---

## Extension Challenge

Extend the study design to include a statistical power analysis: how many patients would you need to detect an improvement of 0.1 Dice score with 80% power at a significance level of 0.05? Research what statistical approaches are standard for paired or unpaired medical image segmentation comparisons and write a one-paragraph analysis plan.

---

## Transfer to Your Own Research

Could you use this six-section study design structure for your next PhD experiment?

The six sections — weakness addressed, research question, proposed method, success criterion, primary risk, fallback plan — apply to almost any experimental science context. Draft a six-section plan for one experiment you are planning or considering in your own research. Pay particular attention to writing the success criterion before you start: what would count as evidence that your hypothesis is supported?
