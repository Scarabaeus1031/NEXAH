from __future__ import annotations

import random
import numpy as np


# ---------------------------------------------------
# BASE CITY SEEDS (real anchors)
# ---------------------------------------------------

BASE_CITIES = [

    ("New York", 40.7128, -74.0060, 8.5),
    ("Los Angeles", 34.0522, -118.2437, 3.9),
    ("Chicago", 41.8781, -87.6298, 2.7),

    ("London", 51.5072, -0.1276, 9.0),
    ("Paris", 48.8566, 2.3522, 2.2),
    ("Berlin", 52.5200, 13.4050, 3.6),
    ("Frankfurt", 50.1109, 8.6821, 0.75),

    ("Tokyo", 35.6762, 139.6503, 14.0),
    ("Shanghai", 31.2304, 121.4737, 24.0),
    ("Delhi", 28.6139, 77.2090, 30.0),

    ("São Paulo", -23.5505, -46.6333, 22.0),
    ("Buenos Aires", -34.6037, -58.3816, 15.0),

    ("Cairo", 30.0444, 31.2357, 20.0),
    ("Lagos", 6.5244, 3.3792, 21.0),

    ("Sydney", -33.8688, 151.2093, 5.3),
    ("Melbourne", -37.8136, 144.9631, 5.1),
]


# ---------------------------------------------------
# CLIMATE CLASSIFICATION
# ---------------------------------------------------

def classify_climate(lat):

    lat = abs(lat)

    if lat < 15:
        return "tropical"

    if lat < 35:
        return "coastal"

    if lat < 55:
        return "urban_heat"

    return "cold"


# ---------------------------------------------------
# SYNTHETIC CITY GENERATOR
# ---------------------------------------------------

def generate_city_cluster(base_name, lat, lon, pop, n=10):

    cities = []

    for i in range(n):

        dlat = random.uniform(-3, 3)
        dlon = random.uniform(-3, 3)

        new_lat = lat + dlat
        new_lon = lon + dlon

        population = max(0.5, pop * random.uniform(0.2, 1.0))

        gdp = population * random.uniform(0.5, 1.5)

        energy = population * random.uniform(0.3, 1.2)

        name = f"{base_name}_{i}"

        climate = classify_climate(new_lat)

        cities.append({

            "name": name,
            "lat": new_lat,
            "lon": new_lon,
            "population": population,
            "gdp": gdp,
            "energy": energy,
            "climate": climate
        })

    return cities


# ---------------------------------------------------
# GLOBAL CITY DATASET
# ---------------------------------------------------

def generate_global_city_dataset(cluster_size=12):

    cities = []

    for base in BASE_CITIES:

        name, lat, lon, pop = base

        cluster = generate_city_cluster(
            name,
            lat,
            lon,
            pop,
            cluster_size
        )

        cities.extend(cluster)

    return cities


# ---------------------------------------------------
# NUMERIC MATRIX EXPORT
# ---------------------------------------------------

def dataset_to_matrix(cities):

    data = []

    for c in cities:

        data.append([
            c["lat"],
            c["lon"],
            c["population"],
            c["gdp"],
            c["energy"]
        ])

    return np.array(data)


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    cities = generate_global_city_dataset()

    print("Generated cities:", len(cities))

    for c in cities[:10]:

        print(
            c["name"],
            c["population"],
            c["climate"]
        )
