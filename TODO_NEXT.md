# Site Improvement Roadmap

This document tracks improvements to the Medical AI and Agentic Coding Lab course site. Items are organised by category and roughly prioritised within each category. Items near the top of each list are higher impact or lower effort.

Update this document after each course run. Add items discovered during delivery, remove items that have been completed, and reprioritise based on student feedback.

---

## Content Improvements

### High Priority

- **Add a dedicated page on BraTS 2021 dataset structure** (`docs/foundations/brats_2021_dataset.md`). Currently, BraTS-specific details are scattered across the MRI Textbook and Mission 1 pages. A single reference page with the exact directory structure, file naming conventions, label value definitions (0=background, 1=necrosis, 2=edema, 4=enhancing tumour), voxel spacing, and number of training subjects would reduce confusion significantly. Link to this page from Mission 1 and from the MRI Textbook's Labels page.

- **Add a sample completed error analysis** to Mission 3 or to the Error Analysis Workflow page. Students often do not know what "enough" error analysis looks like. A worked example — showing the full arc from metrics to failure cases to hypothesis — would calibrate expectations. The example should use fabricated but realistic BraTS results so students cannot copy it directly.

- **Add a sample completed study design** to Mission 5 or to the Study Design Workflow page. The study design mission has the highest variability in output quality. A worked example of a prospective multi-site validation study for brain tumour segmentation would demonstrate what a complete study design looks like at PhD level.

- **Expand the Glossary** with terms that students repeatedly ask about. Priority additions based on experience: confounding variable, out-of-distribution, prospective study, retrospective study, ground truth, inter-rater variability, sensitivity analysis, external validation, regulatory clearance, CE marking, FDA 510(k), health technology assessment.

### Medium Priority

- **Add a "Common Mistakes" section to each Mission page.** Three to five specific, concrete mistakes that students frequently make in that mission, with explanations of why they happen and how to avoid them. These can be drawn from the Where Students Get Stuck instructor notes but written for a student audience.

- **Add a BraTS data statistics table** to the Data Inspection Workflow page: number of subjects, tumour size distribution, sub-region co-occurrence statistics, proportion of cases with each sub-region. This gives students a reference for whether their data loading is correct.

- **Add a section on random seeds and reproducibility** to the Reproducibility Foundations page. Currently, this page covers the concept of reproducibility but does not address the specific challenge of random seed management in PyTorch, which affects whether students can reproduce their own results when they restart training.

- **Add cross-links between the Prompt Library and Mission pages.** Currently, students must navigate separately to the Prompt Library. Adding "relevant prompts" callout boxes at the start of each mission step (with links to the specific Prompt Library section) would reduce friction.

- **Expand the Roles for Claude page** to include two additional roles: Summariser (synthesising large outputs into a structured summary) and Devil's Advocate (identifying the strongest counterargument to a proposed approach). Both are useful in Missions 5 and 6 but are not currently described.

### Lower Priority

- **Add an annotated bibliography page** linking key claims in the Foundations section to primary literature. Priority papers to include: BraTS challenge papers (Menze 2015, Bakas 2018, 2021), landmark segmentation papers (U-Net, nnU-Net), papers on AI in clinical practice (Topol 2019), and one or two papers on the gap between research performance and clinical readiness (Zech 2018 on dataset shift is particularly relevant).

- **Add a "What to Read Next" section** to each major section, pointing to accessible papers, textbooks, or online courses for students who want to go deeper on a specific topic.

- **Add a "Running the Course Offline" guide** for instructors who want to run the course without internet access (conference settings, institutions with restricted networks). This requires documenting how to pre-download Claude models, how to cache the site locally, and how to distribute the lab repo without GitHub Classroom.

---

## Interactive Features to Add

- **Quiz questions embedded in Foundations pages.** Short (3-5 question) comprehension checks using MkDocs Material's `pymdownx.details` (collapsible answer reveal). Priority pages: MRI Basics, Segmentation Basics, Metrics (Dice, Sensitivity, Specificity). These do not require any backend — they are static reveal elements.

