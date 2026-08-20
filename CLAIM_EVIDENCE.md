# Claim-to-evidence production ledger

This ledger maps every paper target to the existing local code and recorded
output. A finite graph proxy pass is evidence about the bounded construction
only; every complete paper claim remains unverified.

## Evidence accounting

| Claim | Scoped points | Available points | Status |
| --- | ---: | ---: | --- |
| C1 | 2 | 2 | FINITE_MODEL_CONSTRUCTION_PROXY |
| C2 | 2 | 2 | FINITE_GRAPH_STRUCTURE_PROXY |
| C3 | 2 | 2 | FINITE_DSEP_ENUMERATION_PROXY |
| C4 | 2 | 2 | FINITE_PC_GRAPH_PROXY |
| C5 | 2 | 2 | TAUTOLOGICAL_MULTI_ENV_PROXY |
| C6 | 0 | 2 | NOT_REPRODUCED |
| Total | 10 | 12 | INCONCLUSIVE |

The point count is an internal completeness measure. It is not a probability,
confidence score, or paper-reproduction score.

## C1 — evolutionary model construction

- Paper target: Definition 1.
- Production code: repro/src/core.py, evolutionary_model.
- Diagnostic runner: repro/src/verify.py, C1_model.
- Raw output: outputs/diagnostics.json:claims.C1_model.
- Canonical verdict: outputs/verdict.json:C1.
- Existing finite result: one T=2 graph contains trait, reproduction,
  heritable-factor, and inheritance edges.
- Status: FINITE_MODEL_CONSTRUCTION_PROXY.
- Limitation: one hand-built graph does not validate general definitions,
  distributional semantics, or assumptions.

## C2 — selection-induced dependencies

- Paper target: Lemma 1.
- Production code: repro/src/core.py, clique_augmented.
- Diagnostic runner: repro/src/verify.py, C2_induced_deps.
- Raw output: outputs/diagnostics.json:claims.C2_induced_deps.
- Canonical verdict: outputs/verdict.json:C2.
- Existing finite result: G+ is a supergraph in three hand-built cases, with
  strict additional edges in two.
- Status: FINITE_GRAPH_STRUCTURE_PROXY.
- Limitation: no generated evolutionary data or general lemma proof is
  provided.

## C3 — selected d-separation

- Paper target: Theorem 1.
- Production code: repro/src/core.py, d_separated and evolutionary_model.
- Diagnostic runner: repro/src/verify.py, C3_dsep_capture.
- Raw output: outputs/diagnostics.json:claims.C3_dsep_capture.
- Canonical verdict: outputs/verdict.json:C3.
- Existing finite result: 36 singleton/empty-set comparisons across three
  hand-built graphs at T=2 have zero mismatches.
- Status: FINITE_DSEP_ENUMERATION_PROXY.
- Limitation: arbitrary variable sets, conditioning sets, generations, and
  theorem assumptions are not checked.

## C4 — PC-style graph interpretation

- Paper target: Theorem 2.
- Production code: repro/src/core.py, pc_skeleton.
- Diagnostic runner: repro/src/verify.py, C4_pc_sound.
- Raw output: outputs/diagnostics.json:claims.C4_pc_sound.
- Canonical verdict: outputs/verdict.json:C4.
- Existing finite result: the local oracle skeleton has zero wrongly removed
  true edges in the three hand-built cases.
- Status: FINITE_PC_GRAPH_PROXY.
- Limitation: no observational data, PC/GES implementation, faithfulness
  check, or precision experiment is present.

## C5 — multi-domain identification

- Paper target: Theorem 4.
- Production code: repro/src/core.py, clique_augmented and d_separated.
- Diagnostic runner: repro/src/verify.py, C5_multi_env.
- Raw output: outputs/diagnostics.json:claims.C5_multi_env.
- Canonical verdict: outputs/verdict.json:C5.
- Existing finite result: the same local d-separation relation is returned
  under two labels.
- Status: TAUTOLOGICAL_MULTI_ENV_PROXY.
- Limitation: both environments reuse the same graph; there is no domain
  shift, data, or CDNOD procedure.

## C6 — seven real-world datasets

- Paper target: Section 5.2.
- Production path: README.md, STATUS.md, SOURCE_AUDIT.md, and
  outputs/verdict.json:C6.
- Existing evidence: datasets_run is 0.
- Status: NOT_REPRODUCED.
- Limitation: DGRP, Cranial, Panzea, PanTHERIA, AVONET, CSES, and PUMS
  data, preprocessing, learned graphs, and comparisons are absent.

## Reproduction boundary

paper_claim_reproduced is false for every claim in claims.json. The result is
INCONCLUSIVE, not a five-claim or six-claim reproduction.
