def simulate_cascade(regime_map, start_state):
    """
    Simulate cascade dynamics through the regime graph.

    Starting from a given state, the cascade follows
    outgoing transitions until a terminal state is reached.

    Parameters
    ----------
    regime_map : dict
        NEXAH regime structure

    start_state : str
        initial system state

    Returns
    -------
    dict
        {
            "start_state": ...,
            "cascade_path": [...],
            "final_state": ...
        }
    """

    graph = regime_map["graph"]

    current_state = start_state

    cascade_path = [current_state]

    visited = set()

    while True:

        visited.add(current_state)

        neighbors = list(graph.successors(current_state))

        if not neighbors:
            break

        next_state = neighbors[0]

        if next_state in visited:
            break

        cascade_path.append(next_state)

        current_state = next_state

    return {
        "start_state": start_state,
        "cascade_path": cascade_path,
        "final_state": cascade_path[-1]
    }
