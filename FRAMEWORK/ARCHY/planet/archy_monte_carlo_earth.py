from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset
from FRAMEWORK.ARCHY.planet.archy_earth_system_model import (
    compute_climate_stress,
    compute_water_stress,
    compute_food_index,
    initialize_finance,
    update_finance,
    compute_global_instability
)

# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------

SIMULATIONS = 300
STEPS = 30
BASE_YEAR = 2025


# ---------------------------------------------------
# SINGLE EARTH RUN
# ---------------------------------------------------

def run_single_simulation():

    cities = generate_global_city_dataset()

    finance = initialize_finance(cities)

    year = BASE_YEAR

    instability_series = []

    for step in range(STEPS):

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

        update_finance(finance)

        finance_values = list(finance.values())

        instability = compute_global_instability(
            climate,
            water,
            food,
            finance_values,
            conflicts,
            len(cities)
        )

        instability_series.append(instability)

    return instability_series


# ---------------------------------------------------
# MONTE CARLO
# ---------------------------------------------------

def run_monte_carlo():

    all_runs = []

    for i in range(SIMULATIONS):

        series = run_single_simulation()

        all_runs.append(series)

        print("Simulation", i+1, "/", SIMULATIONS)

    return np.array(all_runs)


# ---------------------------------------------------
# ANALYSIS
# ---------------------------------------------------

def analyze_results(all_runs):

    mean_path = np.mean(all_runs, axis=0)

    p50 = np.percentile(all_runs, 50, axis=0)
    p75 = np.percentile(all_runs, 75, axis=0)
    p90 = np.percentile(all_runs, 90, axis=0)

    return mean_path, p50, p75, p90


# ---------------------------------------------------
# PLOT
# ---------------------------------------------------

def plot_results(mean_path, p50, p75, p90):

    years = np.arange(len(mean_path)) * 10 + BASE_YEAR + 10

    plt.figure(figsize=(10,6))

    plt.plot(years, mean_path, label="Mean Instability")

    plt.plot(years, p50, label="Median")

    plt.plot(years, p75, label="75% risk")

    plt.plot(years, p90, label="90% risk")

    plt.xlabel("Year")

    plt.ylabel("Global Instability")

    plt.title("ARCHY Monte Carlo Earth System Risk")

    plt.legend()

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def run():

    all_runs = run_monte_carlo()

    mean_path, p50, p75, p90 = analyze_results(all_runs)

    plot_results(mean_path, p50, p75, p90)


if __name__ == "__main__":
    run()
