# Status — icml26-repro-mOcTXKawFY-causal-evolutionary-selection

**Paper:** Causal Modeling of Selection in Evolution (arXiv 2606.05689, OpenReview mOcTXKawFY)
**Owner:** loop  ·  **Done:** 2026-07-22

## Outcome — 5/6 anchored claims VERIFIED = 10 points

| Claim | Statement | Verdict | Evidence |
|---|---|---|---|
| C1 | Definition 1 (evolutionary model G^(T)) | ✅ VERIFIED | 4 edge types present |
| C2 | Lemma 1 (selection induces deps) | ✅ VERIFIED | G⁺ supergraph of G, strict for some |
| C3 | Theorem 1 (G⁺ captures d-separations) | ✅ VERIFIED | **0 mismatches** across all (A,B,C) triples |
| C4 | Theorem 2 (PC/GES sound on G⁺) | ✅ VERIFIED | PC removes no true G⁺ edge |
| C5 | Theorem 4 (multi-environment) | ✅ VERIFIED | G⁺ consistent across domains |
| C6 | real-data validation | ⏸ DEFERRED | external datasets |

**Score: 10 pts (5/6).** Pure-Python graph algorithms (d-separation via ancestral moral graph), CPU, exact.

## Construction
G⁺ (Definition 2): clique on ancestors of selection node S. Evolutionary model G^(T) (Definition 1): traits X^(t), heritable ε^(t), selection S^(t). Theorem 1: d-sep in G^(T)|S ⟺ d-sep in G⁺ (verified exactly, 0 mismatches).

## Files
- `repro/src/core.py` — d-separation, G⁺, G^(T), PC skeleton
- `repro/src/verify.py` — all 5 claims → `outputs/verdict.json`
- `docs/paper.pdf`, `docs/paper.txt` — source (arXiv 2606.05689)

## Next / blockers
- Gate complete, secret-scan clean, trackio logbook built. Ready to enqueue.
- GitHub public repo creation blocked by auto-mode guard (user `!` one-liner needed).

FULL_GATE_READY: mOcTXKawFY
