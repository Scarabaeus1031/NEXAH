"""
Switch Grid Mapper – Maps existing 3x3 / 2x2 Switch Points onto URF Axial Space
"""

import numpy as np
from .urf_axial_space_kernel import URFAxialSpaceKernel


class SwitchGridMapper:
    """
    Maps the v9.0 Switch Layer (3x3 + 2x2 grid) into the 3D URF Axial Space.
    """

    def __init__(self):
        self.kernel = URFAxialSpaceKernel()

    def map_grid_to_urf(self, switch_points: dict) -> dict:
        """
        switch_points example:
        {
            "3x3": [(x1,y1), (x2,y2), ...],
            "2x2": [(x1,y1), ...]
        }
        """
        mapped = {}

        for grid_name, points in switch_points.items():
            mapped[grid_name] = []
            for px, py in points:
                # Simple mapping: x→Theta, y→Magnet-Time, z→Beta Curvature
                state = {
                    "coherence": 0.92,
                    "coupling_dist": 0.05,
                    "theta_hz": px * 10,          # scale to frequency range
                    "flow_direction": py,
                    "beta_curvature": 0.8,
                    "memory_spin": 1.0
                }
                result = self.kernel.step(state)
                mapped[grid_name].append({
                    "grid_point": (px, py),
                    "urf_3d": result["position_3d"].tolist(),
                    "restricted_axis": result["restricted_axis"],
                    "switch_potential": result["switch_potential"]
                })

        return mapped


# Quick test helper
if __name__ == "__main__":
    mapper = SwitchGridMapper()
    example_grid = {
        "3x3": [(-1,1), (0,1), (1,1), (-1,0), (0,0), (1,0), (-1,-1), (0,-1), (1,-1)],
        "2x2": [(-0.5,0.5), (0.5,0.5), (-0.5,-0.5), (0.5,-0.5)]
    }
    result = mapper.map_grid_to_urf(example_grid)
    print("✅ Grid mapped to URF Axial Space")
    print(result)
