# Bristol EP22/EP23: code and aggregate evidence

This public, non-commercial research selection preserves 17 original files byte-for-byte from the EP22 and EP23 author-review research archives. It adds no new results. It includes the geometry-blind collision audit, aggregate comparison and design-support records, and universal held-out finite-design feasibility scripts, fold summaries and recorded certificate-check reports. It does not distribute raw HDF5, row-level predictions, fitted design matrices, detailed screening records, private witness NPZs, or reviewer correspondence. The stored certificate reports are summaries, not the original private certificate arrays.

## Reproduction
Acquire the provider data directly from https://doi.org/10.5523/bris.30c8q39wi1mxf205flnun3l5rl under its terms. The verified project input ZIP identity, archived-byte limitation and dependencies are in EP22/SOURCE_PROVENANCE.json. Use the existing [EP20 code and aggregate package](../R21R8_EP21_PUBLIC/57H3Air_EP20_Bristol_Code_and_Aggregate_Evidence.zip) to regenerate private fitted states in a local, rights-compliant work directory. Follow the EP20 instructions; its data are not bundled here.

1. Run EP22/collision_audit.py --source-zip PATH --out LOCAL_AGGREGATES.
2. Run EP22/design_support_audit.py --results LOCAL_EP20_RESULTS --out LOCAL_AGGREGATES.
3. Run EP23/verify_transport_frontier.py --results LOCAL_EP20_RESULTS --out LOCAL_PRIVATE_EVIDENCE. It regenerates private row-level certificate outputs locally; do not redistribute them automatically.
4. Run EP23/check_saved_certificates.py --results LOCAL_EP20_RESULTS --evidence LOCAL_PRIVATE_EVIDENCE. This checks newly generated certificates against the corresponding reproduced-state hashes. It does not recover missing original private arrays from this public subset.
5. Compare aggregate outputs to the included recorded summaries; verify shipped files with sha256sum -c SHA256SUMS.txt from this directory. Source state hashes in the original QA report identify the original run, not a promise of byte parity across independent refits.

The finite-design results apply to the same fixed-premise model and observed held-out inputs; no acoustic mechanism, NASA-model transfer, population guarantee or new journal acceptance is claimed. No new fits were run for this public release. The source archive identity is the recorded project input, not a separately downloaded official checksum.

## Rights
See LICENSE_SCOPE.md for the upstream attribution, non-commercial restriction and original-code scope. This release does not alter the terms of the EP20 archive.
