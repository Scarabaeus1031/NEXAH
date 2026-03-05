# ==========================================================
# NEXAH BUILDER LAB RUNNER
# Central entry point for all Builder Lab demos
# ==========================================================

import subprocess
import sys
import os


# ----------------------------------------------------------
# Helper
# ----------------------------------------------------------

def run_script(script_path, description):

    print("\n--------------------------------------------------")
    print(description)
    print("--------------------------------------------------\n")

    if not os.path.exists(script_path):
        print("ERROR: Script not found:", script_path)
        sys.exit(1)

    try:
        subprocess.run(
            [sys.executable, script_path],
            check=True
        )
    except subprocess.CalledProcessError:
        print("\nERROR while running:", script_path)
        sys.exit(1)


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    print("\n==================================================")
    print("NEXAH BUILDER LAB")
    print("System Navigation Demo Suite")
    print("==================================================")

    # absolute path to BUILDER_LAB
    base = os.path.dirname(os.path.abspath(__file__))

    demos = os.path.join(base, "demos")
    visuals = os.path.join(base, "visuals")

    print("\nBuilder Lab location:", base)
    print("Visual output folder:", visuals)

    # ensure visuals folder exists
    os.makedirs(visuals, exist_ok=True)

    # ------------------------------------------------------
    # 1 DEMO SIMULATION
    # ------------------------------------------------------

    run_script(
        os.path.join(demos, "nexah_demo.py"),
        "Running basic NEXAH system simulation"
    )

    # ------------------------------------------------------
    # 2 GRAPH WALK
    # ------------------------------------------------------

    run_script(
        os.path.join(demos, "nexah_graph_simulation.py"),
        "Running animated graph simulation"
    )

    # ------------------------------------------------------
    # 3 EXPLORER TOOL
    # ------------------------------------------------------

    run_script(
        os.path.join(demos, "nexah_explorer.py"),
        "Running NEXAH Explorer"
    )

    print("\n==================================================")
    print("Builder Lab complete")
    print("Generated visuals can be found in:")
    print(visuals)
    print("==================================================\n")


if __name__ == "__main__":
    main()

# ----------------------------------------------------------
# COLOR BY REGIME
# ----------------------------------------------------------

def get_color(node):

    r = regime[node]

    if r == "STABLE":
        return "green"

    if r == "STRESS":
        return "orange"

    if r == "FAILURE":
        return "red"

    return "black"


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

G = nx.DiGraph()

for s in states:
    G.add_node(s)

for s, t in delta.items():
    G.add_edge(s, t)

pos = nx.spring_layout(G, seed=42)


# ----------------------------------------------------------
# SIMULATION
# ----------------------------------------------------------

def simulate(start="S1_load_rising", steps=12):

    state = start
    frames = []

    for i in range(steps):

        fig, ax = plt.subplots(figsize=(12,6))

        colors = []

        for node in G.nodes():

            if node == state:
                colors.append("cyan")
            else:
                colors.append(get_color(node))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=1500,
            arrows=True,
            ax=ax
        )

        ax.set_title(f"NEXAH System Walk — step {i} — state {state}")

        fig.canvas.draw()

        # --------------------------------------------------
        # Get frame buffer (Mac-safe)
        # --------------------------------------------------

        frame = np.asarray(fig.canvas.buffer_rgba())

        frames.append(frame)

        plt.close(fig)

        state = delta[state]

    return frames


# ----------------------------------------------------------
# RUN
# ----------------------------------------------------------

frames = simulate()

output = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "visuals",
    "nexah_system_walk.gif"
)

imageio.mimsave(
    output,
    frames,
    duration=1
)

print("\nGIF saved to:", output)
