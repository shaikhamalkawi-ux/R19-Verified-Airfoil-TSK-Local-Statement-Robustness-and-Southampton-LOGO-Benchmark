# R19 experimental design, audited results, and claim limits

## Held-out geometry protocol

The Southampton R19 extension uses **343 frequency observations** organized into **38 spectra** and **seven geometry labels** from one archived experiment. There are seven outer leave-one-geometry-out (LOGO) evaluations, with each entire geometry excluded from fitting and hyperparameter choice. Inner selection uses four-fold **spectrum-grouped** cross-validation within the outer training sample. Scaling, fuzzy clustering and model fitting remain training-only.

| Fitted model | Registered candidate grid per outer geometry |
| --- | --- |
| Extra Trees (400 trees) | `min_samples_leaf` ∈ {1,3,5}, `max_features` ∈ {0.7,1.0}, `max_depth` ∈ {12,None} — **12** settings |
| First-order TSK-Ridge | rule count ∈ {2,4,6}, width factor ∈ {0.75,1.0,1.5}, ridge penalty ∈ {1e-6,1e-4,1e-2,1,100} — **45** settings |

The corrected R19 replay uses all 12 declared Extra Trees configurations. Its superseded candidate archive contained only three and is preserved solely for a transparent source-to-result discrepancy audit. It should **not** be presented as an equivalent clean run.

## Locked performance (source-normalized dimensionless response)

| Aggregation | TSK-Ridge RMSE | Extra Trees RMSE |
| --- | ---: | ---: |
| Equal geometry | 0.0593961028381699 | 0.04783880803883461 |
| Equal spectrum | 0.05636793120717745 | 0.04322684449353849 |
| Equal row | 0.055491916066947145 | 0.04153805373018892 |

Extra Trees has lower aggregate prediction error. This is a valid negative result for TSK predictive performance; the intended contribution is local-statement auditing, not a new predictor.

## Absolute versus normalized fuzzy firing

At the **training-only** fifth-percentile best absolute Gaussian firing cutoff, **30/343** held-out rows are low activation. Ten of those rows nevertheless have a maximum normalized firing weight ≥ 0.9. Relative membership dominance does not establish strong *absolute* rule coverage. Neither absolute nor normalized firing here is a calibrated error-risk score.

## Local statement robustness

**18/18** tested frequency-slope statements in the refitted LOGO training models are protected from zero at registered finite-training-input and relative ridge-objective budgets. This result is conditional on the fitted models, inputs and budgets. These budgeted constraints differ from the 0.1 dB NASA audit because the Southampton response is normalized. None of the 18 protected coefficients is thereby certified as a true causal aerodynamic relationship.

## Post hoc feature roles

Frozen-parameter and independently retuned feature-role ablations disagree in important ways, particularly for the trip indicator. The Southampton data do not cleanly replicate the NASA velocity-antecedent finding: velocity and chord are largely constant or confounded at the geometry level. Frequency is the primary within-spectrum varying predictor. No causal importance claim follows from these tests.

## Primary NASA versus this extension

The manuscript's primary NASA analysis uses **1,503 observations**, **106 operating configurations**, and local statement tests for **510 slopes** on an output measured in **dB**. Those results belong to the NASA scientific baseline and are not wholly reproduced by this R19-only repository. Consult the [parent R5–R9 evidence repository](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility) and its scientific project archive.

## Excluded conclusions

Do **not** claim absolute-noise transfer to an uncalibrated unseen geometry, seven independent experimental laboratories, generalization to all aerofoils, physical-law recovery, causal input importance, universal reliability of fuzzy explanations, or peer-reviewed validation merely because a GitHub check passes.
