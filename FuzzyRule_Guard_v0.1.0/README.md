# FuzzyRule Guard v0.1.0 — TSK local-slope auditor

A runnable research companion to *Beyond Prediction Accuracy: Local-Slope Robustness in Takagi–Sugeno Fuzzy Models of Airfoil Self-Noise*. This is a prototype, not an industrial safety or physical-causality certificate. It does not retrain models or certify antecedent relearning, extrapolation, or unrestricted continuous-domain behavior.

## What it does

For a user-supplied frozen first-order ridge-TSK consequent design, fitted coefficients, centered-target information, and the declared perturbation budgets, the command-line tool generates a numerical upper bound for movement towards zero or an explicitly checked opposite-sign coefficient vector. It reports **PROTECTED**, **REVERSIBLE**, or **UNRESOLVED**. The last status is intentional: failure to find a witness is never evidence of protection. Optional held-out design rows are evaluated for each found witness, not used to construct it. Outputs are CSV and JSON, including dual arrays where applicable and alternative coefficient vectors.

The objective is the mean squared training residual plus a full-coefficient positive ridge penalty. Fixed preprocessing, coefficient ordering, antecedents, and consequent basis must be supplied consistently by the user. All certificates are floating-point checks, not interval-arithmetic proofs. No automatic physical support certification, MATLAB importer, or graphical interface is included.

## Install and run

Tested with Python 3.13.5, NumPy 2.3.5 and SciPy 1.17.0. In a local directory containing the two Python files:

```bash
python -m pip install numpy==2.3.5 scipy==1.17.0
python fuzzyrule_guard.py self-test
python fuzzyrule_guard.py audit my_model.npz --epsilon 0.1 --eta 0.01 --block-size 6 --out my_report
```

Here epsilon is in the response's units, eta is a fraction (0.01 = 1%), and the default strict reversal target has magnitude 0.001 times the original coefficient. Use --indices 1,2,3 or a correct --block-size (intercept then slopes in every rule block). The NPZ may instead contain R, the rule count, to infer block size. Indexing is zero-based.

### Input NPZ format

| Key | Meaning |
| --- | --- |
| P | n-by-q training consequent design; each row contains normalized rule firing weights multiplied by the relevant intercept/input basis |
| beta | q-vector of frozen parent consequent coefficients |
| ytrain | n-vector of original training targets |
| offset | scalar target offset used by the parent fit (zero if none) |
| lam | scalar positive ridge penalty in mean-squared-error convention |
| Pt | optional held-out consequent design with q columns |
| R | optional integer rule count for intercept-first equal-size rule blocks |

Keep the training/test split, unit convention, feature scaling, and coefficient basis consistent. The tool does not infer the physical meaning of a coefficient or choose engineering tolerances for you.

## Reproduce the NASA regression check

Download [AF4 scientific evidence](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/releases/download/h3air-r21r8-ep18-evidence-v1/57H3Air_EP18_AF4_Scientific_Evidence.zip), SHA-256 1edd543fb6544f8bd23de418b3108f1617518251bf35a2cb18ec966d5a7225dd. This is an existing authorized public archive, not a new deposit.

```bash
python fuzzyrule_guard.py replay-af4 57H3Air_EP18_AF4_Scientific_Evidence.zip --out saved_replay
python test_all_folds.py 57H3Air_EP18_AF4_Scientific_Evidence.zip fresh_replay
```

Do not use Python -O. The first command rechecks the original saved certificates/witnesses; the second generates fresh numerical decisions from the ten frozen parent model states and compares them with the archived classifications. Neither refits a parent model. Both checks passed 510/510 in the tested local environment at epsilon = 0.1 dB and eta = 0.01, yielding 403 protected and 107 reversible coefficients. The largest training change among the newly generated strict-reversal witnesses was 0.09995415181643541 dB; maximum relative objective increase was 0.0031667758780086785. The new witnesses need not be identical to the original witnesses; do not substitute their transport counts for the manuscript's historical counts.

## Scope and rights

No numerical result of the paper has been replaced; the software is an additional implementation/verification route. The public AF4 archive and its component-level licences remain unchanged. Original UCI source attribution: Brooks, Pope and Marcolini, *Airfoil Self-Noise*, DOI 10.24432/C5VW2C. Research archive DOI 10.5281/zenodo.24480002 identifies the earlier EP11 deposit, not this later tool and not an article DOI. No new formal reuse licence is asserted for the new prototype. No private manuscript, correspondence, or restricted external data is distributed here.
