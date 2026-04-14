import numpy as np

# --------------------------------------------------
# 🔹 IMPORT REAL SOLVER
# --------------------------------------------------

from APPLICATIONS.power_systems.nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3

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

    # Load shedding reduces effective lambda
    lambda_new -= action.load_shed

    # bounds
    lambda_new = max(0.6, min(1.5, lambda_new))

    return lambda_new


# --------------------------------------------------
# 🔹 REAL IEEE9 SIMULATION
# --------------------------------------------------

def run_ieee9_simulation(lambda_val, action):
    """
    REAL IEEE9 simulation using pandapower
    """

    # map controller → physical action
    action_type = None

    if action.load_shed > 0.05:
        action_type = "EMERGENCY_SHED"
    elif action.load_shed > 0.01:
        action_type = "REDUCE_LOAD"
    elif action.q_support > 0.02:
        action_type = "PREEMPTIVE_STABILIZE"
    elif action.q_support > 0.005:
        action_type = "STABILIZE"

    res = solver.step(lambda_val, action_type)

    # collapse handling
    if not res["converged"]:
        return {
            "risk": 0.1,
            "distance": 0.0,
            "vmin": 0.0,
            "line_loading": 200.0
        }

    vmin = res["vmin"]
    line = res["line_loading"]

    # ----------------------------------------
    # 🔹 DERIVE RISK
    # ----------------------------------------
    risk = max(
        0.0,
        (0.97 - vmin) * 2.0 +      # voltage stress
        (line - 80.0) / 100.0      # line stress
    )

    # ----------------------------------------
    # 🔹 DERIVE DISTANCE
    # ----------------------------------------
    distance = max(0.0, vmin - 0.85)

    return {
        "risk": risk,
        "distance": distance,
        "vmin": vmin,
        "line_loading": line
    }


# --------------------------------------------------
# 🔹 MAIN LOOP
# --------------------------------------------------

lambda_val = 0.6
action = ControlAction()

for step in range(180):

    state = run_ieee9_simulation(lambda_val, action)

    field = evaluate_field(state, targets)

    action = compute_action(field, state)

    lambda_new = apply_action(lambda_val, action)

    print(
        f"[STEP {step}] λ={lambda_val:.4f} → {lambda_new:.4f} | "
        f"risk={state['risk']:.4f} dist={state['distance']:.4f} "
        f"vmin={state['vmin']:.4f} line={state['line_loading']:.2f} "
        f"dλ={action.delta_lambda:.4f} Q={action.q_support:.2f} shed={action.load_shed:.4f}"
    )

    lambda_val = lambda_new
