# test_spiral.py   ← im Root-Ordner von NEXAH

import sys
sys.path.insert(0, ".")        # damit Python das nexah-Package findet

import nexah
from nexah.spiral_coupling import SpiralCouplingLayer, SpiralCouplingKernel

print("✅ Import erfolgreich!")

# Kleiner Test
kernel = SpiralCouplingKernel()
print("✅ SpiralCouplingKernel erstellt")

state = kernel.step(np.zeros(3))
print("✅ Ein Schritt ausgeführt")
print("   Coupling Distance:", state["layer_state"]["avg_coupling_dist"])
print("   Coherence:", state["coherence"])
