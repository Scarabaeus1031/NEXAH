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
        return self.vectors

    def get_state(self, t: int):
        return self.states[t]
    def compute_field(X):
    
    """
    Unified interface for FIELD computation.

    Parameters
    ----------
    X : np.ndarray (T, N)

    Returns
    -------
    vectors : np.ndarray (T, N)
    """
    field = Field(X)
    return field.get_vector_field()
