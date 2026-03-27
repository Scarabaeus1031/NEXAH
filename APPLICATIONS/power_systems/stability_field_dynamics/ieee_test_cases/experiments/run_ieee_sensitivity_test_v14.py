import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
generate_phase_data,
detect_gh_corridor,
)

print(“RUNNING IEEE SENSITIVITY TEST V14 (TRANSITION CARTOGRAPHY OVERLAY)”)

–––––––––––––––––––––––––

CONFIG

–––––––––––––––––––––––––

LOADS = np.linspace(1.0, 5.0, 10)
N = 200

ALPHA_THETA = 0.08
BETA_LOOPS = 2.0
GAMMA_C = 0.5

FOCUS_LOAD = 3.0

OUTPUT_DIR = “APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs”
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []
focus_data = None

–––––––––––––––––––––––––

HELPERS

–––––––––––––––––––––––––

def structure_coupled_state(load: float, n: int = N):
theta, c, loops = generate_phase_data(N=n)
theta = theta * (1.0 + ALPHA_THETA * (load - 1.0))
theta_std = np.std(theta)

loops = loops + BETA_LOOPS * theta_std
c = c * (1.0 + GAMMA_C * theta_std)

return theta, c, loops, theta_std
theta = theta * (1.0 + ALPHA_THETA * (load - 1.0))
theta_std = np.std(theta)

loops = loops + BETA_LOOPS * theta_std
c = c * (1.0 + GAMMA_C * theta_std)

return theta, c, loops, theta_std
def fit_axis(x: np.ndarray, y: np.ndarray):
pts = np.column_stack([x, y])
pts = pts - pts.mean(axis=0)
cov = np.cov(pts.T)
eigvals, eigvecs = np.linalg.eigh(cov)
vec = eigvecs[:, np.argmax(eigvals)]

angle = np.arctan2(vec[1], vec[0])
return angle, vec

–––––––––––––––––––––––––

MAIN LOOP

–––––––––––––––––––––––––

for load in LOADS:
theta, c, loops, theta_std = structure_coupled_state(load)
gh = detect_gh_corridor(theta, c, loops)

gh_points = len(gh["theta_corridor"])
gh_width_theta = np.ptp(gh["theta_corridor"]) if gh_points > 0 else 0.0
gh_width_c = np.ptp(gh["c_corridor"]) if gh_points > 0 else 0.0

c_std = np.std(c)
loops_mean = np.mean(loops)

regime_separation = theta_std * c_std
corridor_anisotropy = gh_width_theta / (gh_width_c + 1e-9)

c_struct = regime_separation * loops_mean
c_struct_norm = (
    (theta_std / (1.0 + theta_std))
    * (c_std / (1.0 + c_std))
    * (loops_mean / (1.0 + loops_mean))
)

row = {
    "load": load,
    "theta_std": theta_std,
    "c_std": c_std,
    "loops_mean": loops_mean,
    "gh_points": gh_points,
    "gh_width_theta": gh_width_theta,
    "gh_width_c": gh_width_c,
    "corridor_anisotropy": corridor_anisotropy,
    "regime_separation": regime_separation,
    "c_struct": c_struct,
    "c_struct_norm": c_struct_norm,
}

results.append(row)

if abs(load - FOCUS_LOAD) < 1e-6:
    focus_data = (theta, c, gh)

–––––––––––––––––––––––––

SAVE RESULTS

–––––––––––––––––––––––––

df = pd.DataFrame(results)
csv_path = os.path.join(OUTPUT_DIR, “ieee_sensitivity_test_v14.csv”)
df.to_csv(csv_path, index=False)

print(”\n— RESULTS —”)
print(df)
print(f”\nSaved: {csv_path}”)

–––––––––––––––––––––––––

TRANSITION CARTOGRAPHY OVERLAY

–––––––––––––––––––––––––

if focus_data is not None:
theta, c, gh = focus_data

x = np.cos(theta) * (1 + c)
y = np.sin(theta) * (1 + c)

fig, ax = plt.subplots(figsize=(8, 8))

# Scatter
ax.scatter(x, y, s=10, alpha=0.4)

# GH corridor
if len(gh["theta_corridor"]) > 0:
    x_gh = np.cos(gh["theta_corridor"]) * (1 + gh["c_corridor"])
    y_gh = np.sin(gh["theta_corridor"]) * (1 + gh["c_corridor"])
    ax.scatter(x_gh, y_gh, s=20, color="gold", label="GH Corridor")

# White circle
circle = Circle((0, 0), radius=2.0, fill=False, linestyle="--", linewidth=1.5)
ax.add_patch(circle)

# Cross (axes)
ax.axhline(0)
ax.axvline(0)

# Fitted axis
angle, vec = fit_axis(x, y)
t = np.linspace(-3, 3, 100)
ax.plot(t * vec[0], t * vec[1], linewidth=2)

# Pentagons (nested)
for r in [0.5, 1.0, 1.5]:
    pent = RegularPolygon((0, 0), numVertices=5, radius=r, fill=False, linewidth=1.5)
    ax.add_patch(pent)

ax.set_aspect("equal")
ax.set_title("Transition Cartography — Knick Field Overlay")
ax.legend()

plt.show()
