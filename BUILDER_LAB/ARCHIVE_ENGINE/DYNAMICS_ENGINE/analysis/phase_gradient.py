# analysis/phase_gradient.py

import numpy as np


def compute_phase_gradient(phase_grid):

    grad = np.zeros_like(phase_grid, dtype=float)

    rows, cols = phase_grid.shape

    for i in range(rows):
        for j in range(cols):

            diffs = []

            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    diffs.append(abs(phase_grid[i, j] - phase_grid[ni, nj]))

            if diffs:
                grad[i, j] = np.mean(diffs)

    return grad
