import matplotlib.pyplot as plt
import numpy as np


class ChaosTransitionMap:
    """
    Detects sensitive transitions between states.

    Measures how unstable a state is by checking
    how many different next states actions produce.
    """

    def __init__(self, env):

        self.env = env

    def compute(self):

        chaos_scores = {}

        for state in self.env.states:

            transitions = set()

            for action in self.env.actions:

                if (state, action) in self.env.action_effect:

                    transitions.add(self.env.action_effect[(state, action)])

                else:

                    transitions.add(self.env.delta[state])

            chaos_scores[state] = len(transitions)

        return chaos_scores

    def plot(self, chaos_scores):

        states = list(chaos_scores.keys())
        values = list(chaos_scores.values())

        plt.figure(figsize=(10,6))

        plt.bar(states, values)

        plt.ylabel("Transition Diversity")
        plt.title("NEXAH Chaos Transition Map")

        plt.show()
