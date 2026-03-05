def simulate_systems(system_names, steps=10):

    systems = {}
    states = {}

    # Load systems
    for name in system_names:

        system = load_system(name)

        systems[name] = system

        transitions = system.get("transitions", {})
        state_list = system.get("states", [])

        if transitions:
            states[name] = list(transitions.keys())[0]

        elif state_list:
            states[name] = state_list[0]

        else:
            print(f"Skipping system with no states: {name}")
            continue

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
