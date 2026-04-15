# APPLICATIONS/power_systems/ieee_test_cases/dual_resonance_v15b.py

import numpy as np


def detect_resonance_peaks(radius, bins=60, top_k=2):
    """
    Detect dominant radius peaks from histogram.
    Returns sorted list of peak centers.
    """
    r_flat = radius.flatten()
    hist, edges = np.histogram(r_flat, bins=bins)

    peak_indices = np.argsort(hist)[-top_k:]
    peaks = [(edges[i] + edges[i + 1]) / 2 for i in peak_indices]

    return sorted(peaks)


def apply_dual_resonance_stabilized(
    Fx,
    Fy,
    band_width=0.05,
    in_band_boost=1.5,
    out_band_damp=0.82,
    gap_boost=0.8,
    noise_strength=0.02,
    top_k=2,
    rng_seed=42
):
    """
    V15b:
    - detect two dominant resonance peaks
    - build dual bands
    - derive interference band from the gap between them
    - keep the gap softer (not over-constrained)
    - add mild noise to recover loops / local structure
    """
    rng = np.random.default_rng(rng_seed)

    radius = np.sqrt(Fx**2 + Fy**2) + 1e-8
    peaks = detect_resonance_peaks(radius, bins=60, top_k=top_k)

    if len(peaks) < 2:
        p1 = peaks[0] if len(peaks) == 1 else np.median(radius)
        p2 = np.max(radius)
        peaks = sorted([p1, p2])

    pA, pB = peaks[0], peaks[-1]
    gap = pB - pA

    mask_A = np.abs(radius - pA) < band_width
    mask_B = np.abs(radius - pB) < band_width
    mask_gap = np.abs(radius - gap) < band_width

    Fx_new = Fx.copy()
    Fy_new = Fy.copy()

    Fx_norm = Fx / radius
    Fy_norm = Fy / radius

    # Band A
    Fx_new[mask_A] = Fx_norm[mask_A] * pA * in_band_boost
    Fy_new[mask_A] = Fy_norm[mask_A] * pA * in_band_boost

    # Band B
    Fx_new[mask_B] = Fx_norm[mask_B] * pB * in_band_boost
    Fy_new[mask_B] = Fy_norm[mask_B] * pB * in_band_boost

    # Gap band softer than before
    Fx_new[mask_gap] = Fx_norm[mask_gap] * gap * gap_boost
    Fy_new[mask_gap] = Fy_norm[mask_gap] * gap * gap_boost

    mask_total = mask_A | mask_B | mask_gap

    # Outside: only mild damping now
    Fx_new[~mask_total] *= out_band_damp
    Fy_new[~mask_total] *= out_band_damp

    # Small noise to break over-determinism
    Fx_new += noise_strength * rng.standard_normal(Fx.shape)
    Fy_new += noise_strength * rng.standard_normal(Fy.shape)

    masks = {
        "A": mask_A,
        "B": mask_B,
        "gap": mask_gap,
        "total": mask_total,
    }

    return Fx_new, Fy_new, masks, radius, peaks, gap
