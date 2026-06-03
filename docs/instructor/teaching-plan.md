# Teaching Plan

!!! warning "Instructor Resource"
    This page is for instructors and teaching assistants only. It contains facilitation notes, pacing guidance, and content that students should not read before completing the missions. If you are a student and have arrived here by accident, please navigate to the [Getting Started](../getting-started/course-overview.md) page instead.

---

## Overview

This course runs as two intensive lab days. The pedagogical arc moves from orientation → exploration → analysis → controlled experiment → study design → translation. Each mission produces a concrete artifact; the artifacts accumulate across the course and collectively constitute the student's research output. The showcase on Day 2 afternoon is the synthesis moment: students present not slides but their actual artifacts.

**Target cohort:** PhD students in medicine, biomedical engineering, computational biology, or related fields. Mixed programming backgrounds. Some may have strong Python skills; others may have minimal coding experience. The agentic approach is designed to be accessible regardless of coding background because Claude Code handles implementation — the student handles research reasoning.

**Room setup:** Individual laptops. Reliable WiFi. At minimum, one projector for instructor demos. A second screen or projector for displaying the dashboard is useful but not required.

---

## Day 1 Teaching Plan

| Time | Activity | Duration | Key teaching point | What to demo |
|---|---|---|---|---|
| 09:00 | Opening and onboarding | 30 min | The clinical motivation: why brain tumour segmentation matters and why the gap between benchmark and clinic is the central problem of this course. | Show one BraTS case slice: ask "would you trust an AI to segment this?" — leave the question open. |
| 09:30 | Foundations lecture: Clinical AI and translation | 60 min | Three ideas: (1) benchmark performance is not clinical utility, (2) AI errors are not random, (3) the researcher is always responsible. | Show a confusion matrix for a high-Dice model that fails on small tumours. |
| 10:30 | Mission 0 — Wake the Lab (instructor-led) | 45 min | CLAUDE.md as project memory. The context-setting first message. The approval loop. | Live demo: open CLAUDE.md, send a cold-start prompt, show context loss. Then add CLAUDE.md and show the difference. See [Live Demo Script](live-demo-script.md). |
| 11:15 | Mission 1 — Receive the Signal | 60 min | The Inspector Role. Observation before hypothesis. Output contract for a JSON data summary. | Circulate. Ask students to read their data summary aloud before moving to Mission 2. |
| 12:15 | Lunch | 60 min | — | — |
| 13:15 | MRI and metrics lecture | 45 min | What Dice measures and what it misses. HD95 intuition. Why WT/TC/ET measure different clinical questions. | Show an error map: same Dice, different spatial pattern. Ask which failure is clinically worse. |
| 14:00 | Mission 2 — Build the First Detector | 90 min | Plan-before-code. Output contract for metrics JSON. The baseline is not the goal — it is the calibration. | Demo the plan step: show that approving a wrong plan costs one message; approving wrong code costs debugging time. |
| 15:30 | Mission 3 — Investigate Failure | 60 min | Observation before hypothesis. Visual Debugger role. Failure mode taxonomy. | Show an error map with red (FP) near the ventricles. Ask what tissue is being confused with tumour — then ask why. |
| 16:30 | Day 1 debrief | 30 min | Every group shares one number (worst Dice) and one sentence (failure hypothesis). Instructor synthesises patterns across the cohort. | Write the cohort's failure hypotheses on a whiteboard. Group them into categories (threshold, boundary, location, subregion). |
| 17:00 | End of Day 1 | — | — | — |

**Day 1 teaching emphasis:** Slow down at Mission 0. Students who rush the context-setting step consistently struggle in Missions 1 and 2. The 15 minutes spent on a good first message saves 45 minutes of context-recovery later.

**What to cut if Day 1 runs long:** Shorten Mission 3 to hypothesis-only (one paragraph, no full error analysis). The Mission 4 intervention still works. Do not cut the Day 1 debrief — it is the foundation for the Day 2 error analysis lecture.

---

## Day 2 Teaching Plan

| Time | Activity | Duration | Key teaching point | What to demo |
|---|---|---|---|---|
| 09:00 | Error analysis lecture | 45 min | Systematic failure analysis: spatial, class-based, patient-subgroup. The distinction between model error and label error. How error analysis sets up Mission 4. | Show two cases with the same Dice but different failure modes. Ask which is more tractable. |
| 09:45 | Mission 4 — Improve With Intent | 90 min | The controlled experiment: one hypothesis, one change, measure and interpret. The hypothesis is a scientific prediction, not a wish. | Demo the hypothesis statement before implementation. Show the difference between "I will try raising the threshold" and "I predict that raising the threshold from 0.3 to 0.5 will reduce FP voxels near the ventricles by approximately 30%, increasing specificity_wt while keeping dice_wt above 0.70." |
| 11:15 | Prompting workshop | 45 min | Three anonymised prompts from the current cohort — one excellent, one adequate, one problematic. Group critique and rewrite. | Select actual student prompts from the morning session (with permission). Protect identities if needed. |
| 12:00 | Mission 5 — Design the Next Study | 60 min | Study design elements: population, reference standard, endpoints, sample size, bias. The role-switch from developer to study designer. | Show the Skeptical Reviewer role applied to a study design: "What are the three most serious weaknesses in this design?" Use a real student design from the session if available. |
| 13:00 | Lunch | 60 min | — | — |
| 14:00 | Mission 6 — Translate Responsibly | 75 min | Honesty constraints. What was not demonstrated. Clinical readiness spectrum. Regulatory pathways. | Read a brief without honesty constraints; then read one with. Ask the class which they would trust if they were the clinical collaborator. |
| 15:15 | Showcase preparation | 30 min | Students select: best result, worst result, failure hypothesis, strongest translation argument. | Circulate. Help students pick one finding, not everything. The best presentations have a single clear point. |
| 15:45 | Student showcase | 60 min | Peer learning. Each group presents 5 minutes; 3 minutes questions. | After each presentation: ask the audience "what would you do differently, and why?" Record notable patterns on the whiteboard. |
| 16:45 | Closing | 20 min | Connecting the course methods to students' own doctoral research. What agentic research makes possible that was not possible before. | Ask: "What would you do differently in your own research after this course?" |
| 17:05 | End of Day 2 | — | — | — |

---

## Pacing for Mixed Groups

**Fast-moving students** (strong coding background, complete missions quickly): Direct them to the optional exploration tasks in each mission brief. In Mission 4, ask them to run a second controlled experiment with a different hypothesis. In Mission 5, ask them to write a sample size justification. Do not let them jump ahead to Mission 6 without completing the Skeptical Reviewer step on their own work.

**Slower-moving students** (limited coding background, struggling with environment): The fallback outputs in `fallback_outputs/` cover Missions 2 and 4. Students can use these to complete Missions 3, 5, and 6 even if their live computation did not produce usable results. The reading and reasoning tasks in these missions are the primary learning objectives; the computed numbers are inputs to that reasoning, not the end goal.

**Groups that finish everything early:** Ask them to prepare a 5-minute peer teaching segment for the showcase: "what we learned that we did not expect." These segments are often the most pedagogically valuable moments of the showcase.

---

## What to Cut If Short on Time

See the `two_day_schedule.md` for the full list of sessions marked ★ (minimum viable). In brief:

- Mission 3 can be hypothesis-only (5 minutes writing, not full error analysis).
- The prompting workshop on Day 2 morning can be cut to 20 minutes or deferred.
- Mission 5 can be a take-home if time does not allow in-session completion.
- Never cut: Mission 0, Day 1 debrief, student showcase.
