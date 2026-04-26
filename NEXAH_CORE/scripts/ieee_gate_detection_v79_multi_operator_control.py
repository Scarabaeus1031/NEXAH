import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------
k_theta = 0.8     # π control (rotation)
k_phi   = 0.6     # φ drift (radial)
k_sqrt  = 0.5     # √2 sheet transition

dt = 0.05
steps = 400

# target
theta_target = 0.8
r_target = 0.9

# initial state
theta = -2.5
r = 1.1

# sheet centers
sheet_centers = np.array([0.54, 0.86, 1.20, 1.60, 1.99])

# gates (example positions)
gates = [(0.8, 0.9), (-1.3, 1.6)]
gate_threshold = 0.15

# logs
theta_path = []
r_path = []
sheet_index_path = []
turning_profile = []

reached_gates = 0

# -----------------------------
# HELPERS
# -----------------------------
def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi

def get_sheet_index(r):
    return np.argmin(np.abs(sheet_centers - r))

def near_gate(theta, r):
    for gt, gr in gates:
        if np.sqrt((theta - gt)**2 + (r - gr)**2) < gate_threshold:
            return True
    return False

def near_sheet_boundary(r):
    distances = np.abs(sheet_centers - r)
    return np.min(distances) < 0.08

# -----------------------------
# SIMULATION
# -----------------------------
for step in range(steps):

    # angle error
    dtheta = wrap_angle(theta_target - theta)

    # --- π control (rotation) ---
    u_pi = -k_theta * dtheta

    # --- φ drift (radial escape) ---
    r_error = r_target - r
    u_phi = k_phi * np.sign(r_error) * np.sqrt(abs(r_error) + 1e-6)

    # --- √2 sheet transition ---
    current_sheet = get_sheet_index(r)
    next_sheet = min(current_sheet + 1, len(sheet_centers)-1)
    r_sheet_next = sheet_centers[next_sheet]

    sheet_gradient = r_sheet_next - r
    u_sheet = k_sqrt * sheet_gradient

    # --- dynamic weights ---
    dist = np.sqrt(dtheta**2 + r_error**2)

    w_phi = min(1.0, abs(r_error))
    w_sqrt = 1.0 if near_sheet_boundary(r) else 0.1
    w_pi = max(0.0, 1.0 - w_phi - w_sqrt)

    # normalize (optional stability)
    total_w = w_pi + w_phi + w_sqrt + 1e-8
    w_pi /= total_w
    w_phi /= total_w
    w_sqrt /= total_w

    # --- final control ---
    u = w_pi * u_pi + w_phi * u_phi + w_sqrt * u_sheet

    # --- update state ---
    theta += u * dt
    r += u_phi * dt  # radial update mainly via φ

    # --- gate check ---
    if near_gate(theta, r):
        reached_gates = min(reached_gates + 1, len(gates))

    # --- log ---
    theta_path.append(theta)
    r_path.append(r)
    sheet_index_path.append(get_sheet_index(r))
    turning_profile.append(u)

# -----------------------------
# RESULTS
# -----------------------------
final_dist = np.sqrt((theta - theta_target)**2 + (r - r_target)**2)

print("NEXAH v79 complete")
print(f"Reached gates: {reached_gates}/{len(gates)}")
print(f"Final distance: {final_dist:.6f}")
