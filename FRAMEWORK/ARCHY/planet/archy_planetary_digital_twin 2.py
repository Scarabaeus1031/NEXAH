from __future__ import annotations

import numpy as np

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


# ---------------------------------------------------
# PLANET STATE
# ---------------------------------------------------

class PlanetState:

    def __init__(self,cities):

        self.cities = cities

        self.year = 2025

        self.global_instability = 0.0

        self.climate_stress = 0.0

        self.financial_stress = 0.0

        self.conflicts = 0


# ---------------------------------------------------
# UPDATE SYSTEM
# ---------------------------------------------------

def update_planet(state):

    state.year += 5

    state.climate_stress += np.random.normal(0.001,0.002)

    state.financial_stress += np.random.normal(0.001,0.003)

    conflict_probability = max(
        0,
        state.climate_stress +
        state.financial_stress +
        np.random.normal(0,0.01)
    )

    if conflict_probability > 0.2:

        state.conflicts += np.random.randint(1,3)

    state.global_instability = (
        state.climate_stress +
        state.financial_stress +
        state.conflicts * 0.01
    )


# ---------------------------------------------------
# RUN
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    state = PlanetState(cities)

    for step in range(50):

        update_planet(state)

        print(
            "Year:",state.year,
            "Climate:",round(state.climate_stress,3),
            "Finance:",round(state.financial_stress,3),
            "Conflicts:",state.conflicts,
            "Instability:",round(state.global_instability,3)
        )


if __name__ == "__main__":
    run()
