# Voxels, Slices, and Spacing

Before you write a single line of segmentation code, you need a clear mental model of what a medical image actually is in memory. A brain MRI is not a photograph — it is a 3D array of numbers, and the physical meaning of those numbers depends critically on metadata that travels alongside the image.

## From Pixels to Voxels

A standard 2D image is made of **pixels** — picture elements arranged in a grid. Each pixel has an (x, y) position and an intensity value (e.g., 0-255 for an 8-bit image). A 3D MRI volume extends this idea: it is made of **voxels** — volumetric pixels arranged in a 3D grid. Each voxel has an (x, y, z) position and a single intensity value representing the MRI signal at that location.

```
2D Image (pixel grid):        3D Volume (voxel grid):

  x →                           x →
y ┌──┬──┬──┬──┐              z ┌─────────────┐
↓ │  │  │  │  │            ↗   │  [slice n]  │
  ├──┼──┼──┼──┤           ↗    │  [slice 2]  │
  │  │  │  │  │          ↗     │  [slice 1]  │
  ├──┼──┼──┼──┤         └──────┴─────────────┘
  │  │  │  │  │               y →
  └──┴──┴──┴──┘
```

For a typical BraTS volume with shape **240 × 240 × 155**: there are 240 voxels in the x-direction (left-right), 240 in the y-direction (anterior-posterior), and 155 in the z-direction (inferior-superior). The total number of voxels is 240 × 240 × 155 = **8,928,000 voxels** per modality. With four modalities (T1, T1ce, T2, FLAIR), a single BraTS case is a 4 × 240 × 240 × 155 array — roughly 35 million numbers.

## Slices and Viewing Planes

A **slice** is a 2D cross-section through the 3D volume. Three standard anatomical planes are used:

```
        AXIAL                  CORONAL               SAGITTAL
   (horizontal cut)        (front-to-back cut)     (left-right cut)

     ┌──────────┐              ┌──────┐               ┌──────┐
     │  ⊙  ⊙   │              │  ⊙   │               │      │
     │          │              │      │               │      │
     │    ▽     │              │  ▽   │               │  ▽   │
     │          │              │      │               │      │
     └──────────┘              └──────┘               └──────┘
  Looking down from top     Looking from front      Looking from side
  Shows: L/R and A/P        Shows: L/R and S/I      Shows: A/P and S/I
  (240 × 240 pixels)        (240 × 155 pixels)      (240 × 155 pixels)
```

Clinical MRI is most commonly viewed **axially** — this is the natural orientation for reading brain scans. However, for brain tumour analysis, radiologists also check coronal and sagittal views, particularly to assess craniocaudal extent and involvement of structures like the corpus callosum or brainstem. AI models using 3D convolutions operate on all three directions simultaneously.

!!! info "Orientation in Code"
    When you load a NIfTI file with nibabel or SimpleITK, be aware that the axis ordering in the numpy array may differ from the standard radiological convention. Always check the affine matrix and orient your slices before making assumptions. A common mistake is displaying a sagittal slice thinking it is axial.

## Voxel Spacing: The Physical Dimension

The most important metadata for a medical image is **voxel spacing** (also called voxel size or resolution): the physical size of each voxel in millimetres.

A volume with shape 240 × 240 × 155 and spacing **1.0 × 1.0 × 1.0 mm** (isotropic) means each voxel represents a 1mm cube of brain tissue. The full volume covers 240mm × 240mm × 155mm — roughly the size of a human head.

**Why spacing is critical for AI:**

- Volume calculations depend on spacing: if voxel spacing is wrong, tumour volume estimates are wrong.
- Distance metrics (Hausdorff distance, surface distance) are computed in mm, not voxels — spacing is required.
- Convolutional kernels have implicit assumptions about spatial relationships; a network trained on isotropic data applied to anisotropic data will distort shape representations.
- Resampling to a consistent spacing is required before training or inference on multi-site data.

## Isotropic vs. Anisotropic Spacing

**Isotropic spacing:** all three dimensions are equal (e.g., 1mm × 1mm × 1mm). Each voxel is a cube. Resolution is uniform in all directions.

**Anisotropic spacing:** dimensions differ (e.g., 1mm × 1mm × 5mm). The voxel is a rectangular slab, not a cube. In-plane resolution (x, y) is high; through-plane resolution (z) is low. This is extremely common in routine clinical MRI — thicker slices are acquired to reduce scan time. A 5mm slice thickness is standard for many clinical sequences.

```
Isotropic (1×1×1mm):          Anisotropic (1×1×5mm):

  ┌──┐  ← 1mm                   ┌────────────┐  ← 5mm (thick slice)
  │  │  ← 1mm                   │            │
  └──┘                           └────────────┘
  cube voxel                     slab voxel
  good for 3D AI                 common in clinic, bad for 3D AI
```

!!! warning "Clinical Data vs. BraTS Data"
    BraTS data has been resampled to 1mm isotropic. Raw clinical MRI from hospitals frequently arrives with anisotropic spacing (1×1×3mm or 1×1×5mm). If you deploy a model trained on BraTS to clinical data without resampling, performance will degrade significantly — the model has never seen thick-slice data. Always check and normalise spacing before inference.

## Resampling

**Resampling** changes the voxel spacing of a volume, producing a new array with a different shape. To increase resolution (upsample) or decrease it (downsample), values at new grid positions are computed by **interpolation** — typically trilinear interpolation for image data, or nearest-neighbour interpolation for label masks (to avoid creating invalid fractional label values).

Resampling introduces a small amount of blurring and is irreversible — information lost during downsampling cannot be recovered. It is a necessary preprocessing step when working with multi-site data at different resolutions, but it should be done thoughtfully.

## Key Terms Reference

| Term | Definition | Why It Matters for AI |
|------|------------|----------------------|
| **Voxel** | 3D volumetric pixel — the basic unit of a 3D image | All operations (convolution, loss) act on voxels |
| **Volume shape** | Number of voxels in each dimension (e.g., 240×240×155) | Determines array size, batch memory requirements |
| **Voxel spacing** | Physical size of each voxel in mm (e.g., 1×1×1mm) | Required for volume/distance metrics; must match training data |
| **Isotropic** | Spacing equal in all three dimensions | Standard for AI; what BraTS provides |
| **Anisotropic** | Spacing unequal (e.g., thick slices) | Common in clinic; requires resampling before AI inference |
| **Slice** | 2D cross-section of the 3D volume | Unit of human reading; AI reads all slices jointly |
| **Axial** | Horizontal slice (z-direction) | Standard clinical reading orientation |
| **Coronal** | Frontal slice (y-direction) | Good for superior-inferior extent, midline structures |
| **Sagittal** | Side slice (x-direction) | Good for anterior-posterior extent, corpus callosum |
| **Resampling** | Changing voxel spacing via interpolation | Required for multi-site normalisation; use NN interpolation for labels |
| **Affine matrix** | 4×4 matrix encoding position, spacing, and orientation | Stored in NIfTI header; defines real-world coordinates |

!!! tip "Connection to Mission 1"
    When you load your first BraTS case, run `print(img.shape)` and `print(img.header.get_zooms())`. You should see shape `(240, 240, 155)` and zooms `(1.0, 1.0, 1.0)`. If you load clinical data later and these numbers differ, resampling is required before running any trained model.
