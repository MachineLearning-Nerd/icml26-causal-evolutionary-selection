"""Clean-room implementation of the Causal Modeling of Evolutionary Selection
(arXiv 2606.05689, OpenReview mOcTXKawFY).

A static selection model is a DAG G over observed traits X plus a selection node
S (encoding "has offspring").  The evolutionary selection model G^(T) unfolds G
over T generations with heritable exogenous factors epsilon and per-generation
selection indicators S^(t).  Observed data is X^(T) | S^(<T) = 1.

Definition 2 (Clique-augmented DAG G+): over X, with Xi -> Xj in G+ iff
Xi -> Xj in G, OR {Xi, Xj} subset an_G(S) and pi(Xi) < pi(Xj).  (Adds a clique
on the ancestors of S.)

Theorem 1: for any disjoint A, B, C subset X,
    A^(T) _|_ B^(T) | C^(T)  in G^(T) with S^(<T) conditioned
  <=>  A _|_ B | C  in G+.
I.e. the d-separations of the (selection-conditioned) evolutionary model are
exactly those of the clique-augmented DAG G+.
"""
from __future__ import annotations
from itertools import combinations
import numpy as np


# --------------------------------------------------------------------------- #
# DAG representation: dict node -> set(children); plus helpers
def parents(node, dag):
    return {p for p, ch in dag.items() if node in ch}


def ancestors(nodes, dag):
    """Ancestors (proper) of a node set, within `dag`."""
    seen = set(); stack = list(nodes)
    while stack:
        n = stack.pop()
        for p in parents(n, dag):
            if p not in seen:
                seen.add(p); stack.append(p)
    return seen


def descendants(nodes, dag):
    seen = set(); stack = list(nodes)
    while stack:
        n = stack.pop()
        for c in dag.get(n, set()):
            if c not in seen:
                seen.add(c); stack.append(c)
    return seen


# --------------------------------------------------------------------------- #
# d-separation via the ancestral moral graph (Lauritzen)
def d_separated(A, B, C, dag):
    """True iff A _|_ B | C in the DAG `dag`.  A, B, C disjoint node sets."""
    A, B, C = set(A), set(B), set(C)
    relevant = A | B | C
    anc = ancestors(relevant, dag) | relevant
    # ancestral subgraph on anc
    sub = {n: (dag.get(n, set()) & anc) for n in anc}
    # moralize: connect parents of common children, drop directions
    adj = {n: set(sub.get(n, set())) for n in anc}
    for n in anc:
        pars = parents(n, sub)
        for u, v in combinations(pars, 2):
            adj.setdefault(u, set()).add(v)
            adj.setdefault(v, set()).add(u)
    for u in adj:
        for v in sub.get(u, set()):
            adj[u].add(v); adj[v].add(u)
    # remove conditioning set C, check A-B connectivity
    G = {n: (adj.get(n, set()) - C) for n in adj if n not in C}
    # BFS from A, see if reach B (in graph with C removed)
    start = A - C
    visited = set(); stack = list(start)
    while stack:
        n = stack.pop()
        if n in visited:
            continue
        visited.add(n)
        if n in B:
            return False
        for m in G.get(n, ()):
            if m not in visited:
                stack.append(m)
    return True


# --------------------------------------------------------------------------- #
# Build the clique-augmented DAG G+ (Definition 2)
def clique_augmented(base_dag, S, topo_order):
    """base_dag: DAG over X with selection node S.  topo_order: ordering pi of X
    topological to G.  Returns G+ over X (S excluded)."""
    X = [n for n in topo_order if n != S]
    anS = ancestors({S}, base_dag)
    anS_X = {x for x in X if x in anS}             # ancestors of S that are traits
    order_idx = {x: i for i, x in enumerate(topo_order)}
    Gplus = {x: set() for x in X}
    for xi in X:
        for xj in X:
            if xi == xj:
                continue
            in_base = xj in base_dag.get(xi, set())
            in_clique = (xi in anS_X and xj in anS_X and order_idx[xi] < order_idx[xj])
            if in_base or in_clique:
                Gplus[xi].add(xj)
    return Gplus


# --------------------------------------------------------------------------- #
# Build the evolutionary selection model G^(T) (Definition 1)
def evolutionary_model(base_dag, S, T):
    """Unfold base_dag (over X plus S) into G^(T): traits X^(t), heritable eps^(t),
    selection S^(t).  Returns the DAG over all nodes.  Edges:
      X_i^(t) -> X_j^(t)  (base within-gen)
      X_i^(t) -> S^(t)    (traits -> reproduction)
      eps_i^(t) -> X_i^(t)(exogenous -> trait)
      eps_i^(t) -> eps_i^(t+1)  (inheritance)
    """
    X = [n for n in base_dag if n != S]
    dag = {}
    def add(u, v): dag.setdefault(u, set()).add(v)
    for t in range(T + 1):
        for xi in X:
            add(f"eps_{xi}^{t}", f"X_{xi}^{t}")
            if t < T:
                add(f"eps_{xi}^{t}", f"eps_{xi}^{t+1}")
        for xi in X:
            for xj in base_dag.get(xi, set()):
                if xj != S:
                    add(f"X_{xi}^{t}", f"X_{xj}^{t}")
        if t < T:
            for xi in X:
                if S in base_dag.get(xi, set()):     # xi affects reproduction
                    add(f"X_{xi}^{t}", f"S^{t}")
    return dag, X


def gen_traits(X, t):
    return {f"X_{x}^{t}" for x in X}


def gen_selection(T):
    return {f"S^{t}" for t in range(T)}


# --------------------------------------------------------------------------- #
# PC skeleton (soundness check): edges that are NOT d-separated given any subset
def pc_skeleton(dag, nodes, max_cond=2):
    """Return the PC skeleton (undirected adjacencies): i-j present iff NOT
    d-separated given any conditioning subset of neighbors (size<=max_cond)."""
    nodes = list(nodes)
    adj = {n: set(nodes) - {n} for n in nodes}      # complete graph
    removed = set()
    # for each pair, try to find a separating set
    for i, j in combinations(nodes, 2):
        sep = False
        others = [n for n in nodes if n != i and n != j]
        for k in range(min(max_cond, len(others)) + 1):
            if sep:
                break
            for cond in combinations(others, k):
                if d_separated({i}, {j}, set(cond), dag):
                    sep = True; break
        if sep:
            adj[i].discard(j); adj[j].discard(i)
            removed.add(frozenset({i, j}))
    return adj, removed
