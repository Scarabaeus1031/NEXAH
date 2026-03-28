def run_2d_stability_scan_v2(
    net,
    min_load=3.5,
    max_load=6.0,
    min_gen=0.3,
    max_gen=1.0,
    steps=40
):
    import numpy as np
    import copy
    import pandapower as pp

    load_factors = np.linspace(min_load, max_load, steps)
    gen_factors = np.linspace(min_gen, max_gen, steps)

    landscape = np.zeros((steps, steps))

    for i, lf in enumerate(load_factors):
        for j, gf in enumerate(gen_factors):

            net_copy = copy.deepcopy(net)

            # 🔥 EXTREMER LOAD STRESS
            net_copy.load["p_mw"] *= lf

            # 🔥 GENERATOR LIMITIERUNG
            net_copy.gen["p_mw"] *= gf

            # 🔥 SLACK BUS LIMITIEREN (KRITISCH!)
            net_copy.ext_grid["vm_pu"] = 1.0

            try:
                pp.runpp(net_copy, max_iteration=20)
                
                # zusätzlicher Instabilitätscheck
                min_vm = net_copy.res_bus["vm_pu"].min()

                if min_vm < 0.7:
                    landscape[i, j] = 0  # instabil (voltage collapse)
                else:
                    landscape[i, j] = 1

            except:
                landscape[i, j] = 0

    return load_factors, gen_factors, landscape
