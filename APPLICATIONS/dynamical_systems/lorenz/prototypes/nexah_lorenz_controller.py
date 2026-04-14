import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# Lorenz system
def lorenz(state, t, sigma=10, rho=28, beta=8/3):

    x,y,z = state

    return [
        sigma*(y-x),
        x*(rho-z)-y,
        x*y-beta*z
    ]


# instability measure
def instability(traj):

    x = traj[:,0]

    # high switching = unstable
    switches = np.sum(np.diff(np.sign(x)) != 0)

    return switches


# simple controller
def controller(state):

    x,y,z = state

    # small intervention
    dx = np.random.uniform(-0.2,0.2)
    dy = np.random.uniform(-0.2,0.2)
    dz = np.random.uniform(-0.2,0.2)

    return [x+dx,y+dy,z+dz]


# simulation parameters
t = np.linspace(0,30,3000)

state = [-3,0,25]

trajectory = []
control_points = []


for step in range(40):

    traj = odeint(lorenz,state,t)

    score = instability(traj)

    trajectory.append(traj)

    if score > 30:

        # system unstable → intervene
        state = controller(traj[-1])

        control_points.append(state)

    else:

        state = traj[-1]


# combine trajectory
full = np.vstack(trajectory)


# plot
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111,projection='3d')

ax.plot(full[:,0],full[:,1],full[:,2],lw=0.6)

if len(control_points) > 0:

    cp = np.array(control_points)

    ax.scatter(
        cp[:,0],
        cp[:,1],
        cp[:,2],
        c="red",
        s=40,
        label="controller actions"
    )

ax.set_title("NEXAH Lorenz Controller Test")

plt.legend()
plt.show()
