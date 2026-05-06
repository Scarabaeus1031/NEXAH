# ============================================================
# 🧭 NEXAH — Transition Graph
# ============================================================
#
# Purpose:
# Build an explicit transition graph from basin sequences.
#
# This is the first structural navigation object:
#
# basins over time
# → transition counts
# → transition probabilities
# → directed weighted graph
#
# Status:
# Core utility / reusable module
#
# ============================================================

import numpy as np


def compute_transition_counts(basins):
    """
    Count directed transitions between basin states.

    Parameters
    ----------
    basins : np.ndarray
        Sequence of basin IDs over time.

    Returns
    -------
    counts : dict
        {(source, target): count}
    nodes : list
        Sorted basin IDs.
    """

    basins = np.asarray(basins)
    nodes = sorted(np.unique(basins).tolist())

    counts = {}

    for i in range(len(basins) - 1):
        source = int(basins[i])
        target = int(basins[i + 1])

        edge = (source, target)
        counts[edge] = counts.get(edge, 0) + 1

    return counts, nodes


def compute_transition_probability_matrix(basins):
    """
    Compute transition probability matrix P.

    P[i, j] = probability of transition node_i → node_j
    """

    counts, nodes = compute_transition_counts(basins)

    index = {node: i for i, node in enumerate(nodes)}
    P = np.zeros((len(nodes), len(nodes)))

    for (source, target), count in counts.items():
        i = index[source]
        j = index[target]
        P[i, j] += count

    row_sums = P.sum(axis=1, keepdims=True)
    P = P / (row_sums + 1e-12)

    return P, nodes


def build_transition_graph(basins):
    """
    Build a directed weighted transition graph.

    Returns
    -------
    graph : dict
        {
            source: {
                target: {
                    "count": int,
                    "probability": float
                }
            }
        }
    """

    counts, nodes = compute_transition_counts(basins)

    outgoing_totals = {node: 0 for node in nodes}

    for (source, target), count in counts.items():
        outgoing_totals[source] += count

    graph = {node: {} for node in nodes}

    for (source, target), count in counts.items():
        total = outgoing_totals[source]
        probability = count / total if total > 0 else 0.0

        graph[source][target] = {
            "count": int(count),
            "probability": float(probability),
        }

    return graph


def strongest_transitions(graph, top_k=None):
    """
    Return strongest transitions sorted by probability, then count.
    """

    edges = []

    for source, targets in graph.items():
        for target, data in targets.items():
            edges.append(
                {
                    "source": source,
                    "target": target,
                    "count": data["count"],
                    "probability": data["probability"],
                }
            )

    edges.sort(
        key=lambda e: (e["probability"], e["count"]),
        reverse=True,
    )

    if top_k is not None:
        return edges[:top_k]

    return edges


def dominant_next_state(graph, source):
    """
    Return most likely next basin from a source basin.
    """

    if source not in graph or not graph[source]:
        return None

    targets = graph[source]

    return max(
        targets.items(),
        key=lambda item: item[1]["probability"],
    )[0]


def print_transition_graph(graph):
    """
    Pretty-print graph for terminal debugging.
    """

    print("\n--- NEXAH Transition Graph ---\n")

    for source, targets in graph.items():
        if not targets:
            print(f"{source} → ∅")
            continue

        for target, data in targets.items():
            print(
                f"{source} → {target} | "
                f"count={data['count']} | "
                f"P={data['probability']:.3f}"
            )


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def _demo():
    basins = np.array([
        0, 0, 1, 1, 2, 2, 1, 1, 0,
        0, 1, 2, 3, 3, 2, 1, 0
    ])

    graph = build_transition_graph(basins)
    P, nodes = compute_transition_probability_matrix(basins)

    print_transition_graph(graph)

    print("\nNodes:")
    print(nodes)

    print("\nTransition Matrix:")
    print(P)

    print("\nStrongest transitions:")
    for edge in strongest_transitions(graph):
        print(edge)


if __name__ == "__main__":
    _demo()
