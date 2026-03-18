import random
from collections import defaultdict


class QLearningAgent:
    """
    Basic Q-learning agent for the NEXAH environment.
    """

    def __init__(
        self,
        env,
        alpha=0.1,
        gamma=0.95,
        epsilon=0.2
    ):
        self.env = env

        # learning rate
        self.alpha = alpha

        # discount factor
        self.gamma = gamma

        # exploration probability
        self.epsilon = epsilon

        # Q-table
        self.q = defaultdict(lambda: defaultdict(float))

    def choose_action(self, state):
        """
        Epsilon-greedy action selection.
        """

        actions = self.env.available_actions()

        if random.random() < self.epsilon:
            return random.choice(actions)

        q_values = self.q[state]

        if not q_values:
            return random.choice(actions)

        return max(actions, key=lambda a: q_values[a])

    def update(self, state, action, reward, next_state):
        """
        Q-learning update rule.
        """

        actions = self.env.available_actions()

        max_next = max(
            [self.q[next_state][a] for a in actions],
            default=0
        )

        old = self.q[state][action]

        self.q[state][action] = old + self.alpha * (
            reward + self.gamma * max_next - old
        )

    def train(self, start_state, episodes=200, max_steps=20):
        """
        Train the agent on the environment.
        """

        for ep in range(episodes):

            state = self.env.reset(start_state)

            for step in range(max_steps):

                action = self.choose_action(state)

                next_state, reward, done, info = self.env.step(action)

                self.update(state, action, reward, next_state)

                state = next_state

                if done:
                    break

    def run_policy(self, start_state, max_steps=10):
        """
        Execute learned policy.
        """

        state = self.env.reset(start_state)

        trajectory = [state]
        total_reward = 0

        for step in range(max_steps):

            actions = self.env.available_actions()

            action = max(actions, key=lambda a: self.q[state][a])

            next_state, reward, done, info = self.env.step(action)

            trajectory.append(next_state)
            total_reward += reward

            state = next_state

            if done:
                break

        return {
            "trajectory": trajectory,
            "total_reward": total_reward
        }

    def print_q_table(self):
        """
        Print learned Q-values.
        """

        print("\nQ TABLE\n")

        for state, actions in self.q.items():

            print(state)

            for a, v in actions.items():
                print(f"   {a:20} {v:.3f}")

            print()
