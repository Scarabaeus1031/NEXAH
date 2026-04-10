# nexah/resonance/olgo_resonance_model.py

import numpy as np


# --- constants ---
phi = (1 + np.sqrt(5)) / 2
pi = np.pi

# core frequency (OLGO anchor)
f0 = (phi**3) / (pi**2)

# band spacing (empirical from your system)
epsilon = 0.029

# shell definitions
shells = [
    f0,
    f0 + epsilon,
    f0 + 2 * epsilon
]


# --- lissajous dynamics ---
def lissajous_3d(t, w1=3.0, w2=2.0, delta=np.pi/2,
                 A=1.0, B=1.0,
                 z_center=None, z_amp=None, Omega=0.2):

    if z_center is None:
        z_center = f0 + epsilon
    if z_amp is None:
        z_amp = epsilon

    x = A * np.sin(w1 * t)
    y = B * np.sin(w2 * t + delta)
    z = z_center + z_amp * np.sin(Omega * t)

    return x, y, z


# --- resonance detection ---
def detect_resonance(z, shells, tol=0.01):
    hits = []
    for s in shells:
        if abs(z - s) < tol:
            hits.append(s)
    return hits


# --- simulation ---
def simulate(T=1000, dt=0.01):
    t_values = np.arange(0, T, dt)

    trajectory = []
    resonance_hits = []

    for t in t_values:
        x, y, z = lissajous_3d(t)

        hits = detect_resonance(z, shells)

        trajectory.append((x, y, z))
        if hits:
            resonance_hits.append((t, z, hits))

    return trajectory, resonance_hits


if __name__ == "__main__":
    traj, hits = simulate()

    print("Core f0:", f0)
    print("Shells:", shells)
    print("Number of resonance hits:", len(hits))

    # show first few hits
    for h in hits[:10]:
        print("t:", h[0], "z:", h[1], "matched shells:", h[2])
