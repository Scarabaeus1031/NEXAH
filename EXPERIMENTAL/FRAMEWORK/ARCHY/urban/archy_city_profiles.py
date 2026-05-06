CITY_PROFILES = {

    "Frankfurt": "financial",
    "Berlin": "spread",
    "London": "dense",
    "Paris": "dense",

    "New York": "dense",
    "Chicago": "dense",
    "Los Angeles": "sprawl",

    "Tokyo": "mega",
    "Shanghai": "mega",
    "Delhi": "mega",

    "São Paulo": "mega",
    "Buenos Aires": "dense",

    "Cairo": "dense",
    "Lagos": "mega",

    "Sydney": "coastal",
    "Melbourne": "coastal"
}


PROFILE_MULTIPLIER = {

    "mega": 1.08,
    "dense": 1.04,
    "financial": 1.03,
    "spread": 0.99,
    "sprawl": 0.95,
    "coastal": 1.01
}


def apply_city_profile(name, stability):

    profile = CITY_PROFILES.get(name, "dense")

    multiplier = PROFILE_MULTIPLIER.get(profile, 1.0)

    return stability * multiplier
