import numpy as np
from basin import assign_basins_by_threshold, assign_basins_kmeans

# simple signal
x = np.linspace(0, 10, 100)

basins = assign_basins_by_threshold(x, thresholds=[3, 7])

print("Threshold basins:", basins[:20])


# 2D example
X = np.column_stack((np.sin(x), np.cos(x)))

labels, centroids = assign_basins_kmeans(X, k=3)

print("KMeans basins:", labels[:20])
print("Centroids:", centroids)
