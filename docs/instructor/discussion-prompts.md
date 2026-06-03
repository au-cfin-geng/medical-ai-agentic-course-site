# Discussion Prompts

!!! warning "Instructor Resource"
    This page is for instructors and teaching assistants. It contains facilitation notes including descriptions of what good and poor student answers look like. Do not share with students before discussion sessions.

These discussion prompts are for use during mission debriefs and the closing showcase. Each mission has three questions. Use two or three per debrief — do not attempt all three unless time allows. Questions marked with (key) are the highest-leverage ones to prioritise if time is short.

---

## Preflight and Mission 0

**Q1 (key): What would have been different if you had not set up CLAUDE.md before your first task prompt?**

Facilitation note: A good answer describes a concrete failure — Claude asking about data location, repeating context that was already established, or producing output to a default path instead of the specified one. A poor answer ("I don't know" or "it would have been worse") suggests the student did not experience the context-setting first message as a meaningful design choice. If most answers are poor, do a brief live demo: send a cold-start prompt without CLAUDE.md and show what happens.

**Q2: What is the approval loop and why does it matter for research integrity?**

Facilitation note: A good answer names both components — Claude's proposed action and the researcher's explicit approval — and connects the approval step to research integrity: the researcher, not the AI, is responsible for every action taken. A poor answer treats the approval loop as a nuisance ("it slows things down"). If this comes up, engage with it directly: the approval loop is not a limitation of the tool; it is the mechanism that keeps you in control of your research.

**Q3: What is one thing in your CLAUDE.md that you would write differently now?**

Facilitation note: This is a metacognitive question with no single right answer. Good answers are specific: "I would add the label convention because Claude assumed label 3 existed when it doesn't in BraTS." Poor answers are generic: "I would make it more detailed." The goal is to establish CLAUDE.md as a living document, not a one-time setup task.

---

## Mission 1 — Data Inspection

**Q1 (key): What was the most surprising finding in your data summary, and how would you communicate it to a clinician?**

Facilitation note: A good answer names a specific finding (e.g., "case BraTS_002 has a whole tumour that is 8× larger than the median, which means any mean Dice across our three cases will be dominated by that one case") and attempts a clinical translation ("the tumours in this dataset vary enormously in size, which means a model that works for large tumours may not work at all for small ones"). A poor answer is either not specific ("the data had some anomalies") or does not attempt translation at all.

**Q2: What distributional properties of this dataset might cause problems if a model trained here were applied to a different hospital's data?**

Facilitation note: Good answers address scanner protocol, patient population selection, or annotation style. The best answers connect these to a specific failure mode: "If the contrast timing protocol differs, T1ce enhancement patterns will look different and the ET subregion prediction will degrade." Poor answers are generic ("different data might not work"). Push: what specifically is different, and why does that specific difference matter?

**Q3: How did your Inspector Role prompt differ from what you would have written without a role assignment? What did the role change about the output?**

Facilitation note: Good answers note that without the inspector role, Claude included code or proposed solutions; with the inspector role, it produced structured observations only. A poor answer ("I don't think the role changed anything") suggests the student may not have applied the role explicitly. This is a good moment to emphasise that role declarations are not just labelling — they constrain the output type, which is what makes the observation step genuinely separate from the analysis step.

---

## Mission 2 — Baseline Evaluation

**Q1 (key): What is your baseline whole tumour Dice, and is that better or worse than you expected? Why?**

Facilitation note: A good answer gives the number, compares it to the BraTS benchmark reference range on the cheatsheet, and provides a reason for the discrepancy ("lower than expected because our threshold was calibrated to the FLAIR modality only and case BraTS_003 has unusual FLAIR signal"). A poor answer is either no number ("we didn't finish") or a number with no interpretation. If a student says their Dice is 0.9, ask: "How many cases? What was the distribution?" A single-case Dice of 0.9 is not a result — it is a data point.

**Q2: Why is a simple threshold baseline sometimes competitive with more complex models on whole tumour Dice?**

