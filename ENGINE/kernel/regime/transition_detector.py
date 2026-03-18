import numpy as np


class TransitionDetector:

    """
    Detect rapid changes indicating regime transitions.
    """

    def __init__(self, delta_threshold=0.5):

        self.delta_threshold = delta_threshold


    def detect(self, state_series):

        if len(state_series) < 2:
            return False

        delta = abs(state_series[-1] - state_series[-2])

        return delta > self.delta_threshold
