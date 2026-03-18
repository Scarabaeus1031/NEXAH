def run_agent(landscape, steps=30, exploration_rate=0.2):
    size = landscape.shape[0]

    pos = (np.random.randint(0, size), np.random.randint(0, size))
    path = [pos]

    for _ in range(steps):

        x, y = pos
        current_value = landscape[x, y]

        neighbors = get_neighbors(pos, size)

        # 🔥 Exploration step
        if np.random.rand() < exploration_rate:
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        # 🔥 Exploitation step (greedy)
        best_pos = pos
        best_value = current_value

        for nx, ny in neighbors:
            val = landscape[nx, ny]
            if val > best_value:
                best_value = val
                best_pos = (nx, ny)

        if best_pos == pos:
            # still allow escape
            pos = neighbors[np.random.randint(len(neighbors))]
            path.append(pos)
            continue

        pos = best_pos
        path.append(pos)

    return path
