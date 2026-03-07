import matplotlib.pyplot as plt
import numpy as np


class StabilityPhaseDiagram:
    """
    Phase diagram showing stability regimes.

    X-axis  : system stress
    Y-axis  : control strength
    Color   : resulting stability
    """

    def __init__(self, env, agent):

        self.env = env
        self.agent = agent

    def simulate(self, start_state, control_strength, steps=12):
        """
        Simulate trajectory with scaled control probability.
        """

        state = self.env.reset(start_state)

        for _ in range(steps):

            actions = self.env.available_actions()

            # best learned action
            best_action = max(
                actions,
                key=lambda a: self.agent.q[state][a]
            )

            # weaken or strengthen control
            if np.random.rand() < control_strength:
                action = best_action
            else:
                action = "noop"

            next_state, reward, done, info = self.env.step(action)

            state = next_state

            if done:
                break

        return self.env.risk_map.get(state, 0)

    def compute_phase_map(
        self,
        start_state="S5_freq_drop",
        stress_levels=20,
        control_levels=20
    ):

        stress = np.linspace(0, 1, stress_levels)
        control = np.linspace(0, 1, control_levels)

        grid = np.zeros((control_levels, stress_levels))

        for i, c in enumerate(control):

            for j, s in enumerate(stress):

                stability = self.simulate(
                    start_state,
                    control_strength=c
                )

                grid[i, j] = stability

        return stress, control, grid

    def plot(self, stress, control, grid, title="Stability Phase Diagram"):

        plt.figure(figsize=(10,7))

        plt.imshow(
            grid,
            origin="lower",
            aspect="auto",
            extent=[stress.min(), stress.max(), control.min(), control.max()]
        )

        plt.colorbar(label="Final Stability")

        plt.xlabel("System Stress")
        plt.ylabel("Control Strength")
        plt.title(title)

        plt.show()
