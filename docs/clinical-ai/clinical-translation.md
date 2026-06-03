# Clinical Translation

## The Gap Between Research and Deployment

Building a model that achieves Dice 0.87 on a BraTS validation set is a technical achievement. Deploying that model in a clinical workflow where its outputs influence treatment decisions for real patients is a categorically different undertaking — one that requires external validation, prospective clinical study, regulatory review, workflow integration, and post-market surveillance. Most research models never make this transition, and for good reason: the requirements are demanding and expensive, and many models fail during prospective validation in ways that were not apparent from retrospective performance.

Understanding this gap is not discouraging — it is essential. Honest communication about where a model sits on the readiness spectrum is a professional obligation. Overclaiming readiness has caused patient harm when systems deployed prematurely produced errors that clinicians were not equipped to catch.

## The Clinical Readiness Spectrum

Clinical AI tools exist on a spectrum from early research to deployed product. Each level has specific requirements:

**Level 1: Research prototype**
A working implementation on a controlled dataset. Internal validation only, no generalisability claims. This is where you will be at the end of this course. Appropriate claim: "This system achieves X on BraTS data under the specific conditions of this training and evaluation pipeline."

**Level 2: Research-grade tool**
Sufficient internal validation to support research use by collaborating scientists. The code is documented, reproducible, and tested. Not for patient-facing use. Appropriate for inclusion in a research paper with appropriate caveats.

**Level 3: Investigational clinical tool**
The system has been externally validated on data from at least one site other than the training site, demonstrating some generalisability. It can be used in a research clinical context under Institutional Review Board (IRB) oversight, with explicit consent and without influencing care decisions. This requires the full preprocessing pipeline, not just the model.

**Level 4: Clinical validation underway**
A prospective clinical study is running. The system's outputs are being compared to standard clinical practice (not just retrospective annotations), and clinical outcomes (not just segmentation metrics) are being tracked. Failure modes are being characterised in the prospective population.

**Level 5: Regulatory submission ready**
Evidence package assembled for regulatory submission. This requires: comprehensive clinical validation data from multiple sites, detailed risk analysis, post-market surveillance plan, substantial equivalence argument (for 510(k)) or clinical benefit demonstration (for De Novo or PMA).

**Level 6: Deployed clinical tool**
FDA cleared (USA) or CE marked (EU) and integrated into clinical workflow with post-market surveillance active.

## FDA Regulatory Pathways

Medical AI software in the USA is regulated as Software as a Medical Device (SaMD) by the FDA's Center for Devices and Radiological Health (CDRH). Three primary pathways apply:

**510(k) — Substantial Equivalence**: The applicant demonstrates that the new device is substantially equivalent in intended use and technological characteristics to a legally marketed predicate device. This is the most common pathway for AI medical devices with an existing comparable cleared device. It does not require clinical trial data in most cases but does require performance data demonstrating equivalence.

**De Novo**: For novel device types with no predicate. The applicant demonstrates reasonable assurance of safety and effectiveness. IDx-DR (autonomous diabetic retinopathy screening) used this pathway in 2018 as the first autonomous AI diagnostic device cleared in the USA. Successful De Novo submissions establish a new device classification that can then serve as a predicate for future 510(k) submissions.

**PMA (Premarket Approval)**: Required for Class III devices (highest risk). Requires valid scientific evidence from clinical investigations demonstrating reasonable assurance of safety and effectiveness. Analogous to the FDA drug approval process. Rare for current AI imaging tools but potentially required for systems making fully autonomous high-stakes decisions.

## CE Marking in Europe

In the European Union, medical devices are regulated under the Medical Device Regulation (MDR, EU 2017/745). AI SaMD is typically classified as Class IIa or IIb under MDR, requiring conformity assessment by a Notified Body. CE marking requires a clinical evaluation demonstrating clinical benefit, a post-market clinical follow-up plan, and ongoing vigilance reporting. Unlike FDA clearance, CE marking covers the entire EU/EEA market.

## Why Dice 0.87 Does Not Mean Clinical Readiness

Even a model with excellent BraTS performance requires substantial additional work before clinical deployment:

**External validation**: Performance on the training institution's data does not predict performance at other sites. External validation on prospectively collected data from at least two independent sites is necessary to claim generalisability.

**Prospective validation**: Retrospective validation on historical data does not capture clinical workflow interactions, real-time performance under operational conditions, or the effect of the system on clinical decision-making.

**Workflow integration**: A segmentation output must be integrated into the PACS or treatment planning system in a form clinicians can actually use. This requires DICOM-RT or similar structured output formats, user interface design, and training for clinical users.

**Failure mode characterisation**: Clinicians using the system must understand when it is likely to fail and what types of errors to expect. This requires systematic failure characterisation beyond aggregate metrics.

**Post-market surveillance**: Once deployed, model performance must be monitored continuously. Patient populations drift, scanner protocols change, and the case mix at a site evolves. A model that performed well at launch may degrade over time without active monitoring.

## The Role of Clinical Champions

No clinical AI system reaches deployment without clinical champions — physicians who understand the technology, can articulate its clinical value, can design the validation study, and can advocate for integration with clinical workflows. Clinical champions translate between the technical and clinical domains: they know which metrics matter clinically, which failure modes are tolerable and which are dangerous, and how to present evidence to regulatory bodies and hospital administrators. If you are building clinical AI without a clinical collaborator, you are missing the most important part of the translation process.

## Responsible Communication of Limitations

Every publication, presentation, and deployment of a clinical AI tool should include explicit characterisation of:
- The population the model was trained and validated on
- The imaging acquisition conditions under which it was validated
- Known failure modes and the conditions under which they occur
- The metrics used and their clinical interpretation
- What the model should and should not be used for

This is not defensive hedging — it is the information that clinicians need to use the tool safely. Omitting it creates the conditions for dangerous misuse.

!!! note "For Mission 6"
    You will write a clinical translation memo that locates your prototype on the readiness spectrum above. The goal is honest characterisation, not salesmanship. A well-written memo that clearly identifies what additional work is needed before clinical use is more professionally valuable than one that overstates readiness. You should address: what population your model was trained on, what sites and scanners it has been tested on, what its known failure modes are, and what the minimum additional steps would be before investigational clinical use could be considered.
