import numpy as np
import matplotlib.pyplot as plt

from FRAMEWORK.NEXAH.core.field_controller import FieldController


controller = FieldController()
result = controller.simulate(x0=np.array([-2.0, -1.5]), steps=120)

states = result.states
coherences = result.coherences

plt.figure()
plt.plot(states[:, 0], states[:, 1], label="trajectory")
plt.scatter(states[0, 0], states[0, 1], label="start")
plt.title("NEXAH Field Controller Demo")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

plt.figure()
plt.plot(coherences)
plt.title("Coherence over Time")
plt.xlabel("step")
plt.ylabel("C(x)")
plt.show()
