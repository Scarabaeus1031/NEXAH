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
    print("==================================================\n")

    # absolute path to BUILDER_LAB
    base = os.path.dirname(os.path.abspath(__file__))

    demos = os.path.join(base, "demos")
    visuals = os.path.join(base, "visuals")

    print("Builder Lab location:", base)
    print("Visual output folder:", visuals)

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
