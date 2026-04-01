import pandapower as pp
import numpy as np
import matpower as mp

def load_ieee14():
    """Lädt das IEEE 14-Bus Netzwerk von Pandapower."""
    return pp.networks.case14()

def load_ieee30():
    """Lädt das IEEE 30-Bus Netzwerk von Pandapower."""
    return pp.networks.case30()

def load_ieee57():
    """Lädt das IEEE 57-Bus Netzwerk von Pandapower."""
    return pp.networks.case57()

def load_ieee118():
    """Lädt das IEEE 118-Bus Netzwerk von Pandapower."""
    return pp.networks.case118()

def load_matpower_case(file_path):
    """Lädt ein Matpower Netzwerk."""
    # Hier könnte man das Matpower Python Interface verwenden
    # Beispiel: mp.loadcase(file_path)
    pass

def load_gridlabd_case(file_path):
    """Lädt ein GridLab-D Netzwerk."""
    # Hier könnte man das GridLab-D Interface verwenden
    pass

def get_network_data(net):
    """Extrahiert nützliche Daten aus einem Netzwerk."""
    return {
        "bus": net.bus,
        "line": net.line,
        "load": net.load
    }

def save_network_state(state, path):
    """Speichert den Zustand des Netzwerks (z.B. als .json oder .csv)."""
    np.savetxt(path, state)
