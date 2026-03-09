from __future__ import annotations

import numpy as np


def climate_stress(lat, year):

    lat = abs(lat)

    # warming increases with time
    warming = (year - 2025) * 0.002

    if lat < 15:
        base = 0.01

    elif lat < 35:
        base = 0.006

    elif lat < 55:
        base = 0.004

    else:
        base = 0.003

    return base + warming
