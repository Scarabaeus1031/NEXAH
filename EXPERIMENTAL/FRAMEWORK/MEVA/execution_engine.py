class ExecutionEngine:
    """
    MEVA Execution Layer

    Responsible for applying actions and evolving the system state.
    """

    def __init__(self, regime_map, risk_geometry):

        self.graph = regime_map["graph"]
        self.risk_geometry = risk_geometry

        self.state = None
        self.trajectory = []

    def set_initial_state(self, state):

        self.state = state
        self.trajectory = [state]

    def get_available_transitions(self):

        return list(self.graph.successors(self.state))

    def apply_transition(self, next_state):

        self.state = next_state
        self.trajectory.append(next_state)

    def step(self, policy):

        """
        Execute one system step using navigation policy.
        """

        next_state = policy(self.state)

        if next_state is None:
            return False

        self.apply_transition(next_state)

        return True

    def run(self, policy, max_steps=20):

        """
        Run system simulation.
        """

        steps = 0

        while steps < max_steps:

            if not self.step(policy):
                break

            steps += 1

        return self.trajectory
