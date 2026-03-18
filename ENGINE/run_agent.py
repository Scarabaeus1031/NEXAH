# ENGINE/run_agent.py

import numpy as np
from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape


def get_neighbors(pos, size):
    x, y = pos
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))

    return neighbors


def main():
    print("NEXAH Agent started")
    print("Initializing system...")

    landscape = generate_stability_landscape()
    size = landscape.shape[0]

    # 🔹 start random
    pos = (np.random.randint(0, size), np.random.randint(0, size))

    print(f"Starting position: {pos}")

    for step in range(10):

        x, y = pos
        current_value = landscape[x, y]

        print(f"\nStep {step}")
        print(f"Position: {pos} | Stability: {current_value:.3f}")

        neighbors = get_neighbors(pos, size)

        # best move
        best_pos = pos
        best_value = current_value

        for nx, ny in neighbors:
            val = landscape[nx, ny]
            if val > best_value:
                best_value = val
                best_pos = (nx, ny)

        if best_pos == pos:
            print("→ Local maximum reached")
            break
        else:
            print(f"→ Moving to {best_pos} (↑ stability)")
            pos = best_pos

    print("\nAgent finished.")


if __name__ == "__main__":
    main()
