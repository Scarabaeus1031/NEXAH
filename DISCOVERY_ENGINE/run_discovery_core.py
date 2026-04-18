"""
NEXAH — Discovery Core Runner

Minimal executable pipeline to test:

Dynamics → Phase → Risk → Structure → Transitions
"""

import numpy as np
import matplotlib.pyplot as plt

# --- IMPORTS FROM CORE ---

from phase.phase_space_map import generate_phase_space
from landscape.risk_landscape import compute_risk_field
from core_analysis.resilience_analyzer import analyze_system
from core_analysis.resilience_critical_point_finder import find_critical_points
from phase.resilience_phase_transition_detector import detect_transitions


# --- SIMPLE TEST SYSTEM (Lorenz-like) ---

def lorenz_step(x, sigma=10, rho=28, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])


def simulate(system_fn, steps=2000, dt=0.01):
    x = np.array([1.0, 1.0, 1.0])
    traj = []

    for _ in range(steps):
        dx = system_fn(x)
        x = x + dt * dx
        traj.append(x.copy())

    return np.array(traj)


# --- PIPELINE ---

def run():

    print("\n--- NEXAH DISCOVERY CORE ---\n")

    # 1. simulate dynamics
    print("Simulating system...")
    traj = simulate(lorenz_step)

    # 2. phase space
    print("Generating phase space...")
    phase = generate_phase_space(traj)

    # 3. risk field
    print("Computing risk field...")
    risk = compute_risk_field(traj)

    # 4. analysis
    print("Running analysis...")
    analysis = analyze_system(traj)

    # 5. critical points
    print("Detecting critical points...")
    critical_points = find_critical_points(traj)

    # 6. transitions
    print("Detecting transitions...")
    transitions = detect_transitions(traj)

    # --- OUTPUT ---

    print("\n--- RESULTS ---\n")

    print(f"Trajectory length: {len(traj)}")
    print(f"Mean risk: {np.mean(risk):.4f}")
    print(f"Critical points found: {len(critical_points)}")
    print(f"Transitions detected: {len(transitions)}")

    # --- VISUALIZATION ---

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], alpha=0.7)
    ax.set_title("NEXAH Discovery Core — Trajectory")

    plt.show()


if __name__ == "__main__":
    run()
