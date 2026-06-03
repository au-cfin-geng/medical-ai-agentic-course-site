# Medical AI + Agentic Coding Lab

**A prompt-first clinical AI research course using Claude Code and brain MRI segmentation**

---

## What This Course Is

This lab course teaches you two things at once: how clinical AI systems are built and evaluated in medical imaging, and how to use agentic AI coding tools as rigorous research instruments. The domain is brain MRI tumour segmentation — a well-defined problem with real stakes, open datasets, and clear evaluation metrics. The method is Claude Code, Anthropic's agentic coding environment, used not just as a convenience tool but as a structured research collaborator.

The course is designed for graduate students and clinical researchers who want hands-on exposure to the full clinical AI pipeline — from raw MRI data to a responsible deployment argument — while developing fluency with modern agentic AI workflows.

---

## What You Will Learn Clinically

By the end of this course you will be able to:

- **Inspect MRI data** — understand modalities (T1, T2, FLAIR), voxel geometry, and annotation conventions before writing a single line of model code
- **Run a baseline segmentation** — implement a threshold or atlas-based detector and understand why simple baselines matter
- **Interpret evaluation metrics** — use Dice coefficient, sensitivity, and specificity correctly, and explain what each metric tells a clinician
- **Conduct structured error analysis** — identify where and why a model fails, and connect failure modes to patient safety implications
- **Improve with a controlled hypothesis** — make one deliberate change, measure its effect, and resist the temptation to change everything at once
- **Design a follow-on study** — specify a research question, dataset, evaluation plan, and statistical approach at a level suitable for a grant or ethics application
- **Argue for clinical translation responsibly** — apply honest uncertainty quantification and regulatory framing to a deployment case

---

## What You Will Learn About Agentic Research with Claude

Claude Code is not a chatbot you ask for code. It is an agentic system with persistent memory, tool use, and role-switching capabilities. This course treats it as a research instrument, not a shortcut. You will learn to:

- **Use CLAUDE.md as project memory** — maintain a living document that defines your research question, dataset, and constraints so every session starts with shared context
- **Write explicit output contracts** — tell Claude exactly what format, naming convention, and validation check you expect before generating any file
- **Prompt with observation and hypothesis** — structure prompts as `Observation → Hypothesis → Test`, mirroring scientific method rather than vague requests
- **Switch roles deliberately** — use Claude as analyst, critic, coder, and clinical advisor in sequence, keeping each role's scope explicit
- **Run controlled prompt iterations** — change one prompt variable at a time and record results, treating prompt engineering as an experiment
- **Evaluate and compare prompts** — use quantitative metrics and qualitative review to judge which prompt strategy produces better research outputs
- **Understand skills, subagents, and MCP** — know when to compose Claude capabilities versus when to keep tasks atomic
- **Apply honesty constraints** — understand AI limitations and safety boundaries relevant to clinical deployment

---

## Two-Assignment Structure

The course uses two assignments that build on each other.

**Assignment 1 — Preflight** establishes your agentic workstation. You configure Claude Code, write your initial CLAUDE.md, verify that your environment can load and inspect MRI data, and submit a setup confirmation. This happens before Day 1.

**Assignment 2 — Main Lab** covers the full clinical AI pipeline across two sessions. You build, evaluate, fail, improve, design, and translate — documenting every step with prompts, outputs, and reflections.

---

## Schedule at a Glance

### Day 0 / Preflight
Set up your agentic workstation. Install Claude Code, clone the lab repository, write your CLAUDE.md, and complete the preflight data inspection. Confirm you can load a BraTS scan and compute a basic Dice score before arriving on Day 1.

### Day 1 — Build and Evaluate (Missions 0–4 + Pack Report)
- **Mission 0** — Wake the Lab: orient Claude to your project and verify the data pipeline end to end
- **Mission 1** — Receive the Signal: inspect and document the MRI dataset with structured prompting
- **Mission 2** — Build the First Detector: implement a baseline segmentation algorithm and run initial evaluation
- **Mission 3** — Investigate Failure: conduct systematic error analysis with Claude in critic role
- **Mission 4** — Improve With Intent: form a hypothesis, make one controlled change, re-evaluate
- **Pack Report**: consolidate findings from Missions 0–4 into a structured research document

### Day 2 — Critique, Improve, Translate (Missions 5–6)
- **Mission 5** — Design the Next Study: draft a follow-on research proposal with dataset, metrics, and statistical plan
- **Mission 6** — Translate Responsibly: write a clinical translation argument with explicit uncertainty and regulatory framing

---

## Relationship to Anthropic Academy

This course references and builds upon publicly available Anthropic Academy learning resources on prompt engineering, Claude's tool use, and responsible AI deployment. Where specific Academy modules are relevant to a lab mission, the [Reading Map](readings/anthropic-academy-reading-map.md) identifies which resources to consult. No Academy content is reproduced here; all references are pointers to external materials.

---

## Quick Navigation

| Where to go | What you will find |
|---|---|
| [Getting Started](getting-started/course-overview.md) | Course overview, classroom workflow, and preflight setup instructions |
| [Lab Missions](labs/preflight.md) | All lab assignments with step-by-step mission briefs |
| [Clinical AI](clinical-ai/what-is-clinical-ai.md) | Conceptual foundations: MRI, segmentation, metrics, translation |
| [Agentic Research](agentic-research/what-is-agentic-research.md) | Claude Code mental models, prompt patterns, and tool use contracts |
| [Handouts](handouts/clinical-ai-one-page.md) | Printable cheatsheets for clinical AI, MRI, metrics, and prompting |
| [Reading Map](readings/anthropic-academy-reading-map.md) | Pointers to Anthropic Academy and further reading |
| [Instructor](instructor/teaching-plan.md) | Teaching plan, discussion prompts, demo scripts, and rubrics |

---

!!! tip "Start Here If You Are a Student"
    Go to [Getting Started — Course Overview](getting-started/course-overview.md) to understand the structure, then jump to [Preflight Setup](getting-started/setup-preflight.md) to configure your environment before Day 1.

!!! note "Start Here If You Are an Instructor"
    Go to [Instructor — Teaching Plan](instructor/teaching-plan.md) for session timing, facilitation notes, and the live demo script.
