# Mission 6 — Translate Responsibly

This is the final mission. Its question is not "how good is our model?" It is "should this model be used in clinical practice?" Most research models should not be — not yet. Honest assessment is the most valuable contribution this mission can make to the field.

---

## Scientific Purpose

The path from a research model that achieves competitive benchmark performance to a clinically deployed medical device is long, expensive, and requires evidence that most research publications do not provide. Regulatory bodies require demonstrable safety and effectiveness in the intended use population. Hospitals require integration with clinical workflows, liability frameworks, and staff training. Clinicians require interpretable outputs that fit into their decision-making process. Patients require protection from harms they cannot assess themselves. This mission asks you to apply all of the scientific and clinical reasoning you have developed over the course to the most important question in clinical AI: is this model ready, and if not, what is specifically missing? Honesty here is not pessimism — it is the highest scientific standard.

---

## Required Background Reading

Before starting this mission, read the following pages on this site:

- [Clinical Translation](../medical_ai_workflow/clinical_translation.md) — understand the full translation pathway from research to deployment
- [Ethics, Privacy and Safety](../foundations/ethics_privacy_and_safety.md) — understand the ethical and governance framework for clinical AI
- [Clinical AI](../foundations/clinical_ai.md) — understand what regulatory clearance means and what it does not mean
- [Study Design](../medical_ai_workflow/study_design.md) — understand what the evidence base for translation must look like

---

## What You Will Ask Claude to Build

Your goal is to produce a clinical translation readiness assessment for the model you developed in this course. This is a structured critical evaluation — not a sales pitch and not pure pessimism, but an honest evidence-based assessment of where the model stands relative to the requirements for clinical deployment.

The assessment should cover: a summary of the model's demonstrated performance and the specific population and task for which it has been validated; the gaps between current validation and what would be required for regulatory clearance (consider: data diversity, external validation, prospective evaluation, safety analysis); a description of the appropriate regulatory pathway — in your jurisdiction, what class of medical device is this? what pre-market pathway would apply?; a stakeholder map identifying all parties involved in deployment (not just the research team) and their interests and concerns; a description of the deployment workflow — at what point in the clinical pathway would the AI output appear? who would see it? what action would they take based on it? what happens if the AI output is wrong?; a post-deployment monitoring plan including what metrics would be tracked, how often, and what would trigger a model update or withdrawal; and a final recommendation with explicit evidence-based justification.

Ask Claude to take a sceptical, regulatory-reviewer posture when drafting this document. Challenge any claim that is not directly supported by the Mission 2-4 results.

---

## Expected Artifacts

| Filename | Contents | What Correct Looks Like |
|---|---|---|
| `results/translation/readiness_assessment.md` | Full structured readiness assessment | All sections above are present; limitations are stated explicitly; the final recommendation is specific and evidence-referenced |
| `results/translation/stakeholder_map.md` or `stakeholder_map_diagram` | Stakeholder map in table or Mermaid diagram format | Includes radiologists, neuro-oncologists, patients, hospital informatics, regulatory bodies, and payers — not just the research team |
| `results/translation/deployment_workflow.md` | Narrative or flowchart describing the clinical workflow | Describes where the AI output appears in the workflow, who acts on it, and what the fallback is if the AI fails |
| `results/translation/monitoring_plan.md` | Post-deployment monitoring specification | Names specific metrics, monitoring frequency, and explicit criteria for escalation or model withdrawal |

---

## How to Inspect Results

**The limitations section.** This is the most important part of the document. Does it accurately describe the constraints of BraTS-only training? Does it acknowledge the population the model has NOT been tested on (paediatric patients, low-grade gliomas, different scanner vendors, non-English-speaking populations with different baseline care standards)? If the limitations section is short, the assessment is probably incomplete.

**The regulatory pathway section.** Does it name a specific class and pathway (e.g., FDA 510(k) for a Class II device, or CE marking under the EU MDR as a Class IIa device)? Does it acknowledge that regulatory clearance requires clinical evidence beyond BraTS performance? If it says "the model would be approved as a Class I device," that is almost certainly wrong for a diagnostic AI tool used in treatment planning — push back.

**The stakeholder map.** Count the stakeholders. A complete map for a hospital-deployed AI tool should include at minimum: radiologists (who review the output), neuro-oncologists (who use it for treatment planning), patients (who are affected by the output), hospital informatics teams (who must integrate it into the PACS/EHR), hospital legal and compliance teams, the regulatory body in the relevant jurisdiction, and insurance payers (who may not reimburse AI-assisted procedures). If the map has only 2-3 nodes, it is incomplete.

**The deployment workflow.** Can you trace the path from "a new patient MRI arrives" to "a clinical decision is made"? Is the AI output shown as a suggestion or as a final determination? Is there a human in the loop, and where? What is the workflow if the AI crashes or produces an implausible output?

**The final recommendation.** Is it specific? "Needs more work" is not a recommendation. "Not ready for deployment: requires external validation on multi-centre data with confirmed scanner heterogeneity and a prospective pilot study demonstrating non-inferiority to expert radiologist segmentation on at least 200 cases" is a recommendation.

---

## Prompt Principle

**The Devil's Advocate role: ask Claude to argue against you.**

