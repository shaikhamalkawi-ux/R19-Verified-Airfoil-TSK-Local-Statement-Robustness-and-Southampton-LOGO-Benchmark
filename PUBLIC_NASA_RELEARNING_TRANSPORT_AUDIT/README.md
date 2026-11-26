# NASA airfoil: antecedent relearning and held-out witness transport

Research evidence clarification — 26 November 2026. This note consolidates three previously reported numerical results from the frozen NASA/UCI airfoil study. It neither changes the fitted models nor reports a new scientific experiment.

| Endpoint | Verified saved-record result | Interpretation |
| --- | --- | --- |
| Whole-configuration bootstrap with antecedent relearning | 7,998 successful attempts out of 8,000; two retained FCM nonconvergences | Subset of the 28,000 original bootstrap attempts; includes F4/F5, ten outer folds and compact/reference structures, not 8,000 independent experiments. |
| F5 one-SE TSK-ridge matched local-function disagreement | 11.612 dB (full precision median 11.61158720006682 dB) | Median of the ten fold-specific medians of configuration-weighted RMS disagreement on joint relative-activation support; weighted Jaccard matching threshold 0.5 and both normalized firing weights at least 0.1. These are matched rules, not identical functions or prediction residuals. |
| Transport of original training-side strict reversal witnesses | 69 of 107 satisfy the 0.1-dB maximum aggregate prediction-change budget on every corresponding outer-held-out input; 38 exceed it | Original F5 one-SE fixed-premise audit, with a 1% training ridge-objective allowance. These are the particular constructed witnesses, not a universal guarantee for all feasible perturbations. |

## Frozen public records

- [R5 bootstrap attempt coverage](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility/blob/6c537312da0388a0c9a2784ee175be95f8657747/results/r5/BOOTSTRAP_REPLICATE_COVERAGE.csv), Git blob `21cff88839c1c5ead3c86060952d96b8c3e5a6a2`. Filter branch = relearn and sum expected, success and fail over the 40 task rows.
- [R9 shared-support fold records](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility/blob/6c537312da0388a0c9a2784ee175be95f8657747/results/r9/SHARED_SUPPORT_FOLDS.csv), Git blob `d286090d369543c3429ca5e66bbaa2beeb59de12`. Filter feature = F5, structure = compact, cutoff = 0.1; take the median of the ten `median_D_common_dB` values.
- [EP18 AF4 authorized scientific evidence ZIP](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/releases/download/h3air-r21r8-ep18-evidence-v1/57H3Air_EP18_AF4_Scientific_Evidence.zip), SHA-256 `1edd543fb6544f8bd23de418b3108f1617518251bf35a2cb18ec966d5a7225dd`. Member `direct_derivative/inputs/RESOLVED_510_STATEMENTS.csv`, SHA-256 `7c99f803a12533a0e7f4252a27855844ca743e2165484640cc07df559c58c8c2`. Select `final_class = FEASIBLE_REVERSAL` and count the `heldout_pointwise_retained` flags. There are 107 selected records, 69 true and 38 false; the other 403 records are protected.

The coverage totals and median were recalculated from the pinned public CSVs; the AF4 archive was hash-matched to its published release digest, passed its ZIP CRC check and supplied the witness table used for the count. These are saved-record checks, not a fresh full model refit.

## Scope and reproducibility

The relearning experiment varies preprocessing and fuzzy antecedents; the coefficient-sign audit holds these fitted objects fixed. A retained witness certifies only its own finite-input budget on the evaluated inputs. The inherited NASA outer folds are not an untouched external campaign. The original 403 protected / 107 reversible split at the declared 0.1-dB/1% budgets remains unchanged.

NASA/UCI Airfoil Self-Noise: Brooks, Pope and Marcolini, DOI [10.24432/C5VW2C](https://doi.org/10.24432/C5VW2C), CC BY 4.0. The [EP11 reconstructed-state research release](../R21R8_EP11_PUBLIC/README_RELEASE.md), the [EP18 release](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/releases/tag/h3air-r21r8-ep18-evidence-v1), and the [EP21 public evidence](../R21R8_EP21_PUBLIC/README.md) remain distinct. The recorded research DOI [10.5281/zenodo.24480002](https://doi.org/10.5281/zenodo.24480002) refers to the earlier EP11 archive, not this note or a journal article. Component-specific rights remain as stated in the [existing licence scope](../R21R8_EP11_PUBLIC/LICENSE_SCOPE.md). No private manuscript, review materials, or non-public third-party arrays are included. No new archival deposit, journal submission, or acceptance is implied.
