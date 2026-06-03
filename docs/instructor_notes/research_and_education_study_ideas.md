!!! warning "Instructor Resource"
    This section is for instructors and teaching assistants. Students may read it, but it is not required course content.

# Research and Education Study Ideas

!!! warning "Important Disclaimer"
    This course is not currently a research study. No student data is being collected for research purposes. Any future research use of student activity data from this course would require full ethics committee review, institutional sign-off, written informed consent from all participants, and GDPR or applicable privacy compliance. The ideas below are speculative possibilities for future consideration, not a current research protocol.

---

## Why This Course Is an Interesting Research Context

This course sits at the intersection of three active research areas: medical AI education, human-computer interaction with AI coding tools, and the question of how domain expertise shapes the use of large language models in professional contexts.

PhD students in life sciences and medicine bring domain knowledge that few AI researchers have: they can evaluate whether a clinical claim is plausible, whether a failure mode matters clinically, and whether a study design is appropriate for the population it claims to address. Watching how this group learns to use agentic AI tools — and where they struggle — has the potential to generate insights that cannot be replicated with a general computer science student population.

The following research angles are presented as possibilities for future consideration. None of them are active. All of them would require ethical approval before any data collection.

---

## Future Research Angles

### 1. Prompt Iteration Patterns and Research Learning

**Research question**: How do students' prompts evolve across the 7 missions? Does prompt sophistication (measured by specificity, constraint use, output format specification, and context-setting) increase over the course of two days? Do researchers with more domain expertise write more specific prompts from the start?

**Why it is interesting**: Prompt quality in this course is a proxy for a cognitive skill — the ability to translate a research intention into a precise, reproducible specification. If this skill can be measured from prompt logs, and if it correlates with other measures of research quality (e.g., quality of Mission 3 error analysis or Mission 5 study design), it could become a useful metric for tracking AI literacy development in graduate research training.

**Methodological approach**: Prompt logs from consenting students could be coded using a rubric for specificity (context provided, output format specified, constraints named, scope limited), and analysed using mixed methods — quantitative coding combined with qualitative analysis of specific prompt sequences that show notable shifts in approach.

**Confound to anticipate**: Students who have prior programming experience may write more structured prompts from the start, not because they have more domain expertise but because structured input is a habit in software development. Domain expertise (clinical or biological) and computational experience would need to be treated as separate independent variables.

---

### 2. Dashboard Artifact Interaction and Scientific Reasoning

**Research question**: Does the frequency and depth of artifact inspection (opening failure case images, comparing before/after metrics, examining training curves) correlate with better Mission 5 study designs or Mission 6 assessments?

**Why it is interesting**: The dashboard was designed to make exploration easy and to make artifacts inspectable. If students who inspect their artifacts more thoroughly also produce better downstream reasoning, this would support the design hypothesis that making artifacts visible and accessible improves scientific reasoning. If there is no correlation, it would suggest that availability alone is not sufficient — guided reflection prompts may be needed.

**Methodological approach**: Dashboard interaction logs (clicks, time spent on each artifact, number of failure cases opened) would need to be collected with student consent. Mission 5 and 6 outputs would be rated by trained coders using a rubric for reasoning quality. Correlation analysis between interaction depth and reasoning quality would be the primary analysis; regression controlling for background variables would be secondary.

**Ethical consideration**: Students must not feel that their dashboard activity is being monitored in ways that affect their grade. Any interaction logging for research purposes must be decoupled from assessment completely.

---

### 3. Agentic Coding Adoption Trajectories

**Research question**: Do life science researchers adopt prompt-first workflows differently than computational researchers? What barriers do clinical PhD students encounter that computational students do not, and vice versa?

**Why it is interesting**: Current literature on AI coding assistant adoption focuses almost entirely on software developers. Life scientists and clinicians are a different population with different mental models of what "code" is, different prior experiences with automation, and different professional stakes in the outputs they produce. Understanding adoption trajectories in this population is relevant to research training programme design.

**Methodological approach**: Mixed methods — structured observation during lab time (coded for help-seeking behaviour, strategy switches, evidence of verification habits) combined with post-course semi-structured interviews with consenting participants. A pre/post survey of self-efficacy with AI coding tools (adapted from existing technology adoption scales) would provide a quantitative baseline.

**Sample size note**: A single cohort of 15-25 PhD students is enough for qualitative analysis but not for quantitative conclusions. A multi-cohort study — the same protocol run at multiple institutions — would be needed for generalisable quantitative findings.

---

### 4. AI Literacy Development

**Research question**: Does completing the 6 missions improve students' ability to critically evaluate clinical AI claims? Specifically, do students improve on a pre/post test of their ability to identify methodological flaws in clinical AI papers?

**Why it is interesting**: The course's Mission 6 is explicitly designed to develop the ability to evaluate AI tools critically — not just as users, but as researchers who can identify what validation evidence is needed and what claims are over-stated. If this learning is measurable on a standardised instrument, the course design could be adopted more broadly in graduate medical and life science programmes.

**Methodological approach**: Develop a pre/post assessment instrument consisting of 5-8 short abstracts from published clinical AI papers with embedded methodological flaws (e.g., no external validation, overfitting in small datasets, inappropriate comparison groups, implausible Dice scores). Score students on their ability to identify and articulate the flaws. Administer before the course opens and after Mission 6 closes. A comparison group — PhD students from the same institution who did not take the course — would strengthen the design.

