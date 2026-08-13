# Claim 4 — Theorem 2

**Paper claim:** PC/GES output has the stated sound interpretation under the
paper's sampling and faithfulness assumptions.

**Local status:** FINITE_PC_GRAPH_PROXY.

The verifier runs the repository's own oracle PC-style skeleton directly on G+
for three toy graphs, with conditioning sets of size at most one. It checks
that no known G+ edge is removed: 0 wrongly removed edges.

No observational samples, PC/GES package, faithfulness test, precision curve,
or paper-scale synthetic experiment is run.
