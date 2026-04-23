"""
Simple test for URF Axial Space Kernel
"""

import sys
import numpy as np
sys.path.insert(0, ".")

from nexah.urf_axial_space import URFAxialSpaceKernel

def main():
    kernel = URFAxialSpaceKernel()

    # Example state from your existing Spiral Coupling
    test_state = {
        "coherence": 0.95,
        "coupling_dist": 0.02,
        "theta_hz": 63.0,           # Mercury example
        "flow_direction": 1.2,
        "beta_curvature": 0.85,
        "memory_spin": 1.0
    }

    result = kernel.step(test_state)

    print("✅ URF Axial Space Kernel Test")
    print(f"3D Position     : {result['position_3d']}")
    print(f"Memory Spin     : {result['memory_spin']:.4f}")
    print(f"Restricted Axis (√∫) : {result['restricted_axis']:.4f}")
    print(f"Coherence       : {result['coherence']}")
    print(f"Stability       : {result['stability']}")
    print(f"Matroschka Layer: {result['matroschka_layer']}")
    print(f"Switch Potential: {result['switch_potential']:.4f}")

if __name__ == "__main__":
    main()
