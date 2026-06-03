# Improving Your Model With Intent

## The Danger of Ad Hoc Improvement

After running a baseline and conducting error analysis, you will be tempted to "just try a few things" — add batch normalisation, change the learning rate, add a new augmentation, switch the loss function — and see what improves Dice. This approach produces improvements that are unreliable, non-reproducible, and uninterpretable. If you change three things simultaneously and Dice improves by 0.03, you do not know which change helped, whether they interacted, or whether the improvement would replicate on a different random seed.

The correct approach is: **one change at a time, motivated by error analysis, evaluated on a held-out validation set, interpreted before moving on**.

---

## The Improvement Cycle

Every improvement attempt should follow this cycle:

1. **Error analysis**: What is the dominant failure mode? (See [Error Analysis](error_analysis.md))
2. **Hypothesis**: Why is this failure occurring? What mechanism produces it?
3. **Targeted change**: What single change addresses this mechanism?
4. **Evaluation**: Train with the change; evaluate on the same validation set; record full metrics including per-case distribution
5. **Interpretation**: Did the change help? Did it help on the failure cases identified in step 1, or just on easy cases? Did it hurt any subgroup?
6. **Next hypothesis**: What does the result suggest about the next change to try?

Example cycle for undersegmentation of small tumours:
- **Error analysis**: Dice drops from 0.88 to 0.55 for tumours <5 mL; the model consistently undersegments small tumours
- **Hypothesis**: Small tumours are underrepresented in the training set; the model has not seen enough examples to learn their appearance; additionally, the Dice loss gradient is dominated by larger tumours
- **Targeted change**: Oversample small-tumour training cases (3x oversampling of cases with tumour volume <10 mL)
- **Evaluation**: Does small-tumour Dice improve? Does overall Dice stay stable or improve?
- **Interpretation**: If small-tumour Dice improves from 0.55 to 0.68 while overall Dice stays flat, the hypothesis is supported. If overall Dice drops, oversampling introduced a bias.

---

## Data Augmentation for Medical Imaging

Data augmentation artificially increases the diversity of training examples by applying random transformations that preserve the semantic label. For brain MRI, anatomically valid augmentations include:

### Geometric Augmentations

**Random horizontal/vertical flips**: The brain has left-right symmetry — a tumour in the left hemisphere looks similar to the equivalent tumour in the right hemisphere. Horizontal (left-right) flipping of axial slices is anatomically valid and effectively doubles your training data. Vertical flipping (anterior-posterior) is also valid but has a slightly weaker anatomical justification.

**Random rotations**: Small-angle rotations (±15°) around the axial plane simulate head positioning variation inside the scanner. The label must be rotated identically to the image.

**Random scaling**: Scaling by a factor of 0.9-1.1 simulates size variation across patients and acquisitions.

**Elastic deformation**: Non-linear spatial transformation that mimics tissue deformability — creates plausible anatomical shape variation. Particularly useful for organ segmentation; moderately useful for brain tumour (the brain is relatively rigid in the skull).

### Intensity Augmentations

**Random brightness/contrast adjustment**: Shifts and scales voxel intensities within a plausible range. Simulates scanner-to-scanner intensity variability (a major source of domain shift in MRI).

**Random Gaussian noise**: Adds low-level noise. Simulates SNR variation across acquisition protocols.

**Gamma correction**: Non-linear intensity transformation (I → I^γ with γ randomly sampled from 0.7-1.5). Simulates differences in reconstruction parameters.

**Why these work**: MRI intensity is not calibrated the way CT Hounsfield units are. The same tissue can have very different signal intensity on different scanners, with different protocols, or even at different time points on the same scanner. Intensity augmentation forces the model to learn tissue features that are robust to these variations.

### What Not to Augment

- Do not flip brain MRI vertically (top-to-bottom) unless you have a specific reason — the cerebellum should be inferior to the cerebrum
- Do not apply augmentations so aggressively that the augmented image no longer looks like real MRI — extreme rotations or unrealistic intensity shifts may teach the model features that do not exist in real data
- Do not augment in the frequency domain without understanding what you are doing — some frequency-domain augmentations produce unrealistic MRI appearances

---

## Loss Function Choices

The loss function determines what the model is optimised for. The choice has a large impact on performance, especially for imbalanced tasks.

### Binary Cross-Entropy (BCE)

