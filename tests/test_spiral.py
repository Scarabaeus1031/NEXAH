# test_spiral.py   ← bitte im Root-Ordner von NEXAH liegen

import sys
sys.path.insert(0, ".")

import numpy as np          # ← Das hat gefehlt!
import nexah
from nexah.spiral_coupling import SpiralCouplingLayer, SpiralCouplingKernel

print("✅ Import erfolgreich!")

# Test starten
kernel = SpiralCouplingKernel()
state = kernel.step(np.zeros(3))      # jetzt funktioniert es

print("✅ SpiralCouplingKernel funktioniert")
print(f"   Coherence:          {state['coherence']:.4f}")
print(f"   Stability:          {state['stability']}")
print(f"   Avg Coupling Dist:  {state['layer_state']['avg_coupling_dist']:.4f}")
