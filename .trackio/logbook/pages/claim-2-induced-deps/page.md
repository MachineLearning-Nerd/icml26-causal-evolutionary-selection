# Claim 2 — Induced deps


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_848f6f11536f", "created_at": "2026-07-22T03:55:53+00:00", "title": "C2: Lemma 1 selection induces deps — VERIFIED"}
-->
Selection induces conditional dependencies absent in the static DAG. The clique-augmented DAG G⁺ (which adds a clique on the ancestors of the selection node S) is **always a supergraph of G** and is **strictly larger** whenever S's ancestors are not already fully connected — demonstrating the selection-induced dependencies.
