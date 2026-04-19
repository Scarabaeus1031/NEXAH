import numpy as np


# --------------------------------------------------
# TRANSITION OVERLAY
# --------------------------------------------------

def compute_transition_overlay(phase_grid, rotation_grid, angle_grid):
    """
    Combines multiple signals into a single transition intensity map
    """

    h, w = phase_grid.shape

    overlay = np.zeros_like(phase_grid, dtype=float)

    for i in range(1, h - 1):
        for j in range(1, w - 1):

            # --------------------------------------------------
            # 1. PHASE CHANGE (Gradient)
            # --------------------------------------------------

            phase_center = phase_grid[i, j]

            phase_diff = 0
            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                if phase_grid[i + di, j + dj] != phase_center:
                    phase_diff += 1

            phase_score = phase_diff / 4.0


            # --------------------------------------------------
            # 2. ROTATION CHANGE
            # --------------------------------------------------

            rot_center = rotation_grid[i, j]

            rot_diff = 0
            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                if rotation_grid[i + di, j + dj] != rot_center:
                    rot_diff += 1

            rot_score = rot_diff / 4.0


            # --------------------------------------------------
            # 3. ANGLE CHANGE
            # --------------------------------------------------

            angle_center = angle_grid[i, j]

            angle_diff = 0.0
            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                neighbor = angle_grid[i + di, j + dj]
                angle_diff += abs(neighbor - angle_center)

            angle_score = angle_diff / 4.0


            # normalize angle influence
            angle_score = angle_score / 180.0


            # --------------------------------------------------
            # COMBINE
            # --------------------------------------------------

            overlay[i, j] = (
                0.4 * phase_score +
                0.3 * rot_score +
                0.3 * angle_score
            )

    return overlay
