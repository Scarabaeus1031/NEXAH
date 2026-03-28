import pandapower as pp
import copy

def run_stability_scan(net, min_factor=1.0, max_factor=2.0, steps=20):
    results = []

    for i in range(steps + 1):
        factor = min_factor + (max_factor - min_factor) * i / steps

        # FIX: pandapowerNet hat kein .deepcopy()
        net_copy = copy.deepcopy(net)

        net_copy.load["p_mw"] *= factor

        try:
            pp.runpp(net_copy)
            stable = True
        except Exception:
            stable = False

        results.append((factor, stable))

    return results
