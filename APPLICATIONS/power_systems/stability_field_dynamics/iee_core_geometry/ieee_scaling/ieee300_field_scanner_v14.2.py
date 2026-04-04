import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn
import pandas as pd
from itertools import product

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

print("🚀 Starte NEXAH Field Scanner v14.2 (smart & eng um gute Konfiguration)\n")

# Bekannte gute Basis (v12.7)
BASE_Q = 1.62
BASE_WINDING = 6.5
BASE_IOTA = 1.15
BASE_CONTRACTION = 0.68

# Kleine Variationen um die gute Konfiguration
Q_VALUES = [1.55, 1.62, 1.68]
WINDING_THRESH = [6.0, 6.5, 7.0, 8.0]
IOTA_YUGO = [1.10, 1.15, 1.20]
CONTRACTION_VALUES = [0.65, 0.68, 0.72]

# ====================== ODE (exakt v12.7 + IOTA) ======================
def nexah_lorenz_ode(t, x, Q, winding_thresh, iota_yugo, contraction):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi)
    f_vdp = (8.0/3.0) * dc * (1 - c**2)
    f_kuramoto = sum((1 + Q) * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota = iota_yugo * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 5.0)
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota) * I_phi * slow_start * contraction
    
    d_phi = 0.0
    if t > 25.0 and abs(dc) > 1.8 and abs(c) > 1.2 and phi == 2:
        d_phi = 26.0 + 16.0
    
    return [dc * contraction, d_dc, d_phi]

# ====================== SCANNER ======================
results = []
net = pn.case300()

best_lead = 0
best_config = None

for Q, thresh, iota, contr in product(Q_VALUES, WINDING_THRESH, IOTA_YUGO, CONTRACTION_VALUES):
    x0 = [0.05, 0.0, 0]
    sol = solve_ivp(
        fun=lambda t, x: nexah_lorenz_ode(t, x, Q, thresh, iota, contr),
        t_span=(0, 80),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.04
    )
    
    t = sol.t
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)
    
    switch_time = None
    for i in range(1, len(phi_idx)):
        if phi_idx[i] > 0 and phi_idx[i-1] == 0:
            switch_time = t[i]
            break
    
    lead = (80 - switch_time) if switch_time is not None else 0.0
    split_str = f"{switch_time:.2f}s" if switch_time is not None else "kein Split"
    
    config = f"Q={Q:.2f} | W={thresh} | Iota={iota:.2f} | Contr={contr:.2f}"
    print(f"{config:40} → Split @ {split_str:8} | Vorsprung {lead:.1f}s")
    
    results.append([Q, thresh, iota, contr, switch_time, lead])
    
    if lead > best_lead:
        best_lead = lead
        best_config = config

# ====================== TABELLE ======================
df = pd.DataFrame(results, columns=["Q", "WINDING", "IOTA_YUGO", "CONTRACTION", "Split_t", "Lead_s"])
df = df.sort_values("Lead_s", ascending=False)

print("\n" + "="*90)
print("🏆 BESTE KONFIGURATIONEN")
print("="*90)
print(df.head(15).to_string(index=False))

print(f"\n🔥 Bester Vorsprung: {best_lead:.1f} Sekunden mit:")
print(best_config)

df.to_csv("ieee300_scanner_results_v14.2.csv", index=False)
print("\n📊 Tabelle gespeichert als: ieee300_scanner_results_v14.2.csv")

print("\nScanner fertig. Schick mir die Ausgabe (die Tabelle + beste Konfiguration).")
print("Dann machen wir direkt die Heatmap-GIF.")
