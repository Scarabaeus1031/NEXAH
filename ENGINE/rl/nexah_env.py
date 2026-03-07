class NexahEnv:
    """
    Minimal RL-style environment for NEXAH.

    State space:
        finite system states

    Action space:
        list of available control actions

    Transition model:
        action_effect if defined, otherwise default drift delta

    Reward:
        stability score of next state

    Done:
        True if terminal state is reached
    """

    def __init__(self, states, actions, delta, action_effect, risk_map, terminal_states=None):
        self.states = states
        self.actions = actions
        self.delta = delta
        self.action_effect = action_effect
        self.risk_map = risk_map
        self.terminal_states = terminal_states or []
        self.current_state = None

    def reset(self, start_state):
        """
        Reset environment to a given start state.
        """
        if start_state not in self.states:
            raise ValueError(f"Unknown start state: {start_state}")

        self.current_state = start_state
        return self.current_state

    def step(self, action):
        """
        Apply one action and advance the environment.

        Returns:
            next_state, reward, done, info
        """
        if self.current_state is None:
            raise RuntimeError("Environment must be reset before calling step().")

        if action not in self.actions:
            raise ValueError(f"Unknown action: {action}")

        state = self.current_state

        if (state, action) in self.action_effect:
            next_state = self.action_effect[(state, action)]
        else:
            next_state = self.delta.get(state, state)

        reward = self.risk_map.get(next_state, 0)
        done = next_state in self.terminal_states

        self.current_state = next_state

        info = {
            "state": state,
            "action": action,
            "next_state": next_state,
            "reward": reward,
            "done": done,
        }

        return next_state, reward, done, info

    def available_actions(self):
        """
        Return the list of valid actions.
        """
        return list(self.actions)

    def sample_action(self):
        """
        Return a simple default action sample.
        """
        if not self.actions:
            raise RuntimeError("No actions defined in environment.")

        return self.actions[0]
