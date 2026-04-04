import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import imageio.v2 as imageio
import glob
import os

print("🚀 NEXAH Real Data Loader v14.8 – bereit für echte deutsche Netzdaten\n")

# ====================== ECHTE DATEN LADEN ======================
# Beispiel: CSV mit Spalten: timestamp, voltage_pu, frequency
# Passe den Pfad an deine echte Datei an
data_file = "deutsche_netzdaten_beispiel.csv"   # ← hier deine echte Datei eintragen

if not os.path.exists(data_file):
    print(f"⚠️  Datei {data_file} nicht gefunden.")
    print("Bitte lege eine CSV mit Spalten 'timestamp' und 'voltage_pu' an.")
    exit()

df = pd.read_csv(data_file)
print(f"✅ {len(df)} Messpunkte geladen")

t_real = df['timestamp'].values.astype(float)      # Zeit in Sekunden
voltage_real = df['voltage_pu'].values.astype(float)

# ====================== NEXAH ODE (an echte Spannung gekoppelt) ======================
def nexah_real_ode(t, x, voltage_target):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    # Hier koppeln wir die echte gemessene Spannung ein
    v_error = voltage_target - (1.0 + c)   # Fehler zur Nominalspannung
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi) + 5.0 * v_error
    f_vdp = (8.0/3.0) * dc * (1 - c**2)
    f_kuramoto = sum(1.62 * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota = 1.15 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 4.5)
    contraction = 0.92 if t < 12 else 0.68
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota) * I_phi * slow_start * contraction
    d_phi = 0.0
    if t > 18.0 and abs(dc) > 1.45 and abs(c) > 1.08 and phi == 2:
        d_phi = 24.0 + 15.0
    
    return [dc * contraction, d_dc, d_phi]

# ====================== SIMULATION ======================
x0 = [0.05, 0.0, 0]
sol = solve_ivp(lambda t, x: nexah_real_ode(t, x, voltage_real[int(min(t, len(voltage_real)-1))]), 
                (0, t_real[-1]), x0, method='RK45', rtol=1e-6, max_step=0.05)

print("✅ Simulation mit echten Daten abgeschlossen")

# Hier kannst du später die GIFs / Plots erzeugen – erstmal nur Test
print("\nOrdner 'real_german_grid_experiments' ist bereit.")
print("Lege jetzt deine echte CSV-Datei hinein und passe den Dateinamen oben an.")
