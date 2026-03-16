# kernel_bridge.py
"""
Schnittstelle für nexah_kernel: Exportiert Schlüssel-Metriken aus structured_oscillator_networks.
"""

from .core.phase_vortex_detector import detect_vortices  # Beispiel-Import (passe an echten Funktionsnamen an)
from .core.chimera_state_detector import detect_chimera
from .topology.shell_frustration_scan import compute_sync_time  # Beispiel
from .resonance.resonance_lattice_3D import compute_resonance_score  # Beispiel

def get_vortex_metrics(phase_grid):
    """
    Extrahiert Vortex-Count und Dichte – Indikator für Instabilität in Regime-Landschaften.
    """
    vortices = detect_vortices(phase_grid)
    return {
        "vortex_count": len(vortices),
        "vortex_density": len(vortices) / phase_grid.size if phase_grid.size > 0 else 0.0
    }

def get_chimera_status(phase_grid):
    """
    Erkennt Chimera-Zustände – Indikator für partielle Synchronisation & mögliche Tipping-Points.
    """
    is_chimera, coherence_map = detect_chimera(phase_grid)
    return {
        "chimera_detected": is_chimera,
        "coherence_ratio": coherence_map.mean() if coherence_map is not None else None
    }

def get_frustration_score(shell_size, sync_time):
    """
    Frustration-Score basierend auf Sync-Delay – Proxy für Cascade-Risiko.
    """
    # Einfache Heuristik – später aus Scans lernen
    base_delay = 10.0  # Beispiel-Baseline
    score = max(0, (sync_time - base_delay) / base_delay)
    return {
        "frustration_score": score,
        "high_risk": score > 1.5
    }

# Weitere Metriken hinzufügen, z. B.:
# def get_resonance_score(phase_grid): ...
# def get_sync_delay(shell_size): ...

__all__ = [
    "get_vortex_metrics",
    "get_chimera_status",
    "get_frustration_score",
    # mehr...
]
