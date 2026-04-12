import numpy as np

def detect_channel_direction(c, dc, indices):
    pts = np.column_stack([c[indices], dc[indices]])
    
    mean = np.mean(pts, axis=0)
    centered = pts - mean
    
    U, S, Vt = np.linalg.svd(centered)
    
    principal_dir = Vt[0]
    
    return principal_dir
