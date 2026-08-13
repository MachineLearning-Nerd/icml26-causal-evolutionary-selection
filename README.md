# ICML 2026 — Causal Modeling of Selection in Evolution

Independent, clean-room evidence audit for:

> Haoyue Dai, Zeyu Tang, Peter Spirtes, and Kun Zhang, “Causal Modeling of
> Selection in Evolution,” arXiv:2606.05689, 2026.

Paper links: [arXiv v1 abstract](https://arxiv.org/abs/2606.05689v1) ·
[HTML paper](https://arxiv.org/html/2606.05689) ·
[ICML 2026 OpenReview anchor](https://openreview.net/forum?id=mOcTXKawFY)

## What the paper is doing

The paper distinguishes one-shot static selection from evolutionary selection,
where repeated reproduction and inheritance shape the observed generation. It
defines an evolutionary selection DAG with trait variables, latent heritable
factors, and reproduction indicators. It then introduces the
clique-augmented DAG G+ over the current-generation traits, characterizes the
conditional independences induced by evolutionary selection, and gives
single-domain and multi-domain identification procedures based on PC/GES and
CDNOD-style reasoning. The paper evaluates the interpretation on synthetic
evolutionary data and seven real-world datasets.

## Audit result

**Overall status: INCONCLUSIVE.** The repository has five passing finite graph
proxies and one unrun real-data item. **0/6 paper-level claims are independently
verified.**

The finite checks are useful falsifiers and implementation diagnostics, but
they are not theorem proofs. The repository does not contain the paper's
synthetic data generator, PC/GES data pipeline, CDNOD experiment, or seven
real-world dataset analyses.

Run the bounded audit with:

~~~bash
python3 repro/src/verify.py
python3 repro/src/finalize_gate.py
~~~

The machine-readable reports are:

- outputs/diagnostics.json — raw finite-proxy evidence.
- outputs/verdict.json — claim ledger and conservative verdict.
- outputs/gate.json — publication gate for this bounded scope.
- publication_gate.json — same gate at repository root.

## Claim-to-evidence ledger

| Claim | Paper statement | Local evidence path | Status | What is still missing |
| --- | --- | --- | --- | --- |
| C1 | Definition 1 has four edge types in the evolutionary model. | verify.py constructs one T=2 graph and checks trait, reproduction, heritable-factor, and inheritance edges. | FINITE_MODEL_CONSTRUCTION_PROXY | General definition and distributional semantics. |
| C2 | Lemma 1: evolution can add dependencies absent from static selection. | verify.py compares G with G+ on three hand-built DAGs and observes extra clique edges in two. | FINITE_GRAPH_STRUCTURE_PROXY | General lemma and generated selected data. |
| C3 | Theorem 1: G+ captures selected evolutionary d-separations. | verify.py compares the local d-separation oracle on G^(2) and G+ for 36 singleton/empty-set cases. | FINITE_DSEP_ENUMERATION_PROXY | Arbitrary sets, generations, assumptions, and proof. |
| C4 | Theorem 2: PC/GES interpretations are sound under the paper assumptions. | verify.py runs the local oracle PC-style skeleton on G+ and checks for wrongly removed true edges. | FINITE_PC_GRAPH_PROXY | Observational samples, PC/GES implementations, faithfulness, and precision curves. |
| C5 | Theorem 4: multi-domain identification is sound and complete. | verify.py repeats the same graph under two labels and compares one d-separation relation. | TAUTOLOGICAL_MULTI_ENV_PROXY | Distinct domains, domain shifts, data, and CDNOD. |
| C6 | Section 5.2 validates the method on seven real-world datasets. | No corresponding run exists in this checkout. | NOT_REPRODUCED | DGRP, Cranial, Panzea, PanTHERIA, AVONET, CSES, and PUMS analyses. |

## How each claim is produced

The audit path is intentionally explicit:

1. repro/src/core.py represents DAGs as node-to-children maps, computes
   ancestors and d-separation with an ancestral-moral-graph procedure, builds
   G+, unfolds a finite G^(T), and runs a small oracle PC-style skeleton.
2. repro/src/verify.py runs the five bounded checks, records their evidence
   and limitations, and records C6 as not reproduced.
3. repro/src/finalize_gate.py maps the raw checks to the six paper claims,
   forces the overall status to INCONCLUSIVE, and writes the publication
   gate.
4. The Trackio logbook in .trackio/logbook/pages/ mirrors the same claim
   ledger for human review.

No paper-level status is inferred from a green local check. A finite proxy
passes only when its narrowly defined diagnostic passes.

## Repository map

~~~text
repro/src/core.py          Small graph and d-separation utilities
repro/src/verify.py        Raw bounded finite-proxy checks
repro/src/finalize_gate.py Conservative status and publication gate
outputs/                   JSON evidence and verdicts
docs/paper.pdf             Pinned source-paper copy supplied with the checkout
.trackio/logbook/          Human-readable audit log
STATUS.md                  Short status summary
GATE_READY.md              Gate meaning and rerun contract
BRANCH_AUDIT.md            Branch and commit-attribution record
~~~

## Branch and attribution policy

The cleaned repository uses one main branch. The original collection anchor
was mOcTXKawFY; it identifies the paper record, not a claim of paper-author
code ownership. Reachable audit commits are attributed to
MachineLearning-Nerd using the GitHub no-reply identity. The repository is an
independent reproduction/evidence audit and is not affiliated with the paper's
authors.

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
  url = {https://arxiv.org/abs/2606.05689v1}
}
~~~

## Thank you

Thank you to Haoyue Dai, Zeyu Tang, Peter Spirtes, and Kun Zhang for making a
subtle distinction between static and evolutionary selection and for
formalizing how inheritance changes causal-discovery interpretation. This
clean-room audit is intended as a transparent, respectful companion to the
paper: it records what the local code can support, what it cannot support, and
what would be needed for a faithful end-to-end reproduction.

## Scope and limitations

This repository is CPU-friendly and dependency-light. It is suitable for
reviewing the finite graph logic and the audit bookkeeping. It is not a
replacement for the paper's proofs, causal-discovery software, synthetic
population simulation, or real-world data study.
