# APPLICATIONS/power_systems/stability_field_dynamics/ieee_application/scripts/run_ieee_field_navigation_poc.py

import numpy as np
from nexah_loader import load_ieee_case  # Der Import von nexah_loader funktioniert jetzt
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.demos.rift_final_controller_v7 import RiftFieldController
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.demos.rift_instability_detector import RiftInstabilityDetector
from nexah.engine.core import NEXAHKernel
from nexah.framework.core_geometry import CoreGeometry

# ================== KONFIGURATION ==================
IEEE_CASE = 30  # 14, 30, 57, 118, 300
RUNS = 5        # Mehrere Durchläufe für Statistik
PRINT_RESULTS = True

# ================== SETUP ==================
print("🚀 NEXAH Field Navigation PoC gestartet...")

# 1. IEEE-Netz laden
grid = load_ieee_case(IEEE_CASE)
print(f"   IEEE {IEEE_CASE}-Bus Netz geladen ({len(grid.buses)} Busse)")

# 2. Core Geometry aktivieren
geometry = CoreGeometry()
geometry.set_mode("hex_phase")  # Oder "root_space" / "tesseract"
print("   Core Geometry aktiviert (Hex-Phase Mode)")

# 3. NEXAH Kernel
kernel = NEXAHKernel(geometry=geometry)

# 4. Rift Detector + Controller
detector = RiftInstabilityDetector(kernel)
controller = RiftFieldController(kernel, version="v28")

# ================== TEST LOOP ==================
stability_before = []
stability_after = []
critical_faden = None

for i in range(RUNS):
    print(f"\n   Run {i+1}/{RUNS} ...")
    
    # Field erzeugen
    field = kernel.build_field(grid)
    
    # Rifts finden
    rifts = detector.detect_rifts(field)
    
    # Vorher-Stabilität berechnen
    stab_before = kernel.compute_stability(field)
    stability_before.append(stab_before)
    
    # Navigation: Kritischen Faden finden und steuern
    action, critical_node = controller.navigate(field, rifts)
    critical_faden = critical_node  # Speichern
    
    # Nachher-Stabilität
    field_after = controller.apply_action(field, action)
    stab_after = kernel.compute_stability(field_after)
    stability_after.append(stab_after)

# ================== ERGEBNISSE ==================
avg_before = np.mean(stability_before)
avg_after = np.mean(stability_after)
improvement = avg_after - avg_before

print("\n" + "="*60)
print("NEXAH FIELD NAVIGATION RESULT")
print("="*60)
print(f"Before Stability : {avg_before:.4f}")
print(f"After Stability  : {avg_after:.4f}")
print(f"Improvement      : +{improvement:.4f} ({improvement*100:.2f} %)")
print(f"Critical Faden   : Node {critical_faden}")
print("="*60)

# Optional: Plot speichern
controller.plot_field_comparison(field, field_after, 
                                 save_path=f"results/ieee_{IEEE_CASE}_field_navigation_poc.png")

print("✅ Demo fertig. Plot gespeichert.")
