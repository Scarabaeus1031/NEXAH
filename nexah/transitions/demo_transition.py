from transition_matrix import compute_transition_matrix

basin_ids = [0, 0, 1, 1, 2, 1, 0, 0]

P, basins = compute_transition_matrix(basin_ids)

print("Basins:", basins)
print("Transition Matrix:\n", P)
