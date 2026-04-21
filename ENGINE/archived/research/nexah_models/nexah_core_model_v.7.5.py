import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# NEXAH v7.5 — Torus Engine
# A/B Flows + Z Transport + Power Field
# ============================================================

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
R = 2.2          # major radius
r = 0.75         # minor radius
omega_A = 1.0
omega_B = -1.0   # opposite direction
phi_shift = np.pi / 2.0

steps = 1400
dt = 0.02

# coupling / transport
coupling_strength = 0.18
z_gain = 0.22
power_gain = 1.0

# torus mesh
nu = 120
nv = 60

u = np.linspace(0, 2*np.pi, nu)
v = np.linspace(0, 2*np.pi, nv)
U, V = np.meshgrid(u, v)

# ------------------------------------------------------------
# TORUS GEOMETRY
# ------------------------------------------------------------
def torus_xyz(theta, phi, R=R, r=r):
    x = (R + r * np.cos(theta)) * np.cos(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    return x, y, z

def torus_surface(U, V, R=R, r=r):
    X = (R + r * np.cos(V)) * np.cos(U)
    Y = (R + r * np.cos(V)) * np.sin(U)
    Z = r * np.sin(V)
    return X, Y, Z

# ------------------------------------------------------------
# FLOW SYSTEM
# ------------------------------------------------------------
def flow_A(t):
    """
    Flow A: major forward, minor oscillatory
    """
    phi = omega_A * t
    theta = 1.7 * t + 0.35 * np.sin(3.0 * t)
    return theta, phi

def flow_B(t):
    """
    Flow B: counter-rotating / phase-shifted
    """
    phi = omega_B * t + phi_shift
    theta = -1.35 * t + 0.28 * np.cos(2.4 * t + 0.4)
    return theta, phi

def local_velocity(theta_prev, phi_prev, theta_now, phi_now, dt):
    dtheta = (theta_now - theta_prev) / dt
    dphi = (phi_now - phi_prev) / dt
    # geometric proxy: combine major/minor angular motion
    speed = np.sqrt((r * dtheta)**2 + ((R + r*np.cos(theta_now)) * dphi)**2)
    return speed, dtheta, dphi

# ------------------------------------------------------------
# POWER / TRANSPORT
# ------------------------------------------------------------
def compute_power(vA, vB, coupling):
    """
    Combined power:
    P = A + B + coupling term
    """
    return power_gain * (vA + vB + coupling * vA * vB)

def compute_z_transport(zA, zB, power):
    """
    Elevator / axial transport:
    stronger when A/B differ in z but power remains high
    """
    return z_gain * power * (zA - zB)

# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
times = np.arange(steps) * dt

trajA = []
trajB = []

power_hist = []
z_transport_hist = []
vA_hist = []
vB_hist = []
coupling_hist = []

thetaA_prev, phiA_prev = flow_A(0.0)
thetaB_prev, phiB_prev = flow_B(0.0)

for i, t in enumerate(times):
    thetaA, phiA = flow_A(t)
    thetaB, phiB = flow_B(t)

    xA, yA, zA = torus_xyz(thetaA, phiA)
    xB, yB, zB = torus_xyz(thetaB, phiB)

    trajA.append((xA, yA, zA))
    trajB.append((xB, yB, zB))

    if i == 0:
        vA, dthetaA, dphiA = 0.0, 0.0, 0.0
        vB, dthetaB, dphiB = 0.0, 0.0, 0.0
    else:
        vA, dthetaA, dphiA = local_velocity(thetaA_prev, phiA_prev, thetaA, phiA, dt)
        vB, dthetaB, dphiB = local_velocity(thetaB_prev, phiB_prev, thetaB, phiB, dt)

    # coupling proxy: closeness on torus
    dist = np.sqrt((xA - xB)**2 + (yA - yB)**2 + (zA - zB)**2)
    coupling = coupling_strength / (dist + 1e-3)

    P = compute_power(vA, vB, coupling)
    ZT = compute_z_transport(zA, zB, P)

    vA_hist.append(vA)
    vB_hist.append(vB)
    coupling_hist.append(coupling)
    power_hist.append(P)
    z_transport_hist.append(ZT)

    thetaA_prev, phiA_prev = thetaA, phiA
    thetaB_prev, phiB_prev = thetaB, phiB

trajA = np.array(trajA)
trajB = np.array(trajB)
power_hist = np.array(power_hist)
z_transport_hist = np.array(z_transport_hist)
vA_hist = np.array(vA_hist)
vB_hist = np.array(vB_hist)
coupling_hist = np.array(coupling_hist)

# combined axis path (staff / elevator)
axis_z = np.cumsum(z_transport_hist) * dt
axis_x = np.zeros_like(axis_z)
axis_y = np.zeros_like(axis_z)

# ------------------------------------------------------------
# 12 + 1 RING POINTS
# ------------------------------------------------------------
ring_angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
ring_points = []
for ang in ring_angles:
    xr = (R + 0.0) * np.cos(ang)
    yr = (R + 0.0) * np.sin(ang)
    zr = 0.0
    ring_points.append((xr, yr, zr))
ring_points = np.array(ring_points)
core_point = np.array([0.0, 0.0, 0.0])

# ------------------------------------------------------------
# POWER FIELD ON TORUS
# ------------------------------------------------------------
def torus_power_field(U, V):
    """
    Static field over torus:
    uses two tube-like channels A and B
    """
    # channel A centered at phase 0
    A = np.exp(-((np.angle(np.exp(1j*U)))**2) / 1.2) * (1.0 + 0.7*np.cos(V))
    # channel B shifted
    U2 = np.angle(np.exp(1j*(U - np.pi)))
    B = np.exp(-(U2**2) / 1.2) * (1.0 - 0.7*np.cos(V))
    P = A + B
    return P, A, B

Pfield, Afield, Bfield = torus_power_field(U, V)
Xt, Yt, Zt = torus_surface(U, V)

# ------------------------------------------------------------
# PLOT 1 — TORUS + A/B FLOWS + STAFF
# ------------------------------------------------------------
fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(Xt, Yt, Zt, rstride=2, cstride=2, alpha=0.14, linewidth=0, color='lightgray')
ax.plot(trajA[:,0], trajA[:,1], trajA[:,2], color='blue', lw=2.0, label='flow A')
ax.plot(trajB[:,0], trajB[:,1], trajB[:,2], color='red', lw=2.0, label='flow B')

# central elevator / staff
zline = np.linspace(axis_z.min(), axis_z.max(), 200)
ax.plot(np.zeros_like(zline), np.zeros_like(zline), zline, color='goldenrod', lw=3, label='staff / elevator')

# 12 + 1
ax.scatter(ring_points[:,0], ring_points[:,1], ring_points[:,2], color='purple', s=35, label='12 ring points')
ax.scatter(core_point[0], core_point[1], core_point[2], color='black', s=80, label='core')

ax.set_title("NEXAH v7.5 — Torus Engine (A/B flows + staff)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 2 — POWER / TRANSPORT TIMELINES
# ------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(13, 8))

axs[0,0].plot(times, vA_hist, color='blue')
axs[0,0].plot(times, vB_hist, color='red')
axs[0,0].set_title("Local flow speeds")
axs[0,0].set_xlabel("time")
axs[0,0].set_ylabel("speed")
axs[0,0].grid(True, alpha=0.25)

axs[0,1].plot(times, coupling_hist, color='purple')
axs[0,1].set_title("Coupling strength")
axs[0,1].set_xlabel("time")
axs[0,1].set_ylabel("coupling")
axs[0,1].grid(True, alpha=0.25)

axs[1,0].plot(times, power_hist, color='darkorange')
axs[1,0].set_title("Power P = A + B + coupling")
axs[1,0].set_xlabel("time")
axs[1,0].set_ylabel("power")
axs[1,0].grid(True, alpha=0.25)

axs[1,1].plot(times, z_transport_hist, color='green')
axs[1,1].set_title("Z transport / elevator")
axs[1,1].set_xlabel("time")
axs[1,1].set_ylabel("transport")
axs[1,1].grid(True, alpha=0.25)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 3 — POWER FIELD ON TORUS (FLATTENED)
# ------------------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(15, 4))

im0 = axs[0].imshow(Afield, origin='lower', aspect='auto', cmap='Blues')
axs[0].set_title("Tube A")
axs[0].set_xlabel("major angle")
axs[0].set_ylabel("minor angle")
plt.colorbar(im0, ax=axs[0])

im1 = axs[1].imshow(Bfield, origin='lower', aspect='auto', cmap='Reds')
axs[1].set_title("Tube B")
axs[1].set_xlabel("major angle")
axs[1].set_ylabel("minor angle")
plt.colorbar(im1, ax=axs[1])

im2 = axs[2].imshow(Pfield, origin='lower', aspect='auto', cmap='magma')
axs[2].set_title("P = A + B")
axs[2].set_xlabel("major angle")
axs[2].set_ylabel("minor angle")
plt.colorbar(im2, ax=axs[2])

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 4 — R/T and POWER RELATION
# ------------------------------------------------------------
T_major_A = 2*np.pi / abs(omega_A)
T_major_B = 2*np.pi / abs(omega_B)

RT_A = R / T_major_A
RT_B = R / T_major_B

fig, axs = plt.subplots(1, 2, figsize=(12, 4))

axs[0].bar(["R/T (A)", "R/T (B)"], [RT_A, RT_B], color=["blue", "red"])
axs[0].set_title("R/T proxy")
axs[0].set_ylabel("R / T")

axs[1].plot(times, power_hist, color='darkorange', label='P(t)')
axs[1].axhline(np.mean(power_hist), color='black', linestyle='--', label='mean P')
axs[1].set_title("Power timeline")
axs[1].set_xlabel("time")
axs[1].set_ylabel("P")
axs[1].legend()
axs[1].grid(True, alpha=0.25)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 5 — TOP VIEW (TWO TUBES INSIDE TORUS)
# ------------------------------------------------------------
plt.figure(figsize=(8, 8))
plt.plot(trajA[:,0], trajA[:,1], color='blue', lw=1.8, label='tube A')
plt.plot(trajB[:,0], trajB[:,1], color='red', lw=1.8, label='tube B')
plt.scatter(ring_points[:,0], ring_points[:,1], color='purple', s=30, alpha=0.8, label='12 ring')
plt.scatter(0, 0, color='black', s=70, label='core')
circle = plt.Circle((0, 0), R, color='gray', fill=False, linestyle='--', alpha=0.5)
plt.gca().add_artist(circle)
plt.axis('equal')
plt.grid(True, alpha=0.25)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Top View — Two Tubes + 12+1 Structure")
plt.legend()
plt.show()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("\n=== NEXAH v7.5 Summary ===")
print("R =", R, "r =", r)
print("T_major_A =", T_major_A, "T_major_B =", T_major_B)
print("R/T A =", RT_A, "R/T B =", RT_B)
print("Power min/max/mean =", float(np.min(power_hist)), float(np.max(power_hist)), float(np.mean(power_hist)))
print("Z transport min/max/mean =", float(np.min(z_transport_hist)), float(np.max(z_transport_hist)), float(np.mean(z_transport_hist)))
print("Mean coupling =", float(np.mean(coupling_hist)))
print("12+1 structure =", len(ring_points), "+ 1 core")
