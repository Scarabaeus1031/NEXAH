# ==========================================================
# NEXAH AUTO SYSTEM LOADER
# Load and simulate NEXAH systems from JSON definitions
# ==========================================================

import json
import os
from system_template import NexahSystem


# ----------------------------------------------------------
# LOAD SYSTEM FROM JSON
# ----------------------------------------------------------

def load_system(json_path):

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"System file not found: {json_path}")

    with open(json_path, "r") as f:
        data = json.load(f)

    states = data["states"]
    regimes = data["regimes"]
    transitions = data["transitions"]

    return NexahSystem(states, regimes, transitions)


# ----------------------------------------------------------
# LOAD ALL SYSTEMS FROM FOLDER
# ----------------------------------------------------------

def load_systems_from_folder(folder):

    systems = []

    if not os.path.exists(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")

    for file in os.listdir(folder):

        if file.endswith(".json"):

            path = os.path.join(folder, file)

            try:
                system = load_system(path)
                systems.append((file, system))

            except Exception as e:

                print(f"Failed to load {file}: {e}")

    return systems


# ----------------------------------------------------------
# RUN SYSTEM
# ----------------------------------------------------------

def run_system(system, start_state=None, steps=10):

    if start_state is None:
        start_state = system.states[0]

    system.simulate(
        start_state=start_state,
        steps=steps,
        save_gif=True
    )


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

if __name__ == "__main__":

    print("\n========================================")
    print("NEXAH AUTO SYSTEM LOADER")
    print("========================================")

    base = os.path.dirname(os.path.abspath(__file__))

    systems_folder = os.path.join(base, "systems")

    print("Loading systems from:", systems_folder)

    systems = load_systems_from_folder(systems_folder)

    if not systems:
        print("No systems found.")
        exit()

    print(f"{len(systems)} systems loaded\n")

    for name, system in systems:

        print("----------------------------------------")
        print("Running system:", name)
        print("----------------------------------------")

        run_system(system)

    print("\nAll systems completed.")
