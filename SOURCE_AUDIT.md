# Repository and source audit

## Paper association

- Paper: Causal Modeling of Selection in Evolution
- arXiv: 2606.05689v1
- OpenReview: mOcTXKawFY
- Authors: Haoyue Dai, Zeyu Tang, Peter Spirtes, and Kun Zhang

## Present source

- repro/src/core.py — graph, d-separation, evolutionary unfolding, G+, and
  oracle skeleton utilities.
- repro/src/verify.py — five finite diagnostics plus an explicit C6 absence
  record.
- repro/src/finalize_gate.py — conservative metadata-only report generator.
- outputs/diagnostics.json — existing finite graph measurements.
- docs/paper.pdf — pinned source-paper copy supplied with the checkout.
- .trackio/logbook — existing readable audit notes.

## Added documentation contract

- README.md, STATUS.md, and GATE_READY.md explain scope and gate meaning.
- CLAIM_EVIDENCE.md maps every claim to code, diagnostic key, output, and
  limitation.
- ENVIRONMENT.md records the non-scientific verification boundary.
- REPORT.md, claims.json, reproduction_verdicts.json, AUTONOMOUS_STATE.json,
  and EVIDENCE_MANIFEST.json provide structured status.
- CITATION.cff and AUTHOR_THANK_YOU.md provide citation and appreciation.
- BRANCH_AUDIT.md and verify_final.py record and enforce branch and attribution
  policy.

## Missing paper scope

The repository does not contain the general proofs or assumption checks,
generated evolutionary populations, faithful PC/GES data pipeline, CDNOD
multi-domain experiment, or seven real-world dataset analyses. Those absences
are part of the verdict and are not silently inferred from finite graph checks.
