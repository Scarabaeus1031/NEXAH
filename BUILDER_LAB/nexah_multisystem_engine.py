def simulate_systems(system_names, steps=10):

    systems = {}
    states = {}

    print("\nLoading systems...")

    for name in system_names:

        system = load_system(name)

        systems[name] = system

        states_list = system.get("states", [])
        transitions = system.get("transitions", {})

        if transitions:
            states[name] = list(transitions.keys())[0]
        elif states_list:
            states[name] = states_list[0]
        else:
            print("Skipping invalid system:", name)
            continue

        print("Loaded:", name, "start:", states[name])

    if not states:
        print("No valid systems found.")
        return

    print("\n========================================")
    print("NEXAH MULTI SYSTEM SIMULATION")
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

        states = new_states
