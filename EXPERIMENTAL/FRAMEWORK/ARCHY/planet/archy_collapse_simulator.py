from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------

BASE_YEAR = 2025
SIM_YEARS = 220
STEP = 10


# ---------------------------------------------------
# SYSTEM FUNCTIONS
# ---------------------------------------------------

def climate_stress(year):

    warming = 1 / (1 + np.exp(-(year - 2080) / 40))

    noise = np.random.normal(0,0.02)

    return max(0, warming + noise)


def water_stress(climate):

    return climate * 0.6 + np.random.normal(0,0.02)


def food_system(climate, water, trade):

    stress = climate * 0.4 + water * 0.4 + (1-trade) * 0.3

    food = max(0.1, 1 - stress)

    return food


def financial_system(previous):

    drift = previous + np.random.normal(0.02,0.03)

    return max(0.1, drift)


def trade_network(conflict):

    return max(0.1, 1 - conflict * 0.05)


def conflict_probability(food, finance):

    base = (1-food) * 0.5 + finance * 0.2

    return max(0, base)


# ---------------------------------------------------
# SINGLE SIMULATION
# ---------------------------------------------------

def run_simulation():

    cities = generate_global_city_dataset()

    year = BASE_YEAR

    finance = 0.8
    trade = 1.0
    conflict = 0

    climate_series=[]
    food_series=[]
    conflict_series=[]
    instability_series=[]

    for step in range(int(SIM_YEARS/STEP)):

        year += STEP

        climate = climate_stress(year)

        water = water_stress(climate)

        food = food_system(climate, water, trade)

        finance = financial_system(finance)

        conflict = conflict_probability(food, finance)

        trade = trade_network(conflict)

        instability = (
            climate*0.3 +
            water*0.2 +
            (1-food)*0.2 +
            finance*0.2 +
            conflict*0.1
        )

        climate_series.append(climate)
        food_series.append(food)
        conflict_series.append(conflict)
        instability_series.append(instability)

    return instability_series


# ---------------------------------------------------
# MONTE CARLO
# ---------------------------------------------------

def run_monte_carlo(n=200):

    runs=[]

    for i in range(n):

        r = run_simulation()

        runs.append(r)

        print("simulation",i+1,"/",n)

    return np.array(runs)


# ---------------------------------------------------
# ANALYSIS
# ---------------------------------------------------

def analyze(runs):

    mean = np.mean(runs,axis=0)

    p50 = np.percentile(runs,50,axis=0)
    p75 = np.percentile(runs,75,axis=0)
    p90 = np.percentile(runs,90,axis=0)

    return mean,p50,p75,p90


# ---------------------------------------------------
# PLOT
# ---------------------------------------------------

def plot(mean,p50,p75,p90):

    years = np.arange(len(mean))*STEP + BASE_YEAR + STEP

    plt.figure(figsize=(10,6))

    plt.plot(years,mean,label="mean")
    plt.plot(years,p50,label="median")
    plt.plot(years,p75,label="75% risk")
    plt.plot(years,p90,label="90% risk")

    plt.ylabel("Global Instability")
    plt.xlabel("Year")

    plt.title("ARCHY Earth System Collapse Scenarios")

    plt.legend()

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def run():

    runs = run_monte_carlo(200)

    mean,p50,p75,p90 = analyze(runs)

    plot(mean,p50,p75,p90)


if __name__=="__main__":

    run()
