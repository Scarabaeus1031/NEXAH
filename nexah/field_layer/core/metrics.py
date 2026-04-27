import numpy as np


class FieldMetrics:
    """
    Basic structural metrics for the FIELD layer.
    """

    def __init__(self, field):
        self.field = field
        self.vectors = field.get_vector_field()

    def curvature(self):
        """
        Approximate curvature via second derivative.
        """
        second_derivative = np.gradient(self.vectors, axis=0)
        return np.linalg.norm(second_derivative, axis=1)

    def fragmentation(self):
        """
        Simple proxy: variance increase across state dimensions.
        """
        return np.var(self.field.states, axis=1)

    def flow_strength(self):
        """
        Magnitude of local flow.
        """
        return np.linalg.norm(self.vectors, axis=1)

        def compute_flow_strength(vectors):
        return np.linalg.norm(vectors, axis=1)


    def compute_acceleration(states):
        """
        Approximate second derivative (curvature proxy)
        """
        first = np.gradient(states, axis=0)
        second = np.gradient(first, axis=0)
        return np.linalg.norm(second, axis=1)
