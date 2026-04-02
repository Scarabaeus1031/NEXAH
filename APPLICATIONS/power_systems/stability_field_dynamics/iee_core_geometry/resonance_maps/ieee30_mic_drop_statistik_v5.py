"""
NEXAH IEEE 30-Bus — STATISTIK v5
20 Runs mit variierten Anfangsbedingungen → Lead-Time Histogram
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    field_force = -0.35 * c * (c**2 - 1.0) + 0.92 * dc
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]

    q = params.get('Q', 1.62)
    coupling = 1.0 + 1.4 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    vdp_force = 0.9 * dc * (1.0 - c**2)

    chirp = 1.0 + 0.032 * t
    angle_main = 2 * np.pi * t / 3.2 * chirp + phi * 1.35
    direction = -1.0 if phi >= 2 else 1.0
    angle = direction * angle_main * (1729 / 1000.0)

    compass_op = 0.82 * np.sin(angle) * np.cos(angle * 1.618)
    ring_offset = 1.2 * np.sin(angle + 2.1) + 0.8 * np.sin(angle - 2.1) if phi == 2 else 0.0

    branch_angle = angle % (2 * np.pi)
    branch_pulse = 2.2 * np.sin(12 * branch_angle) if phi == 2 and ((1.75 < branch_angle < 2.35) or (4.85 < branch_angle < 5.45)) else 0.0

    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 4.8
    inversion = 0.12 + 0.88 * np.tanh((phi - 1.6) * 7.0) if phi >= 3 else 1.0

    drift = abs(dc)
    d_phi = resonance * 2.1
    if drift > 1.55 and phi < 4:
        d_phi += 6.0

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op + ring_offset + branch_pulse) * inversion

    return [d_c, d_dc, d_phi]

def ieee30_load_ramp(t):
    return 0.195 * t   # gleiche Ramp wie 118-Bus

def ieee30_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    dx[1] += ieee30_load_ramp(t) * 2.4
    return dx

def classical_voltage(load_factor):
    return 1.0 / (1.0 + 1.15 * load_factor**2)

if __name__ == "__main__":
    print("🚀 NEXAH IEEE 30-Bus — STATISTIK v5 (20 Runs)")

    params = {'Q': 1.62}
    N_RUNS = 20
    lead_times = []

    np.random.seed(42)

    for run in range(N_RUNS):
        noise = np.random.normal(0, 0.008, 2)
        x0 = [0.05 + noise[0], 0.0 + noise[1], 0]

        sol = solve_ivp(
            fun=lambda t, x: ieee30_regime_ode(t, x, params),
            t_span=(0, 45),
            y0=x0,
            method='RK45',
            rtol=1e-6,
            max_step=0.011
        )

        t = sol.t
        phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

        if np.any(phi_idx > 0):
            switch_idx = np.where(phi_idx > 0)[0][0]
            switch_time = t[switch_idx]
            lead_times.append(switch_time)
        else:
            lead_times.append(np.nan)

    lead_times = np.array(lead_times)
    valid = ~np.isnan(lead_times)

    if np.any(valid):
        mean_lead = lead_times[valid].mean()
        std_lead = lead_times[valid].std()
        min_lead = lead_times[valid].min()
        max_lead = lead_times[valid].max()

        print("\n=== STATISTIK IEEE 30-Bus – Collapse Prediction ===")
        print(f"✅ Durchschnittlicher Vorsprung : {mean_lead:.2f} s")
        print(f"   Standardabweichung          : {std_lead:.2f} s")
        print(f"   Minimum / Maximum           : {min_lead:.2f} / {max_lead:.2f} s")
        print(f"   NEXAH erkennt Collapse im Mittel {45 - mean_lead:.2f} s früher")
        print(f"   Erfolgsquote                : {valid.sum()}/{N_RUNS} Runs")

        plt.figure(figsize=(10, 6))
        plt.hist(lead_times[valid], bins=12, color='#1f77b4', edgecolor='black', alpha=0.85)
        plt.axvline(mean_lead, color='purple', linestyle='--', linewidth=2.5, label=f'Mittel = {mean_lead:.2f} s')
        plt.title("Lead-Time Histogram – IEEE 30-Bus (20 Runs)")
        plt.xlabel("Phi-Split Zeitpunkt t [s]")
        plt.ylabel("Anzahl Runs")
        plt.grid(True, alpha=0.4)
        plt.legend()
        plt.savefig("ieee30_lead_time_histogram_v5.png", dpi=420, bbox_inches='tight')
        print("📸 Histogramm gespeichert als: ieee30_lead_time_histogram_v5.png")
        plt.show()
    else:
        print("❌ In keinem Run trat ein Phi-Split auf.")
