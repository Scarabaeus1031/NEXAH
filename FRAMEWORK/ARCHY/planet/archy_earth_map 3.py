from __future__ import annotations

import random
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_planet_simulator import generate_planet


def generate_world_cities(n=40):

    planet = generate_planet(8)

    cities = []

    for i in range(n):

        lat = random.uniform(-60, 70)
        lon = random.uniform(-180, 180)

        climate, stability = random.choice(
            random.choice(planet)
        )

        cities.append((lat, lon, stability))

    return cities


def plot_world(cities):

    fig = plt.figure(figsize=(12,6))

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    lats = [c[0] for c in cities]
    lons = [c[1] for c in cities]
    stability = [c[2] for c in cities]

    sc = ax.scatter(
        lons,
        lats,
        c=stability,
        cmap="viridis",
        s=120,
        transform=ccrs.PlateCarree()
    )

    plt.colorbar(sc, label="City Stability")

    plt.title("ARCHY Global Stability Map")

    plt.show()


if __name__ == "__main__":

    cities = generate_world_cities(60)

    plot_world(cities)
