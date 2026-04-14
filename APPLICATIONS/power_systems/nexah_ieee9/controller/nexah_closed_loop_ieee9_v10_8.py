import numpy as np
from nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3

# --------------------------------------------------
# 🔹 INIT SOLVER
# --------------------------------------------------

solver = RealPowerFlowSolverV3()


# --------------------------------------------------
# 🔹 CONTROL STRUCTURE
# --------------------------------------------------

class ControlAction:
    def __init__(self):
        self.delta_lambda = 0.0
        self.q_support = 0.0
        self.load_shed = 0.0


# --------------------------------------------------
# 🔹 TARGETS
# --------------------------------------------------

targets = {
    "risk": 0.03,
    "distance": 0.08
}


# --------------------------------------------------
# 🔹 FIELD EVALUATION
# --------------------------------------------------

def evaluate_field(state, targets):
    risk = state["risk"]
    dist = state["distance"]

    TARGET_RISK = targets["risk"]
    TARGET_DIST = targets["distance"]

    field_push = (TARGET_RISK - risk) * 0.8 + (dist - TARGET_DIST) * 0.6

    return field_push


# --------------------------------------------------
# 🔹 ACTION GENERATION
# --------------------------------------------------

def compute_action(field_push, state):
    action = ControlAction()

    # Lambda control
    action.delta_lambda = 0.8 * field_push

    # Voltage support
    if state["vmin"] < 0.97:
        action.q_support = (0.97 - state["vmin"]) * 5.0

    # Emergency shedding
    if state["risk"] > 0.025:
        action.load_shed = (state["risk"] - 0.025) * 10.0

    return action


# --------------------------------------------------
# 🔹 APPLY ACTION
# --------------------------------------------------

def apply_action(lambda_val, action):
    lambda_new = lambda_val + action.delta_lambda

    # Load shedding
    lambda_new -= action.load_shed

    # Clamp
    lambda_new = max(0.6, min(1.5, lambda_new))

    return lambda_new


# --------------------------------------------------
# 🔹 IEEE9 SIMULATION (FIXED)
# --------------------------------------------------

def run_ieee9_simulation(lambda_val):
    res = solver.step(lambda_val)

    # ----------------------------------------
    # COLLAPSE CASE
    # ----------------------------------------
    if not res["converged"]:
        return {
            "risk": 0.1,
            "distance": 0.0,
            "vmin": 0.7,
            "line_loading": 120.0
        }

    V = res["V"]
    vmin = res["vmin"]
    loading = res["line_loading"]

    # ----------------------------------------
    # NONLINEAR RESPONSE
    # ----------------------------------------

    stress = max(0.0, lambda_val - 1.0)

    # Voltage degradation
    v_effective = vmin - 0.12 * (stress ** 2)

    # Risk grows nonlinearly
    risk = max(0.0, 1.0 - v_effective)

    # Distance combines effects
    distance = (
        np.mean(np.abs(V - 1.0)) +
        0.08 * stress +
        0.002 * loading
    )

    return {
        "risk": risk,
        "distance": distance,
        "vmin": v_effective,
        "line_loading": loading
    }


# --------------------------------------------------
# 🔹 MAIN LOOP
# --------------------------------------------------

lambda_val = 0.6

for step in range(180):

    state = run_ieee9_simulation(lambda_val)

    field = evaluate_field(state, targets)

    action = compute_action(field, state)

    lambda_new = apply_action(lambda_val, action)

    print(
        f"[STEP {step}] λ={lambda_val:.4f} → {lambda_new:.4f} | "
        f"risk={state['risk']:.4f} dist={state['distance']:.4f} "
        f"vmin={state['vmin']:.4f} "
        f"dλ={action.delta_lambda:.4f} Q={action.q_support:.2f} shed={action.load_shed:.4f}"
    )

    lambda_val = lambda_new
