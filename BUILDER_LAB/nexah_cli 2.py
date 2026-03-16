# ==========================================================
# NEXAH CLI
# Command line interface for the NEXAH Builder Lab
# ==========================================================

import argparse
import subprocess
import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")


# ----------------------------------------------------------
# RUN SCRIPT
# ----------------------------------------------------------

def run_script(path):

    subprocess.run([sys.executable, path])


# ----------------------------------------------------------
# DEMOS
# ----------------------------------------------------------

def run_demo():
    run_script(os.path.join(BASE_DIR, "demos", "nexah_demo.py"))


def run_graph():
    run_script(os.path.join(BASE_DIR, "demos", "nexah_graph_simulation.py"))


def run_explorer():
    run_script(os.path.join(BASE_DIR, "demos", "nexah_explorer.py"))


def run_system_loader():
    run_script(os.path.join(BASE_DIR, "auto_system_loader.py"))


def run_builder():
    run_script(os.path.join(BASE_DIR, "run_builder_lab.py"))


# ----------------------------------------------------------
# SYSTEM MANAGEMENT
# ----------------------------------------------------------

def list_systems():

    print("\nAvailable NEXAH systems:\n")

    for f in os.listdir(SYSTEMS_DIR):
        if f.endswith(".json"):
            print(" •", f.replace(".json",""))

    print()


def simulate_system(name):

    system_file = os.path.join(SYSTEMS_DIR, f"{name}.json")

    if not os.path.exists(system_file):
        print("System not found:", name)
        return

    print("\nSimulating system:", name)

    run_script(os.path.join(BASE_DIR, "auto_system_loader.py"))


def create_system(name):

    path = os.path.join(SYSTEMS_DIR, f"{name}.json")

    if os.path.exists(path):
        print("System already exists.")
        return

    template = {
        "states": [],
        "regimes": {},
        "transitions": {}
    }

    with open(path,"w") as f:
        json.dump(template,f,indent=2)

    print("System created:", path)


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="NEXAH Builder Lab CLI"
    )

    parser.add_argument(
        "command",
        help="Command to run"
    )

    parser.add_argument(
        "name",
        nargs="?",
        help="Optional system name"
    )

    args = parser.parse_args()

    cmd = args.command


    if cmd == "demo":
        run_demo()

    elif cmd == "graph":
        run_graph()

    elif cmd == "explorer":
        run_explorer()

    elif cmd == "systems":
        run_system_loader()

    elif cmd == "builder":
        run_builder()

    elif cmd == "systems-list":
        list_systems()

    elif cmd == "simulate":
        simulate_system(args.name)

    elif cmd == "create-system":
        create_system(args.name)

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
