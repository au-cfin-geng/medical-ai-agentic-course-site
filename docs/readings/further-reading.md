# Further Reading

This page collects literature and resources that extend the concepts practised in the course. Each section includes a brief orientation — not just what to read, but what to look for when you read it. No URLs are hardcoded because link rot is common in this field; search the titles in your institution's library catalogue or in PubMed, arXiv, or Google Scholar.

---

## Clinical AI and Medical Image Analysis

The foundational literature in clinical AI asks a deceptively simple question: does a model that performs well on a benchmark actually help patients? Look for papers that distinguish between benchmark performance and prospective clinical utility, and for systematic reviews that track the gap between what AI papers claim and what replication studies find. Topol's 2019 review in *Nature Medicine* ("High-performance medicine: the convergence of human and artificial intelligence") remains a useful orientation to the broader landscape, though the field has moved quickly since. Obermeyer and Emanuel's 2016 *NEJM* piece ("Predicting the Future — Big Data, Machine Learning, and Clinical Medicine") is a useful corrective to early hype and raises questions about bias and generalisability that this course addresses directly in Mission 6.

For medical image analysis specifically, look for papers that report not just Dice scores but failure mode characterisation and clinical impact studies. The distinction matters: a model with Dice 0.85 on a curated test set may still fail systematically on the patient subgroup that most needs it.

---

## MRI and Brain Tumour Segmentation (BraTS)

The BraTS challenge is the reference benchmark for brain tumour segmentation and the source of the dataset conventions used in this course. Menze et al. (2015), "The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)" in *IEEE Transactions on Medical Imaging*, is the foundational paper establishing the dataset, label conventions (NCR/NET, oedema, enhancing tumour), and evaluation protocol. Read this to understand why the three evaluation subregions — whole tumour, tumour core, enhancing tumour — were chosen and what clinical question each answers.

Bakas et al. (2018), "Identifying the Best Machine Learning Algorithms for Brain Tumor Segmentation, Progression Assessment, and Overall Survival Prediction in the BRATS Challenge" (available on arXiv), provides a comprehensive analysis of algorithm performance across multiple years of the challenge. Look in particular for the sections on inter-rater variability — these establish the ceiling for how good any automated system can reasonably be expected to be, and they are directly relevant to the honesty constraints in Mission 6.

When reading any BraTS-related paper, pay attention to the test set composition and whether the evaluation is cross-institutional. A model trained and validated within a single centre may show Dice scores 0.05–0.10 higher than one evaluated on genuinely external data.

---

## Reproducible Research in Medical AI

Reproducibility is a structural problem in medical AI, not a collection of individual failures. Pineau et al. (2021), "Improving Reproducibility in Machine Learning Research" in *JMLR*, provides a practical framework for what reproducibility requires: code availability, data documentation, fixed random seeds, and statistical characterisation of results. The machine learning reproducibility checklist from this work maps closely onto the responsible AI checklist used in Mission 6.

Liao and Coiera (2021) and subsequent systematic reviews of AI in radiology have documented that a large proportion of published clinical AI papers cannot be replicated by independent groups. Look for these meta-analyses when you want to understand the baseline rate of irreproducibility in the field. The lesson for your own work: the controlled experiment structure in Mission 4 and the study design in Mission 5 are not bureaucratic requirements — they are the minimum practices that make your findings mean something outside your own laptop.

For a practical implementation guide, the ML Reproducibility Checklist (maintained by Papers With Code) translates these principles into concrete actions. Search for it by name.

---

## Reporting Standards for AI in Medicine (TRIPOD-AI, CONSORT-AI, STARD)

Reporting standards exist because individual researchers consistently omit information that readers need to evaluate and replicate their work. TRIPOD-AI (Transparent Reporting of a Multivariable Prediction Model for Individual Prognosis or Diagnosis — Artificial Intelligence) is the most directly relevant standard for the kind of work done in this course. It extends the original TRIPOD checklist with items specific to AI-based prediction models, including requirements for reporting training data characteristics, model architecture transparency, calibration, and deployment context. Look for the 2024 *BMJ* publication of TRIPOD+AI for the most current version.

CONSORT-AI applies specifically to randomised trials of AI interventions — relevant if your Mission 5 study design proposes a prospective randomised evaluation. STARD (Standards for Reporting Diagnostic Accuracy Studies) is the appropriate reference if your study is framed as a diagnostic accuracy study rather than a treatment comparison. Understanding which standard applies to your study design is itself part of Mission 5.

