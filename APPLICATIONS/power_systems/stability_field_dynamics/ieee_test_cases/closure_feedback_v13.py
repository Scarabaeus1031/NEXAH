import numpy as np


def normalize_field(field):
    fmin = np.min(field)
    fmax = np.max(field)

    if np.isclose(fmax, fmin):
        return np.zeros_like(field)

    return (field - fmin) / (fmax - fmin)


def compute_memory_gradient(memory):
    """
    Gradient of the memory field.
    """
    gy, gx = np.gradient(memory)
    return gx, gy


def apply_closure_feedback(Fx, Fy, memory, alpha=0.35):
    """
    Add feedback toward memory ridges / recurrent regions.

    Fx, Fy : base dynamic flow
    memory : recurrence / density map
    alpha  : feedback strength
    """
    gx, gy = compute_memory_gradient(memory)

    # pull toward recurrent structure
    Fx2 = Fx - alpha * gx
    Fy2 = Fy - alpha * gy

    return Fx2, Fy2


def apply_phase_lock(Fx, Fy, lock_strength=0.15):
    """
    Mild phase-locking:
    reduce local directional noise by nudging vectors toward local mean direction.
    """
    h, w = Fx.shape
    Fx_new = Fx.copy()
    Fy_new = Fy.copy()

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            local_fx = Fx[y - 1:y + 2, x - 1:x + 2]
            local_fy = Fy[y - 1:y + 2, x - 1:x + 2]

            mean_fx = np.mean(local_fx)
            mean_fy = np.mean(local_fy)

            Fx_new[y, x] = (1 - lock_strength) * Fx[y, x] + lock_strength * mean_fx
            Fy_new[y, x] = (1 - lock_strength) * Fy[y, x] + lock_strength * mean_fy

    return Fx_new, Fy_new


def reinforce_loops(Fx, Fy, loops, beta=0.25):
    """
    Reinforce flow along already detected loop fragments.
    """
    Fx2 = Fx.copy()
    Fy2 = Fy.copy()

    for loop in loops:
        if len(loop) < 2:
            continue

        for i in range(len(loop) - 1):
            x1, y1 = loop[i]
            x2, y2 = loop[i + 1]

            xi = int(round(x1))
            yi = int(round(y1))

            if 0 <= yi < Fx.shape[0] and 0 <= xi < Fx.shape[1]:
                dx = x2 - x1
                dy = y2 - y1
                Fx2[yi, xi] += beta * dx
                Fy2[yi, xi] += beta * dy

    return Fx2, Fy2
