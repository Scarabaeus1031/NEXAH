# kernel_bridge.py
"""
Schnittstelle für nexah_kernel: Exportiert Schlüssel-Metriken aus structured_oscillator_networks.
"""

import numpy as np

# Relative Imports – funktionieren nur mit python -m ... (siehe unten)
try:
    from .core.phase_vortex_detector import detect_vortex_defects, vortex_scan
    from .core.chimera_state_detector import local_order_on_ring, classify_chimera_fraction
    from .topology.shell_frustration_scan import run_simulation, order_parameter, vortex_count
except ImportError as e:
    print(f"Warnung: Einige Imports fehlen – passe Pfade/Funktionsnamen an! Fehler: {e}")

def get_vortex_metrics(phase_ring=None, history=None, threshold=2.2):
    """
    Extrahiert Vortex-Count und Dichte – Indikator für Instabilität in Regime-Landschaften.
    """
    try:
        if history is not None:
            defect_map = vortex_scan(history, threshold=threshold)
            vortex_counts = [len(v) for v in defect_map]  # Beispiel-Auswertung
            return {
                "vortex_count_avg": sum(vortex_counts) / len(vortex_counts) if vortex_counts else 0,
                "vortex_density": sum(vortex_counts) / (len(phase_ring) * len(history)) if history and phase_ring is not None else 0
            }
        elif phase_ring is not None:
            defects = detect_vortex_defects(phase_ring, threshold=threshold)
            return {
                "vortex_count": len(defects),
                "vortex_density": len(defects) / len(phase_ring) if len(phase_ring) > 0 else 0.0
            }
        else:
            return {"error": "Weder phase_ring noch history angegeben"}
    except Exception as e:
        return {"error": f"Vortex-Metriken fehlgeschlagen: {e}"}

def get_chimera_status(phase_ring, radius=2):
    """
    Erkennt Chimera-Zustände – Indikator für partielle Synchronisation & mögliche Tipping-Points.
    """
    try:
        local_R = local_order_on_ring(phase_ring, radius=radius)
        fraction, classification = classify_chimera_fraction(local_R)  # passe an echte Rückgabe an
        return {
            "chimera_detected": classification == "chimera",
            "coherence_fraction": fraction
        }
    except Exception as e:
        return {"error": f"Chimera-Status fehlgeschlagen: {e}"}

def get_frustration_score(N, K=1.0, steps=4000, dt=0.01, base_delay=10.0):
    """
    Frustration-Score basierend auf Sync-Delay – Proxy für Cascade-Risiko.
    """
    try:
        # Realer Aufruf – läuft langsam, später optimieren/cachen
        # history, sync_time = run_simulation(N, K, steps, dt)  # Beispiel-Rückgabe anpassen
        sync_time = 15.0  # Platzhalter – später aus run_simulation
        score = max(0, (sync_time - base_delay) / base_delay)
        return {
            "frustration_score": score,
            "high_risk": score > 1.5,
            "shell_size": N,
            "sync_time": sync_time
        }
    except Exception as e:
        return {"error": f"Frustration-Score fehlgeschlagen: {e}"}

# Weitere Metriken – erweitern nach Bedarf
# def get_global_order(theta):
#     return order_parameter(theta)

__all__ = [
    "get_vortex_metrics",
    "get_chimera_status",
    "get_frustration_score",
    # mehr...
]

if __name__ == "__main__":
    print("Kernel Bridge läuft als Skript!")
    print("Beispiel-Aufruf:")
    print("from ENGINE.nexah_kernel.research.experiments.structured_oscillator_networks.kernel_bridge import get_vortex_metrics")
    print("Test: get_vortex_metrics(phase_ring=...)")
    # Optional: Dummy-Test
    dummy_ring = np.random.rand(100)
    print("Dummy Vortex-Metriken:", get_vortex_metrics(phase_ring=dummy_ring))
