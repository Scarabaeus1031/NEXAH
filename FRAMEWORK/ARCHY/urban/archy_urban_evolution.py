from FRAMEWORK.ARCHY.planet.archy_climate_model import climate_stress


def evolve_stability(stability, climate, lat, year):

    noise = np.random.normal(0, 0.002)

    stress = climate_stress(lat, year)

    if climate == "urban_heat":
        trend = 0.002 - stress

    elif climate == "coastal":
        trend = 0.001 - stress

    elif climate == "tropical":
        trend = -0.001 - stress

    else:
        trend = -stress

    return max(0.25, min(0.45, stability + trend + noise))
