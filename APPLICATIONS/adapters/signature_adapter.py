import numpy as np


def signature_to_state(signature):
    """
    Convert signature into discrete state label
    """

    avg_loop = signature.get("avg_loop", 0)
    avg_channel = signature.get("avg_channel", 0)

    if avg_loop > avg_channel * 1.2:
        return "LOOP_DOMINANT"

    if avg_channel > avg_loop * 1.2:
        return "CHANNEL_DOMINANT"

    return "STRUCTURED"


def build_state_graph(results):
    """
    Convert pipeline results into a state graph
    """

    states = []
    transitions = {}

    for i, r in enumerate(results):
        state = signature_to_state(r["signature"])
        states.append(state)

        if i > 0:
            prev_state = signature_to_state(results[i - 1]["signature"])

            if prev_state not in transitions:
                transitions[prev_state] = []

            if state not in transitions[prev_state]:
                transitions[prev_state].append(state)

    return {
        "states": list(set(states)),
        "transitions": transitions
    }
