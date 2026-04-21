import matplotlib.pyplot as plt


class ControlEnergyMap:
    """
    Measures the control effort required to reach
    a stable state from each start state.
    """

    def __init__(self, env, agent, max_steps=20):

        self.env = env
        self.agent = agent
        self.max_steps = max_steps

    def compute(self):

        energy = {}

        for state in self.env.states:

            self.env.reset(state)

            current = state
            steps = 0

            for _ in range(self.max_steps):

                actions = self.env.actions

                action = max(
                    actions,
                    key=lambda a: self.agent.q[current][a]
                )

                next_state, reward, done, info = self.env.step(action)

                steps += 1

                current = next_state

                if done:
                    break

                # stability threshold
                if self.env.risk_map[current] >= 5:
                    break

            energy[state] = steps

        return energy

    def print_report(self, energy):

        print("\nCONTROL ENERGY MAP\n")
        print("----------------------------------------")

        for state, effort in energy.items():

            print(f"{state:20} → {effort} steps")

    def plot(self, energy):

        states = list(energy.keys())
        values = list(energy.values())

        plt.figure(figsize=(10,6))

        plt.bar(states, values)

        plt.ylabel("Control Effort (Steps)")
        plt.title("NEXAH Control Energy Map")

        plt.show()
