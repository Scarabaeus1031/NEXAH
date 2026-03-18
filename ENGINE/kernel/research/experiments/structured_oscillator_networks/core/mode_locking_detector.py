import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")

LOCK_THRESHOLD = 0.05      # Varianzgrenze für Phase Lock
WINDOW = 50                # Sliding window Größe


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

phases = np.load(PHASE_FILE)

# shape expected: (time, layers)
# layers: [inner, middle, outer]

inner = phases[:,0]
middle = phases[:,1]
outer = phases[:,2]

time = np.arange(len(inner))


# ---------------------------------------------------------
# PHASE OFFSETS
# ---------------------------------------------------------

offset_im = np.unwrap(inner - middle)
offset_mo = np.unwrap(middle - outer)


# ---------------------------------------------------------
# VARIANCE SCAN
# ---------------------------------------------------------

def sliding_variance(signal, window):

    var = np.zeros(len(signal))

    for i in range(len(signal)):

        start = max(0, i-window)
        end = min(len(signal), i+window)

        var[i] = np.var(signal[start:end])

    return var


var_im = sliding_variance(offset_im, WINDOW)
var_mo = sliding_variance(offset_mo, WINDOW)


# ---------------------------------------------------------
# LOCKING WINDOWS
# ---------------------------------------------------------

lock_im = var_im < LOCK_THRESHOLD
lock_mo = var_mo < LOCK_THRESHOLD


# ---------------------------------------------------------
# LOCK DURATIONS
# ---------------------------------------------------------

def compute_lock_lengths(lock_array):

    lengths = []
    current = 0

    for val in lock_array:

        if val:
            current += 1
        else:
            if current > 0:
                lengths.append(current)
            current = 0

    if current > 0:
        lengths.append(current)

    return lengths


lengths_im = compute_lock_lengths(lock_im)
lengths_mo = compute_lock_lengths(lock_mo)


# ---------------------------------------------------------
# PLOT OFFSETS
# ---------------------------------------------------------

plt.figure(figsize=(10,4))
plt.plot(time, offset_im, label="inner-middle")
plt.plot(time, offset_mo, label="middle-outer")
plt.title("Phase Offsets")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"mode_locking_offsets.png")
plt.close()


# ---------------------------------------------------------
# PLOT LOCK WINDOWS
# ---------------------------------------------------------

plt.figure(figsize=(10,4))
plt.plot(time, lock_im.astype(int), label="inner-middle lock")
plt.plot(time, lock_mo.astype(int), label="middle-outer lock")
plt.title("Mode Locking Windows")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"mode_locking_windows.png")
plt.close()


# ---------------------------------------------------------
# HISTOGRAM
# ---------------------------------------------------------

plt.figure(figsize=(6,4))
plt.hist(lengths_im, bins=30, alpha=0.6, label="inner-middle")
plt.hist(lengths_mo, bins=30, alpha=0.6, label="middle-outer")
plt.title("Lock Duration Histogram")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR/"mode_locking_lifetime_hist.png")
plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

with open(OUTPUT_DIR/"mode_locking_report.txt","w") as f:

    f.write("Mode Locking Report\n")
    f.write("====================\n\n")

    f.write(f"Total timesteps: {len(inner)}\n\n")

    f.write("Inner-Middle Locks:\n")
    f.write(f"count: {len(lengths_im)}\n")
    if lengths_im:
        f.write(f"mean duration: {np.mean(lengths_im):.2f}\n")
        f.write(f"max duration: {np.max(lengths_im)}\n")

    f.write("\n")

    f.write("Middle-Outer Locks:\n")
    f.write(f"count: {len(lengths_mo)}\n")
    if lengths_mo:
        f.write(f"mean duration: {np.mean(lengths_mo):.2f}\n")
        f.write(f"max duration: {np.max(lengths_mo)}\n")

print("Mode locking analysis complete.")
