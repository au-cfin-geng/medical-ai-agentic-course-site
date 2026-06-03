# Clinical Translation

## The Gap Between Research Performance and Clinical Deployment

A brain tumour segmentation model achieving Dice 0.88 on the BraTS test set is a meaningful research result. It does not mean the model is ready for clinical use. The gap between a research result and clinical deployment is wide, and the majority of medical AI systems that produce high-quality research publications never reach patients. Understanding why — and what closing that gap requires — is essential for anyone intending to build clinically impactful AI.

This page covers what clinical translation actually requires, how regulatory frameworks work, and what happens to AI systems after they are deployed.

---

## What Clinical Translation Actually Requires

Research performance (Dice score on a curated benchmark) is the first gate. Many systems fail before they even reach it. But passing the first gate opens a sequence of additional requirements that are largely independent of the model's technical performance:

### 1. Prospective Validation

Internal benchmark performance and even retrospective external validation are insufficient for clinical deployment. Prospective validation — testing the model on patients who are enrolled going forward, in the actual clinical environment — is required to demonstrate that the model works on freshly acquired data in the real workflow. Prospective validation often reveals operational failures that retrospective analyses miss: data format incompatibilities, DICOM tag inconsistencies, differences in contrast agent protocols, cases that fall outside the model's training distribution.

### 2. Regulatory Clearance

In most jurisdictions, an AI system used to inform clinical decisions is a medical device and requires regulatory clearance before clinical use. The two major regulatory frameworks are the FDA (United States) and CE marking under MDR (European Union).

### 3. Clinical Workflow Integration

Even a validated, cleared system fails to translate if it cannot be integrated into the clinical workflow. Radiologists and oncologists will not use a system that requires them to export DICOMs manually, run a Python script, wait 20 minutes, and manually import results. The system must appear in the radiologist's workstation, return results in minutes, and present output in a form that supports — not disrupts — clinical decision-making.

### 4. Health Technology Assessment

Payers (national health systems, insurance companies) increasingly require evidence of cost-effectiveness before reimbursement. A model that is technically superior to manual segmentation must also be demonstrated to reduce costs, improve throughput, or improve outcomes in a way that justifies the purchase price. This is a separate evidence threshold from regulatory clearance.

### 5. Clinician Training and Acceptance

Without a clinical champion — a radiologist or oncologist who believes in the technology, has tested it personally, and will advocate for adoption in clinical meetings — translation almost always fails. Training programmes must prepare clinicians to understand model outputs, recognise failure cases, and know when to override the AI.

---

## FDA Regulatory Pathways for AI/ML Medical Devices

In the United States, AI medical devices are regulated by the FDA under the device classification framework. Three primary pathways apply:

### 510(k) — Substantial Equivalence

The most common pathway for AI medical devices. The applicant demonstrates that their device is substantially equivalent to a legally marketed predicate device. "Substantial equivalence" means the new device has the same intended use and the same or different technological characteristics — and if different, those differences do not raise new safety or effectiveness questions.

For brain tumour segmentation software: if a predicate device exists that performs brain tumour segmentation (several do), a 510(k) submission compares your device to that predicate. You must demonstrate performance that is non-inferior to the predicate on a clinically relevant population.

**Timeline**: typically 6-12 months from submission to clearance.

### De Novo — Novel Low-to-Moderate Risk Devices

When there is no predicate device (your application is genuinely novel), the De Novo pathway creates a new regulatory category. The FDA reviews the device from first principles and establishes special controls (post-market requirements) appropriate for the novel risk profile.

**Timeline**: 12-24 months; longer than 510(k) because new regulatory precedent is being set.

### PMA — Pre-Market Approval for High-Risk Devices

Reserved for Class III (high-risk) devices where general controls and special controls are insufficient to assure safety and effectiveness. PMA requires clinical trial evidence — the most rigorous standard. Most AI imaging software is Class II (moderate risk) and uses 510(k) or De Novo. PMA would apply to, for example, an AI system that autonomously delivers a dose of radiation without clinician review.

**Timeline**: 2-5+ years; the most demanding pathway.

---

## CE Marking Under MDR in Europe

The European Union Medical Device Regulation (MDR, 2017/745), which replaced MDD and AIMDD and became fully applicable in May 2021, governs medical devices in EU member states.

AI/ML software used for diagnosis or treatment is typically classified as a Class IIa or Class IIb device under MDR, requiring a conformity assessment by a Notified Body — an independent organisation accredited to assess medical devices. Key requirements:

