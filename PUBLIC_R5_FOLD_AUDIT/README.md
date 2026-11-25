# Public R5 prediction-fold audit

Added 25 November 2026 as a standalone reproducibility aid for the existing public research archive. This directory is newly generated from already-public R5 prediction and contrast records. It does not distribute the private author-review manuscript, supplementary files, reviewer correspondence or new fitted states, and is not a full EP16 evidence release.

## Sources (frozen public parent repository)

- [Saved out-of-fold predictions](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility/blob/6c537312da0388a0c9a2784ee175be95f8657747/results/r5/ALL_PRIMARY_OOF.csv): Git blob `13969778bd29858f4117912e9dbf99ca16e6929a`.
- [Original paired contrast table](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility/blob/6c537312da0388a0c9a2784ee175be95f8657747/results/r5/TABLE_PAIRED_CONDITIONAL_RANGES.csv): Git blob `1938e156d2a4d0da41bee5a964cfb8a98553c8cb`.
- NASA/UCI Airfoil Self-Noise: Brooks, Pope and Marcolini, [DOI 10.24432/C5VW2C](https://doi.org/10.24432/C5VW2C). Retain original source attribution and applicable component-level rights.

## Execute

With Node.js 18 or newer, from this directory:

```sh
node recompute_fold_contrasts.mjs > reproduced.json
```

The script downloads the two pinned public inputs, validates their Git blob identities, checks matching observation identifiers, targets, operating groups and folds, and recomputes the overall equal-configuration RMSE differences, the unweighted mean of the ten paired fold differences, and their sample standard deviation. Offline mode accepts the two exact source CSV files as arguments.

The included [audit results](fold_contrast_results.json) were independently calculated from those two public records before this commit, using the same calculation function. All 13 overall contrasts matched the historical public table within 8.882e-16 dB. The 130 fold differences are descriptive; overlapping training folds are not independent experiments, so these summaries are not confidence intervals. No models were refitted and no physical causal or transfer claim is made.

## Release boundaries

The existing [EP11 public release](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/releases/tag/h3air-r21r8-ep11-research-v1) is unchanged. The previously reported [Zenodo research-archive DOI](https://doi.org/10.5281/zenodo.24480002) identifies that earlier archive; this new public-source audit is not asserted to be present in it. Separate later reviewer-only evidence requires component-level release clearance. No blanket licence for private or third-party materials is granted here. See the existing [licence scope](../R21R8_EP11_PUBLIC/LICENSE_SCOPE.md).
