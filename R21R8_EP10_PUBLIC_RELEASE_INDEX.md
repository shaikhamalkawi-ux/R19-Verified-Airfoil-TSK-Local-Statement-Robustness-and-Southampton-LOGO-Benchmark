# Project 57 H3Air — R21R8-EP10 public release index

**Status as of 2026-11-23:** This repository is PUBLIC. The R19 Southampton source-to-result benchmark is already publicly browsable. R21R8-EP10 is the **author-approved scientific manuscript version being prepared for IEEE Access resubmission**; publication of its complete scientific/evidence archive is still being staged and verified, not represented as finished here.

**Article title:** Beyond Prediction Accuracy: Local-Slope Robustness in Takagi–Sugeno Fuzzy Models of Airfoil Self-Noise

**Previous IEEE Access manuscript:** Access-2026-52679 (resubmission not yet submitted; article not accepted).

## Available immediately

- [R19 external-transfer research code, derived datasets and numerical evidence](R19_EXTERNAL_TRANSFER/)
- [R19 integrity verifier](R19_EXTERNAL_TRANSFER/VERIFY_RELEASE.py)
- [R19 reproduction protocol](REPRODUCE.md)
- [NASA/UCI parent public code and evidence](https://github.com/shaikhamalkawi-ux/naca0012-tsk-rule-reproducibility)
- [NASA/UCI official measurements](https://doi.org/10.24432/C5VW2C), CC BY 4.0.
- [Southampton official experimental measurements](https://doi.org/10.5258/SOTON/398169), subject to source conditions.
- [UCI concrete official measurements](https://doi.org/10.24432/C5PK67), CC BY 4.0.

## EP10 materials to be uploaded and verified (NOT claimed as present here yet)

- Clean EP10 manuscript and 27-page supplementary methods PDF; editable LaTeX source, figures, bibliography.
- Additional File 2: 160 selected post hoc executable/code/scalar records.
- Additional File 3: 49 selected frozen-parent state/witness files plus the scoped README and file manifest.
- The public-safe EP10 method scripts, fixed results, source-admission/census records and checksums.
- Full 40-task deterministic bootstrap replay (**28,000 attempts, 27,998 successes, two historical fitting failures**) **only after** a file-level privacy, third-party rights, provenance and reproducibility check. These are NEWLY replayed internal fitted states, not recovered original historical fitted-state bytes.

## Scientific boundaries

NASA 0.1 dB / 1%: 403 protected and 107 strictly reversible slopes out of 510. Separate 1.0 dB / 1% sensitivity: 135 protected and 375 strictly reversible. Neither prediction tolerance is an observation-level calibrated uncertainty bound.

Southampton LOGO results are in **source-normalized dimensionless response units**, with maximum reference information from the experimental source; they are **not** prospective calibration-free absolute-SPL predictions for an unmeasured airfoil. R19 source records are unchanged.

The UCI concrete source/split sensitivity is an exploratory source-and-grouping audit; no causal physical conclusion follows.

## Publication and rights

- A **public repository is not, by itself, an open-source copyright licence**. As of this index no author-approved standalone software licence has been issued for all project code. A proposed SPDX-identified licence must be approved by copyright holders before a `LICENSE` is added. Do not assume permission for every third-party file.
- Do not redistribute copyrighted journal PDFs, unpublished correspondence, passwords, secret links, reviewer letters, provider-controlled files or Bristol HDF5 source material without confirming rights.
- Zenodo draft 23330537 was mentioned in archived planning documents. **Its current publication state and DOI must be verified in Zenodo** before citing it as published. Do not put a draft-only reservation URL or fabricated DOI into the article.
- Final highlighted manuscript is intentionally deferred for final editorial comparison. The six authors' approval of the revised manuscript was reported by the corresponding project user; final portal author and declaration fields remain separate checks.

## Staged release checklist

1. Verify EP10 bytes against the signed/verified local manifest; scan all file members for rights/privacy.
2. Upload allowed self-authored code and derived records, evidence files and document sources under `R21R8_EP10/`; use Git LFS or Releases for files over GitHub's normal limits.
3. Re-run fixed-archive verification, compile the clean LaTeX, publish a SHA-256 manifest of actual online objects.
4. Record the exact GitHub commit and public release link. After Zenodo **publication**, add the actual Zenodo DOI and create a matching manuscript Data Availability change in a new locked source package.
5. Confirm that the public documentation truthfully distinguishes released material from controlled/original-unrecovered artifacts.

This index tracks real public availability; it is not a declaration that steps 1–5 have all been completed.
