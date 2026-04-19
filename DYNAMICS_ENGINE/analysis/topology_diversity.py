# analysis/topology_diversity.py

import numpy as np


def compute_diversity(results, shape):

    grid = np.zeros(shape)

    idx = 0

    for i in range(shape[0]):
        for j in range(shape[1]):

            sig = results[idx]["signature"]

            # simple diversity proxy:
            # wie breit ist degree distribution?
            degree_keys = list(sig["degree_dist"].keys())

            if len(degree_keys) > 0:
                spread = max(degree_keys) - min(degree_keys)
            else:
                spread = 0

            grid[i, j] = spread

            idx += 1

    return grid
