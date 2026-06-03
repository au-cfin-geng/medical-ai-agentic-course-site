# Course Overview

## What This Course Is

This is a two-day intensive PhD-level course in clinical AI research, delivered through a hands-on lab environment where you work with real MRI data, implement real segmentation models, and produce evaluation artifacts that look and feel like the outputs of a real research project.

The course has one central argument: the most important skill in modern clinical AI research is not knowing which model architecture to use. It is knowing how to specify, direct, inspect, and judge computational work — and how to communicate findings honestly to a clinical audience. The agentic AI tools available today make this argument practically important, not just philosophically interesting.

You will spend very little time writing code from scratch. You will spend a great deal of time writing prompts, inspecting outputs, catching errors, and making scientific judgments that no AI can make for you.

---

## Two Assignments, One Research Arc

The course is structured around two assignments that together simulate a complete clinical AI research arc.

**Assignment 1 (Day 1)** covers the technical core of clinical AI: data inspection, baseline modeling, error analysis, and controlled improvement. You build a brain tumour detection model from scratch using MRI data from the BraTS dataset, evaluate it honestly, investigate where it fails, and implement one controlled improvement. Every step produces a required artifact — a file Claude writes according to your specifications.

**Assignment 2 (Day 2)** covers the research and translation side: study design, ethical critique, and responsible clinical communication. You design a prospective clinical study that would validate your model in a real hospital setting, have that design critiqued from multiple perspectives, and produce a clinical translation memo written for a non-specialist audience. You also synthesise everything into a brief reflection on what you would do differently in your own PhD research.

The two assignments are designed to be inseparable. A clinical translation memo that is not grounded in honest error analysis is not science — it is marketing. The course structure enforces this by making Assignment 2 depend on the artifacts from Assignment 1.

---

## What Makes This Different From a Traditional ML Course

Most machine learning courses teach you to write code. This course teaches you to do research.

**Prompt-first, not code-first.** In this course, you write prompts that direct Claude to write the code. This is not a shortcut — it is a different skill, and arguably a harder one. Writing a good prompt requires understanding what the code should do, what it must not assume, what the output should look like, and what would count as an error. You cannot write a good prompt without understanding the domain.

**Artifact-driven, not assignment-driven.** Every mission produces a required artifact: a report, a JSON file, a comparison table. These artifacts have specified filenames, locations, and structures. This forces the kind of output discipline that real research requires. A result that cannot be inspected, compared, or shared is not a result.

**Clinical framing throughout.** Every technical choice is grounded in a clinical question. You are not segmenting tumours because segmentation is interesting. You are asking: could this model be used to assist a radiologist? What would it take to know that it is safe to use? What would a neurosurgeon need to know before trusting it? These questions shape every mission.

**Human judgment is non-optional.** Claude can write code, generate reports, and produce visualisations. Claude cannot tell you whether a segmentation failure is clinically significant. Claude cannot tell you whether your study design has adequate power for the question you are asking. Claude cannot tell you whether a clinical translation memo overstates the evidence. You can. You must.

---

## Day 1 Flow

Day 1 begins with environment setup (Preflight) and an orientation to the project structure (Mission 0). You then work through three missions in sequence:

- **Mission 1** — You inspect the BraTS dataset: volumes, shapes, labels, intensity distributions. You produce a data inspection report.
- **Mission 2** — You implement a threshold-based baseline segmentation model. You evaluate it with Dice coefficient, sensitivity, and specificity. You produce a results file.
- **Mission 3** — You investigate where the baseline model fails. You produce visualisations of failure cases and a written error analysis.

By the end of Day 1 you have a functioning model, an honest evaluation, and a clear picture of its failure modes. You also have three artifacts that document your work in a format that could, in principle, be included in a research paper.

---

## Day 2 Flow

Day 2 begins with Mission 4, which asks you to implement one controlled improvement to your baseline model. The improvement must be specified as a hypothesis before Claude implements it, and the results must be compared directly against the baseline.

Mission 5 asks you to design the prospective clinical study that would validate your improved model in a real hospital. You draft the study design yourself, then have Claude critique it from two distinct perspectives: a study design perspective and a clinical safety perspective.

Mission 6 asks you to write a clinical translation memo. Claude drafts it. You inspect it for overstatement, factual errors, and missing caveats. You revise it. The final memo is your work, not Claude's.

The day closes with a brief showcase where each student or group presents one finding they are genuinely proud of and one thing they would do differently.

---

## What You Build

By the end of the course, you will have produced:

1. A preflight environment report
2. A project orientation report
3. A data inspection report covering the full BraTS subset
4. A baseline segmentation evaluation with quantitative metrics
5. An error analysis report with visualisations
6. A controlled improvement comparison
7. A prospective study design with multi-perspective critique
8. A clinical translation memo

These eight artifacts constitute a miniature research dossier. The skills you used to produce them — directing AI, specifying outputs, inspecting results, making domain judgments, writing for clinical audiences — are the skills you will use in your own PhD research.
