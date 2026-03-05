triggered = set()

for (src_sys, src_state), (tgt_sys, tgt_state) in COUPLINGS.items():

    if (src_sys, src_state) in triggered:
        continue

 HEAD
    if src_sys in states and states[src_sys] == src_state:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")
 6f49789 (nexah_coupled_system_engine.py)

        if tgt_sys in new_states:

            print(
                f"COUPLING: {src_sys}:{src_state} "
                f"→ forces {tgt_sys}:{tgt_state}"
            )

            new_states[tgt_sys] = tgt_state

            triggered.add((src_sys, src_state))
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
# CLI ENTRY
# ----------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="NEXAH Coupled System Engine"
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
        simulate(args.systems, args.steps)

    else:
        print("\nUsage:")
        print("  python BUILDER_LAB/nexah_coupled_system_engine.py --list")
        print("  python BUILDER_LAB/nexah_coupled_system_engine.py --systems energy_grid climate_model supply_chain")
