# Medical AI + Agentic Coding Lab

**A PhD Summer Course on Clinical AI, MRI Analysis, and Prompt-First Research**

---

This is a two-day intensive course for doctoral researchers who want to understand how artificial intelligence is being applied to clinical medicine — and who want hands-on experience building, evaluating, and critically assessing an AI system using real medical imaging data. Over two days you will work through seven lab missions that take you from environment setup all the way to a structured assessment of whether an AI model is ready to support clinical decision-making. You will use Claude Code as your research partner throughout: not as a black box that writes code for you, but as a collaborative agent you direct with precise scientific language. By the end of the course you will have built a brain tumour segmentation pipeline from scratch, run a formal error analysis, and written a structured argument about clinical translation readiness — using prompts as your primary research instrument.

---

## Who This Course Is For

This course is designed for PhD students in medicine, biology, neuroscience, radiology, biomedical engineering, and adjacent fields who are scientifically rigorous but who may not have a background in software engineering or machine learning. You do not need to know how to write Python from memory. You do not need prior experience with neural networks or image processing libraries.

What you do need is the ability to think clearly about a research question, to describe what you expect to happen before you run an experiment, to interrogate results that do not match your expectations, and to maintain appropriate scientific scepticism about tools you did not build yourself.

If you can write a coherent methods section for a clinical study, you have the foundational skills to direct an AI coding agent. That is the premise of this course.

!!! note "A note on diversity of background"
    Participants will arrive with very different technical histories. Some will have written analysis scripts in R or Python; others will not have opened a terminal in years. Both are welcome. The course is calibrated so that scientific judgment — not prior coding ability — determines how much you get out of it.

---

## What You Will Build

Over the two days, you will construct a brain tumour segmentation pipeline using MRI data in the style of the BraTS (Brain Tumour Segmentation) benchmark. This involves:

- **Loading and inspecting multi-contrast MRI volumes** (T1, T1ce, T2, FLAIR) to understand what the data looks like before modelling begins
- **Running a baseline segmentation model** directed entirely through structured prompts to Claude Code, without writing a single line of code manually
- **Evaluating the model** using clinical metrics — Dice coefficient, sensitivity, and specificity — and understanding what those numbers mean for a radiologist reviewing the output
- **Conducting a structured error analysis** to identify where and why the model fails: false positives in white matter lesions, missed infiltrative margins, boundary uncertainty
- **Iterating with intent** — writing a second-generation prompt that encodes your hypotheses about what will improve the model, then verifying whether the results match your prediction
- **Designing a follow-up validation study** with appropriate patient cohort, endpoints, and statistical power reasoning
- **Assessing clinical translation readiness** against the TRIPOD+AI reporting framework and regulatory considerations for AI as a medical device

At the end of Day 2, each participant (or small group) presents their pipeline, their best and worst segmentation cases, and their argument about what would need to be true before this system could enter a clinical workflow.

---

## What Prompt-First Research Means

In conventional computational research, the researcher writes code that implements their scientific intent. The code is the protocol. This creates a high barrier: if you cannot write the code, you cannot do the experiment.

Prompt-first research inverts this relationship. You describe your research intent, your constraints, and your expected outputs in precise natural language — the prompt — and an AI agent translates that intent into executable code. The prompt is the protocol.

!!! tip "Prompts are not magic words"
    This does not mean you can be vague. A poorly written prompt produces poorly targeted code, just as a poorly written methods section produces a poorly conducted study. The discipline of prompt writing is the discipline of making your scientific intent unambiguous. You still need to understand the domain well enough to know whether the output is correct.

This also does not mean coding skill has become irrelevant. A researcher who understands what a segmentation function should return, what a Dice score means computationally, and what a data loading pipeline should produce — that researcher writes better prompts and catches more errors in the AI's output. Scientific knowledge and domain familiarity amplify the value of every prompt you write.

What changes is the bottleneck. Instead of "can I write this function?", the question becomes "can I specify precisely what this function should do, verify that it does it, and interpret the result scientifically?" That is a question researchers with deep domain knowledge are uniquely positioned to answer.

---

