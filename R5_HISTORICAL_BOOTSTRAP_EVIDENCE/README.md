# H3Air — historical R5 stored-output evidence (26 November 2026)

This archive preserves original historical R5 numerical records, independently extracted from the verified October R6 archive. The 285 original payloads are byte-identical to the historical R5 internal manifest. It is complementary to, and not a replacement for, the EP11 40-task newly reconstructed bootstrap states. No new model fitting, journal submission, article DOI, or article acceptance is asserted.

## Contents

- Forty task folders, F4/F5 × ten outer folds × compact/reference, containing 80 original NPZ branch-result files, 80 original replicate CSV registers, 40 completion JSONs, and 40 summary CSVs.
- Forty original training-fold parent-state NPZs, including train/test indices, fitted scaling, centers/widths and parent coefficients, and saved parent activations. They are not complete per-bootstrap-draw antecedent states.
- The historical derived NASA/UCI input CSV and four historical aggregate tables; the October 7 source-verification record, selected original manifest, and a new verification script/report.
- No private R6/R5 full archive, publisher PDFs, third-party mirror bytes, private correspondence, or unrelated external-source measurements.

## Replay and independent stored-output verification

Unzip the complete archive into a directory, then run `python verify_historical.py` with Python 3 and numpy, scipy, pandas installed. For a multipart GitHub delivery, extract every numbered task ZIP and the metadata ZIP into the SAME directory before running the verifier. The task ZIPs are independently valid ZIPs, not concatenated split volumes. See `ORIGINAL_SELECTED_MANIFEST.json` for the SHA-256 of each original payload. The independent verifier tests original file hashes, deterministic seed sequence, parent/train/test consistency, stored assignment matrices and thresholds, the nine saved numerical summary metrics per branch/fit, and the aggregate tables. It does not retrain the models. Successful arrays are stored in register success order, not by raw attempt index; the seeds array covers all attempts, including the two failed slots.

The verification reports 28,000 attempts (20,000 fixed, 8,000 relearned), 27,998 successes and two failures. Both historical F5 relearned failures are retained. The original arrays retain paired LS/Ridge predictions, aligned coefficient arrays, rule assignments, weighted similarities and seeds. The original per-draw FCM centers, widths, scaler statistics and membership arrays were not saved for all relearned draws; they remain unavailable historically. EP11 separately archives the newly reconstructed states. Historical first-download official UCI bytes and their contemporaneous checksum have not been recovered. The historical derived CSV is verified against the October 7 record and public Git blob; the pinned mirror matches 9,018/9,018 numeric values. These facts do not prove byte identity of the first official download.

## Attribution and rights

Airfoil Self-Noise: Brooks, T., Pope, D., & Marcolini, M. (1989). UCI Machine Learning Repository, DOI https://doi.org/10.24432/C5VW2C (CC BY 4.0). The derived input adds row/group identifiers and represents source numbers in CSV; upstream attribution applies. The pinned mirror is referenced by commit and blob in `SOURCE_PROVENANCE.json`, not redistributed. See `LICENSE_SCOPE.md` for the original H3Air materials. Cite the H3Air research archive and its six authors, as listed in the existing EP11 public archive. This archival addendum is separate from the previously reported EP11 Zenodo record; it is not claimed to be deposited there.
