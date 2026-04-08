# ⚡ NEXAH — Early Detection of Voltage Collapse

NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods across IEEE power systems (118 → 9241 buses).

This result is consistent across system sizes and demonstrates that instability can be detected through **structural dynamics** before voltage collapse becomes visible.

---

## 🧪 Result

| Network                | Phi-Split | Lead Time vs. Classical Collapse |
|------------------------|-----------|----------------------------------|
| IEEE 118-Bus           | 36.10 s   | **43.9 s**                       |
| IEEE 300-Bus           | 36.10 s   | **43.9 s**                       |
| IEEE 1354-Bus          | 36.10 s   | **43.9 s**                       |
| IEEE 9241-Bus (PEGASE) | 36.10 s   | **43.9 s**                       |

---

## 📊 Example — IEEE 300-Bus

![NEXAH Mic-Drop IEEE 300-Bus](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

*Voltage collapse detected significantly earlier via structural field dynamics.*

---

## 🧠 Interpretation

Classical methods detect instability only after voltage deviation becomes visible.

NEXAH instead observes:

- structural transitions in the system  
- coherence loss in the field  
- early geometric deformation of trajectories  

This allows detection of instability **before** the voltage collapse phase.

---

## ⚡ Why this matters

- earlier intervention in power grids  
- prevention of cascading failures  
- improved stability under renewable fluctuations  
- shift from reactive → proactive system control  

---

## 🔁 Reproducibility

All results are based on standard IEEE benchmark systems:

- IEEE 118  
- IEEE 300  
- IEEE 1354  
- IEEE 9241 (PEGASE)  

Full implementation and results:

👉 [Power Systems Application](./APPLICATIONS/power_systems/README.md)

---

## 🧭 What this shows

NEXAH is not just a simulation tool.

It provides:

> a structural view of system dynamics that enables early detection and future navigation of stability.

---

## 🚀 Next step

The next phase is to move from:

```text
early detection → controlled navigation
```

This includes:

- collapse avoidance strategies  
- channel-based control  
- regime-aware switching  
- real-time system integration  

---

## Final Statement

This is the first demonstration that:

> instability in complex power systems can be detected early through structure — not just measured after the fact.

---

**NEXAH**  
Structure becomes visible.  
Geometry becomes actionable.  
Stability becomes navigable.
