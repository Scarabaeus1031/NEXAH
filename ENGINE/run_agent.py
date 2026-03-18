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


def run_agent(landscape, steps=30, exploration_rate=0.2):
    size = landscape.shape[0]

    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(steps):

        x, y = pos
        current_value = landscape[x, y]

        neighbors = get_neighbors(pos, size)

        # exploration
        if np.random.rand() < exploration_rate:
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        # exploitation
        best_pos = pos
        best_value = current_value

        for nx, ny in neighbors:
            val = landscape[nx, ny]
            if val > best_value:
                best_value = val
                best_pos = (nx, ny)

        if best_pos == pos:
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        pos = best_pos
        path.append(pos)

    return path


def main():
    print("NEXAH Multi-Agent System (Exploration Mode)")
    print("Initializing landscape...\n")

    landscape = generate_stability_landscape()

    num_agents = 10
    final_positions = []

    for i in range(num_agents):
        path = run_agent(landscape)
        final_pos = path[-1]
        final_value = landscape[final_pos]

        final_positions.append((final_pos, final_value))

        print(f"Agent {i}: final position {final_pos} | stability {final_value:.3f}")

    print("\n--- Summary ---")

    values = [v for _, v in final_positions]

    print(f"Max stability found: {max(values):.3f}")
    print(f"Mean stability: {np.mean(values):.3f}")
    print(f"Unique end points: {len(set([p for p,_ in final_positions]))}")

    print("\nAgent finished.")


if __name__ == "__main__":
    main()
