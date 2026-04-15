import numpy as np

# ----------------------------------------
# 1. Test-Daten (ersetzen durch echte IEEE Daten!)
# ----------------------------------------

voltage = np.array([
    0.98, 0.97, 0.95, 0.92, 0.88,
    0.84, 0.79, 0.74, 0.71, 0.70,
    0.68, 0.65
])

time = np.arange(len(voltage))


# ----------------------------------------
# 2. Collapse Detection (klassisch)
# ----------------------------------------

collapse_threshold = 0.7
collapse_indices = np.where(voltage < collapse_threshold)[0]

if len(collapse_indices) == 0:
    print("❌ No collapse detected")
    collapse_idx = None
else:
    collapse_idx = collapse_indices[0]
    t_classical = time[collapse_idx]


# ----------------------------------------
# 3. Phi-Split Detection (einfacher Drift)
# ----------------------------------------

def compute_drift(v):
    dv = np.diff(v)
    return np.abs(dv)

drift = compute_drift(voltage)

phi_threshold = 0.02  # später anpassen!

phi_indices = np.where(drift > phi_threshold)[0]

if len(phi_indices) == 0:
    print("❌ No Phi-Split detected")
    phi_idx = None
else:
    phi_idx = phi_indices[0]
    t_phi = time[phi_idx]


# ----------------------------------------
# 4. Ergebnis
# ----------------------------------------

print("\n--- RESULTS ---")

if collapse_idx is not None:
    print(f"Collapse at t = {t_classical}")
else:
    print("Collapse not detected")

if phi_idx is not None:
    print(f"Phi-Split at t = {t_phi}")
else:
    print("Phi-Split not detected")

if collapse_idx is not None and phi_idx is not None:
    lead_time = t_classical - t_phi
    print(f"Lead Time = {lead_time}")
else:
    print("Lead Time not computable")
