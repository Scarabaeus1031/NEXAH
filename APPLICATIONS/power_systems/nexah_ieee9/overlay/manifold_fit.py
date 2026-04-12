import numpy as np
from scipy.optimize import curve_fit

def model(c, dc, a, p, q):
    return a * (c**p) * (dc**q)

def fit_manifold(c, dc, d2c):
    def f(X, a, p, q):
        c_, dc_ = X
        return model(c_, dc_, a, p, q)

    popt, _ = curve_fit(f, (c, dc), d2c, maxfev=10000)
    return popt
