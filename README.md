# FuzzyRule Guard — browser companion v0.1.0

Open `index.html` from the published GitHub Pages site, or use the downloadable offline bundle. The tool performs real numerical calculations in your browser; it does not transmit uploaded models. Choose the frozen NASA example or your own compatible NPZ/JSON model, select the prediction and ridge-objective budgets, run an audit, then inspect and export certificates.

The browser solver is a separate, conservative float64 implementation. On 510 archived NASA primary slope statements it issued 487 conclusive classifications (397 protected, 90 reversible), all matching the reference, and abstained on 23. See browser_regression.json. For unresolved cases, use the pinned full Python solver at https://github.com/shaikhamalkawi-ux/R19-Verified-Airfoil-TSK-Local-Statement-Robustness-and-Southampton-LOGO-Benchmark/tree/96a8fe019ce3f9e86a8eff407b4935f982189498/FuzzyRule_Guard_v0.1.0. This is not a physical or safety certificate.

The example is a lossless JSON conversion of the P, beta, ytrain, offset, lam, Pt and R arrays in AF4 direct_derivative/inputs/states/AIRFOIL_ONESE_fold00.npz, with no refit or changes to values. Source archive SHA-256: 1edd543fb6544f8bd23de418b3108f1617518251bf35a2cb18ec966d5a7225dd. Gzip SHA-256: 39a4d78701832b152a7ed14129e1c6152f419aea4b4cccfbb0a5904a0d59fea0. Source attribution: Brooks, Pope and Marcolini, UCI Airfoil Self-Noise, DOI 10.24432/C5VW2C (CC BY 4.0 for source dataset). Component-specific original release terms continue to apply; no additional blanket licence is asserted.

This dedicated branch contains the public interface only. Enable Pages from this branch and /(root), if not already enabled. No manuscript, private reviewer correspondence or controlled external data is present.