$$\mathcal{L}_{BCE} = -\frac{1}{N}\sum_{i} [y_i \log \hat{p}_i + (1-y_i) \log(1 - \hat{p}_i)]$$

Treats every voxel equally. For imbalanced segmentation, the gradient is dominated by background voxels (TN). The model learns that predicting background is easy and correct — it is optimised to predict background well. Result: systematic undersegmentation of small or ambiguous tumour regions.

### Dice Loss

$$\mathcal{L}_{Dice} = 1 - \frac{2\sum_i y_i \hat{p}_i + \epsilon}{\sum_i y_i + \sum_i \hat{p}_i + \epsilon}$$

Directly optimises the Dice coefficient. Ignores TN entirely — only FP and FN receive gradient. Robust to class imbalance. The small constant ε (typically 1e-5 or 1) prevents division by zero for empty predictions. Standard choice for medical image segmentation.

### Focal Loss

$$\mathcal{L}_{focal} = -\sum_i (1-\hat{p}_i)^\gamma y_i \log \hat{p}_i - \sum_i \hat{p}_i^\gamma (1-y_i) \log(1-\hat{p}_i)$$

Down-weights the contribution of easy examples (high-confidence correct predictions) and focuses gradient on hard examples. The γ parameter controls the focusing strength (γ=2 is common). Useful when most background voxels are easily classified correctly and the model needs to focus on hard boundary voxels and small ambiguous regions.

### Combined BCE + Dice Loss

$$\mathcal{L}_{combined} = \alpha \cdot \mathcal{L}_{BCE} + (1-\alpha) \cdot \mathcal{L}_{Dice}$$

The most common choice in published work. BCE provides a gradient signal for all voxels including easy ones; Dice loss corrects for imbalance. α = 0.5 is a standard starting point. Some implementations use α = 0.4 (slightly more weight to Dice).

---

## Architectural Improvements

After exhausting data and loss function improvements, architectural changes may help:

**Deeper encoder**: More convolutional layers can extract more abstract features. Diminishing returns past depth 5.

**Attention gates**: Soft attention mechanisms that weight the skip connections — the decoder learns to focus on the most relevant spatial regions from the encoder. Useful when the tumour is small relative to the image and the model needs to attend to the correct region rather than spreading attention uniformly.

**3D convolutions**: Replace 2D axial processing with 3D patch-based processing. Captures inter-slice context (the tumour is spatially continuous in 3D). Requires more GPU memory and slower training. Often gives 2-5 Dice points improvement over 2D.

**Residual connections**: Add identity skip connections within each encoder/decoder block (ResNet-style). Improves gradient flow in deep networks and often produces more stable training.

---

## Transfer Learning from Non-Medical Data

Pre-trained encoders from ImageNet (trained on millions of natural photographs) are surprisingly useful for medical imaging. Despite the domain difference (photographs vs MRI), the low-level features learned from ImageNet (edges, textures, gradients) transfer well to medical images. Using a pre-trained ResNet or EfficientNet as the encoder of a U-Net and fine-tuning on BraTS often outperforms a randomly-initialised encoder, especially with small training datasets.

---

## Ensemble Methods

Train multiple models with different random seeds, different architectures, or different data augmentation strategies. Average their output probability maps. Ensemble predictions are typically 2-4 Dice points better than any individual model. The cost: inference time multiplies by the number of models. For offline processing (research), this is acceptable. For real-time clinical use, it may not be.

---

## The Test Set Peeking Problem

If you evaluate your model on the test set after each experiment and pick the change that gives the highest test Dice, you are effectively fitting to the test set. The final result will overestimate true performance. This is a form of data leakage.

The solution: make all improvement decisions based on **validation set** performance. Use the test set once, at the very end, to report the final result. If you use a public benchmark like BraTS, the test set is held by the challenge organisers — you cannot overfit to it. For your own datasets, you must enforce this discipline yourself.

---

!!! note "Connect to Lab Mission"
    **Now do the lab — M4 (Model Improvement).**

    In Mission 4, implement one targeted improvement motivated by your M3 error analysis. Start with augmentation or loss function (these are lower-risk changes than architectural modifications). Formulate a written hypothesis before you write any code. Train and evaluate. Write a one-paragraph comparison: what changed, what improved, what did not, and what the result implies about the next step. Use Claude to help generate the augmentation code or modified training loop. Do not implement more than one major change — resist the temptation.
