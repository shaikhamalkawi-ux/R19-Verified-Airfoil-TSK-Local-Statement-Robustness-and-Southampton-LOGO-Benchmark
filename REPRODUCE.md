# Reproduce the R19 Southampton external-geometry results

This repository supports two distinct levels of verification: **fixed-archive numerical integrity** and **full scientific model refitting**. A PASS in the first does not imply that fitting was rerun.

## 1. Fast audit — no external packages

From the repository root, run:

```bash
python3 R19_EXTERNAL_TRANSFER/VERIFY_RELEASE.py
```

The Python-standard-library verifier checks ZIP CRC, **84** payload SHA-256 hashes, original and canonical Southampton data hashes, 343 rows / 38 spectra / 7 geometries, disjoint geometry and spectrum splits, **12** Extra Trees and **45** TSK candidate records per outer fold, the saved NPZ structures and fixed-prediction metrics. It separately checks the 30 low-activation observations and the 10 observations with normalized rule weights at least 0.9.

Expected JSON values include `"status": "PASS"`, `"payload_files_verified": 84`, and:

| Measure | TSK | Extra Trees |
| --- | ---: | ---: |
| Equal-geometry RMSE | 0.0593961028381699 | 0.04783880803883461 |
| Equal-spectrum RMSE | 0.05636793120717745 | 0.04322684449353849 |
| Row RMSE | 0.055491916066947145 | 0.04153805373018892 |

To check the archive itself using SHA-256:

```bash
cd R19_EXTERNAL_TRANSFER
sha256sum -c PUBLIC_ZIP_SHA256.txt
```

GitHub Actions runs these quick checks on the public research snapshot. **It does not refit the models.**

## 2. Full source-to-model refitting

The recorded environment used **Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, scikit-learn 1.8.0 and threadpoolctl 3.6.0**. A compatible Linux/Bash environment is recommended; on Windows, use WSL or another Bash environment. The full rerun is more computationally demanding.

From the repository root:

```bash
unzip R19_EXTERNAL_TRANSFER/R19_Southampton_ExternalTransfer_SourceToResult_Public.zip -d r19_reproduction
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r r19_reproduction/R19_Executable_Reproduction/requirements_R19.txt
bash r19_reproduction/R19_Executable_Reproduction/run_full_reproduction.sh
```

The driver re-extracts the source data, checks canonical CSV byte identity, reselects hyperparameters using training-only spectrum folds, refits seven held-out geometry models, records candidates and model states, replays TSK/Extra Trees outputs numerically, and executes coverage, feature-role and conditional statement audits.

The historical preliminary `R19_Executable_Reproduction/57_H3_Airfoil_R19_LOGO_Candidate/run_logo_external.py` retains its original machine-specific `main()`. **Do not run that original file as a standalone entrypoint.** The portable script `run_logo_external_clean.py` reuses its fitting definitions, resolves correct paths and saves the reproducibility records.

## 3. Data and expected outputs inside the extracted ZIP

- `R19_Executable_Reproduction/R17_Southampton_External_Reproducibility/source/DataFiles.zip`: original attributed source.
- `R19_Executable_Reproduction/R17_Southampton_External_Reproducibility/data/SOUTHAMPTON_CANONICAL.csv`: frozen source-normalized 343-row table.
- `R19_Executable_Reproduction/R19_Clean_12grid/LOGO_PREDICTIONS.csv` and `LOGO_FOLDS.csv`: held-out observations and seven fold summaries.
- `.../candidates/`: 7 × 12 Extra Trees and 7 × 45 TSK candidate results.
- `.../states/` and `.../splits/`: saved numerical states and grouping audits.
- `.../SUMMARY.json`, `INDEPENDENT_REPLAY_QA.json`, `COVERAGE_AUDIT.json`, `FEATURE_ROLE_RETUNED_SUMMARY.csv` and `statement/LOGO_STATEMENT_SUMMARY.csv`: audit-specific endpoints.

## 4. Claim boundaries

The source-normalized target is **dimensionless**, not dB. No evidence of operational absolute-SPL transfer, physical causality, independently calibrated new geometry, error probability from activation, or universal rule stability follows from these checks. The R19 ZIP does **not** rerun the primary NASA 1,503-row/510-statement analysis; see the [parent project repository](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility).
