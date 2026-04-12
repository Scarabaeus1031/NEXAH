def gh_filter(labels, cluster_centers):
    # heuristic:
    # middle clusters = GH corridor
    
    idx_sorted = sorted(range(len(cluster_centers)),
                        key=lambda i: cluster_centers[i][0])
    
    core = idx_sorted[0]
    collapse = idx_sorted[-1]
    
    gh_clusters = idx_sorted[1:-1]
    
    return gh_clusters
