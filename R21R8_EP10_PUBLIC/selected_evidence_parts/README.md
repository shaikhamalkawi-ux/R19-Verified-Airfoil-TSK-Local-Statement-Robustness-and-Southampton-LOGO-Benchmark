# EP10 selected computational evidence: public access and verified scope

This folder publicly exposes the **19-piece, 13,508,700-byte** source/evidence archive. It contains 548 included code, derived-data, model-state, and numerical-witness records, plus 3 provenance/hash files (551 ZIP members). All 19 parts are required.

## Obtain and verify
Download every `H3Air_EP10_public_evidence.zip.part001` through `part019` in this folder, leaving filenames unchanged. Run `python reassemble_and_verify.py` in the downloaded directory. The script checks each part's SHA-256, reconstructs the ZIP, and checks every inside-file SHA-256. On macOS/Linux, concatenate by ascending part number and verify the full archive's hash.

**Expected whole-ZIP SHA-256:** `f2e237822c9e9f3618a6bdd74707874e1a60e323c2447bd0ff92d7895572fc61`.

## Contents and provenance
- Python source for selected R11/R12/R15/R17 and R18 fuzzy/TSK experiments.
- Source-derived NASA/UCI experimental numeric records, derived model comparisons and ablation outputs.
- Source-derived Southampton 2016 normalized experimental spectra and numerical record files.
- Frozen selected parent states and constructed coefficient-sign reversal witnesses. These are not new acoustic measurements.

## What is intentionally excluded
- The unrecovered original historical per-replicate internal bootstrap states, and the separate 27,998 recomputed-state collection (approximately 773 MB in 40 controlled Drive task archives). This is a **selected**, not an exhaustive, reproducibility release.
- Publisher article PDFs, IEEE class/template files, private author workbooks, credentials, correspondence, reviewer-response letters and unpublished manuscript files.
- EP10 science is author-review pending formal IEEE resubmission; the highlighted PDF has intentionally been deferred until final closure.

## Rights and data sources
NASA/UCI Airfoil Self-Noise, DOI https://doi.org/10.24432/C5VW2C, **CC BY 4.0**; University of Southampton aerofoil dataset by Lau and Kim, DOI https://doi.org/10.5258/SOTON/398169, **Creative Commons Attribution**. Appropriate credit and source terms are recorded in the archive's `DATA_SOURCES_AND_LICENSES.md`.

**Research code is publicly viewable/downloadable, but a permissive reuse licence for author-generated software has NOT been approved by all rightsholders.** Do not describe it as MIT/CC BY software or a published Zenodo deposit until those gates close.

This EP10 archive is distinct from the existing publicly browsable R19 transfer code in the repository.
