# R21R8-EP2 companion-study status — 22 November 2026

This is a **documentation update to the historical public R19 Southampton LOGO benchmark**, not a replacement of its source ZIP, original held-out predictions, code, source licensing, or benchmark QA. The separate NASA parent study has advanced to **R21R8-EP2 author review** for a potential IEEE Access resubmission. No journal acceptance, resubmission, final Zenodo publication, or software reuse license is claimed.

## The Southampton experiment remains unchanged

- Experimental source: [University of Southampton, DOI 10.5258/SOTON/398169](https://doi.org/10.5258/SOTON/398169).
- Analysis: **343 source-normalized observations, 38 complete spectra, 7 geometry labels**, grouped leave-one-geometry-out. This is **one public archive**, not seven independent facilities.
- Equal-geometry, **dimensionless** RMSE: **0.059396** for TSK-ridge vs **0.047839** for Extra Trees.
- Relative antecedent-activation cutoff flags **30/343** rows; **10/30** flagged rows nevertheless have normalized max rule weight ≥ 0.9.
- The source-normalized response derives from observed experimental maxima, so these results **cannot establish calibration-free absolute dB prediction** for a new geometry. The R19 scientific computations were **not changed** by the current status update.

## How this relates to the NASA study

The primary NASA study evaluates 1,503 UCI rows in 106 operating configurations and a distinct *finite-training-input, frozen-antecedent coefficient-sign* question. Its original **0.1-dB pointwise / 1% ridge-objective** audit finds **403 protected / 107 strict-reversible signs** among 510. A new **1.0-dB pointwise / 1% objective** contextual sensitivity finds **135 protected / 375 strict-reversible signs** among 510.

The contextual 1-dB value comes from a historical statement about **general agreement between processed microphone-pair spectra** in [NASA RP-1218 (1989), Appendix A, printed p. 104](https://ntrs.nasa.gov/citations/19890016302). It is **not an instrument calibration uncertainty for each UCI observation**. The 0.1-dB headline result remains unchanged.

The historical R5 code and seeds were used to **recompute 28,000 bootstrap attempts across 40 tasks**, with **27,998 successes and two reproduced FCM nonconvergences**. These are **new fitted state files**, not recovered October 2026 historical internal-state bytes. The full 773,361,055-byte replay archive remains under controlled author review and is **not contained in this R19 repository**. Current raw UCI data (1,503×6) agree with the historical derived source table at all 9,018 numerical cells within 1e-12, but the original October acquisition-file SHA-256 is unavailable.

## Reuse, sharing and archival status

The public R19 source-to-result ZIP and `R19_EXTERNAL_TRANSFER/VERIFY_RELEASE.py` still verify the **historical saved R19 results**; they **do not refit** the 2026 R21R8-EP2 study. External source licenses do not automatically license author-written algorithms. No `LICENSE` file has been approved for the research software; published GitHub source visibility alone does not confer software reuse rights.

An older, **unpublished Zenodo draft** exists for a prior study version, and preparing a repository deposit **before IEEE article acceptance** is now under consideration. The creator list, file versions, rights and metadata must be checked and updated before any public release. There is currently **no published R21R8-EP2 Zenodo DOI**. Neither this file nor any GitHub commit is evidence that a draft has been published.

The author-review manuscript and referee response are **not reproduced in this public repo**, and no confidential draft-preview token is included. For public evidence of the historical Southampton calculation, use the unchanged R19 ZIP and its frozen verification script. 
