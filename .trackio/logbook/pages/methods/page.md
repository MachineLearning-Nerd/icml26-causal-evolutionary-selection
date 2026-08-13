# Methods

repro/src/core.py contains the small clean-room graph utilities:

- DAG parent and ancestor traversal.
- d-separation through an ancestral moral graph.
- clique augmentation over ancestors of S.
- finite evolutionary graph construction.
- a small oracle PC-style skeleton.

repro/src/verify.py records five finite diagnostics and one not-reproduced
claim. repro/src/finalize_gate.py converts those results into the conservative
publication ledger. A passing finite diagnostic is not treated as theorem
verification.
