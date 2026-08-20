# Causal selection in evolution — audit status

Paper: Causal Modeling of Selection in Evolution

Authors: Haoyue Dai, Zeyu Tang, Peter Spirtes, and Kun Zhang

Paper: arXiv 2606.05689v1

OpenReview: mOcTXKawFY

## Verdict

**INCONCLUSIVE — 0/6 complete paper claims independently verified.**

The existing checkout contains five finite graph diagnostics, all passing
within their narrow hand-built scope. C6 has no local run. C5 is explicitly
tautological because both environment labels reuse the same graph.

| Claim | Status | What the existing evidence shows |
| --- | --- | --- |
| C1 — Definition 1 | FINITE_MODEL_CONSTRUCTION_PROXY | One T=2 graph contains the four edge types. |
| C2 — Lemma 1 | FINITE_GRAPH_STRUCTURE_PROXY | G+ adds edges in the hand-built cases. |
| C3 — Theorem 1 | FINITE_DSEP_ENUMERATION_PROXY | 0 mismatches in 36 bounded comparisons. |
| C4 — Theorem 2 | FINITE_PC_GRAPH_PROXY | Oracle skeleton has 0 wrongly removed true edges. |
| C5 — Theorem 4 | TAUTOLOGICAL_MULTI_ENV_PROXY | Same graph gives the same local relation twice. |
| C6 — real-world validation | NOT_REPRODUCED | Seven-dataset analysis is absent. |

## Gate

- Finite proxy diagnostics passed: 5/5
- Scoped evidence points: 10/12
- Complete paper claims independently verified: 0/6
- Current score claim: false
- Full-paper publication: not allowed

The authoritative machine-readable files are
[outputs/verdict.json](outputs/verdict.json),
[outputs/gate.json](outputs/gate.json), and
[publication_gate.json](publication_gate.json). The detailed production
ledger is [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md).
