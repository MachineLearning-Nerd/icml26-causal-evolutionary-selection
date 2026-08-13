# Claim 5 — Multi-domain identification

**Paper claim:** Theorem 4 gives soundness and completeness for the multi-domain
identification procedure.

**Local status:** TAUTOLOGICAL_MULTI_ENV_PROXY.

The verifier constructs one graph, assigns it to two environment labels, and
checks that one d-separation relation agrees. This exposes the bookkeeping
path, but it is intentionally marked tautological: there is no domain shift,
data, or CDNOD implementation.
