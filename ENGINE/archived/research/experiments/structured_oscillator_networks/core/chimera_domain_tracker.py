import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

N_INNER = 16
N_MIDDLE = 32

RADIUS = 2
INCOHERENT_THRESHOLD = 0.45

SMOOTH_WINDOW = 60


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def local_order_on_ring(theta_ring, radius=2):

    n = len(theta_ring)
    local_R = np.zeros(n)

    for i in range(n):

        idx = [(i + k) % n for k in range(-radius, radius+1)]

        neighborhood = theta_ring[idx]

        local_R[i] = np.abs(np.mean(np.exp(1j * neighborhood)))

    return local_R


def moving_average(x, w):

    if w <= 1:
        return x

    kernel = np.ones(w)/w
    return np.convolve(x, kernel, mode="same")


def detect_domains(local_R, threshold):

    """
    Returns domain centers of incoherent regions
    """

    incoherent = local_R < threshold

    domains = []

    n = len(incoherent)

    i = 0

    while i < n:

        if incoherent[i]:

            start = i

            while i < n and incoherent[i]:
                i += 1

            end = i

            center = (start + end)/2

            domains.append(center)

        else:
            i += 1

    return domains


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

N_OUTER = nodes - N_INNER - N_MIDDLE

inner = history[:, :N_INNER]
middle = history[:, N_INNER:N_INNER+N_MIDDLE]
outer = history[:, N_INNER+N_MIDDLE:]


# ---------------------------------------------------------
# DOMAIN TRACKING
# ---------------------------------------------------------

inner_domains = []
middle_domains = []
outer_domains = []

for t in range(steps):

    Ri = local_order_on_ring(inner[t], RADIUS)
    Rm = local_order_on_ring(middle[t], RADIUS)
    Ro = local_order_on_ring(outer[t], RADIUS)

    inner_domains.append(detect_domains(Ri, INCOHERENT_THRESHOLD))
    middle_domains.append(detect_domains(Rm, INCOHERENT_THRESHOLD))
    outer_domains.append(detect_domains(Ro, INCOHERENT_THRESHOLD))


# ---------------------------------------------------------
# DOMAIN POSITION ARRAYS
# ---------------------------------------------------------

def domains_to_points(domain_list):

    t_points = []
    x_points = []

    for t, doms in enumerate(domain_list):

        for d in doms:

            t_points.append(t)
            x_points.append(d)

    return np.array(t_points), np.array(x_points)


ti, xi = domains_to_points(inner_domains)
tm, xm = domains_to_points(middle_domains)
to, xo = domains_to_points(outer_domains)


# ---------------------------------------------------------
# PLOT DOMAIN TRACKS
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

plt.scatter(ti, xi, s=5, label="inner")
plt.scatter(tm, xm + N_INNER, s=5, label="middle")
plt.scatter(to, xo + N_INNER + N_MIDDLE, s=5, label="outer")

plt.xlabel("time")
plt.ylabel("node index")

plt.title("Chimera Domain Tracks")

plt.legend()

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "chimera_domain_tracks.png")

plt.close()


# ---------------------------------------------------------
# DOMAIN COUNT OVER TIME
# ---------------------------------------------------------

count_inner = [len(d) for d in inner_domains]
count_middle = [len(d) for d in middle_domains]
count_outer = [len(d) for d in outer_domains]

count_inner = moving_average(np.array(count_inner), SMOOTH_WINDOW)
count_middle = moving_average(np.array(count_middle), SMOOTH_WINDOW)
count_outer = moving_average(np.array(count_outer), SMOOTH_WINDOW)

plt.figure(figsize=(10,4))

plt.plot(count_inner, label="inner")
plt.plot(count_middle, label="middle")
plt.plot(count_outer, label="outer")

plt.xlabel("time")
plt.ylabel("domain count")

plt.title("Chimera Domain Count")

plt.legend()

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "chimera_domain_count.png")

plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

mean_inner = np.mean([len(d) for d in inner_domains])
mean_middle = np.mean([len(d) for d in middle_domains])
mean_outer = np.mean([len(d) for d in outer_domains])

with open(OUTPUT_DIR / "chimera_domain_report.txt","w") as f:

    f.write("Chimera Domain Tracker Report\n")
    f.write("=============================\n\n")

    f.write(f"nodes: {nodes}\n")
    f.write(f"timesteps: {steps}\n\n")

    f.write("Average incoherent domains per layer\n\n")

    f.write(f"inner: {mean_inner:.3f}\n")
    f.write(f"middle: {mean_middle:.3f}\n")
    f.write(f"outer: {mean_outer:.3f}\n")


print("Domain tracking complete.")
print("Output written to /output")
