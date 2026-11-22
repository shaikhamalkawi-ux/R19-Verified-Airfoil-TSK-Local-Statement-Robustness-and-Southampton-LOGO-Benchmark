# Publication, release, and reuse status

**Historical R19 snapshot: 12 October 2026; updated author-review context: 22 November 2026.**

- **Journal:** the manuscript *Local-Statement Robustness in Takagi–Sugeno Airfoil Self-Noise Regression: A Finite-Input Audit* is in **IEEE Access author-review / submission HOLD**, not accepted or published.
- **GitHub:** the corrected Southampton R19 research snapshot is public and verified. Its methods and numerical outputs are not a journal publication.
- **Reproduction:** GitHub Actions verifies the saved dataset, research ZIP (CRC and SHA-256), candidate counts, groups, and held-out metrics. The CI job does **not** refit the full scientific pipeline.
- **NASA lineage:** the historical R5–R9 parent repository and locked R18 NASA results remain distinct. No historical scientific result has been overwritten by this publication.
- **Software license:** none has been authorised; no `LICENSE` file is intentionally provided. The upstream Southampton and UCI dataset licenses do not automatically apply to original software code.
- **GitHub Release:** none has been published. GitHub commits and Actions successes are not peer-review acceptance or software release certificates.
- **Zenodo DOI:** An older *unpublished* Zenodo draft (record 23330537, for R20R1) already exists with a reserved identifier. It is **not a published R21R8-EP2 archive or registered project DOI**. The owner is now considering an approved pre-acceptance deposit; this historical post-acceptance-only planning restriction is superseded, but software rights, creator lists, correct version files, and metadata still require verification.

## Administrative actions before a formal software release

Confirm the author/maintainer names, select a code license consistent with third-party source terms, approve public repository metadata and the immutable code/data archive, and then consider tagging a stable commit and publishing a GitHub Release. **An author-approved Zenodo deposit may precede article acceptance**, provided all file rights, attribution, current versions and journal posting restrictions are handled; do not represent a draft reserved identifier as an already published DOI. A documentation correction may be committed without changing the locked experimental archive; changing numerical evidence requires an explicit scientific revision and new audit.

## R21R8-EP2: evidence and release control

The latest **author-review scientific summary** and limits are documented in [R21R8_EP2_20261122_STUDY_STATUS.md](R21R8_EP2_20261122_STUDY_STATUS.md). This note does not modify or replace R19 numerical tables or CI.

- Full internal bootstrap replay: 40/40 tasks, 28,000 attempts, 27,998 successful fresh state files and two reproduced FCM convergence failures. These controlled states are not in this public repository.
- NASA finite-input primary 0.1-dB/1% audit: 403 protected, 107 strict reversal witnesses, 510 coefficients; additional 1.0-dB/1% context sensitivity: 135 protected, 375 reversible.
- Neither bound is an empirically calibrated uncertainty certificate; the larger pointwise bound was motivated by microphone-pair spectral agreement reported in NASA RP-1218, not from a UCI row-wise metrology audit.
- A public Zenodo record can be created independently of journal acceptance in principle. The old draft must be updated **before** publication; once public, Zenodo versioning/record-edit limitations apply. The research owner can approve publication of content they control but cannot unilaterally license coauthor/third-party material without the required rights.
- Until rights and author metadata are confirmed, do not publish a LICENSE, tag this historical R19 code as newly scientifically refit, or label the unpublished draft a public citation.
