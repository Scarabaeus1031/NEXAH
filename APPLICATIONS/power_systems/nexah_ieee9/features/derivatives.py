import numpy as np

def compute_derivatives(x, y):
    dy = np.gradient(y, x)
    d2y = np.gradient(dy, x)
    return dy, d2y
