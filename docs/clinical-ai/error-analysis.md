# Error Analysis

A single Dice score tells you how well your model performs on average across your validation set. It does not tell you which cases fail, why they fail, whether failures are concentrated in a specific patient subgroup, or how dangerous the failures are clinically. Error analysis moves beyond aggregate metrics to build a mechanistic understanding of model behaviour. This understanding is what separates a researcher who can systematically improve a model from one who can only run experiments and hope.

## Why Aggregate Metrics Are Not Enough

Dice 0.82 across 50 validation cases could mean:
- The model performs uniformly at 0.82 on all cases.
- The model performs at 0.92 on 45 typical cases and catastrophically at 0.20 on 5 atypical cases.

These two scenarios have the same aggregate Dice but radically different clinical implications. The second scenario is more common, more dangerous, and more informative — because the 5 failing cases are likely telling you something specific about the model's limitations. Finding those cases, characterising them, and forming a falsifiable hypothesis about why they fail is the scientific work of error analysis.

## Types of Segmentation Errors

**False positives** occur when the model predicts tumour in a region that is actually healthy tissue. Common causes include: healthy tissue with intensity patterns similar to tumour (T2 hyperintensity from white matter lesions or leukoaraiosis being confused for FLAIR-positive tumour); imaging artefacts (susceptibility artefacts near air-tissue interfaces) that resemble tumour signal; and regions adjacent to the tumour margin where the model has high uncertainty. False positives in eloquent cortex (motor strip, Broca's area) would be particularly dangerous if they led to unnecessary resection.

**False negatives** occur when the model fails to include actual tumour voxels in its prediction — missing tumour. This is generally the more dangerous error direction. Missed enhancing tumour leads to under-treatment of the most aggressive tumour component. Missed tumour core affects surgical planning. Infiltrative margins that are FLAIR-positive but not labelled by the model may cause radiotherapy fields to miss part of the target. Common causes include: small lesion components below the effective resolution of the model; low-contrast regions where tumour signal is close to surrounding tissue; cases where the enhancing rim is thin or patchy.

**Boundary errors** occur when the model correctly identifies the tumour location but gets the extent wrong — the segmentation is in the right place but too large or too small, with the error concentrated at the periphery. High Dice with high HD95 indicates boundary errors without large volume errors. These can be caused by inconsistent preprocessing (poorly corrected bias field making the tumour-oedema boundary appear sharper or blurrier than in training data) or by training label noise at the annotated boundary.

## Spatial Pattern Analysis

Errors that are random across cases suggest irreducible uncertainty (perhaps the task is genuinely ambiguous in those regions) or model underfitting. Errors that cluster spatially — concentrated in specific anatomical regions or in specific parts of a scan — suggest a systematic failure mode that can potentially be addressed.

Questions to ask during spatial analysis:
- Do failures occur predominantly in specific lobes (frontal, temporal, occipital)?
- Are false positives concentrated near the skull edge (suggests skull stripping artefacts)?
- Do boundary errors occur more on the inferior/superior slices (suggests 2D models struggle at the ends of volumes)?
- Are false negatives concentrated in small tumours vs large tumours?
- Do the worst cases share a radiological feature — for example, multifocal tumour, or tumours crossing the midline?

## The Observation → Evidence → Hypothesis Discipline

Good error analysis follows a rigorous structure:

1. **Observation**: A specific, measurable finding from your results. "The five worst-performing cases have a mean Dice of 0.41 vs 0.87 for the remaining cases."

2. **Evidence**: Concrete data supporting and characterising the observation. "Visual inspection of these five cases shows that four have multifocal tumours (two or more disconnected lesion components), and one has a very small tumour volume (< 5cm³)."

3. **Hypothesis**: A specific, falsifiable claim about the mechanism. "The model's connected component post-processing retains only the largest predicted region, causing it to systematically miss secondary lesion components in multifocal cases."

4. **Test**: A specific experiment that could confirm or refute the hypothesis. "If I remove the largest-component filter and retain all predictions above a size threshold, Dice on multifocal cases should improve, while Dice on single-lesion cases should remain stable or slightly decrease."

This discipline matters because it constrains your next experiment. Without a specific hypothesis, any improvement in Mission 4 could be attributable to any change you made — you learn nothing transferable. With a specific hypothesis, you can design a targeted intervention and interpret the result as evidence about the mechanism.

## Failure Mode Taxonomy for Segmentation

A working taxonomy of segmentation failure modes, useful for structuring Mission 3 analysis:

| Failure type | Description | Diagnostic sign |
|---|---|---|
| Complete miss | Model predicts all-background for a positive case | Dice = 0, case has ground truth tumour |
| Severe under-segmentation | Model finds tumour but misses most of it | Dice < 0.5, low sensitivity |
| Over-segmentation | Model predicts much more than actual tumour | High FP, low specificity, HD95 elevated |
| Boundary imprecision | Correct location, wrong extent | Dice acceptable, HD95 elevated |
| Region confusion | Correct overall mask, wrong subregion labels | WT good, TC or ET poor |
| Multifocal failure | Misses secondary components | Dice poor on cases with multiple lesion foci |
| Small lesion failure | Model misses small tumours | Dice correlated with tumour volume |

## Error Analysis Drives Improvement

Mission 4 asks you to implement a targeted improvement to your baseline model. The connection is explicit: your improvement hypothesis must reference the failure mode you identified in Mission 3. A model change motivated by a specific failure hypothesis is more likely to succeed than a generic hyperparameter sweep, and it produces interpretable results regardless of outcome. "We hypothesised X, implemented Y to address it, and found Z" is a complete scientific statement. "We tried several things and the best one gave Dice 0.84" is not.

Error analysis is more scientifically valuable than metric optimisation precisely because it produces understanding, not just numbers. A model whose failure modes are characterised and understood is safer to deploy than a model with a higher aggregate metric and unknown failure behaviour.

!!! example "What a good failure hypothesis looks like"
    **BAD**: "The model does poorly on some slices."

    This is an observation, not a hypothesis. It does not identify a mechanism, does not suggest a specific intervention, and cannot be tested.

    **GOOD**: "The model consistently over-segments in axial slices with low FLAIR contrast at the tumour-oedema boundary, possibly because the training set is dominated by high-contrast cases where the boundary is clearly defined. The model may have learned to treat any moderate FLAIR elevation as tumour, rather than learning to identify the specific boundary pattern."

    This is a hypothesis. It identifies: (1) where the failure occurs (low FLAIR contrast boundary slices); (2) a proposed mechanism (training set bias toward high-contrast cases); (3) an implicit prediction (the failure rate should correlate with FLAIR contrast at the boundary); and (4) a direction for intervention (augmenting training with low-contrast cases, or adjusting the loss weighting at boundary voxels).
