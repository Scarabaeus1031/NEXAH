import numpy as np


def build_mode_fields(shape, center, eigvals, eigvecs, scale=6.0):
    """
    Create two spatial mode fields from PCA eigenvectors.

    Returns:
        mode1_field
        mode2_field
    """
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]

    if center is None or eigvals is None or eigvecs is None:
        zeros = np.zeros(shape)
        return zeros, zeros

    cx, cy = center
    x = xx - cx
    y = yy - cy

    v1 = eigvecs[:, 0]
    v2 = eigvecs[:, 1]

    lam1 = np.sqrt(max(eigvals[0], 1e-9)) * scale
    lam2 = np.sqrt(max(eigvals[1], 1e-9)) * scale

    # project coordinates onto eigenvectors
    p1 = (x * v1[0] + y * v1[1]) / lam1
    p2 = (x * v2[0] + y * v2[1]) / lam2

    # gaussian envelopes
    env1 = np.exp(-(p1**2 + 0.25 * p2**2))
    env2 = np.exp(-(p2**2 + 0.25 * p1**2))

    # signed mode fields
    mode1 = p1 * env1
    mode2 = p2 * env2

    return mode1, mode2


def simulate_mode_interaction(mode1, mode2, steps=24, omega1=1.0, omega2=1.6, phase_shift=np.pi/2):
    """
    Time-dependent interaction between two modes.

    Returns list of frames.
    """
    frames = []

    for t in np.linspace(0, 2 * np.pi, steps, endpoint=False):
        a1 = np.cos(omega1 * t)
        a2 = np.sin(omega2 * t + phase_shift)

        field = a1 * mode1 + a2 * mode2
        frames.append(field)

    return frames


def compute_turn_field(frames):
    """
    Estimate local 'turning' / reversal intensity from temporal differences.
    """
    if len(frames) < 2:
        return np.zeros_like(frames[0])

    acc = np.zeros_like(frames[0], dtype=float)

    for i in range(1, len(frames)):
        prev = frames[i - 1]
        curr = frames[i]

        # sign-change = reversal / U-turn tendency
        sign_flip = (np.sign(prev) != np.sign(curr)).astype(float)
        delta = np.abs(curr - prev)

        acc += sign_flip * delta

    return acc / (len(frames) - 1)


def normalize_field(field):
    fmin = np.min(field)
    fmax = np.max(field)
    if np.isclose(fmax, fmin):
        return np.zeros_like(field)
    return (field - fmin) / (fmax - fmin)