- Clinical evaluation demonstrating safety and performance
- Post-market clinical follow-up (PMCF) plan
- Technical documentation meeting MDR Annex II/III requirements
- Quality management system certified to ISO 13485
- EU Declaration of Conformity
- Registration in the EUDAMED database

MDR is substantially more demanding than the previous MDD framework, and many device manufacturers underestimated the transition requirements. For AI software, additional guidance from the MDCG (Medical Device Coordination Group) addresses the specific challenges of adaptive algorithms and software qualification.

---

## The Role of Clinical Champions

No medical AI system translates to clinical use without a clinical champion. This is not a soft observation — it is a consistent finding across translation case studies.

A clinical champion is typically a consultant radiologist, oncologist, or neurosurgeon who:
- Has reviewed the published evidence and believes the system can help their patients
- Has tested the system personally on real cases and found it clinically useful
- Is willing to present the evidence at departmental clinical governance meetings
- Will escalate issues with the system through the appropriate institutional channels

The clinical champion is not the same as a researcher who published the model. The champion is the practicing clinician who will use it. Engaging clinicians early in the development process — including them in error analysis, study design, and endpoint selection — is how you produce technology that clinicians find credible and useful.

---

## Post-Market Surveillance and Distribution Shift

Regulatory clearance is not the end of the process. Both FDA and MDR require **post-market surveillance** — ongoing monitoring of device performance after deployment. For AI systems, this is particularly important because of **distribution shift**: the statistical properties of the data the model encounters after deployment may differ from the training data.

### What Causes Distribution Shift in Brain Tumour AI

- **New scanner acquisition**: the hospital replaces a 1.5T scanner with a 3T scanner; image quality changes
- **Protocol changes**: the neuroradiology department updates their MRI protocol; sequence parameters differ
- **Demographic shift**: the hospital's patient population changes (e.g., due to a new referral pathway); age distribution or comorbidity profile changes
- **Epidemiological change**: treatment patterns change; more patients present post-treatment with treatment-related changes that differ from pre-treatment appearances

Distribution shift causes **silent performance degradation** — the model continues to generate outputs that look plausible but are less accurate than they were at the time of clearance. Without active monitoring, neither the AI vendor nor the clinical team may notice until a sentinel clinical event occurs.

### Monitoring Infrastructure

A deployed AI system requires:
- **Automated quality metrics**: flag cases where model confidence is unusually low (potential OOD cases)
- **Periodic reference standard comparison**: sample a fraction of cases for expert re-annotation; compute ongoing Dice against the deployed model
- **Audit trail**: record every case processed, the model version, the output, and any manual corrections
- **Drift detection**: statistical process control on model output distributions; alert if output statistics shift

The analogy from clinical biochemistry is useful: laboratory test results are monitored continuously against internal quality controls; a run that fails QC is flagged before results are released. AI system outputs require equivalent ongoing quality control.

---

## The Clinical Translation Hierarchy

| Stage | Question | Evidence Required |
|-------|----------|-------------------|
| Algorithm development | Does it work at all? | Internal validation, benchmark performance |
| External validation | Does it generalise? | Multi-site retrospective data |
| Prospective validation | Does it work in the real workflow? | Prospective observational study |
| Regulatory clearance | Is it safe enough for clinical use? | Regulatory submission (510k / De Novo / CE) |
| Health technology assessment | Is it cost-effective? | Economic modelling, budget impact analysis |
| Clinical deployment | Does it actually improve care? | Interventional study, post-market surveillance |

Each stage requires evidence from the previous stage. Jumping from algorithm development to clinical deployment — skipping external validation, prospective study, and regulatory clearance — is not unusual in clinical practice ("we just started using it") and represents a significant patient safety risk.

---

!!! note "Connect to Lab Mission"
    **Now do the lab — M6 (Translation Planning).**

    In Mission 6, you will assess your brain tumour segmentation model against the clinical translation hierarchy above. For each stage, write one paragraph answering: what evidence do you currently have, what evidence is missing, and what is the most important next step. Then draft a brief post-market surveillance plan: what would you monitor, at what frequency, and what threshold would trigger a review of the deployed model? Use Claude to help identify the most relevant FDA guidance documents for AI/ML-based software as a medical device (SaMD) — specifically the 2021 action plan on AI/ML-based SaMD. This final mission bridges the technical work of the course to the regulatory and clinical reality of deploying the systems you have built.
