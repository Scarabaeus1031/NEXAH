import pandapower.networks as pn
import pandapower as pp
import numpy as np


def create_base_case():
    net = pn.case9()
    return net


def powerflow_solver(lam):
    net = create_base_case()

    # --- scale loads ---
    net.load["p_mw"] *= lam
    net.load["q_mvar"] *= lam

    try:
        pp.runpp(net, algorithm='nr')
        converged = True
    except:
        converged = False

    # --- extract results ---
    if converged:
        V = net.res_bus.vm_pu.values
        theta = np.deg2rad(net.res_bus.va_degree.values)
    else:
        # fallback values
        V = np.ones(len(net.bus)) * np.nan
        theta = np.zeros(len(net.bus))

    return {
        "V": V,
        "theta": theta,
        "converged": converged
    }
