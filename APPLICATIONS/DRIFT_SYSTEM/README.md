# Drift Systems

This module introduces **Drift Systems**, a class of dynamical systems in which the evolution of the system state is influenced not only by the stability landscape, but also by **external forces**.

While gradient systems evolve purely along the gradient of a stability function, drift systems include additional influences that can push the system away from the natural gradient flow.

---

# Core Idea

In drift systems, the evolution of a system state is governed by two components:

1. the **stability gradient** of the landscape
2. an **external forcing term**

Together, these influences determine the direction of system evolution.

The general form of a drift system can be written as:

dx/dt = -∇V(x) + F(x,t)

where

- **V(x)** is the stability potential
- **∇V(x)** is the gradient of the stability landscape
- **F(x,t)** represents external forces acting on the system

---

# Conceptual Interpretation

In a drift system:

- the **landscape** defines the natural direction of stability
- the **gradient** pulls the system toward attractors
- the **external force** pushes the system through the state space

The resulting motion is therefore a combination of **gradient descent and directional drift**.

---

# Typical Behavior

Drift systems often show behaviors that differ from pure gradient systems.

Examples include:

- systems moving across attractor basins
- persistent directional motion
- delayed stabilization
- forced transitions between regimes

External forces may prevent the system from settling into equilibrium.

---

# Examples of Drift Systems

Many real-world systems behave as drift systems.

Examples include:

- ocean currents influenced by temperature gradients and wind
- atmospheric transport processes
- migration flows in ecological systems
- particle transport in fluid environments

In these systems, the underlying stability landscape still exists, but external forces continuously influence the system trajectory.

---

# Relation to Gradient Systems

Drift systems extend the **Gradient System Model**.

If the external forcing term disappears

F(x,t) = 0

the system reduces to a pure gradient system:

dx/dt = -∇V(x)

Drift systems therefore represent a **generalization of gradient dynamics**.

---

# Next Step

The next module introduces **Regime Systems**, which describe systems that operate within multiple structural regimes and may transition between them.

These systems capture behaviors such as tipping points, phase transitions, and regime shifts.
