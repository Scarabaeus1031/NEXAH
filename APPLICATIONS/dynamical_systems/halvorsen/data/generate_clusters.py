import numpy as np
from sklearn.cluster import KMeans

traj = np.load("APPLICATIONS/dynamical_systems/halvorsen/data/trajectory.npy")

k = 18  # passt zu deinem System
kmeans = KMeans(n_clusters=k, random_state=0).fit(traj)

clusters = kmeans.labels_

np.save("APPLICATIONS/dynamical_systems/halvorsen/data/clusters.npy", clusters)

print("✓ clusters saved")
