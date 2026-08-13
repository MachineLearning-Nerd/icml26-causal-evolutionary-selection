"""Run bounded clean-room graph checks for arXiv 2606.05689.

The checks are deliberately labelled finite proxies. They do not prove the
paper's general definitions or theorems, and they do not reproduce the paper's
PC/GES/CDNOD data experiments or seven real-world datasets.
"""
from __future__ import annotations

import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from core import (ancestors, clique_augmented, d_separated, evolutionary_model,
                  gen_selection, pc_skeleton)


OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)

PAPER = {
    "title": "Causal Modeling of Selection in Evolution",
    "authors": ["Haoyue Dai", "Zeyu Tang", "Peter Spirtes", "Kun Zhang"],
    "arxiv": "2606.05689",
    "collection_anchor": "mOcTXKawFY",
}

rep: dict = {
    "paper": PAPER["collection_anchor"],
    "title": PAPER["title"],
    "authors": PAPER["authors"],
    "arxiv": PAPER["arxiv"],
    "collection_anchor": PAPER["collection_anchor"],
    "scope": "bounded_clean_room_finite_graph_proxy",
    "claims": {},
}


def _dump(value):
    import numpy as np

    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.integer):
        return int(value)
    return str(value)


def _record(key, paper_claim, status, passed, limitation, evidence):
    result = {
        "paper_claim": paper_claim,
        "status": status,
        "finite_proxy_passed": bool(passed),
        "limitation": limitation,
        "evidence": evidence,
    }
    rep["claims"][key] = result
    return result


def base_graphs():
    """Return three small base DAGs over traits X and a selection node S."""
    g1 = {"X1": {"X2"}, "X2": {"X3", "S"}, "X3": set(), "S": set()}
    pi1 = ["X1", "X2", "X3", "S"]
    g2 = {"X1": {"X3", "S"}, "X2": {"X3", "S"}, "X3": set(), "S": set()}
    pi2 = ["X1", "X2", "X3", "S"]
    g3 = {"X1": {"X2"}, "X2": {"S"}, "X3": {"X2"}, "S": set()}
    pi3 = ["X1", "X3", "X2", "S"]
    return [("G1", g1, pi1), ("G2", g2, pi2), ("G3", g3, pi3)]


def claim_C1():
    """Check that one generated toy model contains Definition 1's edge types."""
    base = {"X1": {"X2"}, "X2": {"S"}, "S": set()}
    dag, _ = evolutionary_model(base, "S", T=2)
    edge_types = {
        "trait_within_generation": "X_X2^0" in dag.get("X_X1^0", set()),
        "trait_to_reproduction": "S^0" in dag.get("X_X2^0", set()),
        "heritable_factor_to_trait": "X_X1^0" in dag.get("eps_X1^0", set()),
        "inheritance": "eps_X1^1" in dag.get("eps_X1^0", set()),
    }
    passed = all(edge_types.values())
    return _record(
        "C1_model",
        "Definition 1: the evolutionary selection model has four edge types.",
        "FINITE_MODEL_CONSTRUCTION_PROXY",
        passed,
        "One hand-built T=2 graph checks edge presence; it does not validate the general definition, distributional semantics, or assumptions.",
        {"edge_types_present": edge_types},
    )


def claim_C2():
    """Compare G with G+ on three hand-built graphs."""
    cases = []
    supergraph_always = True
    any_strict = False
    for name, graph, order in base_graphs():
        traits = [node for node in order if node != "S"]
        gplus = clique_augmented(graph, "S", order)
        base_edges = {
            (source, target)
            for source in traits
            for target in graph.get(source, set())
            if target != "S"
        }
        plus_edges = {
            (source, target)
            for source in traits
            for target in gplus.get(source, set())
        }
        is_superset = base_edges.issubset(plus_edges)
        extra = len(plus_edges - base_edges)
        supergraph_always = supergraph_always and is_superset
        any_strict = any_strict or extra > 0
        cases.append(
            {
                "graph": name,
                "base_trait_edges": len(base_edges),
                "clique_augmented_edges": len(plus_edges),
                "extra_edges": extra,
                "supergraph": is_superset,
            }
        )
    passed = supergraph_always and any_strict
    return _record(
        "C2_induced_deps",
        "Lemma 1: evolutionary selection can induce dependencies not present in the static graph.",
        "FINITE_GRAPH_STRUCTURE_PROXY",
        passed,
        "A larger G+ on two toy graphs is structural evidence only; it does not generate evolutionary data or establish the lemma for all DAGs and distributions.",
        {
            "cases": cases,
            "Gplus_always_supergraph": supergraph_always,
            "strict_case_present": any_strict,
        },
    )


