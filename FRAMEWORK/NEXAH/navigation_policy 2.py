def get_available_transitions(graph, state):

    successors = list(graph.successors(state))

    return successors


def select_safest_transition(state, regime_map, risk_geometry):
    """
    Select the next state that maximizes safety
    based on the MESO risk gradient.
    """

    graph = regime_map["graph"]
    gradient = risk_geometry["risk_gradient"]

    successors = get_available_transitions(graph, state)

    if not successors:
        return None

    best_state = None
    best_score = -1

    for next_state in successors:

        score = gradient.get(next_state, 0)

        if score > best_score:
            best_score = score
            best_state = next_state

    return best_state


def compute_safe_path(start_state, regime_map, risk_geometry, max_steps=20):
    """
    Compute a navigation path that maximizes safety
    (moves away from collapse states).
    """

    graph = regime_map["graph"]

    path = [start_state]

    current = start_state
    visited = set()

    steps = 0

    while steps < max_steps:

        visited.add(current)

        successors = get_available_transitions(graph, current)

        if not successors:
            break

        best = select_safest_transition(current, regime_map, risk_geometry)

        if best is None:
            break

        if best in visited:
            break

        path.append(best)

        current = best
        steps += 1

    return path
