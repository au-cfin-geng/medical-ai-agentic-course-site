# Course Blueprint

This document records the design decisions behind the Medical AI and Agentic Coding Lab course site. It is intended for the course team — faculty, TAs, and site maintainers — and should be updated when significant design decisions change.

---

## Course Philosophy

### Clinical Relevance First

Every technical choice in this course is grounded in a clinical question. Students do not learn Dice because it is a metric — they learn it because it is the standard measure used to evaluate segmentation tools, and understanding what it does and does not capture is necessary for evaluating whether a segmentation tool is safe to use. The BraTS dataset is not chosen because it is convenient — it is chosen because brain tumour delineation is a real and consequential clinical task where AI tools have been deployed in clinical practice.

This means the course avoids synthetic datasets, toy problems, and purely illustrative examples whenever possible. Where simplification is necessary (the model used in the lab is smaller than clinical-grade models; training epochs are reduced for time), this is made explicit and the real-world equivalent is described.

### AI as Tool, Not Magic

Students arrive with a wide range of assumptions about what AI is and what it can do. Some overestimate capabilities ("Claude can write the whole paper for me"); others underestimate them ("AI can't actually do useful research"). The course is designed to replace both of these with an accurate, nuanced model: AI tools are powerful research accelerators that require human scientific judgment to use well.

This philosophy is operationalised in every mission. The AI executes; the researcher judges. Students use Claude to write code, generate analyses, and draft text — but they are responsible for checking the output, interpreting the results, and making scientific decisions. The missions are structured so that a student who accepts all of Claude's outputs uncritically will produce inferior work to a student who interrogates them.

### Prompt as Protocol

The central metaphor of the course is that a prompt is a protocol. In wet lab research, a protocol describes exactly what will be done, in what order, with what materials. A prompt to an AI research assistant serves the same epistemic function: it is a record of what was asked for, what constraints were applied, and what was expected. A vague protocol is a reproducibility failure; a vague prompt is a reproducibility failure.

This metaphor was chosen because it maps directly onto existing norms in research (protocols, methods sections, lab notebooks) rather than introducing new vocabulary. Researchers who already write careful protocols understand immediately why a precise prompt matters. Researchers who do not write careful protocols encounter the concept of precision-as-reproducibility in a context where the feedback is immediate (Claude gives a worse response to a vague prompt than to a precise one), which is more effective than explaining it abstractly.

### Scientific Judgment Always Belongs to the Researcher

AI tools can generate analyses, surface patterns, and identify failure modes — but they cannot determine whether a failure mode matters clinically, whether a study design is ethical, or whether an improvement is meaningful. These judgments require domain knowledge, contextual understanding, and professional responsibility that AI tools do not have.

The course makes this boundary explicit in every mission. Mission 3 uses Claude to generate a structured error analysis, but requires students to inspect actual failure cases themselves. Mission 5 uses Claude to draft a study design, but requires students to evaluate whether the design is clinically appropriate. Mission 6 uses Claude to generate a translation document, but requires students to apply a readiness checklist that no AI can complete without human judgment.

---

## The 7-Mission Pedagogical Arc

The missions are designed to follow the arc of a miniature research project, from setup to communication. Each mission builds on the previous one and motivates the next.

**Mission 0 — Wake the Lab**: First contact with Claude Code. Purpose: remove the unfamiliarity barrier before any substantive work begins. Students should leave Mission 0 having used the tool at least three times, with a rough intuition for what a good prompt looks like. No scientific content is introduced here — the only learning outcome is comfort with the tool.

**Mission 1 — Receive the Signal**: Data inspection and environment validation. Purpose: before training any model, students should understand the data. This mission teaches data-first thinking — the habit of looking at raw data before running any analysis. It also surfaces the dataset-specific properties of BraTS that will be relevant in later missions (class imbalance between edema and enhancing tumour; variability in tumour size; the four-modality structure).

**Mission 2 — Build the First Detector**: Training the first model and recording first results. Purpose: produce a result that can be analysed. The Dice score from Mission 2 is not an endpoint — it is the input to Mission 3. The mission is designed to ensure students understand what they submitted (data split, model configuration, training duration) well enough to interpret the results.

**Mission 3 — Investigate Failure**: Error analysis. This is the pedagogical core of the course. Purpose: teach the habit of understanding before acting. Students who complete Mission 3 will have identified at least one specific failure pattern, connected it to a plausible cause, and described what evidence would confirm or disconfirm that cause. This is the same intellectual structure as scientific hypothesis formation, which is the point.

