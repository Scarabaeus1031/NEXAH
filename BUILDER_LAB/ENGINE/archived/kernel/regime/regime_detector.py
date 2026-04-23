import numpy as np


class RegimeDetector:

    """
    Detect system regimes from time-series state data.
    """

    def __init__(self, stable_threshold=0.1, oscillation_threshold=1.0):

        self.stable_threshold = stable_threshold
        self.oscillation_threshold = oscillation_threshold


    def detect(self, state_series):

        if len(state_series) < 2:
            return "UNKNOWN"

        variance = np.var(state_series)

        if variance < self.stable_threshold:
            return "STABLE"

        if variance < self.oscillation_threshold:
            return "OSCILLATORY"

        return "CHAOTIC"
