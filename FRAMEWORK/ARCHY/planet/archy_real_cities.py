from __future__ import annotations

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.urban.archy_city_fields import simulate_city


# -----------------------------------------
# GLOBAL CITY LIST
# -----------------------------------------

CITIES = [

    ("Frankfurt", 50.1109, 8.6821),
    ("Berlin", 52.5200, 13.4050),
    ("London", 51.5072, -0.1276),
    ("Paris", 48.8566, 2.3522),

    ("New York", 40.7128, -74.0060),
    ("Chicago", 41.8781, -87.6298),
    ("Los Angeles", 34.0522, -118.2437),

    ("Tokyo", 35.6762, 139.6503),
    ("Shanghai", 31.2304, 121.4737),
    ("Delhi", 28.6139, 77.2090),

    ("São Paulo", -23.5505, -46.6333),
    ("Buenos Aires", -34.6037, -58.3816),

    ("Cairo", 30.0444, 31.2357),
    ("Lagos", 6.5244, 3.3792),

    ("Sydney", -33.8688, 151.2093),
    ("Melbourne", -37.8136, 144.9631),
]


# -----------------------------------------
# CLIMATE CLASSIFICATION
# -----------------------------------------

def classify_climate(lat: float) -> str:
    """
    Map latitude to ARCHY environments.
    """

    lat = abs(lat)

    if lat < 15:
        return "tropical"

    if lat < 35:
        return "coastal"

    if lat < 55:
        return "urban_heat"

    return "coastal""cold"


# -----------------------------------------
# CITY SIMULATION
# -----------------------------------------

def simulate_city_stability():

    results = []

    for name, lat, lon in CITIES:

        climate = classify_climate(lat)

        city, field, modified = simulate_city(
            climate,
            20,
            10
        )

        stability = modified.mean()

        results.append(
            (name, lat, lon, stability, climate)
        )

    return results


# -----------------------------------------
# PLOT WORLD MAP
# -----------------------------------------

def plot_world(cities):

    fig = plt.figure(figsize=(12,6))

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    lats = [c[1] for c in cities]
    lons = [c[2] for c in cities]
    stability = [c[3] for c in cities]

    sc = ax.scatter(
        lons,
        lats,
        c=stability,
        cmap="viridis",
        s=200,
        transform=ccrs.PlateCarree()
    )

    # label cities
    for name, lat, lon, _, climate in cities:
        ax.text(
            lon + 1,
            lat + 1,
            f"{name}",
            fontsize=8
        )

    plt.colorbar(sc, label="City Stability")

    plt.title("ARCHY Global Stability Map — Climate Aware")

    plt.show()


# -----------------------------------------
# MAIN
# -----------------------------------------

if __name__ == "__main__":

    cities = simulate_city_stability()

    for name, lat, lon, stability, climate in cities:

        print(
            f"{name:12} | climate={climate:10} | stability={stability:.3f}"
        )

    plot_world(cities)
