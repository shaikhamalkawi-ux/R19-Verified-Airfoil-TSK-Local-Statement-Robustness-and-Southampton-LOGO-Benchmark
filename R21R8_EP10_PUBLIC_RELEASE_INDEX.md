# Project 57 H3Air — R21R8-EP10 public release index

**Status as of 2026-11-23:** This repository is PUBLIC. The R19 Southampton source-to-result benchmark is already publicly browsable. R21R8-EP10 is the **author-review manuscript version being prepared for possible IEEE Access resubmission**; Two selected public EP10 archives are now online and SHA-256-verified by GitHub Actions. The complete 28,000-attempt new-state archive is not yet public.

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

## Public EP10 archives — verified and accessible now

- **[EP10 manuscript, supplementary PDF, editable LaTeX and authored figures](R21R8_EP10_PUBLIC/57H3Air_R21R8_EP10_Public_Preprint_and_Editable_Source.zip)** — 4,043,013 bytes, SHA-256 `1b36bcdbd9859dc3721a782279aa81f4e97fed3d5c0fb065377bbb7dc4ea4d52`.
- **[EP10 selected analysis code, derived records and fitted-state/witness evidence](R21R8_EP10_PUBLIC/57H3Air_R21R8_EP10_Public_Selected_Code_and_Numerical_Evidence.zip)** — 12,089,248 bytes, SHA-256 `10c766acb2f0669aaf9d760c55bf17daba96a8cb827217f1ba6a0229c80ff091`.
- [Live GitHub Actions verification](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/actions/workflows/assemble-ep10-public.yml) verifies ZIP CRC, inner member hashes, exact outer SHA-256 and byte counts.
- Original reviewer comments/response correspondence are **excluded** from this public source publication. An IEEE journal-facing author-response DOCX/PDF is available only through controlled author sharing.

## Still pending — not claimed as public

- Full 40-task newly reconstructed bootstrap state archive (**28,000 attempts, 27,998 successes, two fitting failures**). Only the selected evidence is public above; remaining files require separate release and hash audit.
- Formal project-wide software reuse license, explicit contributor permission for that license and an actual published Zenodo DOI.
- Any later clean manuscript containing a Zenodo DOI must be a separately verified version; the DOI is not yet inserted.


## Scientific boundaries

NASA 0.1 dB / 1%: 403 protected and 107 strictly reversible slopes out of 510. Separate 1.0 dB / 1% sensitivity: 135 protected and 375 strictly reversible. Neither prediction tolerance is an observation-level calibrated uncertainty bound.

Southampton LOGO results are in **source-normalized dimensionless response units**, with maximum reference information from the experimental source; they are **not** prospective calibration-free absolute-SPL predictions for an unmeasured airfoil. R19 source records are unchanged.

The UCI concrete source/split sensitivity is an exploratory source-and-grouping audit; no causal physical conclusion follows.

## Publication and rights

- A **public repository is not, by itself, an open-source copyright licence**. As of this index no author-approved standalone software licence has been issued for all project code. A proposed SPDX-identified licence must be approved by copyright holders before a `LICENSE` is added. Do not assume permission for every third-party file.
- Do not redistribute copyrighted journal PDFs, unpublished correspondence, passwords, secret links, reviewer letters, provider-controlled files or Bristol HDF5 source material without confirming rights.
- Zenodo draft 23330537 was mentioned in archived planning documents. **Its current publication state and DOI must be verified in Zenodo** before citing it as published. Do not put a draft-only reservation URL or fabricated DOI into the article.
- Final highlighted manuscript is intentionally deferred for final editorial comparison. Final approval from all six authors, their contribution and declaration records, and portal confirmation must still be documented; no signed author approval is claimed here.

## Staged release checklist

1. Verify EP10 bytes against the signed/verified local manifest; scan all file members for rights/privacy.
2. Upload allowed self-authored code and derived records, evidence files and document sources under `R21R8_EP10/`; use Git LFS or Releases for files over GitHub's normal limits.
3. Re-run fixed-archive verification, compile the clean LaTeX, publish a SHA-256 manifest of actual online objects.
4. Record the exact GitHub commit and public release link. After Zenodo **publication**, add the actual Zenodo DOI and create a matching manuscript Data Availability change in a new locked source package.
5. Confirm that the public documentation truthfully distinguishes released material from controlled/original-unrecovered artifacts.

This index tracks real public availability; it is not a declaration that steps 1–5 have all been completed.

## Supplementary public EP10 evidence release (SHA-verified)

- [Selected EP10 computational source, results, frozen parents, and reversal witnesses — 548 research records](R21R8_EP10_PUBLIC/selected_evidence_parts/README.md). This is a separately curated 13,508,700-byte public ZIP published as 19 downloadable parts; [reassembly verifier](R21R8_EP10_PUBLIC/selected_evidence_parts/reassemble_and_verify.py) and per-part SHA-256 manifest are provided.
- [Controlled full-replay audit code and QA (86,633-byte ZIP)](R21R8_EP10_PUBLIC/R21R8_Controlled_Evidence_Audit_Code.zip).
- [GitHub Actions PASS: all 19 parts, archive SHA-256 and internal file hashes](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/actions/runs/45244387971).
- **Not** the full 27,998-state new replay archive; author-controlled archive size is about 773 MB and still needs a permitted Zenodo/access decision.
