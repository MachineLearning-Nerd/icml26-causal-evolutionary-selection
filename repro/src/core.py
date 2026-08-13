"""Small clean-room graph utilities for arXiv 2606.05689.

The utilities represent a static selection DAG G, unfold it over a few
generations, add a clique on ancestors of S, and calculate d-separation. They
support bounded finite proxies in verify.py; they are not an implementation of
the paper's full causal-discovery experiments.

Definition 2 (Clique-augmented DAG G+): over X, with Xi -> Xj in G+ iff
Xi -> Xj in G, OR {Xi, Xj} subset an_G(S) and pi(Xi) < pi(Xj). (Adds a clique
on the ancestors of S.)
"""
from __future__ import annotations

from itertools import combinations


def parents(node, dag):
    return {parent for parent, children in dag.items() if node in children}


def ancestors(nodes, dag):
    """Return proper ancestors of a node set within a DAG."""
    seen = set()
    stack = list(nodes)
    while stack:
        node = stack.pop()
        for parent in parents(node, dag):
            if parent not in seen:
                seen.add(parent)
                stack.append(parent)
    return seen


def descendants(nodes, dag):
    seen = set()
    stack = list(nodes)
    while stack:
        node = stack.pop()
        for child in dag.get(node, set()):
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return seen


def d_separated(A, B, C, dag):
    """Return whether A and B are d-separated by C in a DAG."""
    A, B, C = set(A), set(B), set(C)
    relevant = A | B | C
    ancestral = ancestors(relevant, dag) | relevant
    subgraph = {
        node: dag.get(node, set()) & ancestral
        for node in ancestral
    }
    adjacency = {node: set(subgraph.get(node, set())) for node in ancestral}
    for node in ancestral:
        node_parents = parents(node, subgraph)
        for left, right in combinations(node_parents, 2):
            adjacency.setdefault(left, set()).add(right)
            adjacency.setdefault(right, set()).add(left)
    for source in adjacency:
        for target in subgraph.get(source, set()):
            adjacency[source].add(target)
            adjacency[target].add(source)
    graph_without_conditioning = {
        node: neighbors - C
        for node, neighbors in adjacency.items()
        if node not in C
    }
    visited = set()
    stack = list(A - C)
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node in B:
            return False
        stack.extend(
            neighbor
            for neighbor in graph_without_conditioning.get(node, ())
            if neighbor not in visited
        )
    return True


def clique_augmented(base_dag, selection_node, topo_order):
    """Build the clique-augmented DAG G+ over traits."""
    traits = [node for node in topo_order if node != selection_node]
    selection_ancestors = ancestors({selection_node}, base_dag)
    selected_traits = {
        node for node in traits if node in selection_ancestors
    }
    order_index = {node: index for index, node in enumerate(topo_order)}
    augmented = {node: set() for node in traits}
    for source in traits:
        for target in traits:
            if source == target:
                continue
            base_edge = target in base_dag.get(source, set())
            clique_edge = (
                source in selected_traits
                and target in selected_traits
                and order_index[source] < order_index[target]
            )
            if base_edge or clique_edge:
                augmented[source].add(target)
    return augmented


def evolutionary_model(base_dag, selection_node, T):
    """Unfold a base DAG into the finite evolutionary graph G^(T)."""
    traits = [node for node in base_dag if node != selection_node]
    dag = {}

    def add_edge(source, target):
        dag.setdefault(source, set()).add(target)

    for generation in range(T + 1):
        for trait in traits:
            add_edge(
                f"eps_{trait}^{generation}",
                f"X_{trait}^{generation}",
            )
            if generation < T:
                add_edge(
                    f"eps_{trait}^{generation}",
                    f"eps_{trait}^{generation + 1}",
                )
        for source in traits:
            for target in base_dag.get(source, set()):
                if target != selection_node:
                    add_edge(
                        f"X_{source}^{generation}",
                        f"X_{target}^{generation}",
                    )
        if generation < T:
            for trait in traits:
                if selection_node in base_dag.get(trait, set()):
                    add_edge(
                        f"X_{trait}^{generation}",
                        f"S^{generation}",
                    )
    return dag, traits


def gen_selection(T):
    return {f"S^{generation}" for generation in range(T)}


def pc_skeleton(dag, nodes, max_cond=2):
    """Return an oracle PC-style skeleton and the pairs it removes."""
    nodes = list(nodes)
    adjacency = {node: set(nodes) - {node} for node in nodes}
    removed = set()
    for left, right in combinations(nodes, 2):
        others = [node for node in nodes if node not in {left, right}]
        separated = False
        for size in range(min(max_cond, len(others)) + 1):
            for condition in combinations(others, size):
                if d_separated({left}, {right}, set(condition), dag):
                    separated = True
                    break
            if separated:
                break
        if separated:
            adjacency[left].discard(right)
            adjacency[right].discard(left)
            removed.add(frozenset({left, right}))
    return adjacency, removed
