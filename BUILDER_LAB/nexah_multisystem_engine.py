# ==========================================================
# NEXAH MULTI SYSTEM ENGINE
# Simulate multiple NEXAH systems in parallel
# ==========================================================

import os
import json
import argparse


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")


# ----------------------------------------------------------
# LOAD SYSTEM
# ----------------------------------------------------------

def load_system(name):

    path = os.path.join(SYSTEMS_DIR, f"{name}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"System not found: {name}")

    with open(path) as f:
        return json.load(f)


# ----------------------------------------------------------
# SIMULATE MULTI SYSTEM
# ----------------------------------------------------------

def simulate_systems(system_names, steps=10):

    systems = {}
    states = {}

    # Load systems
    for name in system_names:

        system = load_system(name)

        systems[name] = system

        transitions = system["transitions"]

        # start state = first key
        states[name] = list(transitions.keys())[0]

    print("\n========================================")
    print("NEXAH MULTI SYSTEM SIMULATION")
    print("========================================")

    for step in range(steps):

        print(f"\nSTEP {step}")
        print("----------------------------------------")

        new_states = {}

        for name in system_names:

            system = systems[name]
            transitions = system["transitions"]
            regimes = system["regimes"]

            state = states[name]

            regime = regimes.get(state, "UNKNOWN")

            next_state = transitions.get(state, state)

            print(f"{name:20} | {state:15} | {regime:8} → {next_state}")

            new_states[name] = next_state

        states = new_states


# ----------------------------------------------------------
# LIST SYSTEMS
# ----------------------------------------------------------

def list_systems():

    print("\nAvailable systems:\n")

    for f in os.listdir(SYSTEMS_DIR):

        if f.endswith(".json"):
            print(" •", f.replace(".json",""))

    print()


# ----------------------------------------------------------
# CLI ENTRY
# ----------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="NEXAH Multi System Simulation Engine"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available systems"
    )

    parser.add_argument(
        "--systems",
        nargs="+",
        help="Systems to simulate"
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=10,
        help="Number of simulation steps"
    )

    args = parser.parse_args()

    if args.list:

        list_systems()

    elif args.systems:

        simulate_systems(args.systems, args.steps)

    else:

        print("\nUsage:")
        print("  python BUILDER_LAB/nexah_multisystem_engine.py --list")
        print("  python BUILDER_LAB/nexah_multisystem_engine.py --systems energy_grid climate_model")
