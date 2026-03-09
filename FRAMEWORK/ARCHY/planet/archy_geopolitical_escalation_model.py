from __future__ import annotations

import numpy as np

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# STRESS MODELS
# ---------------------------------------------------

def climate_pressure(year):

    base = (year - 2025) * 0.01

    noise = np.random.normal(0,0.02)

    return max(0, base + noise)


def water_pressure(lat):

    belt = np.exp(-((abs(lat) - 25) ** 2) / 200)

    noise = np.random.normal(0,0.03)

    return max(0, belt + noise)


def food_pressure(lat):

    tropics = max(0, 1 - abs(lat)/40)

    noise = np.random.normal(0,0.02)

    return max(0, tropics + noise)


def financial_pressure():

    return np.random.uniform(0,0.3)


# ---------------------------------------------------
# CONFLICT PROBABILITY
# ---------------------------------------------------

def conflict_probability(climate, water, food, finance):

    stress = climate*0.3 + water*0.3 + food*0.2 + finance*0.2

    probability = min(1.0, stress)

    return probability


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    year = 2025

    for step in range(40):

        year += 5

        conflicts = 0

        for city in cities:

            climate = climate_pressure(year)

            water = water_pressure(city["lat"])

            food = food_pressure(city["lat"])

            finance = financial_pressure()

            p = conflict_probability(climate,water,food,finance)

            if np.random.random() < p*0.05:

                conflicts += 1

        print("Year:",year,"Conflicts:",conflicts)


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    run()
