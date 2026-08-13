"""Build the conservative publication gate for this paper audit."""
from __future__ import annotations

import json
import os


ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUTPUTS = os.path.join(ROOT, "outputs")

CLAIMS = [
    {
        "id": "C1",
        "key": "C1_model",
        "paper_claim": "Definition 1: the evolutionary selection model has four edge types.",
        "status": "FINITE_MODEL_CONSTRUCTION_PROXY",
        "limitation": (
            "One hand-built T=2 graph checks edge presence; it does not validate "
            "the general definition, distributional semantics, or assumptions."
        ),
    },
    {
        "id": "C2",
        "key": "C2_induced_deps",
        "paper_claim": "Lemma 1: evolutionary selection can induce dependencies absent from the static graph.",
        "status": "FINITE_GRAPH_STRUCTURE_PROXY",
        "limitation": (
            "A larger G+ on two toy graphs is structural evidence only; it does "
            "not generate evolutionary data or establish the lemma for all DAGs."
        ),
    },
    {
        "id": "C3",
        "key": "C3_dsep_capture",
        "paper_claim": "Theorem 1: G+ represents the selected evolutionary d-separations.",
        "status": "FINITE_DSEP_ENUMERATION_PROXY",
        "limitation": (
            "Only singleton A/B/C cases and empty conditioning sets on three "
            "hand-built graphs at T=2 are checked."
        ),
    },
    {
        "id": "C4",
        "key": "C4_pc_sound",
        "paper_claim": "Theorem 2: PC/GES interpretations are sound under the paper assumptions.",
        "status": "FINITE_PC_GRAPH_PROXY",
        "limitation": (
            "The local oracle runs on G+ directly; it does not use observational "
            "data, PC/GES implementations, faithfulness checks, or precision experiments."
        ),
    },
    {
        "id": "C5",
        "key": "C5_multi_env",
        "paper_claim": "Theorem 4: multi-domain identification is sound and complete.",
        "status": "TAUTOLOGICAL_MULTI_ENV_PROXY",
        "limitation": (
            "Both environments reuse the same graph and no data, domain shift, "
            "or CDNOD procedure is run."
        ),
    },
    {
        "id": "C6",
        "key": "C6_real_data",
        "paper_claim": "Section 5.2: seven real-world datasets support the method's interpretation.",
        "status": "NOT_REPRODUCED",
        "limitation": (
            "The seven datasets, preprocessing, learned graphs, and reported "
            "quantitative comparisons are absent from this checkout."
        ),
    },
]


def main():
    with open(os.path.join(OUTPUTS, "diagnostics.json"), encoding="utf-8") as handle:
        diagnostics = json.load(handle)

    raw_claims = diagnostics["claims"]
    claims = []
    for definition in CLAIMS:
        claim = dict(definition)
        claim["evidence"] = raw_claims.get(definition["key"], {})
        claim["finite_proxy_passed"] = bool(
            claim["evidence"].get("finite_proxy_passed", False)
        )
        claims.append(claim)

    finite_passed = sum(
        claim["finite_proxy_passed"] for claim in claims[:5]
    )
    finite_total = 5
    tests_passed = bool(
        finite_passed == finite_total
        and diagnostics["finite_proxy_diagnostics_passed"] == finite_total
        and diagnostics["finite_proxy_diagnostics_total"] == finite_total
        and diagnostics["paper_claims_verified"] == 0
    )
    report = {
        "paper": diagnostics["paper"],
        "title": diagnostics["title"],
        "authors": diagnostics["authors"],
        "arxiv": diagnostics["arxiv"],
        "collection_anchor": diagnostics["collection_anchor"],
        "scope": diagnostics["scope"],
        "overall_status": "INCONCLUSIVE",
        "paper_claims_verified": 0,
        "paper_claims_total": len(claims),
        "finite_proxy_diagnostics_passed": finite_passed,
        "finite_proxy_diagnostics_total": finite_total,
        "claims": claims,
        "claim_status": {claim["id"]: claim["status"] for claim in claims},
        "attribution": "MachineLearning-Nerd",
    }
    gate = {
        **report,
        "tests_passed": tests_passed,
        "publication_gate_passed": tests_passed,
        "gate_meaning": (
            "Ready for the documented finite-proxy scope; this gate is not "
            "evidence that the six paper claims or paper experiments were reproduced."
        ),
        "verification_command": (
            "python3 repro/src/verify.py && "
            "python3 repro/src/finalize_gate.py"
        ),
    }
    for path in [
        os.path.join(OUTPUTS, "gate.json"),
        os.path.join(ROOT, "publication_gate.json"),
    ]:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(gate, handle, indent=2)
            handle.write("\n")
    with open(os.path.join(OUTPUTS, "verdict.json"), "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")

    print(f"Publication gate passed: {tests_passed}")
    print("Paper-level claims independently verified: 0/6")
    print(f"Finite proxy diagnostics passed: {finite_passed}/{finite_total}")


if __name__ == "__main__":
    main()
