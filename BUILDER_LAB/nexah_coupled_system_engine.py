# ==========================================================
# NEXAH COUPLED SYSTEM ENGINE
# Multi-system simulation with cross-system influence
# ==========================================================

import os
import json
import argparse


BASE_DIR = os.path.dirname(os.path.abspath(file))
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
# COUPLING RULES
# ----------------------------------------------------------
# format:
# (source_system, source_state) → (target_system, forced_state)

COUPLINGS = {

    ("climate_model", "S3_failure"): ("energy_grid", "S5_freq_drop"),

    ("energy_grid", "S11_blackout"): ("supply_chain", "S3_breakdown")

}


# ----------------------------------------------------------
# SIMULATION
# ----------------------------------------------------------

def simulate(system_names, steps=10):

    systems = {}
    states = {}

    print("\nLoading systems...")

    for name in system_names:

        system = load_system(name)

        systems[name] = system

        transitions = system.get("transitions", {})
        states_list = system.get("states", [])

        if transitions:
            states[name] = list(transitions.keys())[0]
        elif states_list:
            states[name] = states_list[0]
        else:
            print("Skipping invalid system:", name)

        print("Loaded:", name, "start:", states[name])


    print("\n========================================")
    print("NEXAH COUPLED SYSTEM SIMULATION")
    print("========================================")


    for step in range(steps):

        print(f"\nSTEP {step}")
        print("----------------------------------------")

        new_states = {}

        for name in states:

            system = systems[name]

            transitions = system.get("transitions", {})
            regimes = system.get("regimes", {})

            state = states[name]
            regime = regimes.get(state, "UNKNOWN")

            next_state = transitions.get(state, state)

            print(f"{name:20} | {state:15} | {regime:8} → {next_state}")

            new_states[name] = next_state


        # --------------------------------------------------
        # APPLY COUPLINGS
        # --------------------------------------------------

        for (src_sys, src_state), (tgt_sys, tgt_state) in COUPLINGS.items():

            if src_sys in states and states[src_sys] == src_state:

                if tgt_sys in new_states:

                    print(
                        f"COUPLING: {src_sys}:{src_state} "
                        f"→ forces {tgt_sys}:{tgt_state}"
                    )

                    new_states[tgt_sys] = tgt_state


        states = new_states


# ----------------------------------------------------------
# LIST SYSTEMS
# ----------------------------------------------------------

def list_systems():

    print("\nAvailable systems:\n")

    for f in os.listdir(SYSTEMS_DIR):
        if f.endswith(".json"):
            print(" •", f.replace(".json", ""))

    print()


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

if name == "main":

    parser = argparse.ArgumentParser(
        description="NEXAH Coupled System Engine"
    )

    parser.add_argument(
        "--list",
        action="store_true"
    )

    parser.add_argument(
        "--systems",
        nargs="+"
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=10
    )

    args = parser.parse_args()


    if args.list:

        list_systems()

    elif args.systems:

        simulate(args.systems, args.steps)

    else:

        print("\nUsage:")
        print("python nexah_coupled_system_engine.py --systems energy_grid climate_model supply_chain")
