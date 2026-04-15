import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.dynamical_systems.lorenz.attractor.lorenz_density_map import generate_trajectory
from APPLICATIONS.dynamical_systems.lorenz.regimes.lorenz_switch_heatmap import compute_switch_points


def classify_regime(x, z):

    if abs(x) > 25 or z > 45:
        return "ESCAPE"

    if x < -5:
        return "LEFT"

    if x > 5:
        return "RIGHT"

    return "TRANSITION"


def regime_risk(regime):

    risk_map = {
        "LEFT": 0.2,
        "RIGHT": 0.2,
        "TRANSITION": 0.7,
        "ESCAPE": 1.0
    }

    return risk_map[regime]


def choose_direction(x, z):

    # probe nearby points
    candidates = [
        (x + 1, z),
        (x - 1, z),
        (x, z + 1),
        (x, z - 1)
    ]

    best = None
    best_risk = 999

    for cx, cz in candidates:

        regime = classify_regime(cx, cz)
        risk = regime_risk(regime)

        if risk < best_risk:
            best = (cx, cz)
            best_risk = risk

    return best


def run_agent(steps=200):

    x, z = 0.0, 25.0

    path = [(x, z)]

    for _ in range(steps):

        x, z = choose_direction(x, z)
        path.append((x, z))

    return np.array(path)


def main():

    traj = generate_trajectory(20000)
    switch = compute_switch_points(traj)

    agent_path = run_agent()

    plt.figure(figsize=(8,8))

    # background attractor
    plt.scatter(
        traj[:,0],
        traj[:,2],
        s=0.1,
        alpha=0.1,
        color="cyan"
    )

    # regime switches
    plt.scatter(
        switch[:,0],
        switch[:,2],
        s=5,
        color="red",
        label="switch points"
    )

    # agent trajectory
    plt.plot(
        agent_path[:,0],
        agent_path[:,1],
        color="yellow",
        linewidth=2,
        label="agent path"
    )

    plt.title("NEXAH Chaos Navigation Agent")
    plt.xlabel("x")
    plt.ylabel("z")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
