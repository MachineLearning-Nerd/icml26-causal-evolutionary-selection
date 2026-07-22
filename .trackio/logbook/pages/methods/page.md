# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_697510fee5bb", "created_at": "2026-07-22T03:55:54+00:00", "title": "Clean-room d-separation + clique augmentation"}
-->
**Core** `repro/src/core.py`: d-separation (Lauritzen ancestral-moral-graph), ancestors/descendants, clique-augmented DAG G⁺ (Definition 2: add clique on an_G(S)), evolutionary model G^(T) (Definition 1: traits X^(t), heritable ε^(t), selection S^(t), 4 edge types), PC skeleton.

**Verification:** C3 cross-checks d-separation in G^(T)|S vs G⁺ (exact match). d-separation is the standard algorithm; the d-sep match is an independent falsifier of Theorem 1.
