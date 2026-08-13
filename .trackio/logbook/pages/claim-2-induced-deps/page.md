# Claim 2 — Induced dependencies

**Paper claim:** Lemma 1 says evolutionary selection can induce dependencies
that are not represented by the static selection graph.

**Local status:** FINITE_GRAPH_STRUCTURE_PROXY.

The verifier builds G+ by adding a topologically ordered clique over ancestors
of S. On three hand-built graphs, G+ remains a supergraph of the trait edges and
adds one edge in two cases.

This is structural evidence only. No evolutionary population is generated and
the general lemma is not proved.