- **Interactive Mermaid diagrams** on the Lab Alignment page and the Two-Day Schedule page. The flowcharts on these pages are static images or text descriptions; converting them to rendered Mermaid (already supported by the site's mkdocs.yml configuration) would make them more readable and easier to update.

- **Embedded Jupyter notebook previews** via nbviewer for the data inspection and visualisation steps. Students who are not comfortable with the terminal can preview expected outputs before running code themselves. The nbviewer embed approach does not require nbconvert or a backend server — it uses a public iframe.

- **Progress tracking** — a simple client-side checklist (using JavaScript, no backend required) that lets students mark missions as complete and track their artifact status. This does not require server-side state — it can use localStorage. Useful for students who work across multiple days or return to the site outside course hours.

- **Collapsible hint system** in each Mission page. Currently, hints are embedded in the mission text and visible to all students. A collapsible system (e.g., "Stuck? Click to see a hint") would allow students to attempt the step first before reading the hint, which is better pedagogy.

---

## Video and Media to Create

- **Walkthrough video for Mission 0** (10-12 minutes): screen recording of opening Claude Code, the contrast between a vague and specific prompt, and the CLAUDE.md file walkthrough. This would allow students to preview the experience before the course and would be useful for students who miss Day 1 morning.

- **MRI anatomy tour** (8-10 minutes): a narrated walkthrough of a BraTS case in an open-source viewer (3D Slicer or ITK-SNAP), showing FLAIR, T1, T1ce, and T2 in the same case, pointing out the tumour regions visible in each modality, and showing how the label overlay aligns with the visual anatomy. This is the single most-requested piece of content from clinical students.

- **"What Dice means visually" animation** (3-4 minutes): an animation showing two overlapping shapes and computing the Dice coefficient step by step, with examples at various Dice values and an illustration of why small structures get lower Dice scores for the same absolute boundary error.

- **Showcase examples from a pilot run** (if available): 2-3 short clips (3-5 minutes each) of student groups presenting their dashboard walkthrough from a previous cohort. This gives future students a concrete expectation for what the showcase looks like and helps calibrate the standard.

- **Mission 3 failure case gallery** (no narration needed): a collection of 10-15 annotated static images showing common failure modes with labels explaining what the failure is and what might cause it. These could be hosted as a simple image gallery page or embedded in the Error Analysis Workflow page.

---

## Student Feedback Integration

- **Add a post-course survey link** to the home page and to Mission 6. The survey should cover: which missions were most valuable, which parts of the site were hardest to navigate, what prerequisite knowledge students wished they had had, and one open question ("what would you change about this course?"). Use a simple form tool (Google Forms, Typeform) and review responses before each future run.

- **Create a feedback mechanism for specific pages.** MkDocs Material supports a page feedback widget ("Was this page helpful?") that can be configured to send responses to a Google Form or similar. Enable this on the Mission pages first, where feedback is most actionable.

- **Run a prompt log review** after each cohort. Ask consenting students to share their prompt logs from one mission. Analyse: which prompt patterns led to better results? Where did students get stuck in their prompting and how did they recover? Use findings to improve the Prompt Library and mission guidance.

- **Document instructor observations** after each run. The Where Students Get Stuck instructor notes page should be updated after each cohort with new patterns observed. Add a "Version history" section at the bottom of that page indicating which cohort added which observation.

---

## Accessibility

- **Add alt text for all images.** Currently, several images in the Foundations and MRI Textbook sections use generic or missing alt text. Screen reader users cannot access this content. Priority: all images on mission pages and cheat sheets.

- **Check colour contrast for all custom CSS.** The `docs/assets/stylesheets/extra.css` file overrides some default Material theme colours. Run all custom colour combinations through the WCAG AA contrast checker (contrast ratio 4.5:1 for normal text, 3:1 for large text). Fix any failures.

- **Add keyboard navigation testing.** Verify that all interactive elements (collapsible sections, tabs, admonitions) are accessible via keyboard (Tab, Enter, Space). Test with VoiceOver (macOS) or NVDA (Windows).

- **Ensure Mermaid diagrams have text alternatives.** Rendered Mermaid diagrams are SVGs and may not be accessible to screen readers. Add a plain text description of each diagram's content immediately after the Mermaid block.

- **Review heading hierarchy.** All pages should use h1 for the page title, h2 for major sections, h3 for subsections. Skipped heading levels (e.g., h1 to h3) break screen reader navigation. Audit all pages with an automated tool (axe browser extension or pa11y CLI).

---

## Mobile Optimisation

- **Test print stylesheet for all handout pages.** The cheat sheet pages (`docs/handouts/`) are intended to be printed. The current MkDocs Material theme has a basic print stylesheet but navigation elements and sidebar may print unnecessarily. Add a `@media print` CSS block to hide navigation, sidebar, and the header when printing these pages.

- **Check table rendering on narrow screens.** Several pages (especially CONTENT_MAP.md and LAB_ALIGNMENT_SUMMARY.md) contain wide tables that will overflow on mobile screens. Options: convert to scrollable tables using a CSS wrapper, convert to definition lists for mobile, or add a note that these are designed for desktop viewing.

- **Test code blocks on iOS Safari.** Long code blocks do not scroll horizontally on some iOS browsers. Verify that the `content.code.copy` Material feature works correctly on mobile and that horizontal scrolling is enabled for code blocks.

- **Reduce page load time for the MRI anatomy pages.** If annotated image files are added (see Media section above), compress them to web-appropriate sizes. MRI images converted from NIfTI to PNG or JPEG should target under 200KB per image for acceptable mobile load times on 4G connections.

---

## Multilingual Possibilities

- **Assess demand before committing to translation.** Key question: will this course be run at institutions where the primary research language is not English? If yes, which languages are highest priority? German, French, and Spanish cover most European medical research contexts; Mandarin and Japanese cover significant Asia-Pacific PhD student populations.

- **If translating, prioritise the Mission pages and Cheat Sheets.** These are the pages students interact with most intensively during the course. The Instructor Notes and Blueprint files can remain English-only. MkDocs Material supports multi-language sites with the `i18n` plugin.

- **Consider a "key terms in multiple languages" section in the Glossary** as a low-effort first step. Adding the French, German, and Spanish equivalents of key terms (segmentation, voxel, sensitivity, specificity, ground truth) would help students who are reading medical AI literature in other languages.

---

## Assessment Rubrics

- **Formalise rubrics for each mission artifact.** Currently, what "good" looks like is described in the instructor notes but not made available to students. Converting the showcase judging criteria (Quality of Error Analysis, Strength of Hypothesis, Honest Gap Assessment, Prompt Quality) into a student-facing rubric would let students self-assess before the showcase.

- **Add a "self-check" question list to each Mission page.** Three to five questions students should be able to answer about their artifact before moving to the next mission. Example for Mission 2: "Can you describe your training split? Can you explain why your Dice score is at the level it is? Can you show me the training and validation loss curves?" These are assessment rubrics in the form of self-reflection prompts.

- **Create a capstone rubric for Mission 6.** Mission 6 is the most complex and the one most likely to be the basis for post-course feedback. A detailed rubric for the Translation Document — covering readiness checklist quality, gap analysis specificity, and realism of recommended next steps — would help instructors give consistent feedback and help students understand what is expected.

---

## Connection to Specific Papers

- **Annotated bibliography linking tutorial claims to primary literature.** Priority papers to annotate:
  - Menze et al. (2015) — BraTS challenge original paper: context for the dataset
  - Bakas et al. (2018) — BraTS segmentation labels: authoritative source for label definitions
  - Ronneberger et al. (2015) — U-Net: architectural context for the model used in the lab
  - Isensee et al. (2021) — nnU-Net: best-practice baseline for medical image segmentation
  - Zech et al. (2018) — dataset shift in chest X-ray AI: exemplar of generalisation failure
  - Topol (2019) — "High-performance medicine": accessible overview of clinical AI opportunities and limitations
  - Kelly et al. (2019) — Key challenges for delivering clinical impact from AI in medical imaging: practical gap analysis framework

---

## Community Contribution Guide

- **Write a contribution guide** (`CONTRIBUTING.md`) explaining how other instructors can: (1) report issues with existing content; (2) suggest improvements via GitHub Issues; (3) submit improvements via pull requests; (4) propose new pages or sections.

- **Define a style guide** for course content. All pages should follow consistent conventions for: heading levels, admonition types (note/tip/warning/danger), code block language tags, terminology (use "student" not "learner"; use "mission" not "lab" or "exercise"; use "Claude Code" not "Claude" when referring to the CLI tool).

- **Create a template for new Mission pages** and a template for new Prompt Library entries. Consistent structure reduces the time needed to add new content and makes the site easier to navigate as it grows.

- **Establish a versioning policy.** When the course is run at a new institution with significantly different student backgrounds or time constraints, consider whether the changes warrant a new version branch (e.g., `v2-condensed-1day`) rather than modifying the main site. This allows different institutions to customise without losing the original design.

- **Consider a GitHub Discussions board** for instructors running the course at different institutions to share experiences, effective prompts, and student feedback patterns.
