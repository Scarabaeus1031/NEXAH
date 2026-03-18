from .models import RegimeLandscape


def build_regime_landscape(landscape_data):

    attractors = landscape_data.get("attractors", [])
    basins = landscape_data.get("basins", {})
    thresholds = landscape_data.get("thresholds", [])

    return RegimeLandscape(
        attractors=attractors,
        basins=basins,
        thresholds=thresholds,
    )
