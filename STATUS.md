# Status — ICML 2026 Causal Modeling of Selection in Evolution

**Paper:** Causal Modeling of Selection in Evolution
**Authors:** Haoyue Dai, Zeyu Tang, Peter Spirtes, Kun Zhang
**Paper:** [arXiv:2606.05689](https://arxiv.org/abs/2606.05689)
**Collection anchor:** mOcTXKawFY
**Audit owner:** MachineLearning-Nerd

## Outcome

**INCONCLUSIVE — 0/6 paper-level claims independently verified.**

| Claim | Local status | Evidence |
| --- | --- | --- |
| C1 Definition 1 | FINITE_MODEL_CONSTRUCTION_PROXY | One T=2 graph contains the four edge types. |
| C2 Lemma 1 | FINITE_GRAPH_STRUCTURE_PROXY | G+ adds edges on two of three toy graphs. |
| C3 Theorem 1 | FINITE_DSEP_ENUMERATION_PROXY | 0 mismatches in 36 bounded comparisons. |
| C4 Theorem 2 | FINITE_PC_GRAPH_PROXY | Oracle skeleton check has 0 wrong removals. |
| C5 Theorem 4 | TAUTOLOGICAL_MULTI_ENV_PROXY | Same graph gives the same local relation twice. |
| C6 real-world validation | NOT_REPRODUCED | Seven-dataset analysis is absent. |

Five finite diagnostics pass, but none reproduces a paper theorem or
paper-scale experiment. C5 is explicitly marked tautological because both
environment labels reuse the same graph and no data or CDNOD implementation is
run.

## Rerun

~~~bash
python3 repro/src/verify.py
python3 repro/src/finalize_gate.py
~~~

The canonical records are outputs/diagnostics.json, outputs/verdict.json,
outputs/gate.json, and publication_gate.json.

FULL_GATE_READY: mOcTXKawFY