**Instrument development note**: This instrument does not currently exist in a validated form for this population. Developing and validating it would itself be a publishable contribution to medical education research.

---

### 5. HCI and AI Education Angle

**Research question**: How does Claude's response style affect student mental models of AI capabilities and limitations? Do students who receive more detailed, step-by-step Claude responses develop more accurate mental models than students who receive more concise ones?

**Why it is interesting**: This course is a natural laboratory for studying how non-programmers learn to use agentic AI tools. Claude's response style (explanation-heavy versus action-heavy) can vary based on prompt design. If the educational context benefits from explanation-heavy responses even when they are slower, this has implications for how AI tools should be configured for educational versus professional use.

**Methodological approach**: This is the most technically demanding design, requiring either A/B testing with different system prompt configurations (complex to set up ethically and technically) or retrospective analysis of prompt-response pairs correlated with student outcomes. The simpler version: collect student responses to "what do you think Claude is doing when it runs your prompt?" before and after the course, coded for accuracy and sophistication. No A/B testing required.

---

## Data That Could Be Collected (Only With Approval and Consent)

The following data types are relevant to the research questions above. None may be collected without full ethics approval and individual written informed consent.

- **Claude Code session logs**: the full sequence of prompts and responses during each lab mission. These logs contain the most direct evidence of prompt iteration and adoption patterns, but they also contain student work product and potentially sensitive reasoning. De-identification is non-trivial because prompt content often contains identifying context.
- **Dashboard interaction logs**: timestamped records of which artifacts each student opened, how long they viewed them, and whether they navigated to failure cases specifically. Lower sensitivity than session logs; de-identification is more straightforward.
- **Prompt sequences and revision patterns**: extracted from session logs — specifically, instances where students revised or retried a prompt. This captures the iteration dynamic without the full text of every interaction.
- **Pre/post surveys**: self-reported AI self-efficacy, background in computation and clinical medicine, prior experience with large language models. Standard survey data; straightforward ethics process.
- **Reflection responses**: students' written responses to the reflection questions embedded in each mission. These are part of the course activity and should not be collected for research without explicit consent, even though they are submitted through the dashboard.
- **Optional interviews**: 30-45 minute semi-structured interviews with consenting students 4-6 weeks after the course, to assess retention and transfer of prompt-first thinking to their own research.

---

## Ethical Considerations

**Student privacy**: All data must be de-identified before analysis. De-identification of free-text data (prompts, reflections) is harder than de-identification of structured data (click logs, survey scores) and requires careful review.

**Voluntary participation**: Grades must not depend on research participation in any way. Students who decline to participate should experience the course identically to students who consent. This must be stated clearly in the consent process.

**Transparency**: Students must know, before the course begins, what data would be collected and why. Retroactive consent (asking for consent after the course ends) is ethically acceptable for some data types but requires careful justification.

**Data storage and retention**: Research data involving human participants requires a data management plan specifying where data is stored, who has access, how long it is retained, and how it is destroyed. This plan must be submitted as part of the ethics application.

**Institutional data governance**: Many universities have policies about student data that go beyond general research ethics requirements. Check with your institution's data protection officer before designing a study that involves any student activity logs.

---

## How to Set Up a Future Study

If you are interested in pursuing a research study using this course as a setting, the following steps apply:

1. **Consult your IRB or ethics committee early** — before you have committed to a design. In the US, this is typically the Institutional Review Board. In EU and UK institutions, it is the Research Ethics Committee or equivalent. Describe the general research area and the proposed data types, and ask for preliminary guidance. This conversation often identifies issues that would cause a full application to fail, and it is better to find them early.

2. **Develop a consent framework** that clearly separates research participation from course participation. This typically means a two-document approach: the course information sheet (which describes what the course involves and does not mention research) and a separate research information sheet and consent form (which describes the study, the data, and students' rights). Students receive both documents at enrollment but sign only the research consent form if they choose to participate.

3. **Consider a pilot study with a single cohort** before scaling. The research questions here are exploratory, and the measurement instruments (especially the prompt coding rubric and the AI literacy assessment) are not yet validated. A pilot study with 15-20 students would allow you to test the data collection procedures, refine the coding approach, and estimate effect sizes for a properly powered follow-up study.

4. **Identify relevant literature** to situate the work. Key bodies of literature include: medical AI education research (sparse), HCI research on AI coding assistants (growing rapidly since 2023), medical education research on clinical reasoning development, and learning analytics. A literature review scoped to these four areas would reveal the gaps this research could address.

5. **Consider a collaborative design** involving medical education researchers, HCI researchers, and clinical AI researchers. The research questions here span all three disciplines, and a single-discipline team will miss important aspects. Many funding bodies (Wellcome Trust, NIH, NIHR, DFG) have mechanisms for interdisciplinary education research.

---

## A Note on Priorities

This course was designed to be an excellent learning experience first. Research value is a secondary consideration. If pursuing a research study creates any tension with student experience — more burden on students, concern about monitoring, pressure to perform in observable ways — the student experience takes priority.

The most important outcome of running this course is that PhD students leave with a more sophisticated and critical understanding of medical AI than they arrived with, and with practical skills that improve their research. That outcome does not require a research study. Research would be a welcome addition, but it is not the goal.
