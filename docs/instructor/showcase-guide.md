# Showcase Guide

!!! warning "Instructor Resource"
    This page is for instructors and teaching assistants. Review before Day 2 afternoon. The showcase is the highest-leverage teaching session in the course — protect this time.

The student showcase at the end of Day 2 is not a performance review and it is explicitly not judged by Dice score. It is a peer learning event where students practise the kind of scientific communication they will need in clinic-facing research: explaining what you found, what you cannot claim, and what would need to be true for the result to matter.

---

## The Showcase in Context

The showcase works because students have spent two days building up real artifacts — data summaries, error maps, metrics JSONs, controlled experiment comparisons, study designs, and translation briefs. They are not presenting hypothetical work; they are presenting the actual outputs of their research session. This gives the discussion real stakes and makes critique constructive rather than abstract.

The showcase also serves a latent function: it shows every student in the room that all their peers made mistakes, had unexpected failures, and produced imperfect results. That normalisation is pedagogically important in a cohort of PhD students who are often reluctant to share early-stage work.

---

## Three Showcase Formats

### Format A: Full Group Sequential (default, groups of up to 5)

Each student or pair presents for 5 minutes. The instructor or a peer asks one question (3 minutes). Total time: 8 minutes per group. Works for cohorts of up to 8 groups (64 minutes for showcase, leaving time for closing discussion).

**Facilitation:** Keep a visible timer. At 4 minutes, signal that the presenter should move to their conclusion. After each presentation, ask the audience (not the instructor) for the one-question follow-up. Rotate who asks: do not always take the first hand.

### Format B: Gallery Walk (for larger cohorts or when parallel sharing is pedagogically appropriate)

Each group prepares a one-page summary of their four key artifacts (best result, worst result, failure hypothesis, translation brief excerpt). These are posted around the room or shared on a shared screen. Students circulate for 20 minutes, leaving written comments on sticky notes or in a shared document. The instructor then facilitates a 20-minute plenary on the three most interesting divergences across the cohort.

**When to use:** Cohorts of 10+ groups, or when time is very limited. The gallery walk produces more total feedback across the cohort but reduces the depth of any single discussion.

### Format C: Curated Panel (for courses with an expert audience or clinical collaborator present)

The instructor selects three or four presentations in advance — ideally one with the best Dice score, one with the worst Dice score, and one or two with the most interesting failure hypotheses. These are presented as a panel to an invited clinical or research audience. The audience asks questions for the final 20 minutes.

**When to use:** When a clinical collaborator, department head, or external expert is attending Day 2. The curation is done transparently: tell the full class that three or four groups will present in depth, and all artifacts will be shared in the cohort portfolio.

---

## Judging Criteria

**The showcase is not judged by Dice score.** Explicitly say this at the start: "The group with the highest Dice score is not the group that learned the most. We are looking for something else."

What the showcase is judged by — informally, in terms of what makes a presentation excellent:

1. **Precision of failure characterisation.** The student names a specific failure mode, localises it anatomically, and explains why it matters clinically. Vague failure descriptions ("our model didn't work well on some cases") score poorly in the room; specific ones ("our model systematically undersegments the enhancing tumour in cases where T1ce shows heterogeneous enhancement — about 30% of our test cases — and that would matter clinically because ET is used to define the radiation boost volume") make the audience lean forward.

2. **Honest prototype maturity statement.** The student states explicitly what level of clinical readiness was reached and what additional evidence would be required. Students who overstate their results are typically identified and challenged by peers — this is one of the most valuable moments in the showcase.

3. **Quality of the hypothesis.** The failure hypothesis should be falsifiable ("I believe the FP near the ventricles are caused by CSF-adjacent FLAIR signal — a model that uses T1 as a prior would reduce them") not aspirational ("we should try a better model next time").

4. **One specific next step.** The closing sentence of the showcase presentation should name one specific, concrete next step that follows directly from the findings. Not "do more research" but "run the same threshold experiment on the five cases with smallest tumours to see whether our improvement holds for that subgroup."

---

## Closing Discussion Framework

After all presentations, facilitate a 15-minute structured closing discussion. Use this framework — these four elements correspond directly to the course's core learning objectives:

**"State your best result."**
Each group states, in one sentence, their best metric result and the conditions under which it was obtained. Instructor writes these on the whiteboard in a table (case count, Dice WT, Dice TC, Dice ET). The table makes the cohort's variation visible: some groups will be at 0.65, others at 0.88. Ask the class: "Why does this variation exist, given we all ran on the same dataset?"

**"State your failure hypothesis."**
Each group states their primary failure hypothesis in one sentence. Instructor clusters these on the whiteboard: threshold-related, boundary-related, registration-related, subregion-related. Ask: "What would you need to run to test which of these hypotheses is correct?" This is the study design question posed in reverse.

**"State your prototype maturity."**
Each group names their clinical readiness level (1–5). This is usually uniformly Level 1 or Level 2, and that is the expected and correct answer. If any group says Level 3 or above, ask them to justify it: what external validation was performed? This is one of the most important moments in the course because it directly addresses the gap between benchmark performance and clinical utility.

**"State your next step."**
Each group names one specific next step. Instructor records these on the whiteboard. At the end, ask: "Which of these next steps would you prioritise if you had one more day? Why?" This closing question is forward-looking and leaves students with a concrete research agenda rather than a sense of having completed an exercise.

---

## Common Facilitation Challenges

**Students who present only their Dice score and nothing else.** Redirect: "Tell us about your worst case. What did you find when you looked at the error map?" The worst case is almost always more interesting than the best case.

**Students who apologise for low Dice scores.** Interrupt gently: "You don't need to apologise for this. The failure mode is the finding. Tell us what you observed." Normalise failure as data.

**Students who present a very high Dice score without context.** Ask: "How many cases? What subregions? What was your test set?" A Dice of 0.92 based on three cases is a promising signal, not a validated result. Help the student articulate this distinction without undermining their sense of accomplishment.

**Groups who run out of time during the showcase.** Signal at 4 minutes. If they are still in the failure analysis section at 4:30, ask them to jump to the next step directly. The translation brief is the most important part of the showcase presentation; protect time for it.

**A quiet room after a presentation.** If the audience does not ask questions, ask one yourself — then explicitly turn it to the audience: "Does anyone want to follow up on that?" If the room is still quiet, ask a direct question to a specific student: "You had a similar failure mode — does that hypothesis match what you saw?"
