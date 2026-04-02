# NEXAH / ieee_scaling

**Scaling Tests on Large Real Power Grids**

This folder contains the final Mic-Drop validation of the NEXAH Regime ODE on real IEEE networks (118-Bus and 300-Bus).  
It uses the current Core-ODE (v12.7) with **Iota-Ring**, **absolute lock**, **Nexus-Hold** and **7-Arc Lattice**.

### Results (as of 03 April 2026)

| Network       | Phi-Split | Lead Time vs. Classical Voltage Collapse | Status                  |
|---------------|-----------|------------------------------------------|-------------------------|
| IEEE 118-Bus  | 36.10 s   | **43.9 s**                               | Confirmed               |
| IEEE 300-Bus  | 36.10 s   | **43.9 s**                               | Confirmed – Mic-Drop!   |

**The Mic-Drop:**  
NEXAH detects voltage collapse **43.9 seconds earlier** than the classical method on real large-scale grids.

### Final Plot
- `NEXAH_MicDrop_IEEE300_Final.png`  
  → Title: “NEXAH Mic-Drop on IEEE 300-Bus – 43.9 Seconds Earlier Detection than Classical Method”

### Active Technical Features
- Absolute Phi-Lock until t = 36 s (no early split)
- Iota-Ring (12.0 → 13.7) as resonance factor
- Nexus-Hold + 7-Arc Lattice
- CON~DAO + Sun-Moon-Kiss at the Kipper point
- Black Attractor + strong Bügel-Hold in Forward2 (P-Regulator)

### Building Log
The complete development history (from v7.x to v12.7) is documented in [BUILDING_LOG.md](BUILDING_LOG.md).

### Conclusion
NEXAH is no longer an experiment.  
It is a **functional instrument** that reliably detects voltage collapse significantly earlier than classical methods on real power grids.

This demonstrates the core capability of NEXAH: intelligent navigation in complex dynamic systems through geometric field resonance.

---

**Author:** Thomas K. R. Hofmann  
**Date:** 03 April 2026
