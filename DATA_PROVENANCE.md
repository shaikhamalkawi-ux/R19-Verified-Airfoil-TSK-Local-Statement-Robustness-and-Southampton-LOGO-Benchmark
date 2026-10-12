# Dataset provenance, transformation and reuse terms

This research uses **two distinct datasets** that must not be conflated.

| Resource | Citation and source | License shown by original source | Study role |
| --- | --- | --- | --- |
| Southampton aerofoil trailing-edge spectra | Lau, A. S. H., & Kim, J. W. (2016), *Dataset for “A study on the prediction of aerofoil trailing-edge noise for wind-turbine applications”*. University of Southampton. [DOI 10.5258/SOTON/398169](https://doi.org/10.5258/SOTON/398169); [source landing page](https://eprints.soton.ac.uk/398169/) | **Creative Commons Attribution**; the public record does not clearly identify a version, so no version is assumed here | 343 frequency rows, 38 spectra, seven geometries; R19 geometry-held-out audit |
| NASA/UCI Airfoil Self-Noise | Brooks, T., Pope, D., & Marcolini, M. (1989). *Airfoil Self-Noise* [Dataset]. UCI Machine Learning Repository. [DOI 10.24432/C5VW2C](https://doi.org/10.24432/C5VW2C); [dataset page](https://archive.ics.uci.edu/dataset/291/airfoil+self-noise) | **CC BY 4.0**, as stated by UCI | Main 1,503-row / 106-configuration work, held in the parent project and its archive |

## Southampton data lineage

The original `DataFiles.zip` is retained within the full source-to-result ZIP. A deterministic parser extracts **experimental** observations and omits source model-prediction columns. The resulting canonical `SOUTHAMPTON_CANONICAL.csv` has 343 rows, 38 distinct spectra and seven geometries.

The target `response_norm` is **source-normalized experimental response**, not an absolute measurement in dB. Its normalization uses experimentally measured reference maxima, which are not necessarily available for a new unmeasured geometry. Consequently, the archived LOGO evaluation does **not** establish practical calibration-free absolute-noise prediction.

Each outer fold excludes an entire geometry. Model fitting and hyperparameter selection use training-only data, with inner folds grouped by spectrum. Seven geometries in one archive are not seven independent laboratories.

## Verifiable source hashes (SHA-256)

| Byte stream | Recorded SHA-256 |
| --- | --- |
| Original Southampton `DataFiles.zip` | `5cf21445afb0b32bbadf1b94550ea8a9d8561a23aac94f8ad49aab95f152f8eb` |
| Canonical Southampton CSV | `b7cfb8f60bbfee139ce6c9183a16de46979152906a35b55fbba22f34557e7fd4` |
| Public R19 source-to-result ZIP | `f932dd9f8c2fd269935738b51cbb5a00f3cba67bd25ad0b3904741fa9b9fed6c` |

The verifier checks these hashes alongside 84 manifested payload files.

## Code versus data permissions

Dataset-specific rights and attribution **do not grant a license to this project's Python software**. The repository remains without a project `LICENSE` until the responsible author approves an appropriate software license. Public GitHub visibility by itself is not authorization for unrestricted source-code reuse. Third-party attribution must remain visible.