## The Seven Mission Arc

The course is structured around seven lab missions, each building on the previous. You complete these in the GitHub Classroom repository provided at the start of Day 1.

| Mission | Name | One-Sentence Description |
|---------|------|--------------------------|
| **M0** | Wake the Lab | Verify your environment, clone the repository, and confirm that all tools are installed and responsive. |
| **M1** | Receive the Signal | Load a multi-contrast MRI volume, inspect its metadata and visual structure, and write a data quality report using Claude Code as your analysis assistant. |
| **M2** | Build the First Detector | Prompt Claude Code to implement a baseline brain tumour segmentation model and run it on three representative cases; collect raw metric output. |
| **M3** | Investigate Failure | Select your worst-performing case, conduct a structured error analysis, and produce a written hypothesis about the model's failure mode. |
| **M4** | Improve With Intent | Encode your failure hypothesis as a specific prompt refinement, re-run the pipeline, and measure whether the change had the predicted effect. |
| **M5** | Design the Next Study | Write a structured study design document — patient cohort, endpoints, sample size reasoning — for a prospective validation of your pipeline. |
| **M6** | Translate Responsibly | Complete a clinical translation assessment: regulatory pathway, reporting checklist, failure mode catalogue, and deployment prerequisites. |

!!! info "The arc matters"
    Missions are not independent exercises. M3 depends on output from M2. M4 depends on the hypothesis you wrote in M3. M6 draws on everything. If you skip ahead, you will have less to work with at the end.

---

## How to Use This Site

This tutorial site is organised into parallel chapters that map to the lab missions. The intended workflow for each session is:

1. **Read the chapter** — absorb the conceptual and clinical background before touching the lab
2. **Do the mission** — open the GitHub Classroom repo and follow the mission brief
3. **Inspect the artifact** — every mission produces a specific output file (a plot, a metrics table, a written report); read it carefully before moving on
4. **Reflect** — each chapter ends with a reflection question; write a one-paragraph answer in your lab notebook
5. **Optional extension** — if you have time, each mission has a stretch task that takes the science further

!!! tip "Do not skip the reading"
    The lab missions assume you have read the corresponding tutorial section. The missions do not re-explain concepts; they ask you to apply them. A student who skips the MRI chapter and proceeds to Mission 1 will find the data inspection questions opaque.

---

## How This Site Connects to the Lab

There are two distinct components to this course and it is important to understand what each one provides.

**This site** (the one you are reading now) provides:

- Conceptual and clinical background for every topic in the course
- Worked examples of how to structure research prompts
- A Prompt Library of ready-to-use templates for Claude Code
- Reference tables for metrics, MRI sequences, and regulatory frameworks
- Printable handout cards for the live sessions

**The GitHub Classroom repository** (provided separately) provides:

- The actual MRI data (BraTS-format, three training cases)
- Mission brief files (`mission_00/`, `mission_01/`, etc.) with specific tasks and grading rubrics
- A scaffold Python environment with dependency pinning
- An auto-generated dashboard that displays your segmentation metrics after each run
- Instructor-visible submission artefacts

!!! info "The site teaches; the repo is where you work"
    Think of this site as the textbook and the repo as the laboratory. You would not attempt a wet-lab protocol without reading the relevant biochemistry first; the same logic applies here.

---

## Quick Start

!!! info "Day 1 — Where to Begin"
    **Before the first session:**

    1. Accept the GitHub Classroom assignment link (provided by your instructor via email or the course LMS).
    2. Read [Foundations → Clinical AI](foundations/clinical_ai.md) — approximately 15 minutes.
    3. Read [Agentic Research → What Is Agentic Coding](agentic_research/what_is_agentic_coding.md) — approximately 10 minutes.

    **At the start of Day 1:**

    Open the [Two-Day Schedule](course_map/two_day_schedule.md) in one browser tab and your GitHub Classroom repo in another. The instructor will walk through Mission 0 together before students work independently.

    **If you are already comfortable with the terminal:**
    Jump directly to the [Prompt Library](prompt_library/overview.md) after Mission 0 to see the full template collection you will be using throughout the two days.
