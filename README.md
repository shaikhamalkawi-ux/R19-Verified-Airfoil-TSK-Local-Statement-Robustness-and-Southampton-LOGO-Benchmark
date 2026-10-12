# Local-Statement Robustness in Takagi–Sugeno Airfoil Self-Noise Regression: A Finite-Input Audit

**R19 Southampton Leave-One-Geometry-Out (LOGO) Benchmark — Source, Data, Results and Reproducibility**

[![R19 verification](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/actions/workflows/verify-r19-snapshot.yml/badge.svg)](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/actions/workflows/verify-r19-snapshot.yml)

This is the computational companion to the **author-review** manuscript *Local-Statement Robustness in Takagi–Sugeno Airfoil Self-Noise Regression: A Finite-Input Audit*, being prepared for **IEEE Access**. The scientific question is whether predictive accuracy is sufficient to support claims about the stability of individual Takagi–Sugeno (TSK) fuzzy-rule statements. **The journal manuscript has not been accepted or published; no article or Zenodo DOI is assigned.**

## Two datasets — different targets and audit scopes

| Component | Scope | Target and purpose | Reproducibility source |
| --- | --- | --- | --- |
| NASA/UCI Airfoil Self-Noise (primary) | 1,503 observations, 106 operating configurations | Held-out sound-pressure predictions in **dB**, relearned-rule matching, finite-input local-statement audits | [Parent NASA/UCI research repository](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility); **not fully replayed by this R19-only ZIP** |
| Southampton aerofoil spectra (R19) | 343 frequency observations, 38 spectra, 7 geometries from **one** source archive | Held-out geometry evaluation on a **dimensionless source-normalized response**, and rule-activation/statement diagnostics | **This repository** — `R19_EXTERNAL_TRANSFER/` |

The Southampton response uses reference maxima derived from experimental targets. Its errors **must not be reported in dB**, and LOGO evaluation is **not** evidence of calibration-free absolute-noise prediction for a truly new geometry.

## R19 recorded results

Seven outer folds exclude all rows and spectra of the held-out geometry. Within each fold, four-fold spectrum-grouped tuning, feature scaling, clustering and fitting use training data only. The corrected search evaluates **12 Extra Trees configurations** and **45 TSK configurations** per geometry.

| RMSE (dimensionless source-normalized response) | TSK-Ridge | Extra Trees |
| --- | ---: | ---: |
| Equal-geometry | 0.059396 | **0.047839** |
| Equal-spectrum | 0.056368 | **0.043227** |
| Equal-row | 0.055492 | **0.041538** |

Extra Trees has lower aggregate predictive error. Separately, **30/343** held-out rows fall below the fold-specific training-only fifth-percentile absolute Gaussian activation cutoff; **10/30** still have a highest normalized rule weight of at least 0.9. This is a normalization/coverage diagnostic, **not** a calibrated error-risk score. **18/18** tested local frequency slopes in the refitted LOGO models are conditionally protected at the declared finite-input/ridge budgets; this is not a physical law or cross-geometry certification.

## Find the right file

| Path | Purpose |
| --- | --- |
| [`R19_EXTERNAL_TRANSFER/README.md`](R19_EXTERNAL_TRANSFER/README.md) | Exact R19 scope, source-to-result layout, locked findings and scientific limits |
| [`R19_EXTERNAL_TRANSFER/VERIFY_RELEASE.py`](R19_EXTERNAL_TRANSFER/VERIFY_RELEASE.py) | Python-standard-library-only checksum, split/candidate-table and fixed-output verifier |
| [Complete R19 source-to-result ZIP](R19_EXTERNAL_TRANSFER/R19_Southampton_ExternalTransfer_SourceToResult_Public.zip) | Original source, executable scripts, inner/outer splits, saved NPZ states, predictions, candidate tables and diagnostics |
| [`R19_EXTERNAL_TRANSFER/code_reference/`](R19_EXTERNAL_TRANSFER/code_reference/) | Browsable code mirrors and pinned scientific dependencies |
| [`R19_EXTERNAL_TRANSFER/data/`](R19_EXTERNAL_TRANSFER/data/) | Canonical source-normalized data |
| [`R19_EXTERNAL_TRANSFER/results/`](R19_EXTERNAL_TRANSFER/results/) | Selected benchmark, coverage, role-sensitivity and replay results |
| [`REPRODUCE.md`](REPRODUCE.md) | Fast verification versus full model refitting |
| [`DATA_PROVENANCE.md`](DATA_PROVENANCE.md) | Dataset DOIs, source licenses, hashes and normalization details |
| [`METHODS_AND_LIMITS.md`](METHODS_AND_LIMITS.md) | Registered methods, results and restricted scientific claims |
| [`CITATION.md`](CITATION.md) | Interim repository citation with no invented article DOI |
| [`PUBLICATION_STATUS.md`](PUBLICATION_STATUS.md) | Author-review, software license and archival status |

## Quick reproducibility check

From the repository root:

```bash
python3 R19_EXTERNAL_TRANSFER/VERIFY_RELEASE.py
```

This checks the **89-entry** ZIP with **84 SHA-256 manifested payloads**, source hashes, train/test partitions, candidate-grid counts, and RMSE reconstructed from **saved held-out predictions**. It does **not** retrain the models. For full refitting, extract the ZIP and follow [REPRODUCE.md](REPRODUCE.md). The recorded scientific environment uses Python 3.13.5 and pinned package versions.

Frozen ZIP SHA-256:

```text
f932dd9f8c2fd269935738b51cbb5a00f3cba67bd25ad0b3904741fa9b9fed6c
```

## Attribution, scope and status

Southampton data: [Lau and Kim (2016), DOI 10.5258/SOTON/398169](https://doi.org/10.5258/SOTON/398169), listed under a Creative Commons Attribution license. NASA/UCI Airfoil Self-Noise: [DOI 10.24432/C5VW2C](https://doi.org/10.24432/C5VW2C), CC BY 4.0. Data-source permissions do **not** automatically license original analysis code. **No project software license has been author-approved;** no license is represented as granted.

All seven Southampton geometries are from one source archive, not seven independent experiments. The effect of altering antecedent inputs is a model-specific, post hoc diagnostic, not causal feature importance. The earlier NASA benchmark and locked R18 scientific results are not superseded by this R19 extension.

For questions, use [GitHub Issues](../../issues). **Zenodo deposition and DOI assignment will be considered only after journal acceptance**, as requested by the project owner. Neither journal acceptance nor a formal GitHub Release is claimed.
