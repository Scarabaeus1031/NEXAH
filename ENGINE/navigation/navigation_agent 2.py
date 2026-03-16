class NavigationAgent:
    """
    Autonomous stabilization agent.

    Observes system state, computes stabilization strategy
    using the StrategicNavigator, and executes actions step-by-step.
    """

    def __init__(self, navigator, delta, action_effect):
        self.navigator = navigator
        self.delta = delta
        self.action_effect = action_effect


    def next_state(self, state, action):
        """
        Compute next state after applying action.
        """

        if (state, action) in self.action_effect:
            return self.action_effect[(state, action)]

        return self.delta.get(state, state)


    def choose_action(self, state):
        """
        Compute best strategy and extract next action.
        """

        path, score = self.navigator.best_strategy(state)

        if path is None or len(path) < 2:
            return None, state, score

        next_state = path[1]

        action = None

        for a in self.navigator.actions:

            candidate = self.next_state(state, a)

            if candidate == next_state:
                action = a
                break

        return action, next_state, score


    def step(self, state):
        """
        Execute one navigation step.
        """

        action, next_state, score = self.choose_action(state)

        return action, next_state, score


    def run(self, start_state, steps=10):
        """
        Run autonomous stabilization simulation.
        """

        state = start_state

        history = []

        for t in range(steps):

            action, next_state, score = self.step(state)

            history.append(
                {
                    "step": t,
                    "state": state,
                    "action": action,
                    "next_state": next_state,
                    "strategy_score": score
                }
            )

            state = next_state

        return history