Facilitation note: This is a conceptual question. The key insight is that WT is defined as all tumour tissue, and tumour tissue on FLAIR has a distinctive brightness that a threshold exploits well. Complexity helps most for ET and TC subregions where the signal is less distinct from background. A good answer names the reason (signal contrast, subregion difficulty); a poor answer guesses without reasoning ("maybe simple is better sometimes"). If the class is stuck, show the BraTS benchmark ranges: WT is where baselines are most competitive.

**Q3: How did you write your output contract? Did Claude produce the exact format you specified? What happened when it didn't?**

Facilitation note: This is a process question, not a results question. A good answer describes the output contract they wrote, whether it matched the template format, and how they handled a format mismatch (re-prompting with clarification, or using the self-verification step). A poor answer is "it worked fine" without being able to describe the contract structure. The goal is to establish the output contract as a reproducibility mechanism, not a formality.

---

## Mission 3 — Investigate Failure

**Q1 (key): What is the primary failure mode in your worst-performing case, and what is its clinical implication?**

Facilitation note: A good answer uses the failure mode taxonomy (undersegmentation, oversegmentation, boundary error, etc.), names the anatomical location, and connects it to a clinical consequence: "The model undersegments the tumour core in this case — it misses the necrotic centre. In a surgical planning context, that would lead to incomplete resection margins." A poor answer names the failure without clinical connection. If this happens, ask: "If a surgeon used this segmentation to plan a resection, what would happen?" The clinical consequence forces specificity.

**Q2: Did using Claude in the Skeptical Reviewer role feel different from using it in the Developer role? What was different about the output?**

Facilitation note: A good answer is specific: "In developer role it produced code immediately; in reviewer role it produced a ranked list of concerns without any solution proposals, which forced me to think about the solution myself before asking for implementation." A poor answer ("it felt the same") suggests the student may not have applied the role distinction. This is a good moment to emphasise that the discipline of not asking for solutions in the same prompt as critique is intentional — it prevents premature closure.

**Q3: Which failure mode you observed has the most serious clinical implication, and how would you prioritise fixing it?**

Facilitation note: This question has no single right answer, but good answers reason from clinical stakes: missing enhancing tumour may be more dangerous than oversegmenting oedema because ET underprediction affects treatment targeting, while oedema overprediction primarily affects reported tumour burden. A poor answer chooses the failure mode with the lowest Dice without reasoning about clinical impact. Encourage students to argue for their prioritisation rather than simply asserting it.

---

## Mission 4 — Improve With Intent

**Q1 (key): What was your hypothesis, what did you change, and was the hypothesis supported? If not, why not?**

Facilitation note: A good answer has three parts: a specific falsifiable prediction ("I expected specificity_wt to increase by at least 0.03"), a single implemented change, and an honest interpretation of the result ("the hypothesis was refuted — specificity increased by 0.01, below my threshold, and dice_wt dropped by 0.04 which I did not predict"). A poor answer changes multiple things at once, or reports a result without referencing the original hypothesis. If a student says "I changed a few things and it got better," ask: "Which change caused the improvement?" If they cannot answer, that is the teaching moment.

**Q2: How do you know the improvement you observed (if any) is real and not due to chance or the specific cases you tested on?**

Facilitation note: This question surfaces statistical reasoning. A good answer acknowledges the limitation (three cases is not a statistically robust sample) and proposes what would be needed to know (more cases, confidence intervals, paired comparison). A poor answer treats the three-case result as definitive. The goal is not to make students feel bad about their result — it is to establish the distinction between a promising signal and a validated finding.

**Q3: What would you need to show a clinical colleague to convince them that your improvement matters?**

Facilitation note: A good answer moves beyond Dice: "I would need to show a case where the improved model correctly delineates a tumour boundary that the baseline missed, and explain what clinical decision would have been different." A poor answer stays at the metric level ("I would show them my Dice score"). The gap between these two answers is the gap between a number and evidence.

---

## Mission 5 — Design the Next Study

**Q1 (key): What patient population did you specify, and what populations did you explicitly exclude? What is the clinical implication of those exclusions?**

