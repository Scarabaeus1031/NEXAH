# APPLICATIONS/power_systems/ieee_test_cases/lanif_band_v13c.py

import numpy as np


def apply_lanif_band(
    Fx,
    Fy,
    target_radius=0.26,
    band_width=0.05,
    in_band_boost=1.8,
    out_band_damp=0.6
):
    """
    V13c — LANIF Band

    Idea:
    Quantize the flow field onto a preferred radius band.

    - radius = flow magnitude
    - particles in band → amplified (resonance channel)
    - outside → damped (decay / shadow region)

    Returns:
        Fx_new, Fy_new, mask, radius
    """

    # ===== RADIUS =====
    radius = np.sqrt(Fx**2 + Fy**2) + 1e-8  # avoid division by zero

    # ===== BAND MASK =====
    mask = np.abs(radius - target_radius) < band_width

    # ===== NORMALIZE FLOW DIRECTION =====
    Fx_norm = Fx / radius
    Fy_norm = Fy / radius

    # ===== NEW FIELD =====
    Fx_new = Fx.copy()
    Fy_new = Fy.copy()

    # in-band → amplify + align to target radius
    Fx_new[mask] = Fx_norm[mask] * target_radius * in_band_boost
    Fy_new[mask] = Fy_norm[mask] * target_radius * in_band_boost

    # out-of-band → damp
    Fx_new[~mask] *= out_band_damp
    Fy_new[~mask] *= out_band_damp

    return Fx_new, Fy_new, mask, radius
