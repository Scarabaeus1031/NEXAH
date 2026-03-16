from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability
from FRAMEWORK.ARCHY.planet.archy_population_model import CITY_POPULATION


# ---------------------------------------------------
# INITIAL ENERGY INFRASTRUCTURE
# ---------------------------------------------------

CITY_ENERGY_CAPACITY = {

    "Frankfurt": 1.2,
    "Berlin": 2.5,
    "London": 3.0,
    "Paris": 2.2,

    "New York": 3.5,
    "Chicago": 2.0,
    "Los Angeles": 2.8,

    "Tokyo": 4.0,
    "Shanghai": 4.5,
    "Delhi": 3.0,

    "São Paulo": 3.0,
    "Buenos Aires": 2.2,

    "Cairo": 2.0,
    "Lagos": 1.0,

    "Sydney": 1.8,
    "Melbourne": 1.6
}


# ---------------------------------------------------
# ENERGY DEMAND MODEL
# ---------------------------------------------------

def energy_demand(population):

    base = population * 0.12
    noise = np.random.normal(0, 0.02)

    return max(0.05, base + noise)


# ---------------------------------------------------
# ENERGY INFRASTRUCTURE EVOLUTION
# ---------------------------------------------------

def evolve_energy_capacity(capacity):

    investment = 0.01
    decay = 0.004

    noise = np.random.normal(0, 0.003)

    return capacity * (1 + investment - decay + noise)


# ---------------------------------------------------
# ENERGY STRESS → STABILITY IMPACT
# ---------------------------------------------------

def energy_stress(demand, capacity):

    ratio = demand / capacity

    if ratio > 1.2:
        return -0.02

    if ratio > 1.0:
        return -0.01

    if ratio < 0.8:
        return +0.003

    return 0


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run_energy_simulation():

    cities = simulate_city_stability()

    city_data = {}

    for name, lat, lon, stability, climate in cities:

        population = CITY_POPULATION.get(name, 1)
        capacity = CITY_ENERGY_CAPACITY.get(name, 1)

        city_data[name] = {
            "lat": lat,
            "lon": lon,
            "population": population,
            "capacity": capacity,
            "stability": stability
        }

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    year = 2025

    def draw():

        ax.clear()

        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)

        lats = []
        lons = []
        stability = []
        sizes = []

        for city in city_data:

            data = city_data[city]

            lats.append(data["lat"])
            lons.append(data["lon"])
            stability.append(data["stability"])

            sizes.append(data["population"] * 20)

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

        ax.set_title(f"ARCHY Energy Simulator — {year}")

        return sc

    def update(frame):

        nonlocal year
        year += 10

        for city in city_data:

            data = city_data[city]

            pop = data["population"]
            capacity = data["capacity"]

            demand = energy_demand(pop)

            new_capacity = evolve_energy_capacity(capacity)

            stress = energy_stress(demand, new_capacity)

            data["capacity"] = new_capacity
            data["stability"] += stress

        print("Year:", year)

        return draw()

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=25,
        interval=1200
    )

    draw()

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_energy_simulation()
