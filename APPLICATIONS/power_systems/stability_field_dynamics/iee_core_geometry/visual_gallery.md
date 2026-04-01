# NEXAH Visual Gallery – Core ODE Evolution

**Stand:** April 2026 | iee_core_geometry/core_odes/

### Wichtige Versionen & Erkenntnisse

**v1.9** – Starke nested Schlaufen + 3 Lücken  
**v2.0** – Final nested Möbius + klares Band + Expansion rechts

### Wichtige Beobachtungen

- Phi-State ist der **Regulator** (kommt aus 0, steigt stufenweise)
- Q-Wert wirkt als **Verstärker** der Geometrie (ab Q ≈ 1.28 wird das Band deutlich)
- c(t) zeigt **3 klare Dämpfungen/Lücken** (Regime-Übergänge)
- Phase Portrait zeigt **nested Möbius** (Schlaufe in der Schlaufe + Band)
- Inversion (Bass-Schlüssel) tritt bei Reverse-Zuständen auf

**Nächstes Ziel:** Integration mit IEEE 9-Bus Testfall

(Die Plots liegen in `core_odes/nexah_regime_test_v*.png`)
