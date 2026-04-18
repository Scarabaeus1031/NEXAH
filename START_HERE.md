# 🚀 START HERE — NEXAH

**Welcome.**

NEXAH turns complex system behavior into a **navigable stability landscape**.

Instead of asking:

> “Will the system become unstable?”

NEXAH answers:

> **Where are we in the field — and how can we move safely?**

---

## ⚡ Step 1 — Run the Core Demo (Lorenz System)

This is the fastest way to understand NEXAH.

Run:

```bash
python APPLICATIONS/core_demos/lorenz/lorenz_meta_control_v6_switch.py
```

You will see:

- chaotic dynamics (Lorenz attractor)  
- structured trajectories  
- adaptive control behavior  
- regime transitions ("switches")  

---

## 🧠 What is happening?

The system:

- extracts structure from chaos  
- builds symbolic states  
- detects patterns and transitions  
- applies adaptive control strategies  
- reacts to regime changes  

👉 This creates a **local navigation system inside a chaotic environment**

---

## 🔍 What to look for

- trajectories stabilizing without fixed targets  
- switching between control modes  
- repeated patterns in chaotic motion  
- structured regions in phase space  

---

## 🌊 Key Idea

Instead of:

> controlling toward a fixed goal  

NEXAH:

> moves **within the structure of the system itself**

---

## ⚡ Step 2 — Real System (Power Grid)

Once you understand the Lorenz system, try:

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

This shows:

- a real dynamical system (power grid)  
- structure-based interpretation of stability  
- trajectory-based control behavior  

---

## ⚠️ Important

- NEXAH is currently a **prototype system**  
- behavior is **locally reliable, not globally predictive**  
- real-world validation is **ongoing**  

---

## 🧠 In one sentence

NEXAH turns complex dynamics into a **structure you can move within**

---

## 🧭 Explore Next

- 🧠 Framework → FRAMEWORK/README.md  
- ⚡ Applications → APPLICATIONS/README.md  
- 🧭 Navigation → NAVIGATOR/CORE/NAVIGATION_ARCHITECTURE.md  

---

## 🚀 What NEXAH enables

- understand structure in chaotic systems  
- detect regime transitions  
- apply adaptive control strategies  
- explore navigation within system dynamics  

---

## 🧩 Want to build on this?

NEXAH is not a finished system — it is a working prototype.

You can actively experiment with it.

---

## 🔧 Try this (2 minutes)

Open:

APPLICATIONS/core_demos/lorenz/lorenz_meta_control_v6_switch.py

---

### Step 1 — change control strength

Find this line in the code:

control = -0.30 * dx

Try changing it to:

control = -0.10 * dx

or:

control = -0.80 * dx

👉 Then run the script again.

---

### Step 2 — observe

Watch how the system changes:

- does it stabilize faster?  
- does it become unstable?  
- does it switch modes more often?  

---

### Step 3 — modify behavior

Try changing:

- mode selection logic  
- thresholds (risk / entropy / confidence)  
- memory strength  
- switching sensitivity  

---

## 🧠 What you are doing

You are not tuning parameters.

You are:

> **changing how a system navigates itself**

---

## 🚀 Where to go next

You can extend:

### 🔧 Control
- design new control laws  
- test alternative stabilization strategies  

### 🧠 Prediction
- improve pattern detection  
- test different prediction models  

### 🌐 Systems
- apply NEXAH to your own system  
- connect simulations or real data  

---

## 💡 Philosophy

NEXAH is not meant to be used as a black box.

It is meant to be:

> explored, modified, and extended

---

👉 If you change something and observe new behavior,  
you are already contributing to the system.

---

**NEXAH · Thomas K. R. Hofmann · 2026**

