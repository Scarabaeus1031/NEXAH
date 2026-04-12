import numpy as np

def classify_states(c, dc, d2c, fragmentation,
                    labels, gh_clusters, window=3):
    
    states = []
    
    for i in range(len(c)):
        
        # --- conditions ---
        frag_high = fragmentation[i] > np.percentile(fragmentation, 70)
        accel_high = abs(d2c[i]) > np.percentile(abs(d2c), 80)
        in_gh = labels[i] in gh_clusters
        
        # persistence
        start = max(0, i-window)
        persistent = sum([labels[j] in gh_clusters for j in range(start, i+1)]) >= 2
        
        # --- classification ---
        if not frag_high:
            state = "SAFE"
        
        elif frag_high and in_gh and persistent:
            state = "WARNING"
        
        elif accel_high and in_gh:
            state = "CRITICAL"
        
        else:
            state = "TRANSIENT"
        
        states.append(state)
    
    return states
