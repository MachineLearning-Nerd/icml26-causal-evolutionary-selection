# Reproduction report

## Verdict

The bounded audit is **INCONCLUSIVE**. Five of five finite graph diagnostics
pass, C6 is not reproduced, and zero of six complete paper claims are
independently verified.

## Counts

- Finite proxy diagnostics: 5/5
- Negative diagnostics: 0
- Scoped evidence points: 10/12
- Paper claims independently verified: 0/6
- Current score claim: false
- Publication as a full reproduction: not allowed

## Interpretation

The code provides finite evidence for selected graph construction,
d-separation, oracle-skeleton, and internal consistency behaviors. C5 is
tautological because it reuses the same graph under two labels. None of these
checks establishes the paper's general theorems or data analyses.

The authoritative structured files are outputs/verdict.json, outputs/gate.json,
publication_gate.json, and claims.json.
