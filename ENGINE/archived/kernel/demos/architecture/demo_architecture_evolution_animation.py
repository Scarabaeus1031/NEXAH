"""
NEXAH Architecture Evolution Animation
======================================

Visualizes how an architecture evolves while optimizing
the spectral stability metric

    λ₂ / λmax

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_evolution_animation
"""

import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# mutation
# ---------------------------------------------------------

def mutate_graph(G):

    G_new = G.copy()

    nodes = list(G.nodes)

    if random.random() < 0.5 and G_new.number_of_edges() > 0:

        edge = random.choice(list(G_new.edges))
        G_new.remove_edge(*edge)

    else:

        u, v = random.sample(nodes, 2)

        if not G_new.has_edge(u, v):
            G_new.add_edge(u, v)

    return G_new


# ---------------------------------------------------------
# optimizer with history
# ---------------------------------------------------------

def evolve_architecture(G, steps=60):

    history = [G.copy()]

    score = spectral_stability_score(G)

    for _ in range(steps):

        G_candidate = mutate_graph(G)

        candidate_score = spectral_stability_score(G_candidate)

        if candidate_score > score:

            G = G_candidate
            score = candidate_score

        history.append(G.copy())

    return history


# ---------------------------------------------------------
# animation
# ---------------------------------------------------------

def animate(history):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(
        output_dir,
        "architecture_evolution.gif"
    )

    fig, ax = plt.subplots()

    pos = nx.spring_layout(history[0], seed=1)

    def update(frame):

        ax.clear()

        G = history[frame]

        score = spectral_stability_score(G)

        nx.draw(
            G,
            pos,
            ax=ax,
            with_labels=True,
            node_size=500
        )

        ax.set_title(f"Step {frame}  |  λ₂/λmax = {score:.3f}")

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(history),
        interval=400
    )

    ani.save(path, writer="pillow")

    print("\nSaved animation to:")
    print(path)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nRunning architecture evolution animation...\n")

    G = nx.erdos_renyi_graph(6, 0.3)

    history = evolve_architecture(G)

    animate(history)


if __name__ == "__main__":
    run_demo()
