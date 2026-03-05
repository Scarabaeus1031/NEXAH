# ==========================================================
# NEXAH SYSTEM TEMPLATE
# Generic template for building new NEXAH system simulations
# ==========================================================

import networkx as nx
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os


# ==========================================================
# NEXAH SYSTEM CLASS
# ==========================================================

class NexahSystem:

    def __init__(self, states, regimes, transitions):

        self.states = states
        self.regimes = regimes
        self.transitions = transitions

        self.graph = nx.DiGraph()

        self._build_graph()


    # ------------------------------------------------------
    # BUILD GRAPH
    # ------------------------------------------------------

    def _build_graph(self):

        for s in self.states:
            self.graph.add_node(s)

        for s, t in self.transitions.items():
            self.graph.add_edge(s, t)

        self.pos = nx.spring_layout(self.graph, seed=42)


    # ------------------------------------------------------
    # REGIME COLOR
    # ------------------------------------------------------

    def regime_color(self, node):

        r = self.regimes[node]

        if r == "STABLE":
            return "green"

        if r == "STRESS":
            return "orange"

        if r == "FAILURE":
            return "red"

        if r == "COLLAPSE":
            return "black"

        return "gray"


    # ------------------------------------------------------
    # DRAW GRAPH
    # ------------------------------------------------------

    def draw(self, highlight=None):

        colors = []

        for node in self.graph.nodes():

            if node == highlight:
                colors.append("cyan")
            else:
                colors.append(self.regime_color(node))

        nx.draw(
            self.graph,
            self.pos,
            with_labels=True,
            node_color=colors,
            node_size=1500,
            arrows=True
        )


    # ------------------------------------------------------
    # RUN SIMULATION
    # ------------------------------------------------------

    def simulate(self, start_state, steps=10, save_gif=False, gif_name="nexah_simulation.gif"):

        state = start_state
        frames = []

        os.makedirs("frames", exist_ok=True)

        plt.figure(figsize=(12,6))

        for i in range(steps):

            plt.clf()

            self.draw(highlight=state)

            plt.title(f"NEXAH Simulation — step {i} — state {state}")

            filename = f"frames/frame_{i}.png"

            plt.savefig(filename)

            frames.append(imageio.imread(filename))

            if state in self.transitions:
                state = self.transitions[state]

        if save_gif:

            imageio.mimsave(
                gif_name,
                frames,
                duration=1
            )

            print("GIF saved:", gif_name)

        plt.show()


# ==========================================================
# EXAMPLE USAGE
# ==========================================================

if __name__ == "__main__":

    states = [
        "S0",
        "S1",
        "S2",
        "S3",
        "S4"
    ]

    regimes = {
        "S0":"STABLE",
        "S1":"STABLE",
        "S2":"STRESS",
        "S3":"FAILURE",
        "S4":"COLLAPSE"
    }

    transitions = {
        "S0":"S1",
        "S1":"S2",
        "S2":"S3",
        "S3":"S4",
        "S4":"S4"
    }

    system = NexahSystem(states, regimes, transitions)

    system.simulate(
        start_state="S0",
        steps=10,
        save_gif=True
    )
