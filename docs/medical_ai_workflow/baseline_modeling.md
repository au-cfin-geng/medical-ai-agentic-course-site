# Building a Baseline Model

## Why You Need a Baseline Before You Optimise

A baseline model serves one purpose: it gives you a reference point. Without a baseline, you cannot know whether your proposed improvement actually works, whether the improvement is due to the change you made or some other factor, or whether the published results you are comparing against used a fair experimental setup.

The baseline should be simple enough to implement in a few hours, reproducible enough that you can train it again next week and get the same result, and honest — it should not include any trick that you would not consider "standard practice." The baseline is not something to be ashamed of. It is the foundation of your scientific argument.

---

## The Floor: Intensity Thresholding

Before building any neural network, it is worth knowing what a completely naive method achieves. For brain tumour segmentation, a simple threshold on FLAIR intensity captures some of the tumour region — GBM causes FLAIR hyperintensity due to peritumoral oedema. A threshold-based method might achieve whole-tumour Dice of 0.3-0.5 on easy cases and near zero on others.

This is the floor. Any trained model should substantially exceed it. If your trained model is only marginally better than a FLAIR threshold, something is wrong with your training pipeline.

---

## The U-Net Architecture

The standard baseline for medical image segmentation is the U-Net (Ronneberger, Fischer, and Brox, 2015). Originally designed for biomedical image segmentation, U-Net has become the near-universal starting point for any new segmentation task because it is:

- Architecturally straightforward: encoder, bottleneck, decoder with skip connections
- Computationally tractable: can be trained on a single GPU for small datasets
- Well-studied: years of published results to compare against

### Encoder (Contracting Path)

The encoder is a sequence of convolutional blocks, each typically consisting of two 3x3 convolutions with batch normalisation and ReLU activation, followed by a 2x2 max-pooling operation that halves the spatial resolution. As spatial resolution decreases, the number of feature channels increases (e.g., 32 → 64 → 128 → 256). The encoder learns hierarchical features: early layers detect edges and local texture; deeper layers detect more abstract patterns like "enhancing ring" or "necrotic core."

### Bottleneck

The bottleneck is the deepest layer of the network, operating at the lowest spatial resolution. It captures global context — the model "knows" roughly where in the brain it is looking, which is important for spatial priors (GBM rarely occurs in the cerebellum).

### Decoder (Expanding Path)

The decoder progressively upsamples the feature map back to the original spatial resolution, using transposed convolutions or bilinear upsampling followed by convolution. After each upsampling step, the decoder concatenates the feature map with the corresponding encoder feature map via a **skip connection**. This is the key innovation of U-Net: skip connections allow the decoder to use both high-resolution spatial detail from the encoder and high-level semantic context from the bottleneck simultaneously.

### Skip Connections

Without skip connections, the bottleneck must encode all the spatial detail needed for precise boundary delineation — this is too much to ask of a small feature map. Skip connections solve this by providing a shortcut: fine spatial detail from the encoder is directly available to the decoder. The result is segmentation masks with accurate boundaries rather than blurry, spatially imprecise predictions.

---

## Key Choices for a Baseline

### 2D vs. 3D

Brain MRI is a 3D volume, but you can train either on 2D axial slices (treating each slice as an independent image) or on 3D patches. 

- **2D baseline**: faster to train, simpler to implement, more stable training due to larger effective batch size; misses inter-slice context
- **3D baseline**: captures volumetric context, often gives better Dice on 3D metrics, but requires more GPU memory and smaller batch sizes

For a first baseline, **2D U-Net on axial slices** is entirely appropriate and will give you results competitive with published work from 2017-2019.

### Patch Size

For 2D: use full slices (240x240 for BraTS). For 3D: common patch sizes are 128x128x128 or 96x96x96. Smaller patches fit in memory but lose global context.

### Batch Size and Learning Rate

For a 2D U-Net on BraTS slices: batch size 8-16, learning rate 1e-4 with Adam optimiser is a stable starting point. Use a learning rate scheduler (e.g., reduce on plateau) to decay the learning rate when validation metrics stop improving.

### Loss Function

This choice matters more than most architectural choices for imbalanced segmentation:

- **Binary cross-entropy**: treats every voxel equally. For a dataset where tumour voxels are <5% of the total, the gradient is dominated by the easy correct background predictions. The model learns to predict background everywhere.
- **Dice loss**: directly optimises the Dice coefficient. Invariant to class imbalance because it only considers the foreground region. Standard for medical image segmentation.
- **Combined BCE + Dice loss**: the most common choice in published work. BCE provides gradient signal for all voxels; Dice loss corrects for imbalance. A 0.5/0.5 combination is a reasonable starting point.

### Number of Epochs

Train for at least 100 epochs with early stopping based on validation Dice. Do not stop at 50 epochs if the validation metric is still improving — you will underestimate your baseline performance.

---

## What to Expect from a First-Run Baseline

Typical results for a well-implemented 2D U-Net baseline on BraTS:

| Region | Expected Dice Range |
|--------|-------------------|
| Whole Tumour (WT) | 0.75 - 0.87 |
| Tumour Core (TC) | 0.65 - 0.80 |
| Enhancing Tumour (ET) | 0.60 - 0.75 |

If your results are substantially below this range, investigate:

1. Is your data loading pipeline correct? (Check a few training samples visually)
2. Is your loss function appropriate? (Try Dice loss if you used BCE)
3. Is your learning rate too high? (Loss exploding or oscillating)
4. Did training actually run for enough epochs? (Check training curves)

If your first-run results are substantially above this range, be suspicious. Check whether your train/validation split leaks data, whether you are using test set labels for training, and whether your Dice computation is correct.

---

## The Difference Between Training Loss and Validation Metrics

After training, you should plot both training loss and validation Dice coefficient over epochs. Four patterns to recognise:

- **Both improving**: training is working, stop when validation Dice plateaus
- **Training loss decreasing, validation Dice plateauing early**: overfitting — the model is memorising the training set
- **Training loss oscillating**: learning rate too high
- **Neither improving**: learning rate too low, or a bug in the training loop

Overfitting is the most common problem for small medical imaging datasets. With a few hundred BraTS cases split 80/20 for training and validation, a U-Net has enough capacity to memorise the training set if regularisation is absent. Use data augmentation and dropout to mitigate this.

---

## The Reproducibility Requirement

Set a random seed at the start of your training script. Document your exact hyperparameters. Log training and validation metrics to a file. These are not optional — a baseline that you cannot reproduce next week is not a baseline, it is a lucky run.

```python
import torch
import numpy as np
import random

def set_seed(seed=42):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
```

!!! note "Connect to Lab Mission"
    **Now do the lab — M2 (Baseline Model Training).**

    In Mission 2, you will implement a 2D U-Net baseline for whole-tumour segmentation on BraTS. Use Claude to help scaffold the model code, data loader, and training loop. Your deliverables: a training curve plot, validation Dice score at convergence, and a brief interpretation of the result — is this Dice score clinically adequate? If not, what is the most likely cause of the gap? Document every hyperparameter decision you made and the reasoning behind it.
