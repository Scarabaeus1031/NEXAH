# APPLICATIONS/power_systems/ieee_test_cases/lanif_band_v14.py

import numpy as np


def detect_resonance_peaks(radius, bins=60, top_k=2):
    """
    Find dominant radius values (peaks) from histogram.
    """
    r_flat = radius.flatten()

    hist, edges = np.histogram(r_flat, bins=bins)

    peak_indices = np.argsort(hist)[-top_k:]

    peaks = [(edges[i] + edges[i+1]) / 2 for i in peak_indices]

    return sorted(peaks)


def apply_lanif_band_auto(
    Fx,
    Fy,
    band_width=0.05,
    in_band_boost=1.8,
    out_band_damp=0.6,
    top_k=2
):
    """
    V14 — Auto LANIF Resonance Band

    - detect dominant radii
    - build multiple resonance bands
    """

    radius = np.sqrt(Fx**2 + Fy**2) + 1e-8

    peaks = detect_resonance_peaks(radius, top_k=top_k)

    mask_total = np.zeros_like(radius, dtype=bool)

    for r0 in peaks:
        mask = np.abs(radius - r0) < band_width
        mask_total |= mask

    # normalize direction
    Fx_norm = Fx / radius
    Fy_norm = Fy / radius

    Fx_new = Fx.copy()
    Fy_new = Fy.copy()

    # in-band → amplify
    Fx_new[mask_total] = Fx_norm[mask_total] * radius[mask_total] * in_band_boost
    Fy_new[mask_total] = Fy_norm[mask_total] * radius[mask_total] * in_band_boost

    # out-of-band → damp
    Fx_new[~mask_total] *= out_band_damp
    Fy_new[~mask_total] *= out_band_damp

    return Fx_new, Fy_new, mask_total, radius, peaks
