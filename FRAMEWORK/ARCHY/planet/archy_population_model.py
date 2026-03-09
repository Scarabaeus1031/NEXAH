from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability


# ---------------------------------------------------
# INITIAL POPULATION DATA (very rough estimates)
# ---------------------------------------------------

CITY_POPULATION = {

    "Frankfurt": 0.75,
    "Berlin": 3.6,
    "London": 9.0,
    "Paris": 2.2,

    "New York": 8.5,
    "Chicago": 2.7,
    "Los Angeles": 3.9,

    "Tokyo": 14.0,
    "Shanghai": 24.0,
    "Delhi": 30.0,

    "São Paulo": 22.0,
    "Buenos Aires": 15.0,

    "Cairo": 20.0,
    "Lagos": 21.0,

    "Sydney": 5.3,
    "Melbourne": 5.1
}


# ---------------------------------------------------
# POPULATION DYNAMICS
# ---------------------------------------------------

def evolve_population(pop, stability):

    # base growth
    growth_rate = 0.01

    # instability reduces growth
    stress = (0.35 - stability) * 0.05

    noise = np.random.normal(0, 0.002)

    new_pop = pop * (1 + growth_rate - stress + noise)

    return max(0.1, new_pop)


# ---------------------------------------------------
# STABILITY IMPACT FROM POPULATION
# ---------------------------------------------------

def population_stress(pop):

    # large cities get infrastructure stress
    if pop > 20:
        return -0.01

    if pop > 10:
        return -0.005

    return 0.002


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run_population_simulation():

    cities = simulate_city_stability()

    city_data = {}

    for name, lat, lon, stability, climate in cities:

        population = CITY_POPULATION.get(name, 1)

        city_data[name] = {
            "lat": lat,
            "lon": lon,
            "stability": stability,
            "population": population
        }

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    year = 2025

    def draw():

        ax.clear()

        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)

        lats = []
        lons = []
        sizes = []
        stability = []

        for city in city_data:

            data = city_data[city]

            lats.append(data["lat"])
            lons.append(data["lon"])

            sizes.append(data["population"] * 20)
            stability.append(data["stability"])

        sc = ax.scatter(
            lons,
            lats,
            c=stability,
            s=sizes,
            cmap="viridis",
            transform=ccrs.PlateCarree(),
            vmin=0.25,
            vmax=0.40
        )

        for city in city_data:

            ax.text(
                city_data[city]["lon"] + 1,
                city_data[city]["lat"] + 1,
                city,
                fontsize=8
            )

        ax.set_title(f"ARCHY Population Simulator — {year}")

        return sc

    def update(frame):

        nonlocal year

        year += 10

        for city in city_data:

            data = city_data[city]

            pop = data["population"]
            stability = data["stability"]

            new_pop = evolve_population(pop, stability)

            stress = population_stress(new_pop)

            data["population"] = new_pop
            data["stability"] += stress

        print("Year:", year)

        return draw()

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=20,
        interval=1200
    )

    draw()

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_population_simulation()
