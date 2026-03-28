import pandapower as pp
import copy
import numpy as np


def find_collapse_point(net, bus, min_factor=1.0, max_factor=6.0, steps=50):
    factors = np.linspace(min_factor, max_factor, steps)

    for f in factors:
        net_copy = copy.deepcopy(net)

        mask = net_copy.load["bus"] == bus
        net_copy.load.loc[mask, "p_mw"] *= f

        try:
            pp.runpp(net_copy)
        except Exception:
            return f  # first collapse detected

    return max_factor  # no collapse found


def run_sensitivity_analysis(net):
    results = {}

    load_buses = net.load["bus"].unique()

    for bus in load_buses:
        collapse = find_collapse_point(net, bus)
        results[int(bus)] = collapse

    return results
