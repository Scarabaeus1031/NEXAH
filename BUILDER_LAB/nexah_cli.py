# ==========================================================
# NEXAH CLI
# Command line interface for the NEXAH Builder Lab
# ==========================================================

import argparse
import subprocess
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def run_script(path):

    subprocess.run([sys.executable, path])


# ----------------------------------------------------------
# COMMANDS
# ----------------------------------------------------------

def run_demo():

    script = os.path.join(BASE_DIR, "demos", "nexah_demo.py")
    run_script(script)


def run_graph():

    script = os.path.join(BASE_DIR, "demos", "nexah_graph_simulation.py")
    run_script(script)


def run_explorer():

    script = os.path.join(BASE_DIR, "demos", "nexah_explorer.py")
    run_script(script)


def run_systems():

    script = os.path.join(BASE_DIR, "auto_system_loader.py")
    run_script(script)


def run_builder():

    script = os.path.join(BASE_DIR, "run_builder_lab.py")
    run_script(script)


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="NEXAH Builder Lab CLI"
    )

    parser.add_argument(
        "command",
        choices=[
            "demo",
            "graph",
            "explorer",
            "systems",
            "builder"
        ],
        help="Command to run"
    )

    args = parser.parse_args()

    if args.command == "demo":
        run_demo()

    elif args.command == "graph":
        run_graph()

    elif args.command == "explorer":
        run_explorer()

    elif args.command == "systems":
        run_systems()

    elif args.command == "builder":
        run_builder()


if __name__ == "__main__":
    main()
