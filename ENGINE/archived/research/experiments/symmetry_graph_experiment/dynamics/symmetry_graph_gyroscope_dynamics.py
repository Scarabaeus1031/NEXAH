"""
NEXAH Symmetry Graph – Gyroscope Dynamics
-----------------------------------------

First dynamic experiment for the dual-hub symmetry graph.

Idea:
- two coupled hubs (center_A, center_B)
- oscillatory phase dynamics
- load sharing across the outer symmetry modules
- synchronization / resonance score over time

This is not a full physical gyroscope model.
It is a minimal dual-core phase-coupling experiment.
"""

import math
import random
import statistics
import matplotlib.pyplot as plt


# ---------------------------------
# Dual hub initialization
# ---------------------------------

def initialize_state():
    return {
        "phase_A": random.uniform(0, 2 * math.pi),
        "phase_B": random.uniform(0, 2 * math.pi),
        "omega_A": 1.0 + random.uniform(-0.02, 0.02),
        "omega_B": 1.02 + random.uniform(-0.02, 0.02)
    }


# ---------------------------------
# Helper functions
# ---------------------------------

def wrap_angle(theta):
    return theta % (2 * math.pi)


def phase_distance(a, b):
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def sync_score(a, b):
    d = phase_distance(a, b)
    return 1 - d / math.pi


# ---------------------------------
# Simulation step
# ---------------------------------

def step_dynamics(state, dt=0.05, coupling=0.18, noise=0.015):

    phase_A = state["phase_A"]
    phase_B = state["phase_B"]

    omega_A = state["omega_A"]
    omega_B = state["omega_B"]

    # Kuramoto-style coupling
    dA = omega_A + coupling * math.sin(phase_B - phase_A)
    dB = omega_B + coupling * math.sin(phase_A - phase_B)

    # noise
    dA += random.uniform(-noise, noise)
    dB += random.uniform(-noise, noise)

    phase_A = wrap_angle(phase_A + dA * dt)
    phase_B = wrap_angle(phase_B + dB * dt)

    state["phase_A"] = phase_A
    state["phase_B"] = phase_B

    return state


# ---------------------------------
# Run simulation
# ---------------------------------

def run_simulation(steps=400):

    state = initialize_state()

    phases_A = []
    phases_B = []
    sync_values = []

    for _ in range(steps):

        state = step_dynamics(state)

        a = state["phase_A"]
        b = state["phase_B"]

        phases_A.append(a)
        phases_B.append(b)

        sync_values.append(sync_score(a, b))

    return phases_A, phases_B, sync_values


# ---------------------------------
# Visualization
# ---------------------------------

def plot_results(phases_A, phases_B, sync_values):

    fig, axs = plt.subplots(3, 1, figsize=(10, 8))

    axs[0].plot(phases_A)
    axs[0].set_title("Hub A Phase")

    axs[1].plot(phases_B)
    axs[1].set_title("Hub B Phase")

    axs[2].plot(sync_values)
    axs[2].set_title("Synchronization Score")

    plt.tight_layout()
    plt.show()


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    print("\nRunning Gyroscope Dynamics Experiment...\n")

    phases_A, phases_B, sync_values = run_simulation()

    print("Mean synchronization:", statistics.mean(sync_values))
    print("Min synchronization:", min(sync_values))
    print("Max synchronization:", max(sync_values))

    plot_results(phases_A, phases_B, sync_values)
