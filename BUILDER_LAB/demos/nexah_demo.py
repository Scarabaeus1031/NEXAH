# ==========================================================
# NEXAH DEMO RUNNER
# Entry point for Builder Lab simulations
# ==========================================================

from collections import deque

# ----------------------------------------------------------
# SYSTEM DEFINITION
# ----------------------------------------------------------

states = [
    "S0_normal",
    "S1_load_rising",
    "S2_peak_stable",
    "S3_line_congested",
    "S4_gen_strained",
    "S5_freq_drop",
    "S6_voltage_sag",
    "S7_line_trip",
    "S8_gen_trip",
    "S9_islanding",
    "S10_cascade_risk",
    "S11_blackout",
]

regime = {
    "S0_normal":"STABLE",
    "S1_load_rising":"STABLE",
    "S2_peak_stable":"STABLE",
    "S3_line_congested":"STRESS",
    "S4_gen_strained":"STRESS",
    "S5_freq_drop":"STRESS",
    "S6_voltage_sag":"STRESS",
    "S7_line_trip":"FAILURE",
    "S8_gen_trip":"FAILURE",
    "S9_islanding":"FAILURE",
    "S10_cascade_risk":"COLLAPSE",
    "S11_blackout":"COLLAPSE",
}

# default drift (Δ)
delta = {
    "S0_normal":"S1_load_rising",
    "S1_load_rising":"S3_line_congested",
    "S2_peak_stable":"S3_line_congested",
    "S3_line_congested":"S5_freq_drop",
    "S4_gen_strained":"S5_freq_drop",
    "S5_freq_drop":"S7_line_trip",
    "S6_voltage_sag":"S7_line_trip",
    "S7_line_trip":"S9_islanding",
    "S8_gen_trip":"S9_islanding",
    "S9_islanding":"S10_cascade_risk",
    "S10_cascade_risk":"S11_blackout",
    "S11_blackout":"S11_blackout"
}

# actions
actions = [
    "noop",
    "ramp_generation",
    "start_reserve",
    "shed_load",
    "reconfigure_grid"
]

# action effects
action_effect = {

    ("S3_line_congested","ramp_generation"):"S2_peak_stable",
    ("S4_gen_strained","start_reserve"):"S2_peak_stable",

    ("S5_freq_drop","start_reserve"):"S3_line_congested",
    ("S6_voltage_sag","reconfigure_grid"):"S3_line_congested",

    ("S7_line_trip","reconfigure_grid"):"S6_voltage_sag",
    ("S8_gen_trip","start_reserve"):"S4_gen_strained",

    ("S9_islanding","reconfigure_grid"):"S6_voltage_sag",
    ("S10_cascade_risk","shed_load"):"S4_gen_strained"
}

# ----------------------------------------------------------
# GRAPH
# ----------------------------------------------------------

def build_graph():

    graph = {s:[] for s in states}

    for s in states:
        graph[s].append(delta[s])

    return graph

graph = build_graph()


# ----------------------------------------------------------
# MESO : risk geometry
# ----------------------------------------------------------

def distance_to_blackout(start):

    target = "S11_blackout"

    if start == target:
        return 0

    q = deque([(start,0)])
    visited = {start}

    while q:

        node,dist = q.popleft()

        for n in graph[node]:

            if n == target:
                return dist+1

            if n not in visited:

                visited.add(n)
                q.append((n,dist+1))

    return None


# ----------------------------------------------------------
# NEXAH policy
# ----------------------------------------------------------

def choose_action(state):

    r = regime[state]

    if r == "STABLE":
        return "noop"

    if r == "STRESS":

        if state == "S3_line_congested":
            return "ramp_generation"

        if state == "S4_gen_strained":
            return "start_reserve"

        if state in ["S5_freq_drop","S6_voltage_sag"]:
            return "start_reserve"

    if r == "FAILURE":

        if state in ["S7_line_trip","S9_islanding"]:
            return "reconfigure_grid"

        if state == "S8_gen_trip":
            return "start_reserve"

    if r == "COLLAPSE":

        if state == "S10_cascade_risk":
            return "shed_load"

    return "noop"


# ----------------------------------------------------------
# MEVA execution
# ----------------------------------------------------------

def step(state):

    action = choose_action(state)

    if (state,action) in action_effect:

        new_state = action_effect[(state,action)]

    else:

        new_state = delta[state]

    return action,new_state


# ----------------------------------------------------------
# RUN SIMULATION
# ----------------------------------------------------------

def run_demo(start="S1_load_rising",steps=12):

    s = start

    print("\n===================================================")
    print("NEXAH SYSTEM SIMULATION")
    print("===================================================\n")

    for t in range(steps):

        risk = distance_to_blackout(s)

        action,next_state = step(s)

        print(
            f"{t:02d} | {s:20} | {regime[s]:8} | risk:{risk} | action:{action:18} → {next_state}"
        )

        s = next_state


# ----------------------------------------------------------
# ENTRY POINT
# ----------------------------------------------------------

if __name__ == "__main__":

    print("\nNEXAH BUILDER LAB DEMO\n")

    print("Demo 1: Starting from stable load\n")
    run_demo("S1_load_rising")

    print("\nDemo 2: Starting from stress state\n")
    run_demo("S5_freq_drop")

    print("\nDemo 3: Starting from failure state\n")
    run_demo("S9_islanding")

    print("\nDemo 4: Starting near collapse\n")
    run_demo("S10_cascade_risk")
