# 🚀 START HERE — NEXAH

![NEXAH Field](./visuals/output/v7_separatrix.png)

**This is not chaos.**  
This is a **stability field**.

---

## 🧠 What you are looking at

A system is moving through:

- stable regions  
- transition zones  
- instability boundaries  

Instead of asking:

> “Will the system become unstable?”

NEXAH shows:

> **Where the system is — and where it is going**

---

## ⚡ Step 1 — Run the Core Demo

```bash
python ENGINE/run_nexah_demo.py
```

This generates:

- a trajectory (system behavior)  
- a field (how the system moves)  
- regimes (stable / transition / unstable)  
- boundaries between them  

---

## 🔍 What to look for

- where motion slows down → stability  
- where it accelerates → instability  
- where it crosses boundaries → regime change  
- how trajectories follow the field  

---

## 🌊 Key Idea

Systems do not randomly become unstable.

They:

> **move through regions of stability**

---

## ⚡ Step 2 — See it in Action (Lorenz System)

```bash
python APPLICATIONS/core_demos/lorenz/lorenz_meta_control_v6_switch.py
```

Now you will see:

- chaotic dynamics (Lorenz attractor)  
- structured trajectories  
- adaptive behavior  
- regime transitions ("switches")  

---

## 🧠 What changed?

Before:

> the system moved blindly

Now:

> the system **reacts to the structure**

---

## ⚡ Step 3 — Real System (Power Grid)

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

---

## ⚠️ Important

- NEXAH is a **prototype system**  
- behavior is **locally reliable, not globally predictive**  
- real-world validation is **ongoing**  

---

## 🧠 In one sentence

NEXAH turns complex dynamics into a:

> **structure you can move within**

---

## 🧭 Explore Next

- 🧠 Framework → FRAMEWORK/README.md  
- ⚡ Applications → APPLICATIONS/README.md  
- 🧭 Navigation → NAVIGATOR/CORE/NAVIGATION_ARCHITECTURE.md  

---

## 🧩 Want to experiment?

Open:

```
APPLICATIONS/core_demos/lorenz/lorenz_meta_control_v6_switch.py
```

---

### 🔧 Try this (2 minutes)

Change:

```python
control = -0.30 * dx
```

to:

```python
control = -0.10 * dx
```

or:

```python
control = -0.80 * dx
```

---

### 👀 Observe

- does it stabilize faster?  
- does it become unstable?  
- does it switch more often?  

---

## 🧠 What you are doing

You are not tuning parameters.

You are:

> **changing how a system navigates itself**

---

## 💡 Philosophy

NEXAH is not a black box.

It is meant to be:

> explored, modified, and extended

---

👉 If you change something and observe new behavior,  
you are already contributing to the system.

---

**NEXAH · Thomas K. R. Hofmann · 2026**
