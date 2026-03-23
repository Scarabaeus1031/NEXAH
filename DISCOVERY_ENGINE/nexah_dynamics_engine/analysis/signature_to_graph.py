import numpy as np


# --------------------------------------------------
# BUILD STATE GRAPH FROM RESULTS
# --------------------------------------------------

def build_state_graph(results):
    """
    Convert phase_map results into a discrete state graph

    Each grid point → state
    Transitions → neighbors in grid
    """

    states = []
    transitions = {}

    # --------------------------------------------------
    # CREATE STATES
    # --------------------------------------------------

    for i, res in enumerate(results):

        state_id = f"S{i}"

        label = res.get("classification", "unknown")

        states.append(state_id)

        transitions[state_id] = []

    # --------------------------------------------------
    # CONNECT STATES (SEQUENTIAL NEIGHBORS)
    # --------------------------------------------------

    for i in range(len(states) - 1):

        current_state = states[i]
        next_state = states[i + 1]

        transitions[current_state].append(next_state)

    # --------------------------------------------------
    # OPTIONAL: CLASS-BASED CONNECTIONS
    # --------------------------------------------------

    class_groups = {}

    for i, res in enumerate(results):
        cls = res.get("classification", "unknown")
        state_id = f"S{i}"

        if cls not in class_groups:
            class_groups[cls] = []

        class_groups[cls].append(state_id)

    # connect same-class states
    for cls, group in class_groups.items():

        for i in range(len(group) - 1):
            transitions[group[i]].append(group[i + 1])

    # --------------------------------------------------
    # METADATA
    # --------------------------------------------------

    metadata = {
        "num_states": len(states),
        "num_classes": len(class_groups),
        "classes": list(class_groups.keys())
    }

    return {
        "states": states,
        "transitions": transitions,
        "metadata": metadata
    }