When reading any clinical AI paper, check whether it was written against one of these standards. Papers that do not cite a reporting standard are much more likely to omit crucial methodological details.

---

## AI Ethics and Algorithmic Bias

Bias in clinical AI is not a hypothetical concern — it is a documented reality with patient-facing consequences. Obermeyer et al. (2019), "Dissecting racial bias in an algorithm used to manage the health of populations" in *Science*, is the landmark paper demonstrating that a widely deployed commercial algorithm systematically underestimated the illness severity of Black patients relative to white patients. Read this paper for the mechanism: the bias arose from using healthcare cost as a proxy for healthcare need, which reflects historical disparities in access rather than true illness burden.

For medical imaging specifically, look for papers examining performance variation across demographic subgroups in imaging AI. The BraTS dataset itself has known composition biases; performance on paediatric cases, low-grade gliomas, or cases from low-income countries may differ substantially from the headline benchmark numbers. This is directly relevant when you complete the population characterisation section of Mission 6.

Gebru et al., "Datasheets for Datasets" (available on arXiv), proposes a documentation framework for datasets analogous to the data sheets that accompany electronic components. Look for this when thinking about what a responsible data documentation practice for your own future research would look like.

---

## Regulatory Frameworks for AI Medical Devices

In the European Union, AI-based medical devices are regulated under the Medical Device Regulation (MDR, 2017/745) and, for software specifically, under the AI Act (2024). In the United States, the FDA classifies AI-based clinical decision support software under its Software as a Medical Device (SaMD) framework and has published a series of guidance documents on AI/ML-based SaMD. The FDA's 2021 "Artificial Intelligence/Machine Learning (AI/ML)-Based Software as a Medical Device (SaMD) Action Plan" is the foundational policy document; search for it on the FDA website. The FDA has subsequently proposed a regulatory framework for predetermined change control plans, which is relevant for AI systems that update after deployment.

For the UK, the MHRA has published guidance on software and AI as a medical device that broadly parallels the EU framework. Mission 6 asks you to identify the regulatory pathway for your system; read the relevant framework document for your jurisdiction before completing that section. The key questions the regulatory framework asks — what is the intended use, what is the risk class, what clinical evidence is required — are exactly the questions a rigorous translation brief must answer.

---

## Prompt Engineering and Agentic AI

The technical literature on prompt engineering is younger and less settled than the clinical AI literature, but several papers have established results that are directly relevant to this course. Wei et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (*NeurIPS*), demonstrated that asking a language model to show its reasoning step by step substantially improves performance on complex tasks. The plan-before-code pattern used in Mission 2 and the observation-before-hypothesis pattern in Mission 3 are practical applications of this principle.

For agentic AI specifically, look for papers on tool use and multi-step reasoning in large language models. The literature moves quickly; searching arXiv for "agentic AI" or "LLM tool use" will surface recent work. The key concept to watch for is the distinction between task completion (finishing the immediate prompt) and task specification (understanding what the researcher actually needed) — this distinction drives the entire prompt design methodology in this course.

Anthropic's published model specifications and usage policies, available on the Anthropic website, describe the principles governing Claude's behaviour, including honesty, helpfulness, and harm avoidance. Reading these is useful background for understanding why certain kinds of prompts work better than others and why the honesty constraint pattern in Mission 6 is not just a rhetorical device.

---

## AI in Medical Education

The use of AI in medical education raises questions that go beyond tool selection: what does it mean to learn a skill when an AI can perform that skill on demand? How do medical educators assess competence in an environment where AI assistance is ubiquitous? This course takes a clear position — you are the researcher, Claude is the instrument — but the broader debate is worth engaging with.

Topol and colleagues have written on AI in medical training, arguing that AI will shift emphasis from memorisation toward reasoning and interpretation. Several papers in medical education journals have begun to explore how clinical reasoning competencies should be assessed when AI tools are available during assessment. Look for these in journals such as *Medical Education*, *Academic Medicine*, and *BMJ Medical Education*.

For the specific context of computational and AI literacy in medicine, look for papers on how medical schools are adapting their curricula. The competency frameworks that have emerged from these discussions — distinguishing between AI literacy, AI fluency, and AI research skill — map directly onto the learning objectives of this course.
