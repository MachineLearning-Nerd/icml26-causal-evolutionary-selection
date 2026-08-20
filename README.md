# ICML 2026 — Causal Modeling of Selection in Evolution

Paper-level result: **INCONCLUSIVE**.

This repository is an independent, bounded clean-room audit of **Causal
Modeling of Selection in Evolution**. It contains five finite graph
diagnostics for selected model-construction, graph-structure, d-separation,
oracle-skeleton, and multi-environment consistency behaviors. It does not
reproduce the paper's general proofs, causal-discovery data pipeline, CDNOD
experiment, or seven real-world datasets.

Five of five finite proxies pass, C6 is not reproduced, and zero of six
complete paper claims are independently verified. The repository is suitable
for publication as a scoped audit only; it makes no current external score
claim.

## Paper

- Title: Causal Modeling of Selection in Evolution
- Authors: Haoyue Dai, Zeyu Tang, Peter Spirtes, and Kun Zhang
- arXiv: [2606.05689](https://arxiv.org/abs/2606.05689), version 1
- HTML paper: [arxiv.org/html/2606.05689](https://arxiv.org/html/2606.05689)
- OpenReview: [mOcTXKawFY](https://openreview.net/forum?id=mOcTXKawFY)
- Canonical repository: [MachineLearning-Nerd/icml26-causal-evolutionary-selection](https://github.com/MachineLearning-Nerd/icml26-causal-evolutionary-selection)

The paper distinguishes one-shot static selection from evolutionary selection,
where reproduction and inheritance shape later generations. It defines an
evolutionary selection DAG, constructs the clique-augmented graph G+, studies
selected d-separations, and develops causal-discovery and multi-domain
identification interpretations. The paper also reports synthetic and
seven-dataset real-world analyses.

## Claim-to-evidence summary

| ID | Paper target | Evidence produced here | Status |
| --- | --- | --- | --- |
| C1 | Definition 1: four edge types | One T=2 hand-built evolutionary graph | FINITE_MODEL_CONSTRUCTION_PROXY |
| C2 | Lemma 1: selection-induced dependencies | Three hand-built G versus G+ comparisons | FINITE_GRAPH_STRUCTURE_PROXY |
| C3 | Theorem 1: G+ selected d-separations | 36 bounded oracle comparisons | FINITE_DSEP_ENUMERATION_PROXY |
| C4 | Theorem 2: PC/GES interpretation | Oracle PC-style skeleton on G+ | FINITE_PC_GRAPH_PROXY |
| C5 | Theorem 4: multi-domain identification | Same graph reused under two labels | TAUTOLOGICAL_MULTI_ENV_PROXY |
| C6 | Section 5.2: seven real-world datasets | No corresponding run in this checkout | NOT_REPRODUCED |

These statuses describe local evidence, not successful reproduction of the
paper claims. The machine-readable contract is in [claims.json](claims.json),
and detailed production paths and limitations are in
[CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md).

## How each claim is produced

The existing raw measurements are preserved in
[outputs/diagnostics.json](outputs/diagnostics.json). The clean-room graph
utilities are [repro/src/core.py](repro/src/core.py), and the existing
scientific diagnostic script is [repro/src/verify.py](repro/src/verify.py).
This documentation workflow consumes the recorded diagnostics; it does not run
the scientific implementation.

The metadata-only publication path is:

~~~bash
python3 repro/src/finalize_gate.py
python3 verify_final.py
~~~

The finalizer converts the existing raw diagnostics into
[outputs/verdict.json](outputs/verdict.json), [outputs/gate.json](outputs/gate.json),
and [publication_gate.json](publication_gate.json). The final verifier checks
the claim statuses, evidence counts, required documentation, branch policy,
attribution, and fail-closed publication flags.

## Evidence boundary

- Finite proxy diagnostics passed: **5/5**
- Scoped evidence points: **10/12**
- Complete paper claims independently verified: **0/6**
- C6 real-world evidence: **not reproduced**
- Current score claim: **false**
- Publication as a full reproduction: **not allowed**

The following remain outside the verified boundary:

- the general definitions, theorem assumptions, and proofs;
- generated evolutionary-selection populations and observational samples;
- faithful PC/GES implementations, faithfulness checks, and precision curves;
- distinct domains and a CDNOD-style multi-domain experiment;
- DGRP, Cranial, Panzea, PanTHERIA, AVONET, CSES, and PUMS analyses.

## Repository map

- [repro/src/core.py](repro/src/core.py) — DAG, G+, unfolding, d-separation, and oracle skeleton utilities.
- [repro/src/verify.py](repro/src/verify.py) — source of the five existing finite diagnostics.
- [repro/src/finalize_gate.py](repro/src/finalize_gate.py) — metadata-only conservative gate generator.
- [outputs/diagnostics.json](outputs/diagnostics.json) — existing raw measurements.
- [docs/paper.pdf](docs/paper.pdf) — pinned source-paper copy supplied with the checkout.
- [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) — claim-to-evidence production ledger.
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md) — contents and missing-scope audit.
- [verify_final.py](verify_final.py) — fail-closed final-state verifier.

## Branches and attribution

main is the only canonical publication branch. The former repository name was
icml26-repro-mOcTXKawFY-causal-evolutionary-selection; the live repository is
icml26-causal-evolutionary-selection. See [BRANCH_AUDIT.md](BRANCH_AUDIT.md)
for the recovery bundle, source tip, branch policy, and identity normalization.

Reachable maintenance commits use:

MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>

This is repository-maintenance attribution and does not claim authorship of
the paper or its implementation.

## Citation

~~~bibtex
@inproceedings{dai2026causal,
  title = {Causal Modeling of Selection in Evolution},
  author = {Dai, Haoyue and Tang, Zeyu and Spirtes, Peter and Zhang, Kun},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year = {2026},
  eprint = {2606.05689},
  archivePrefix = {arXiv},
  primaryClass = {cs.LG},
  url = {https://arxiv.org/abs/2606.05689}
}
~~~

The repository metadata citation is also available in
[CITATION.cff](CITATION.cff).

## Thank you

Thank you to Haoyue Dai, Zeyu Tang, Peter Spirtes, and Kun Zhang for
formalizing the distinction between static and evolutionary selection and its
causal-discovery consequences. This independent audit records finite graph
evidence and its limitations so readers can distinguish a bounded diagnostic
from the paper's general guarantees and data analyses.

See [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md) for the standalone note.