def claim_C3():
    """Enumerate a small set of d-separation comparisons for Theorem 1."""
    cases = []
    all_match = True
    generation = 2
    for name, graph, order in base_graphs():
        traits = [node for node in order if node != "S"]
        gplus = clique_augmented(graph, "S", order)
        evolutionary, _ = evolutionary_model(graph, "S", T=generation)
        selection = gen_selection(generation)
        mismatches = 0
        total = 0
        for a, b, c in itertools.permutations(traits, 3):
            left = d_separated(
                {f"X_{a}^{generation}"},
                {f"X_{b}^{generation}"},
                {f"X_{c}^{generation}"} | selection,
                evolutionary,
            )
            right = d_separated({a}, {b}, {c}, gplus)
            mismatches += left != right
            total += 1
        for a, b in itertools.permutations(traits, 2):
            left = d_separated(
                {f"X_{a}^{generation}"},
                {f"X_{b}^{generation}"},
                selection,
                evolutionary,
            )
            right = d_separated({a}, {b}, set(), gplus)
            mismatches += left != right
            total += 1
        match = mismatches == 0 and total > 0
        all_match = all_match and match
        cases.append(
            {
                "graph": name,
                "generation": generation,
                "comparisons": total,
                "mismatches": mismatches,
                "all_selected_comparisons_match": match,
            }
        )
    return _record(
        "C3_dsep_capture",
        "Theorem 1: the clique-augmented DAG represents the selected evolutionary d-separations.",
        "FINITE_DSEP_ENUMERATION_PROXY",
        all_match,
        "Only singleton A/B/C cases and empty conditioning sets on three hand-built graphs at T=2 are checked; this is not a proof for arbitrary sets, generations, or model assumptions.",
        {"cases": cases, "all_comparisons_match": all_match},
    )


def claim_C4():
    """Run the local oracle PC-skeleton diagnostic on G+."""
    cases = []
    all_sound = True
    max_conditioning = 1
    for name, graph, order in base_graphs():
        traits = [node for node in order if node != "S"]
        gplus = clique_augmented(graph, "S", order)
        _, removed = pc_skeleton(gplus, traits, max_cond=max_conditioning)
        true_edges = {
            (source, target)
            for source in traits
            for target in gplus.get(source, set())
        }
        true_pairs = {(min(a, b), max(a, b)) for a, b in true_edges}
        wrongly_removed = [
            pair for pair in removed
            if tuple(sorted(pair)) in true_pairs
        ]
        sound = not wrongly_removed
        all_sound = all_sound and sound
        cases.append(
            {
                "graph": name,
                "max_conditioning_set_size": max_conditioning,
                "clique_augmented_edges": len(true_edges),
                "removed_pairs": len(removed),
                "true_edges_wrongly_removed": len(wrongly_removed),
                "oracle_skeleton_check_passed": sound,
            }
        )
    return _record(
        "C4_pc_sound",
        "Theorem 2: PC/GES interpretations are sound under the paper's sampling and faithfulness assumptions.",
        "FINITE_PC_GRAPH_PROXY",
        all_sound,
        "This uses the repository's own d-separation oracle on G+, not observational data, the paper's PC/GES implementations, faithfulness checks, or precision experiments.",
        {"cases": cases, "all_oracle_checks_passed": all_sound},
    )


def claim_C5():
    """Repeat one identical graph in two labels to expose the old tautology."""
    graph = {"X1": {"X2"}, "X2": {"S"}, "S": set()}
    order = ["X1", "X2", "S"]
    gplus_a = clique_augmented(graph, "S", order)
    gplus_b = clique_augmented(graph, "S", order)
    relation_a = d_separated({"X1"}, {"X2"}, set(), gplus_a)
    relation_b = d_separated({"X1"}, {"X2"}, set(), gplus_b)
    consistent = relation_a == relation_b
    return _record(
        "C5_multi_env",
        "Theorem 4: the multi-domain identification procedure has soundness and completeness guarantees.",
        "TAUTOLOGICAL_MULTI_ENV_PROXY",
        consistent,
        "Both environments reuse the same graph object and no data, domain shift, or CDNOD procedure is run; this is an internal consistency check, not multi-environment evidence.",
        {
            "ancestors_of_selection": sorted(ancestors({"S"}, graph)),
            "same_graph_reused": True,
            "dsep_relation_environment_a": relation_a,
            "dsep_relation_environment_b": relation_b,
            "consistent": consistent,
        },
    )


def main():
    claim_C1()
    claim_C2()
    claim_C3()
    claim_C4()
    claim_C5()
    rep["claims"]["C6_real_data"] = {
        "paper_claim": "Section 5.2: results on seven real-world datasets support the method's interpretation.",
        "status": "NOT_REPRODUCED",
        "finite_proxy_passed": False,
        "limitation": "The seven datasets, preprocessing, learned graphs, and reported quantitative comparisons are absent from this checkout.",
        "evidence": {"datasets_run": 0},
    }
    finite_claims = list(rep["claims"].values())[:5]
    rep["finite_proxy_diagnostics_passed"] = sum(
        claim["finite_proxy_passed"] for claim in finite_claims
    )
    rep["finite_proxy_diagnostics_total"] = 5
    rep["paper_claims_verified"] = 0
    rep["paper_claims_total"] = 6
    rep["overall_status"] = "INCONCLUSIVE"
    rep["not_run"] = [
        "synthetic evolutionary-selection data generation",
        "PC and GES data experiments",
        "CDNOD multi-domain experiment",
        "seven real-world datasets",
    ]
    for path in [
        os.path.join(OUT, "diagnostics.json"),
        os.path.join(OUT, "verdict.json"),
    ]:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(rep, handle, indent=2, default=_dump)
            handle.write("\n")
    print(
        "Finite proxy diagnostics passed: "
        f"{rep['finite_proxy_diagnostics_passed']}/"
        f"{rep['finite_proxy_diagnostics_total']}"
    )
    print("Paper-level claims independently verified: 0/6")
    print("Overall status: INCONCLUSIVE")
    print("Saved outputs/diagnostics.json and outputs/verdict.json")


if __name__ == "__main__":
    main()
