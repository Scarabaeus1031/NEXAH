from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# GLOBAL PARAMETERS
# ---------------------------------------------------

BASE_YEAR = 2025
CLIMATE_MIDPOINT = 2080
CLIMATE_RATE = 0.015
MAX_CLIMATE_STRESS = 5.0


# ---------------------------------------------------
# CLIMATE
# ---------------------------------------------------

def compute_climate_stress(lat: float, year: int) -> float:

    warming = MAX_CLIMATE_STRESS / (
        1 + np.exp(-CLIMATE_RATE * (year - CLIMATE_MIDPOINT))
    )

    lat_factor = 1 + (abs(lat) / 90.0) * 0.5
    drought = np.exp(-((abs(lat) - 25.0) ** 2) / 200.0)

    extreme = 0.0
    if np.random.rand() > 0.97:
        extreme = np.random.uniform(0.2, 0.6)

    noise = np.random.normal(0, 0.05)

    stress = warming * lat_factor * 0.5 + drought + extreme + noise

    return max(0.0, stress)


# ---------------------------------------------------
# WATER
# ---------------------------------------------------

def compute_water_stress(lat: float, year: int) -> float:

    warming = (year - BASE_YEAR) * 0.0015

    dry_zone = max(0.0, 1.0 - abs(lat - 25.0) / 25.0)

    noise = np.random.normal(0, 0.05)

    stress = warming * dry_zone + noise * 0.02

    return max(0.0, stress)


# ---------------------------------------------------
# FOOD
# ---------------------------------------------------

def compute_food_index(lat: float, year: int) -> float:

    base = 1.0

    climate_loss = (year - BASE_YEAR) * 0.002

    tropic_penalty = max(0.0, 1.0 - abs(lat) / 30.0)

    noise = np.random.normal(0, 0.05)

    food_index = base - climate_loss * tropic_penalty + noise

    return max(0.3, food_index)


# ---------------------------------------------------
# FINANCE
# ---------------------------------------------------

def initialize_finance(cities):

    finance = {}

    for city in cities:
        finance[city["name"]] = float(np.random.uniform(0.6, 1.0))

    return finance


def update_finance(finance):

    cascades = 0

    for name in finance:

        finance[name] += np.random.normal(0.02, 0.03)

        finance[name] *= np.random.uniform(0.98, 1.02)

        finance[name] = max(0.3, finance[name])

        if finance[name] > 1.3 and np.random.random() < 0.2:
            cascades += 1

    return cascades


# ---------------------------------------------------
# GLOBAL INSTABILITY
# ---------------------------------------------------

def compute_global_instability(climate, water, food, finance, conflicts, n):

    climate_term = np.mean(climate) / 5.0
    water_term = min(1.0, np.mean(water))
    food_term = max(0.0, 1.0 - np.mean(food))
    finance_term = min(1.0, np.mean(finance) / 2.0)
    conflict_term = conflicts / n

    instability = (
        climate_term * 0.25 +
        water_term * 0.20 +
        food_term * 0.20 +
        finance_term * 0.20 +
        conflict_term * 0.15
    )

    return max(0.0, min(1.0, instability))


# ---------------------------------------------------
# DRAW MAP
# ---------------------------------------------------

def draw_map(ax, cities, metric, year):

    ax.clear()

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    lats = [c["lat"] for c in cities]
    lons = [c["lon"] for c in cities]

    ax.scatter(
        lons,
        lats,
        c=metric,
        cmap="viridis",
        transform=ccrs.PlateCarree()
    )

    ax.set_title(f"ARCHY Earth System Stress {year}")


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    finance = initialize_finance(cities)

    fig = plt.figure(figsize=(14,8))

    ax_map = plt.subplot(221, projection=ccrs.PlateCarree())
    ax_instability = plt.subplot(222)
    ax_systems = plt.subplot(223)
    ax_conflicts = plt.subplot(224)

    year = BASE_YEAR

    years = []
    instability_series = []
    conflict_series = []

    climate_series = []
    water_series = []
    food_series = []
    finance_series = []

    def update(frame):

        nonlocal year

        year += 10

        climate = []
        water = []
        food = []

        conflicts = 0

        for city in cities:

            lat = city["lat"]
            name = city["name"]

            c = compute_climate_stress(lat, year)
            w = compute_water_stress(lat, year)
            f = compute_food_index(lat, year)

            climate.append(c)
            water.append(w)
            food.append(f)

            if np.random.random() < (c + w + (1-f)) * 0.02:
                conflicts += 1

        cascades = update_finance(finance)

        finance_values = list(finance.values())

        instability = compute_global_instability(
            climate,
            water,
            food,
            finance_values,
            conflicts,
            len(cities)
        )

        years.append(year)
        instability_series.append(instability)
        conflict_series.append(conflicts)

        climate_series.append(np.mean(climate))
        water_series.append(np.mean(water))
        food_series.append(np.mean(food))
        finance_series.append(np.mean(finance_values))

        print(
            "Year:",year,
            "Climate:",round(np.mean(climate),3),
            "Water:",round(np.mean(water),3),
            "Food:",round(np.mean(food),3),
            "Finance:",round(np.mean(finance_values),3),
            "Conflicts:",conflicts,
            "Cascades:",cascades,
            "Instability:",round(instability,3)
        )

        draw_map(ax_map, cities, climate, year)

        ax_instability.clear()
        ax_instability.plot(years, instability_series)
        ax_instability.set_ylim(0,1)
        ax_instability.set_title("Global Instability")

        ax_systems.clear()
        ax_systems.plot(years, climate_series,label="Climate")
        ax_systems.plot(years, water_series,label="Water")
        ax_systems.plot(years, food_series,label="Food")
        ax_systems.plot(years, finance_series,label="Finance")
        ax_systems.legend()
        ax_systems.set_title("System Stress")

        ax_conflicts.clear()
        ax_conflicts.plot(years, conflict_series)
        ax_conflicts.set_title("Conflicts")

    anim = animation.FuncAnimation(fig, update, frames=30, interval=1000)

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