After months of working on a model, researchers develop optimism bias. The technical community calls this "p-hacking"; the clinical community calls it "enthusiastic reporting." One of the most effective prompting strategies for critical evaluation is to explicitly ask Claude to argue against your conclusions — to find the strongest objections, not the best defences.

!!! failure "Confirmation-seeking prompt"
    ```
    Help me write an assessment of our model's readiness for clinical deployment.
    We achieved Dice 0.85, which is competitive.
    ```
    Claude produces a balanced-seeming document that is actually optimistic, because you framed it as a success that needs to be written up.

!!! success "Devil's advocate prompt"
    ```
    Act as a sceptical regulatory reviewer at the FDA reviewing our application for 510(k)
    clearance for a brain tumour segmentation AI.

    Our model achieves mean Dice 0.85 on the BraTS 2020 validation set.

    Your job is to identify the strongest arguments AGAINST clearance.
    Do not be encouraging. Do not acknowledge the positive results unless they are directly
    relevant to a specific regulatory standard.

    Specifically:
    1. What additional clinical evidence would you require?
    2. What patient populations has this model NOT been tested on?
    3. What failure modes would concern you from a patient safety perspective?
    4. What is missing from a post-market surveillance perspective?

    After you have listed the regulatory objections, help me draft a readiness assessment that
    honestly acknowledges these gaps.
    Save the assessment to results/translation/readiness_assessment.md.
    ```

The principle: **adversarial role + explicit negation + structured objections before drafting.** The document you produce will be more honest and more useful than one drafted under optimism bias.

---

## Reflection Questions

1. You produced a final recommendation. If your recommendation is "not yet ready for deployment," what would need to be true for you to change that recommendation? Be specific — name the evidence, the thresholds, and the study design that would change your answer.

2. The deployment workflow you described assumes a specific clinical setting (e.g., a large academic medical centre with a neuroradiology department). How would the workflow differ at a community hospital without a dedicated neuroradiology team? Does the risk profile change?

3. You identified post-deployment monitoring metrics. Who is responsible for collecting them? In a real deployment, this is often not specified in the research paper — it falls to the hospital informatics team or the AI vendor. What happens when a model's performance degrades on new patient data and no one is monitoring it?

4. One of your stakeholders is the patient. At what point in the workflow does the patient's data enter the AI system? Does the patient know? Should they? What is the ethical framework for answering this question in your jurisdiction?

5. A startup company offers to commercialise your model. They want to deploy it in 50 hospitals in 12 countries over the next 18 months, starting with a soft launch (no formal regulatory clearance). What are your scientific obligations as the researcher who developed the model? What would you require before agreeing to this arrangement?

---

## Optional Challenge

Produce a one-page "Model Card" for your segmentation model following the format proposed by Mitchell et al. (2019). A Model Card is a brief structured document describing: intended use, out-of-scope uses, performance across demographic groups, evaluation data, training data, and ethical considerations. Model Cards are increasingly required by journals, regulators, and hospital procurement processes. This is a transferable skill for any AI system you build after this course.

---

## Common Failure Modes

**The assessment is too optimistic.** BraTS performance does not generalise to clinical practice. A model that achieves Dice 0.88 on a benchmark has not been shown to be safe or effective in a hospital. If your assessment says the model is "ready for clinical trials" based solely on BraTS performance, it is not scientifically defensible. Ask Claude to explicitly identify what is missing.

**The regulatory pathway is described incorrectly or not at all.** Many students write "we would submit to the FDA" without specifying the device class, the pathway, or the type of evidence required. The FDA's AI/ML action plan and the EU MDR Article 22 are specific regulatory frameworks — the assessment should engage with at least one of them at the level of device class and evidence standard.

**Stakeholders only include the research team and clinicians.** Missing stakeholders in clinical AI include: hospital legal teams (liability), insurance payers (reimbursement), patients and patient advocacy groups (consent and trust), informatics and IT teams (integration), and the regulatory body itself. A deployment that succeeds clinically but fails on reimbursement or IT integration will not reach patients.

**The deployment workflow stops at "the radiologist sees the output."** What does the radiologist do with it? Do they act on it directly? Do they always review the underlying images? What training do they receive? What happens if the AI is confidently wrong? A complete workflow traces all the way from input data to clinical action and back to patient outcome.

**No mention of post-market surveillance.** Regulatory bodies increasingly require active monitoring of AI system performance after deployment. If your monitoring plan says "we will review the model annually," that is inadequate — the plan should specify what triggers an out-of-cycle review (e.g., a cluster of cases with unexpectedly low confidence scores, a change in scanner vendor, a new chemotherapy protocol that changes tumour appearance on MRI).

---

## Expected Learning Outcome

After completing this mission you can: produce a structured clinical translation readiness assessment that honestly identifies gaps between research performance and clinical deployment requirements; describe the components of a regulatory submission for a diagnostic AI device; map clinical stakeholders for a hospital AI deployment including parties beyond the research team; articulate a post-deployment monitoring plan with specific metrics and escalation criteria; use Claude in a devil's advocate mode to produce more honest and scientifically rigorous assessments; explain why responsible translation is a scientific obligation, not optional caution.