Facilitation note: A good answer is specific: "We included adults ≥18 years with histologically confirmed high-grade glioma (WHO grade III-IV), MRI acquired within 2 weeks of surgery. We excluded paediatric cases, low-grade gliomas, and patients with prior surgery — these are common exclusions in BraTS-style studies but they mean our model has no evidence base for those populations." A poor answer is generic ("we would include patients with brain tumours"). The exclusion list is as important as the inclusion list because it defines where claims cannot be made.

**Q2: What is your reference standard, and how does it compare to what was used in your Mission 2–4 evaluations?**

Facilitation note: A good answer names the reference standard (expert multi-rater annotation, consensus label, pathological ground truth) and acknowledges the gap: the BraTS labels are expert annotations, not ground truth — inter-rater variability means even perfect performance against BraTS labels might not translate to perfect pathological accuracy. A poor answer treats the training labels as objective truth.

**Q3: What role did the Skeptical Reviewer prompting play in your study design? What weakness did it surface that you had not noticed yourself?**

Facilitation note: This is a metacognitive process question. A good answer names a specific weakness the reviewer role surfaced: "It pointed out that our planned sample size had no statistical power justification — we said 30 patients without explaining why." A poor answer ("it didn't surface anything new") may indicate the student did not apply the role in this mission. If so: ask them to apply it now, live, to their study design.

---

## Mission 6 — Translate Responsibly

**Q1 (key): What additional evidence would your system need before deployment in a real clinical setting?**

Facilitation note: A good answer is specific and stratified: external validation at ≥2 independent centres; prospective evaluation showing that clinical decisions made with the AI are not inferior to decisions made without it; regulatory clearance under the applicable pathway; defined retraining protocol for distribution shift. A poor answer is generic ("more testing"). If the answer is generic, ask: "Testing on what? Measured how? Compared to what baseline?"

**Q2: How did writing the honesty constraints change the tone of your translation brief? What language did you have to remove or rephrase?**

Facilitation note: A good answer names specific language that was changed: "Claude originally wrote 'our system demonstrates clinical-grade performance' and I replaced it with 'our system achieves a whole-tumour Dice of 0.81 on a 3-case internal test set, which is within the acceptable range of the BraTS benchmark but has not been validated externally.'" A poor answer ("the honesty constraints made it more cautious") does not name specific changes. Ask for an example.

**Q3: What regulatory pathway would apply to your system, and what would that pathway require?**

Facilitation note: This question has a factual component. For a brain tumour segmentation system used in treatment planning, the most likely US pathway is FDA 510(k) clearance as a Class II medical device, requiring substantial equivalence to a predicate device; or De Novo classification if no predicate exists. EU would require CE marking under MDR. A good answer names a pathway and at least one requirement. A poor answer is "I'm not sure" without an attempt to reason through it. Encourage reasoning: "What makes this system high-risk? What makes it lower-risk? Which pathway follows from that?"

---

## End-of-Course Discussion

**Closing question 1: What is the most important thing you learned about agentic research that you did not expect?**

Facilitation note: Good answers are specific and often personal: "I didn't expect that the role assignments would change the output so dramatically — I thought they were mostly cosmetic." Collect answers on the whiteboard. Look for emergent patterns: if many students say they were surprised by how much CLAUDE.md mattered, the next cohort should spend more time on Mission 0.

**Closing question 2: What would need to be true for you to use these methods in your own doctoral research?**

Facilitation note: This question is intentionally open-ended and practically oriented. Good answers identify specific barriers (compute access, data availability, institutional approval) and specific opportunities (automating literature review, structuring failure analysis for ongoing experiments). Poor answers are either completely optimistic ("I'll start tomorrow") or dismissive ("this doesn't apply to my field"). Both extremes are worth engaging with.

**Closing question 3: If you were advising a clinical collaborator who wanted to deploy an AI segmentation system today — not yours, a commercial one — what three questions would you ask first?**

Facilitation note: The three questions from the Clinical AI One-Page Reference are one good answer, but any three well-reasoned questions work. What matters is that students have internalised the principle that performance claims require interrogation. A student who asks "what is your Dice score?" and nothing else has not yet internalised this. A student who asks "on which population, compared to what baseline, validated at how many external centres?" has.
