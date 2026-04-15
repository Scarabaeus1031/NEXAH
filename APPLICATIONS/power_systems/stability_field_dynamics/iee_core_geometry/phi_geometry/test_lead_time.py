import numpy as np

# Beispiel: Spannungstrajektorie (ersetzen durch echte Daten!)
time = np.arange(0, 100, 1)
voltage = np.array([...])  # <- IEEE Daten

# Klassischer Collapse (z. B. V < 0.7)
collapse_idx = np.where(voltage < 0.7)[0][0]
t_classical = time[collapse_idx]

# Phi-Split (deine Drift-Logik)
def compute_drift(v):
    dv = np.diff(v)
    return np.abs(dv)

drift = compute_drift(voltage)

phi_split_idx = np.where(drift > 0.02)[0][0]  # placeholder threshold
t_phi = time[phi_split_idx]

lead_time = t_classical - t_phi

print("Phi-Split:", t_phi)
print("Collapse:", t_classical)
print("Lead Time:", lead_time)
