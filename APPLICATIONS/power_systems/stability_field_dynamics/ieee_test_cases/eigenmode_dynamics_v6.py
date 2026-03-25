import numpy as np


def extract_boundary_points(boundary):
    """
    Extract (x, y) coordinates of boundary pixels.
    Returns array of shape (N, 2).
    """
    ys, xs = np.where(boundary > 0)
    if len(xs) == 0:
        return np.empty((0, 2))
    return np.column_stack([xs, ys])


def compute_pca_axes(points):
    """
    Compute principal axes of boundary point cloud using PCA.
    Returns:
        center: mean point
        eigvals: eigenvalues (descending)
        eigvecs: eigenvectors (columns, descending)
    """
    if len(points) < 2:
        return None, None, None

    center = points.mean(axis=0)
    centered = points - center

    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)

    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    return center, eigvals, eigvecs


def compute_hessian_like_curvature(field):
    """
    Simple second-derivative structure for curvature-like analysis.
    """
    gy, gx = np.gradient(field)
    gyy, gyx = np.gradient(gy)
    gxy, gxx = np.gradient(gx)

    curvature = gxx + gyy
    return curvature, (gxx, gxy, gyx, gyy)


def normalize_field(field):
    fmin = np.min(field)
    fmax = np.max(field)
    if np.isclose(fmax, fmin):
        return np.zeros_like(field)
    return (field - fmin) / (fmax - fmin)
