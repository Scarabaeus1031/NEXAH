import numpy as np


class Field:
    """
    Minimal Field representation.

    Transforms discrete system states into a continuous vector field approximation.
    """

    def __init__(self, states: np.ndarray):
        """
        Parameters
        ----------
        states : np.ndarray
            Shape: (T, N) time series of system states
        """
        self.states = states
        self.vectors = self._compute_vectors()

    def _compute_vectors(self):
        """
        Approximate local flow using finite differences.
        """
        return np.gradient(self.states, axis=0)

    def get_vector_field(self):
        """
        Returns the computed vector field.
        """
        return self.vectors

    def get_state(self, t: int):
        """
        Returns the state at time t.
        """
        return self.states[t]


# ----------------------------
# Functional Interface (API)
# ----------------------------

def compute_field(states: np.ndarray):
    """
    Unified interface for FIELD computation.

    This is the function the pipeline should use.

    Parameters
    ----------
    states : np.ndarray
        Shape (T, N)

    Returns
    -------
    vectors : np.ndarray
        Shape (T, N)
    """
    field = Field(states)
    return field.get_vector_field()
