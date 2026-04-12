import numpy as np

def compute_residual(c, dc, d2c, params):
    a, p, q = params
    pred = a * (c**p) * (dc**q)
    return d2c - pred


def compute_distance(c, dc, rift_points):
    dists = []
    for i in range(len(c)):
        point = np.array([c[i], dc[i]])
        dist = np.min(np.linalg.norm(rift_points - point, axis=1))
        dists.append(dist)
    return np.array(dists)
