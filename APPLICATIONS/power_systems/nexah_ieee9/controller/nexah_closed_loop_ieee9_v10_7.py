import numpy as np

# 🔥 REAL SOLVER IMPORT
from nexah_ieee9.simulation.powerflow_solver_real_v2 import RealPowerFlowSolverV2

solver = RealPowerFlowSolverV2()


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

    # Lambda steering
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

    # Load shedding wirkt direkt
    lambda_new -= action.load_shed

    # Clamp
    lambda_new = max(0.6, min(1.5, lambda_new))

    return lambda_new


# --------------------------------------------------
# 🔹 REAL IEEE9 SIMULATION
# --------------------------------------------------

def run_ieee9_simulation(lambda_val):
    res = solver.step(lambda_val)

    if not res["converged"]:
        return {
            "risk": 0.1,
            "distance": 0.0,
            "vmin": 0.7,
            "line_loading": 120.0
        }

    V = res["V"]

    vmin = np.min(V)
    vmean = np.mean(V)

    # 🔥 risk = voltage collapse proximity
    risk = max(0, 1.0 - vmin)

    # 🔹 distance = deviation from nominal
    distance = np.mean(np.abs(V - 1.0))

    return {
        "risk": risk,
        "distance": distance,
        "vmin": vmin,
        "line_loading": 0.0
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
