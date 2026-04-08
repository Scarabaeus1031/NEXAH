import sys
import numpy as np
sys.path.insert(0, ".")

from nexah.urf_axial_space.switch_grid_mapper import SwitchGridMapper

def main():
    mapper = SwitchGridMapper()

    example_grid = {
        "3x3": [(-1,1), (0,1), (1,1), (-1,0), (0,0), (1,0), (-1,-1), (0,-1), (1,-1)],
        "2x2": [(-0.5,0.5), (0.5,0.5), (-0.5,-0.5), (0.5,-0.5)]
    }

    result = mapper.map_grid_to_urf(example_grid)

    print("✅ Switch Grid Mapper → URF Axial Space")
    print(f"3x3 points mapped: {len(result['3x3'])}")
    print(f"2x2 points mapped: {len(result['2x2'])}")
    print("\nBeispiel-Punkt (3x3 Mitte):")
    print(result["3x3"][4])   # der Punkt (0,0)

if __name__ == "__main__":
    main()