**Mission 4 — Improve With Intent**: One targeted improvement, motivated by the error analysis. Purpose: teach the discipline of evidence-based experimentation. Students are held to one change, one hypothesis, one result. The constraint is uncomfortable and intentional — it is the difference between research and random hyperparameter tuning.

**Mission 5 — Design the Next Study**: Prospective validation study design. Purpose: teach the difference between exploratory results and definitive evidence, and what would be required to produce the latter. This mission has the highest clinical domain dependency — students with clinical backgrounds often produce stronger outputs here.

**Mission 6 — Translate Responsibly**: Clinical translation assessment using a structured readiness checklist. Purpose: close the loop between research and clinical practice by making the gap explicit, honest, and specific. Students should leave Mission 6 able to explain, concretely, what additional work would be needed before their model could be considered for clinical use.

---

## Learning Outcome Taxonomy (Bloom's Alignment)

| Level | Bloom's Category | Example Learning Outcome in This Course |
|-------|-----------------|----------------------------------------|
| 1 | Remember | Name the four MRI modalities used in BraTS and describe what each shows |
| 2 | Understand | Explain why Dice is sensitive to small structures differently than large ones |
| 3 | Apply | Use the Planner pattern to produce a detailed training plan before writing code |
| 4 | Analyse | Identify the primary failure mode of a trained segmentation model from evaluation metrics and visual inspection |
| 5 | Evaluate | Assess whether an improvement is meaningfully better than the baseline, given the experimental context |
| 6 | Create | Design a prospective multi-site validation study for a segmentation model |

The missions are sequenced to move through these levels in order. Missions 0-1 operate primarily at levels 1-2. Missions 2-3 move to levels 3-4. Missions 4-6 operate at levels 4-6. Students who arrive with strong computational backgrounds will move through the lower levels quickly and should be encouraged to focus on levels 5 and 6.

---

## Assessment Philosophy

This course does not use grades or ranked leaderboards. Artifacts demonstrate mastery.

The assessment philosophy rests on three principles:

1. **Process is more important than output.** A student who produces a Dice of 0.65 with clear documentation, a motivated hypothesis, and an honest error analysis has demonstrated more research competence than a student who produces a Dice of 0.82 through undocumented experimentation.

2. **Honesty about limitations is a scientific virtue.** Students are explicitly rewarded (in the showcase criteria and in instructor feedback) for identifying gaps in their work rather than downplaying them. This is the opposite of the reflex most students have learned in coursework, where limitations are weaknesses.

3. **The artifact is the evidence.** Each mission produces at least one artifact: a training run record, an error analysis document, an improvement report, a study design, a translation assessment. These artifacts, taken together, constitute a portfolio demonstrating that the student can execute the complete arc of a medical AI research project. A student who has all six artifacts has something to show a supervisor or a grant committee.

---

## The "Prompt as Protocol" Metaphor

The central metaphor was chosen after considering several alternatives:

- "Prompt as query" (too passive — implies you are retrieving information, not directing action)
- "Prompt as instruction" (too hierarchical — implies the AI is following orders, which misrepresents the interaction)
- "Prompt as conversation starter" (too informal — loses the precision requirement)
- "Prompt as specification" (accurate but jargon-heavy for non-technical students)
- "Prompt as protocol" (maps onto a concept researchers already value and practise)

The protocol metaphor has one important limitation: protocols are fixed before execution, while prompts can be revised in response to output. In practice, agentic coding involves iteration — a first prompt, a review of the output, a revised prompt. This is more like the wet lab practice of piloting a protocol before formalising it. The metaphor holds well enough for the course's purposes.

---

## Technical Infrastructure Decisions

### MkDocs Material (Static Site)

MkDocs Material was chosen over alternatives (Sphinx, Docusaurus, Jupyter Book, Notion, Google Sites) for the following reasons:

- **Markdown-first**: all content is in plain Markdown files, which are version-controlled alongside the site configuration. No database, no proprietary format, no export required.
- **Static output**: the built site is a folder of HTML files that can be hosted on GitHub Pages, Netlify, or any web server for free. No backend, no maintenance overhead.
- **Material theme features**: admonitions, code tabs, Mermaid diagrams, search, and dark mode are available without plugins. These features are used throughout the course site.
- **Version-controlled**: the entire site, including content and configuration, lives in a git repository. This means course updates are tracked, reviewable, and reversible. Multiple instructors can contribute via pull requests.
- **Free to host**: GitHub Pages hosting is free for public repositories and very low-cost for private ones. The total hosting cost for this course site is zero.

