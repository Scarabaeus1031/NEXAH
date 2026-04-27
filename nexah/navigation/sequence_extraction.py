# ============================================================
# 🧭 NEXAH v16 — Sequence Extraction
# ============================================================

import numpy as np

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    compute_adaptive_levels,
    assign_basins,
)

from nexah.navigation.transition_graph import build_transition_graph


# ------------------------------------------------------------
# EXTRACT SEQUENCE
# ------------------------------------------------------------

def extract_basin_sequence(n=500, n_basins=10):
    x = generate_signal(n=n)
    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    return x, basins


# ------------------------------------------------------------
# COMPRESS SEQUENCE (remove duplicates)
# ------------------------------------------------------------

def compress_sequence(seq):
    compressed = [seq[0]]

    for s in seq[1:]:
        if s != compressed[-1]:
            compressed.append(s)

    return compressed


# ------------------------------------------------------------
# FIND LOOPS
# ------------------------------------------------------------

def find_loops(sequence, max_len=10):
    loops = []

    for i in range(len(sequence)):
        for j in range(i + 2, min(len(sequence), i + max_len)):
            sub = sequence[i:j]

            if len(sub) > 1:
                # check repetition
                next_chunk = sequence[j:j + len(sub)]

                if list(sub) == list(next_chunk):
                    loops.append(sub)

    return loops


# ------------------------------------------------------------
# MAIN ANALYSIS
# ------------------------------------------------------------

def analyze_sequence():
    x, basins = extract_basin_sequence()

    compressed = compress_sequence(basins)

    graph = build_transition_graph(basins)

    loops = find_loops(compressed)

    print("\n--- Raw Basin Sequence (first 50) ---")
    print(basins[:50])

    print("\n--- Compressed Sequence ---")
    print(compressed[:50])

    print("\n--- Sequence Length ---")
    print(len(compressed))

    print("\n--- Detected Loops ---")
    for loop in loops[:10]:
        print(loop)

    print("\n--- Transition Graph (Summary) ---")
    for src, targets in graph.items():
        for tgt, data in targets.items():
            print(f"{src} -> {tgt} | P={data['probability']:.3f}")


if __name__ == "__main__":
    analyze_sequence()
