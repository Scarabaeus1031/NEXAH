import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

# --------------------------------
# Output
# --------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# --------------------------------
# Lorenz parameters
# --------------------------------

sigma = 10
rho = 28
beta = 8/3

dt = 0.01
T = 4.0
steps = int(T/dt)

# --------------------------------
# Lorenz system
# --------------------------------

def lorenz(state):
    x,y,z = state
    
    dx = sigma*(y-x)
    dy = x*(rho-z)-y
    dz = x*y-beta*z
    
    return np.array([dx,dy,dz])

# --------------------------------
# Integrator
# --------------------------------

def integrate(state):
    
    s = state.copy()
    
    for i in range(steps):
        s = s + dt*lorenz(s)
        
    return s

# --------------------------------
# FTLE grid
# --------------------------------

x_vals = np.linspace(-20,20,120)
z_vals = np.linspace(0,50,120)

epsilon = 1e-5

ftle = np.zeros((len(z_vals),len(x_vals)))

# --------------------------------
# FTLE calculation
# --------------------------------

for i,x in enumerate(x_vals):
    
    for j,z in enumerate(z_vals):
        
        y = 0
        
        p0 = np.array([x,y,z])
        p1 = p0 + np.array([epsilon,0,0])
        
        a = integrate(p0)
        b = integrate(p1)
        
        d0 = epsilon
        dT = np.linalg.norm(a-b)
        
        ftle[j,i] = (1/T)*np.log(dT/d0)

# --------------------------------
# Plot
# --------------------------------

plt.figure(figsize=(10,6))

plt.imshow(
    ftle,
    origin="lower",
    extent=[x_vals.min(),x_vals.max(),z_vals.min(),z_vals.max()],
    cmap="inferno",
    aspect="auto"
)

plt.colorbar(label="FTLE")

plt.xlabel("X")
plt.ylabel("Z")

plt.title("Lorenz FTLE Field (Lagrangian Coherent Structures)")

file_output = f"{OUTPUT_DIR}/lorenz_ftle_lcs_{timestamp}.png"

plt.savefig(file_output,dpi=300,bbox_inches="tight")

print("saved:",file_output)

plt.show()
