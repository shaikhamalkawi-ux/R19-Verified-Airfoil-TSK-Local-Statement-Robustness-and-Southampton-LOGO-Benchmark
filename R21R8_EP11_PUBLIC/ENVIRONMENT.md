# Reproducibility environment and checks

The source-recorded R5 execution environment used Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, scikit-learn 1.8.0, XGBoost 3.1.3, pandas 2.2.3, and matplotlib 3.10.8. These versions are in `requirements.txt`. The released `verify_release_assets.py` uses only the Python standard library, so it can be run without installing the full model-fitting environment.

Verification levels:

1. `verify_release_assets.py` checks the 40 exact ZIP bytes and internal integrity, journal coverage, all state-file hashes, and the two recorded failures. This is repeatable from the public release alone.
2. The author-recorded independent numerical QA compared all successful replayed states with original frozen R5 saved arrays under absolute tolerance 1e-7 and relative tolerance 1e-9. The historical saved arrays and per-draw registers are a separate dependency and are not supplied in this release. The audit report is supplied as evidence, but its full historical comparison cannot be rerun from these public assets alone.
3. Refit experiments use the original R5 scripts in the NASA parent repository and the frozen source/split records. A full rerun can depend on external source data and historical inputs. This release does not claim byte-for-byte recovery of earlier internal states.

The current official UCI airfoil file was compared numerically with all 9,018 cells in the inherited derived table; the first October 2026 download bytes remain unavailable.

