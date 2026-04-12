from sklearn.cluster import KMeans
import numpy as np

def cluster_overlay(distance, residual, k=4):
    X = np.column_stack([distance, residual])
    
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
    
    return kmeans.labels_, kmeans.cluster_centers_
