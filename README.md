# R19 — Airfoil TSK Local-Statement Robustness and Southampton LOGO Benchmark

Research code, reported outputs, source-data provenance, and integrity checks for the **R19 Southampton leave-one-geometry-out (LOGO)** extension of the manuscript:

*Local-Statement Robustness in Takagi–Sugeno Airfoil Self-Noise Regression: A Finite-Input Audit*.

## Reproducibility files

The independently verified source-to-result archive, executable verifier, code, candidate tables, and result summaries are under [`R19_EXTERNAL_TRANSFER/`](R19_EXTERNAL_TRANSFER/README.md).

Run the dependency-free snapshot audit from the repository root:

```bash
python3 R19_EXTERNAL_TRANSFER/VERIFY_RELEASE.py
```

For full model fitting, extract the R19 ZIP, install the pinned scientific dependencies, and follow the [reproduction instructions](R19_EXTERNAL_TRANSFER/README.md). The quick check validates archived bytes and predictions; it **does not retrain models**.

## Verified scope and findings

- 343 frequency observations, 38 spectra and seven geometries, all from **one** Southampton experimental archive.
- Geometry-held-out model evaluation with inner spectrum-grouped tuning on training data.
- Equal-geometry RMSE on the **dimensionless source-normalized response**: **TSK 0.0593961028381699**, **Extra Trees 0.04783880803883461**.
- Corrected selection over 12 Extra Trees candidate settings per geometry; full recorded output and independent numerical replay.
- Small absolute Gaussian firing can coexist with apparently strong normalized weights; this does not establish a calibrated error-risk detector.
- All local-statement findings depend on the specified fitted models, training support, and numerical budgets.

**Important limitations:** This is **not** absolute sound-pressure-level prediction in dB on a calibration-free new aerofoil; seven geometries do not represent seven independent experimental campaigns; the work makes no causal aerodynamic claim.

## Lineage and provenance

The [parent NASA/UCI TSK research repository](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility) retains the earlier R5–R9 evidence, as well as the original copy of this independently checked R19 extension. That repository and the locked R18 NASA scientific results are unchanged by creating this dedicated R19 repository.

Southampton dataset: Lau and Kim, DOI [10.5258/SOTON/398169](https://doi.org/10.5258/SOTON/398169). NASA/UCI Airfoil Self-Noise benchmark: DOI [10.24432/C5VW2C](https://doi.org/10.24432/C5VW2C). See [attribution and claim limits](R19_EXTERNAL_TRANSFER/ATTRIBUTION_AND_LIMITS.md).

## Publication and license status

This is a public **research-reproducibility snapshot**, **not** a published journal article or Zenodo deposit. The IEEE Access manuscript is still in author review. **No software license has been approved or granted here**; original dataset terms and attribution must be respected. Public access does not itself authorize unrestricted software reuse.
