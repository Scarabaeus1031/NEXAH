import numpy as np


class FieldMetrics:
    """
    Basic structural metrics for the FIELD layer.
    """

    def __init__(self, field):
        self.field = field
        self.vectors = field.get_vector_field()
        self.states = field.states

    def curvature(self):
        """
        Approximate curvature via second derivative.
        """
        second_derivative = np.gradient(self.vectors, axis=0)
        return np.linalg.norm(second_derivative, axis=1)

    def fragmentation(self):
        """
        Simple proxy: variance across state dimensions.
        """
        return np.var(self.states, axis=1)

    def flow_strength(self):
        """
        Magnitude of local flow.
        """
        return np.linalg.norm(self.vectors, axis=1)


# ----------------------------
# Functional Interface (API)
# ----------------------------

def compute_flow_strength(vectors: np.ndarray):
    return np.linalg.norm(vectors, axis=1)


def compute_curvature(vectors: np.ndarray):
    second_derivative = np.gradient(vectors, axis=0)
    return np.linalg.norm(second_derivative, axis=1)


def compute_fragmentation(states: np.ndarray):
    return np.var(states, axis=1)


def compute_risk(states: np.ndarray, vectors: np.ndarray):
    """
    Default risk signal used in pipeline.

    risk = curvature × flow_strength
    """
    flow = compute_flow_strength(vectors)
    curvature = compute_curvature(vectors)

    return curvature * (flow + 1e-8)
