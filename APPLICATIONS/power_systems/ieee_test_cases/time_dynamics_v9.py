import numpy as np


def seed_particles_from_boundary(boundary, n_particles=80, jitter=0.15, rng_seed=42):
    """
    Seed particles near the detected boundary.
    Returns array of shape (N, 2) with positions in (x, y).
    """
    rng = np.random.default_rng(rng_seed)

    ys, xs = np.where(boundary > 0)
    if len(xs) == 0:
        return np.empty((0, 2), dtype=float)

    idx = rng.choice(len(xs), size=min(n_particles, len(xs)), replace=True)
    px = xs[idx].astype(float) + rng.normal(0.0, jitter, size=len(idx))
    py = ys[idx].astype(float) + rng.normal(0.0, jitter, size=len(idx))

    return np.column_stack([px, py])


def bilinear_sample(field, x, y):
    """
    Bilinear interpolation for a 2D field at floating-point position (x, y).
    """
    h, w = field.shape

    if x < 0 or x >= w - 1 or y < 0 or y >= h - 1:
        return 0.0

    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    x1 = x0 + 1
    y1 = y0 + 1

    dx = x - x0
    dy = y - y0

    v00 = field[y0, x0]
    v10 = field[y0, x1]
    v01 = field[y1, x0]
    v11 = field[y1, x1]

    return (
        v00 * (1 - dx) * (1 - dy) +
        v10 * dx * (1 - dy) +
        v01 * (1 - dx) * dy +
        v11 * dx * dy
    )


def advect_particles(Ix, Iy, particles, dt=0.6, steps=120, damping=0.98):
    """
    Advect particles through the current field.
    """
    if len(particles) == 0:
        return []

    h, w = Ix.shape
    positions = particles.copy()
    velocities = np.zeros_like(positions)

    trajectories = [[p.copy()] for p in positions]

    for _ in range(steps):
        for i in range(len(positions)):
            x, y = positions[i]

            fx = bilinear_sample(Ix, x, y)
            fy = bilinear_sample(Iy, x, y)

            velocities[i, 0] = damping * velocities[i, 0] + dt * fx
            velocities[i, 1] = damping * velocities[i, 1] + dt * fy

            positions[i, 0] += velocities[i, 0]
            positions[i, 1] += velocities[i, 1]

            # clamp into domain
            positions[i, 0] = np.clip(positions[i, 0], 0, w - 1.001)
            positions[i, 1] = np.clip(positions[i, 1], 0, h - 1.001)

            trajectories[i].append(positions[i].copy())

    return [np.array(traj) for traj in trajectories]


def build_density_map(shape, trajectories):
    """
    Build visit-density map from trajectories.
    """
    density = np.zeros(shape, dtype=float)

    for traj in trajectories:
        for x, y in traj:
            xi = int(np.clip(round(x), 0, shape[1] - 1))
            yi = int(np.clip(round(y), 0, shape[0] - 1))
            density[yi, xi] += 1.0

    if density.max() > 0:
        density /= density.max()

    return density
