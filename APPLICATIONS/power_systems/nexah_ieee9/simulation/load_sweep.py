import numpy as np

def run_load_sweep(powerflow_solver, lambdas):
    results = []

    for lam in lambdas:
        res = powerflow_solver(lam)

        results.append({
            "lambda": lam,
            "V": res["V"],
            "theta": res["theta"],
            "converged": res["converged"]
        })

    return results
