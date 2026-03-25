radius(Fx, Fy)
    mask = np.abs(radius - target_radius) < band_width

    Fx2[mask] *= in_band_boost
    Fy2[mask] *= in_band_boost

    Fx2[~mask] *= out_band_damp
    Fy2[~mask] *= out_band_damp

    return Fx2, Fy2, mask, radius


def apply_multi_lanif_bands(Fx, Fy, bands=None, band_width=0.04,
                            in_band_boost=1.6, out_band_damp=0.75):
    """
    Optional multi-band version if you later want several discrete levels.

    bands default:
        [0.26, 0.48, 0.96]
    """
    if bands is None:
        bands = [0.26, 0.48, 0.96]

    Fx2 = Fx.copy()
    Fy2 = Fy.copy()

    radius = compute_flow_radius(Fx, Fy)

    mask = np.zeros_like(radius, dtype=bool)
    for b in bands:
        mask |= np.abs(radius - b) < band_width

    Fx2[mask] *= in_band_boost
    Fy2[mask] *= in_band_boost

    Fx2[~mask] *= out_band_damp
    Fy2[~mask] *= out_band_damp

    return Fx2, Fy2, mask, radius
