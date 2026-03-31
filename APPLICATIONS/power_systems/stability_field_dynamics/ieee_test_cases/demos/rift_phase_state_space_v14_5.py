# rift_phase_state_space_v14_5.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

# --------------------------------------------------

# LOAD

# --------------------------------------------------

def load_data():
for name in ["trajectory.npy", "states.npy"]:
path = os.path.join(BASE_DIR, name)
if os.path.exists(path):
traj = np.load(path)
print(f"Loaded trajectory: {name}")
break
else:
raise FileNotFoundError("No trajectory found")

```
rift = np.load(os.path.join(RIFT_DIR, "rift_curve.npy"))
print("Loaded rift")

return traj[:, :2], rift
```

# --------------------------------------------------

# HELPERS

# --------------------------------------------------

def dominant_freq(signal):
fft_vals = np.fft.rfft(signal)
power = np.abs(fft_vals)
freqs = np.fft.rfftfreq(len(signal))
idx = np.argmax(power[1:]) + 1
return freqs[idx]

def wrap(x):
return (x + np.pi) % (2*np.pi) - np.pi

def regime_from_drive(d):
if d > 0.3:
return 1
elif d < -0.3:
return -1
else:
return 0

# --------------------------------------------------

# STATE EVOLUTION

# --------------------------------------------------

def run_state_model(traj):

```
x = traj[:, 0].copy()
y = traj[:, 1].copy()

f0 = dominant_freq(x)

N = len(x)

phi = np.zeros(N)
dphi = np.zeros(N)
drive = np.zeros(N)
regime = np.zeros(N)

ref_phi = np.zeros(N)

phi[0] = 0.0

for t in range(1, N):

    ref_phi[t] = (2*np.pi*f0*t) % (2*np.pi)

    # velocity
    v = traj[t] - traj[t-1]
    speed = np.linalg.norm(v)

    # curvature
    if t > 1:
        v_prev = traj[t-1] - traj[t-2]
        turn = np.linalg.norm(v - v_prev)
    else:
        turn = 0.0

    # phase error
    pe = wrap(phi[t-1] - ref_phi[t-1])

    # phase update
    dphi[t] = (
        2*np.pi*f0
        + 0.02 * speed
        + 0.015 * turn
        - 0.4 * pe
    )

    phi[t] = (phi[t-1] + dphi[t]) % (2*np.pi)

    # drive
    drive[t] = (
        np.sin(phi[t])
        + 0.5*np.sin(2*phi[t])
        + 0.3*np.sin(3*phi[t])
    )

    regime[t] = regime_from_drive(drive[t])

return phi, dphi, drive, regime
```

# --------------------------------------------------

# PLOTS

# --------------------------------------------------

def plot_state_space(phi, dphi, regime):

```
plt.figure(figsize=(8, 6))

for r, c in [(-1, "purple"), (0, "gold"), (1, "green")]:
    mask = regime == r
    plt.scatter(phi[mask], dphi[mask], s=20, label=f"regime {r}", color=c)

plt.axhline(0, linestyle="--")
plt.axvline(0, linestyle="--")

plt.xlabel("φ")
plt.ylabel("dφ/dt")
plt.title("V14.5 State Space (φ vs dφ/dt)")

plt.legend()
plt.grid(True)

path = os.path.join(RIFT_DIR, "v14_5_state_space.png")
plt.savefig(path, dpi=150)
print(f"Saved → {path}")
plt.close()
```

def plot_phase_time(phi, dphi, regime):

```
plt.figure(figsize=(10, 5))

plt.plot(phi, label="φ", color="blue")
plt.plot(dphi, label="dφ/dt", color="red")

for i in range(len(regime)):
    if regime[i] == 1:
        plt.axvline(i, color="green", alpha=0.05)
    elif regime[i] == -1:
        plt.axvline(i, color="purple", alpha=0.05)

plt.legend()
plt.grid(True)
plt.title("State Evolution")

path = os.path.join(RIFT_DIR, "v14_5_state_evolution.png")
plt.savefig(path, dpi=150)
print(f"Saved → {path}")
plt.close()
```

# --------------------------------------------------

# MAIN

# --------------------------------------------------

def main():

```
traj, _ = load_data()

phi, dphi, drive, regime = run_state_model(traj)

plot_state_space(phi, dphi, regime)
plot_phase_time(phi, dphi, regime)

print("V14.5 State-Space DONE")
```

if **name** == "**main**":
main()
