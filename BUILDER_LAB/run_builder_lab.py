# ==========================================================
# NEXAH BUILDER LAB RUNNER
# Central entry point for all Builder Lab demos
# ==========================================================

import subprocess
import sys
import os


# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

DEMO_FILES = [
    "nexah_demo.py",
    "nexah_graph_simulation.py",
    "nexah_explorer.py"
]


# ----------------------------------------------------------
# HELPER
# ----------------------------------------------------------

def run_script(script_path):

    name = os.path.basename(script_path)

    print("\n--------------------------------------------------")
    print(f"Running demo: {name}")
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

        print("\nERROR while running:", name)
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
    print("Demos folder:", demos)
    print("Visual output folder:", visuals)

    # ensure visuals folder exists
    os.makedirs(visuals, exist_ok=True)

    print("\nStarting demo suite...")

    for demo in DEMO_FILES:

        script_path = os.path.join(demos, demo)
        run_script(script_path)

    print("\n==================================================")
    print("Builder Lab complete")
    print("All demos executed")
    print("Generated visuals can be found in:")
    print(visuals)
    print("==================================================\n")


# ----------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------

if __name__ == "__main__":

    main()
