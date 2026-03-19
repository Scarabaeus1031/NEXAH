# kernel_bridge.py
"""
Schnittstelle für nexah_kernel: Exportiert Schlüssel-Metriken aus structured_oscillator_networks.
"""

import numpy as np

# Absolute Imports (geändert für die Skriptausführung)
try:
    from core.phase_vortex_detector import detect_vortex_defects, vortex_scan
    from core.chimera_state_detector import local_order_on_ring, classify_chimera_fraction
    from topology.shell_frustration_scan import run_simulation, order_parameter, vortex_count
except ImportError as e:
    print(f"Warnung: Einige Imports fehlen – Fehler: {e}")

def get_vortex_metrics(phase_ring=None, history=None, threshold=2.2):
    """
    Vortex-Count und Dichte – Indikator für Instabilität.
    """
    try:
        if history is not None and phase_ring is not None:
            defect_map = vortex_scan(history, threshold=threshold)
            vortex_counts = [len(v) for v in defect_map if v is not None]
            return {
                "vortex_count_avg": sum(vortex_counts) / len(vortex_counts) if vortex_counts else 0,
                "vortex_density": sum(vortex_counts) / (len(phase_ring) * len(history)) if len(phase_ring) > 0 and len(history) > 0 else 0
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
        return {"error": str(e)}

def get_chimera_status(phase_ring, radius=2):
    """
    Chimera-Status – Indikator für partielle Synchronisation.
    """
    try:
        local_R = local_order_on_ring(phase_ring, radius=radius)
        result = classify_chimera_fraction(local_R)
        if isinstance(result, tuple) and len(result) >= 2:
            fraction = result[0]
            classification = result[1]
        else:
            fraction = result
            classification = "unknown"
        return {
            "chimera_detected": classification == "chimera",
            "coherence_fraction": float(fraction) if fraction is not None else None,
            "classification": classification
        }
    except Exception as e:
        return {"error": str(e)}

def get_frustration_score(N=50, K=1.0, steps=4000, dt=0.01, base_delay=1000.0):
    """
    Frustration-Score basierend auf Sync-Delay – Proxy für Cascade-Risiko.
    """
    try:
        # Echter Aufruf – run_simulation gibt Tuple zurück
        result = run_simulation(N, K=K, steps=steps, dt=dt)
        
        # Flexibel unpacken – anpassen an deine echte Rückgabe
        if isinstance(result, tuple):
            sync_time = result[0] if len(result) > 0 else steps * dt
            R = result[1] if len(result) > 1 else 0.0
            history = result[2] if len(result) > 2 else None
        else:
            sync_time = result if isinstance(result, (int, float)) else steps * dt
            R = 0.0
            history = None
        
        score = max(0, (sync_time - base_delay) / base_delay)
        return {
            "frustration_score": score,
            "high_risk": score > 1.0,
            "shell_size": N,
            "sync_time": sync_time,
            "order_parameter": R
        }
    except Exception as e:
        return {"error": str(e)}

__all__ = [
    "get_vortex_metrics",
    "get_chimera_status",
    "get_frustration_score",
    "detect_vortex_defects", "vortex_scan",
    "local_order_on_ring", "classify_chimera_fraction",
    "run_simulation", "order_parameter", "vortex_count"
]

if __name__ == "__main__":
    print("Kernel Bridge läuft als Skript!")
    
    try:
        history = np.load('output/phase_history.npy')
        print("Phase-History geladen, Shape:", history.shape)
        
        phase_ring = history[-1] if history.ndim == 2 else history
        print("Vortex Metrics (echte Daten):", get_vortex_metrics(phase_ring=phase_ring, history=history))
        
        print("Chimera Status (letzter Snapshot):", get_chimera_status(phase_ring=phase_ring))
        
        print("Frustration Score (N=50):", get_frustration_score(N=50))
    except Exception as e:
        print("Fehler beim Laden echter Daten:", e)
