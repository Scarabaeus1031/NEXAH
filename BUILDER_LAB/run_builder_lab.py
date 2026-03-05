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

def run_script(path, description):

    print("\n--------------------------------------------------")
    print(description)
    print("--------------------------------------------------\n")

    subprocess.run([sys.executable, path])


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    print("\n==================================================")
    print("NEXAH BUILDER LAB")
    print("System Navigation Demo Suite")
    print("==================================================\n")

    base = os.path.dirname(__file__)

    demos = os.path.join(base, "demos")

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
    print("BUILDER_LAB/visuals/")
    print("==================================================\n")


if __name__ == "__main__":
    main()
