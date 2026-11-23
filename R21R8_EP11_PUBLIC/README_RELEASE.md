# Project 57 H3Air R21R8-EP11 research archive

Public archive: [GitHub Release](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/releases/tag/h3air-r21r8-ep11-research-v1) · [Zenodo DOI 10.5281/zenodo.24480002](https://doi.org/10.5281/zenodo.24480002). The DOI identifies the research archive, not an IEEE Access article.

This release accompanies the author-review manuscript *Beyond Prediction Accuracy: Local-Slope Robustness in Takagi–Sugeno Fuzzy Models of Airfoil Self-Noise*. The manuscript is not an accepted or published IEEE Access article.

## Contents and verification

- Forty `*_NEW_STATES_AND_AUDIT.zip` files cover F4/F5, compact/reference, and ten outer folds: 28,000 recorded bootstrap attempts, 27,998 newly reconstructed fitted-state files, and two reproduced FCM fitting failures (`F5_fold00_compact/relearn/141` and `F5_fold02_reference/relearn/115`). The aggregate size is 773,361,055 bytes.
- `SHA256SUMS.txt` lists the exact SHA-256 of each task archive and the two previously published EP10 research ZIPs. The EP10 ZIPs remain at their existing repository paths and are not duplicated as GitHub Release assets.
- `R21R8_FULL40_Completion_Certificate.json` and `R21R8_Independent_Full28k_QA.json` are author-recorded audit evidence. `verify_release_assets.py` independently checks all distributed ZIP bytes, CRCs, 28,000 journal entries, 27,998 state-member hashes, and the two failure identities using only the released files. It does not redo model fitting or compare against unavailable original historical fitted-state bytes.
- The original analysis code and selected numerical evidence are in the existing [EP10 public code/evidence ZIP](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/blob/main/R21R8_EP10_PUBLIC/57H3Air_R21R8_EP10_Public_Selected_Code_and_Numerical_Evidence.zip). The [NASA parent repository](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility) contains the original R5 scripts. `requirements.txt` records the R5 scientific environment, and `ENVIRONMENT.md` explains the distinct verification levels.

Download the 40 ZIP assets into one directory with `SHA256SUMS.txt`, `R21R8_FULL40_Completion_Certificate.json`, and `verify_release_assets.py`, then run:

```bash
python verify_release_assets.py --archives . --manifest SHA256SUMS.txt --certificate R21R8_FULL40_Completion_Certificate.json
```

The verifier uses the Python standard library. Full numerical replay against the frozen R5 per-draw reference arrays additionally requires the original historical `results/bootstrap` tree, which is not present in this public release. The author-recorded independent comparison found all 27,998 new states consistent with saved historical predictions, coefficients, assignments, similarities, and seeds under the declared tolerances. That result does **not** establish byte identity with the missing historical fitted-state files.

## Scientific limits

NASA/UCI has 1,503 rows and 106 operating groups. At a 0.1 dB prediction budget plus 1% ridge-objective allowance, 403 of 510 local slope signs are protected and 107 strictly reversible. At a separate 1 dB plus 1% contextual sensitivity, the counts are 135 and 375. Neither threshold is a calibrated per-row error interval. Southampton has 343 source-normalized rows, 38 spectra, and seven geometries; equal-geometry normalized RMSE is 0.059396 for TSK and 0.047839 for Extra Trees. This is not prospective absolute-SPL transfer.

The original October 2026 UCI download bytes and original historical fitted-state bytes remain unavailable. The newly reconstructed states are separate replay outputs.

## Rights and provenance

See `LICENSE_SCOPE.md`. MIT applies only to original H3Air research code for which the relevant rights holders approved it. CC BY 4.0 applies only to original authored documentation and derived research records for which the relevant rights holders approved it. Third-party measurements and other materials retain their upstream conditions; no source-data licence is transferred to project code. Confidential correspondence, reviewer material, credentials, publisher classes/logos, and Bristol raw HDF5 are excluded.

Original data sources: [NASA/UCI](https://doi.org/10.24432/C5VW2C), [Southampton](https://doi.org/10.5258/SOTON/398169), [UCI Concrete](https://doi.org/10.24432/C5PK67). The Bristol source is cited only in the manuscript and is not rehosted.