### GitHub Classroom

GitHub Classroom was chosen for lab distribution because it integrates with the tools researchers already use (git, GitHub) and does not require learning a new platform. The lab repository is distributed as a GitHub Classroom assignment; students accept the assignment, get a private copy of the repo, and work in their own copy. Their Claude Code session logs and any artifacts they commit are in their own repository.

This has one disadvantage: students who are not comfortable with git will spend time in Mission 0 on git setup rather than on Claude. The setup instructions are written to minimise this, and TAs should be prepared to help with git problems in Mission 0.

### Claude Code

Claude Code (the CLI tool) was chosen over Claude.ai (the web interface) for the following reasons:

- **No GUI barrier**: the CLI runs in the same terminal where students run Python code, view logs, and interact with the file system. There is no context switch between "AI conversation" and "coding environment."
- **Inspectable interactions**: Claude Code shows what files it is reading, what commands it is running, and what its plan is before executing. This transparency is essential for the course goal of teaching students to verify AI output rather than accept it.
- **Project context**: CLAUDE.md provides project-level context that persists across sessions, making the interaction more relevant to the specific lab setup than a generic web chat.
- **File-level operations**: Claude Code can read, write, and modify files directly. This makes it a genuine coding assistant rather than a Q&A tool, which is appropriate for the research tasks in the lab.

---

## Content Design Decisions

### Why the Foundations Section Comes Before the Missions

Students arrive with widely varying backgrounds. A clinical PhD student may know nothing about PyTorch; a computational biology student may know nothing about BraTS sub-regions. The Foundations section provides a shared reference point that both groups can use — not as required reading, but as on-demand reference.

The sequence (clinical AI, medical imaging pipeline, MRI basics, brain tumour imaging, segmentation basics, reproducibility, ethics) is designed to move from motivation (why does medical AI matter?) to context (how does this specific imaging workflow work?) to methodology (what are the tools and their limitations?). Students with strong backgrounds in any area can skip those pages; students who are unfamiliar with the area will find what they need before starting the missions.

### Why the MRI Textbook Is Separate

The MRI Textbook section is more detailed and more technical than the Foundations section. It exists because MRI literacy is essential for interpreting brain tumour segmentation results, and the available resources (textbook chapters, Wikipedia) are either too shallow or too technical for a PhD student in life sciences or medicine.

The MRI Textbook is designed to be read in parallel with Missions 1 and 2, not before. Students who try to read it all before starting the lab will spend too long on it. The mission instructions point to specific MRI Textbook pages when the relevant concepts arise.

### Why the Prompt Library Is a Dedicated Section

The Prompt Library is a reference document, not a tutorial. Students should not read it start to finish — they should use it as a lookup tool when they are working on a specific mission and want examples of effective prompts for that type of task.

Making it a dedicated section (rather than embedding prompts in the mission pages) serves two purposes: it makes the prompts easier to find, and it emphasises that prompts are reusable, generalisable tools — not one-time recipes tied to a specific task. A student who learns the structure of a good error analysis prompt in Mission 3 should be able to adapt it for their own research.

---

## What the Site Intentionally Does Not Cover

The following topics were considered for inclusion and deliberately omitted:

**Detailed Python tutorials**: students in a PhD programme should have enough Python to follow the lab code. If they do not, the two-day format does not allow time to teach it. Students who need Python basics are pointed to external resources (Python for Scientists, Software Carpentry) and encouraged to complete them before the course.

**MRI physics derivations**: the MRI Textbook covers what each sequence shows clinically and what the preprocessing steps do — it does not derive the Bloch equations or explain spin echo physics mathematically. Radiologists do not need to understand the physics to read scans; researchers using MRI data do not need to understand the physics to use the data responsibly. Students who want the physics are pointed to standard references.

**A statistics course**: the course touches on statistical concepts (p-values in study design, confidence intervals in result reporting) but does not teach statistics. Students in PhD programmes have statistics training; this course applies it to a specific context.

**Deep learning theory**: the course uses a U-Net style model and describes what it does architecturally, but does not derive backpropagation, explain attention mechanisms, or cover neural architecture design. These topics are well covered in existing courses (fast.ai, Stanford CS231n, DeepMind's introductory lectures) and are not the focus of a course on medical AI methodology and research practice.
