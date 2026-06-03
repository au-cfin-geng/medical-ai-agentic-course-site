# How to Use This Site

This page explains the structure of the tutorial site, what the different callout boxes mean, how to navigate, and where to find the reference materials you will use during live sessions. Read this page once at the beginning of the course and refer back to it whenever you are unsure what a particular element is asking of you.

---

## The Read-Then-Do Workflow

Every session in this course follows the same three-phase cycle:

**Phase 1 — Read the tutorial chapter.**
Each major topic in the course has a corresponding tutorial page on this site. The tutorial page provides the conceptual and clinical background you need before entering the lab. It explains why the topic matters, introduces the vocabulary, and connects the concept to the mission you are about to attempt. Depending on the chapter, reading takes between 10 and 25 minutes.

**Phase 2 — Do the mission.**
Open the GitHub Classroom repository. Navigate to the folder for the current mission (`mission_00/`, `mission_01/`, etc.). Read the mission brief file (`README.md` inside that folder). This brief tells you exactly what to produce and how to submit it. Use the prompt templates from this site's [Prompt Library](../prompt_library/overview.md) as your starting points, but adapt them to your specific data and results.

**Phase 3 — Reflect.**
Each tutorial chapter ends with a reflection question. Write a short answer — one paragraph is sufficient — in the lab notebook file provided in the repo (`lab_notebook.md`). The reflection is not graded for correctness; it is graded for evidence of genuine engagement with the question. The questions are designed to surface assumptions you may not have noticed you were making.

!!! tip "The optional extension"
    If you complete all three phases with time remaining, each mission brief includes an optional extension task. These are not required and do not affect your standing in the course. They are offered for students who want to push the science further — for example, running the pipeline on a fourth case, computing additional subregion metrics, or reading a cited paper. Instructors are happy to discuss extension work during the showcase.

---

## What the Callout Boxes Mean

Throughout this site you will encounter coloured callout boxes (also called admonitions). Each colour and type encodes a specific kind of information. Learning to recognise them quickly will help you skim the chapters efficiently during live sessions.

### Clinical Relevance (green — `!!! success`)

!!! success "Clinical Relevance"
    A green box signals that this concept connects directly to clinical decision-making. It answers the question: *why would a radiologist, oncologist, or neurosurgeon care about this?* These boxes are worth reading carefully even if you are confident in the technical content, because the clinical interpretation is where the scientific contribution of your analysis lives.

### Prompt Principle (blue — `!!! info`)

!!! info "Prompt Principle"
    A blue box contains a guiding principle for how to translate the surrounding concept into a Claude Code prompt. It often includes a brief example of phrasing. Think of these as mini-protocol templates: they tell you the *shape* of the instruction you should give the agent for this type of task.

### Lab Bridge (indigo — `!!! note`)

!!! note "Lab Bridge"
    An indigo note box makes an explicit connection between the tutorial content and a specific mission task. If you are reading quickly, these boxes tell you precisely which part of the lab applies what you just read. They often point to a specific section of the mission brief or a specific output file to inspect.

### Reflection (amber — `!!! question`)

!!! question "Reflection"
    An amber question box poses the reflection question for the section. These are the questions you write a paragraph about in your lab notebook. They are intentionally open-ended. There is no single correct answer; the point is to reason carefully about the concept in a way that connects to your own research context.

### Warning and Caution (orange/red — `!!! warning`, `!!! danger`)

!!! warning "Be careful here"
    Orange warning boxes flag a common mistake or a place where students frequently go wrong. Pay close attention to these before submitting your mission artefacts.

!!! danger "Do not do this"
    Red danger boxes indicate an action that could cause significant problems — for example, overwriting a data file, committing credentials to a public repo, or running a function that assumes normalised data on un-normalised input. These are rare in the tutorial site but should be taken seriously.

### Instructor Notes (yellow — `!!! warning "Instructor note"`)

Instructor notes are marked with a yellow banner and the label "Instructor note." Students are welcome to read them — they contain useful context about teaching decisions and common student difficulties — but they are not required reading. They are addressed to the person facilitating the session rather than the person completing the missions.

---

## Navigating the Site

### Tabs

The primary navigation is the tab bar across the top of the screen. The tabs group the site into logical sections:

- **Home** — the welcome page and quick start
- **Course Map** — schedule, outcomes, lab alignment (you are here)
- **Foundations** — clinical and scientific background, ethics
- **MRI Textbook** — the imaging science you need for Mission 1 and beyond
- **Medical AI Workflow** — the end-to-end pipeline from question to translation
- **Agentic Research** — how to work with Claude Code effectively
- **Lab Missions** — overview pages for each mission (the detailed briefs live in the repo)
- **Prompt Library** — ready-to-use prompt templates
- **Handouts** — printable reference cards
- **Instructor Notes** — teaching guidance

### Table of Contents

On wide screens, a table of contents appears on the right-hand side of each page, showing the headings within the current chapter. Use this to jump to a specific section without scrolling.

### Search

The search icon in the header opens a full-text search across all pages. This is the fastest way to find a specific term, metric name, or concept during a live session. The search is available offline if you have loaded the site previously.

---

## The Handouts Section

The [Handouts](../handouts/cheat_sheet_clinical_ai.md) section contains five printable reference cards:

| Card | Contents |
|------|----------|
| Clinical AI Cheat Sheet | Key definitions, scope, failure mode taxonomy |
| MRI Cheat Sheet | Sequence properties, tissue contrasts, clinical roles |
| Metrics Cheat Sheet | Dice, sensitivity, specificity — formulae and clinical interpretations |
| Prompting Cheat Sheet | Prompt anatomy, quality criteria, common mistakes |
| Lab Commands Cheat Sheet | Shell commands and Claude Code invocations used in the missions |

These cards are designed to be printed on A4 or Letter paper and kept on the desk during sessions. The instructor will have printed copies available for Day 1, but the digital versions are always accessible here.

---

## The Prompt Library

The [Prompt Library](../prompt_library/overview.md) is one of the most practically useful parts of this site. It contains ready-to-use prompt templates organised by task type:

| Section | What It Contains |
|---------|-----------------|
| Setup Prompts | Environment verification, dependency checking, directory structure |
| Data Prompts | MRI loading, inspection, quality reporting |
| Visualisation Prompts | Segmentation overlays, slice plots, intensity histograms |
| Modeling Prompts | Baseline segmentation, pipeline implementation, inference |
| Error Analysis Prompts | Failure classification, spatial analysis, hypothesis generation |
| Reviewer Prompts | Critical evaluation of outputs, consistency checking |
| Translation Prompts | Regulatory mapping, TRIPOD+AI checklist, deployment assessment |
| Bonus Prompts | Extensions, additional analyses, research ideation |

!!! info "Prompt Principle"
    The templates in the Prompt Library are starting points, not finished products. Before you use a template, read it carefully and adapt the placeholder text — file paths, case numbers, specific hypotheses — to your actual situation. A prompt that refers to the wrong data file will produce output you cannot use, and you will lose time diagnosing the mismatch. The discipline of reading the template before pasting it is the discipline of understanding what you are asking for.

---

## Instructor Notes Are Not Required Reading

Pages in the [Instructor Notes](../instructor_notes/teaching_flow.md) section are addressed to the course facilitator. They contain guidance on pacing, common student difficulties, how to run the live demo, and how to facilitate the showcase discussion. Students are welcome to read them — the content about where students typically struggle is often useful for students who want to anticipate difficulty — but there will be no exam or reflection question that draws on instructor note content.
