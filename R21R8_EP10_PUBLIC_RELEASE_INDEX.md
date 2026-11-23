# Project 57 H3Air — public EP10 and EP11 release index

**Research archive published 23 November 2026:** [GitHub Release](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/releases/tag/h3air-r21r8-ep11-research-v1) · [Zenodo record and DOI 10.5281/zenodo.24480002](https://doi.org/10.5281/zenodo.24480002). This is an author-review research archive, not an accepted IEEE Access article or article DOI.

## Previously published EP10 ZIPs

- [Preprint, supplement and editable authored source](R21R8_EP10_PUBLIC/57H3Air_R21R8_EP10_Public_Preprint_and_Editable_Source.zip): 4,043,013 bytes; SHA-256 `1b36bcdbd9859dc3721a782279aa81f4e97fed3d5c0fb065377bbb7dc4ea4d52`.
- [Selected code and numerical evidence](R21R8_EP10_PUBLIC/57H3Air_R21R8_EP10_Public_Selected_Code_and_Numerical_Evidence.zip): 12,089,248 bytes; SHA-256 `10c766acb2f0669aaf9d760c55bf17daba96a8cb827217f1ba6a0229c80ff091`.

These files remain at their verified GitHub paths. They were not duplicated as GitHub Release assets; both are included in the complete Zenodo record.

## Newly reconstructed bootstrap states

The [EP11 GitHub Release](https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/releases/tag/h3air-r21r8-ep11-research-v1) carries 40 task ZIPs totaling 773,361,055 bytes, covering F4/F5, compact/reference and ten outer folds. The public [SHA-256 manifest](R21R8_EP11_PUBLIC/SHA256SUMS.txt), [completion certificate](R21R8_EP11_PUBLIC/R21R8_FULL40_Completion_Certificate.json), [independent QA record](R21R8_EP11_PUBLIC/R21R8_Independent_Full28k_QA.json) and [standalone verifier](R21R8_EP11_PUBLIC/verify_release_assets.py) document 28,000 attempts, 27,998 new states and two reproduced FCM fitting failures.

**These new states are separate replay outputs.** The original historical fitted-state bytes and the exact first October 2026 UCI download bytes remain unavailable. The public verifier checks release bytes, ZIP CRCs, journals, state hashes and failure identities. Full historical-array comparison still requires reference arrays outside this public bundle. See [reproduction instructions](R21R8_EP11_PUBLIC/README_RELEASE.md).

The [Zenodo record](https://doi.org/10.5281/zenodo.24480002) contains the 40 task ZIPs, both EP10 ZIPs, the clean EP11 manuscript and supplement, authored source without publisher assets, selected Additional Files 2–3, manifests and rights/provenance documentation. The journal response to 16 reviewers, confidential correspondence, publisher assets and Bristol raw HDF5 are excluded from the public research deposit.

## Rights and scientific limits

[Component-level rights](R21R8_EP11_PUBLIC/LICENSE_SCOPE.md): MIT only for authorized original code; CC BY 4.0 only for authorized original authored data and documentation. NASA/UCI, Southampton and Concrete source material retain their upstream attribution and licence terms.

NASA 0.1 dB + 1%: 403 protected and 107 strict reversals among 510 slopes. Separate 1 dB + 1% context sensitivity: 135 protected and 375 strict reversals. Neither threshold is a calibrated per-row uncertainty interval. Southampton LOGO error is dimensionless and source-normalized (TSK 0.059396; Extra Trees 0.047839), not prospective absolute-SPL transfer. These locked scientific outcomes were not changed by publication.

The final Highlighted PDF remains deferred. The article has not been submitted to IEEE Access in this release.
