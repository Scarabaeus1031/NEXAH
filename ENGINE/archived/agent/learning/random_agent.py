import random


class RandomAgent:
    """
    Very simple agent that interacts with NexahEnv
    by selecting random actions.
    """

    def __init__(self, env):
        self.env = env

    def run_episode(self, start_state, max_steps=10):
        """
        Run one random episode.
        """

        state = self.env.reset(start_state)

        trajectory = [state]
        total_reward = 0

        for step in range(max_steps):

            action = random.choice(self.env.available_actions())

            next_state, reward, done, info = self.env.step(action)

            trajectory.append(next_state)
            total_reward += reward

            if done:
                break

        return {
            "trajectory": trajectory,
            "total_reward": total_reward
        }
