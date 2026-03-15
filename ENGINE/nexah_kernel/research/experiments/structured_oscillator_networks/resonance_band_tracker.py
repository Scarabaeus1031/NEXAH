# Default Drei-Layer-Split passend zu deinem Longrun:
N_INNER = 16
N_MIDDLE = 32
N_OUTER = total_nodes - N_INNER - N_MIDDLE

if N_OUTER <= 0:
    raise RuntimeError("Layer split invalid. Check node counts.")

inner_nodes = history[:, :N_INNER]
middle_nodes = history[:, N_INNER:N_INNER + N_MIDDLE]
outer_nodes = history[:, N_INNER + N_MIDDLE:]


# ---------------------------------------------------------
# LAYER MEAN PHASE
# ---------------------------------------------------------

def circular_mean(phases):
    return np.angle(np.mean(np.exp(1j * phases), axis=1))


inner_phase = circular_mean(inner_nodes)
middle_phase = circular_mean(middle_nodes)
outer_phase = circular_mean(outer_nodes)


# ---------------------------------------------------------
# PHASE OFFSETS
# ---------------------------------------------------------

offset_im = wrap_angle(inner_phase - middle_phase)
offset_mo = wrap_angle(middle_phase - outer_phase)


# Glätten
offset_im = moving_average(offset_im, SMOOTH_WINDOW)
offset_mo = moving_average(offset_mo, SMOOTH_WINDOW)


time = np.arange(steps)


# ---------------------------------------------------------
# RESONANCE BAND DETECTION
# ---------------------------------------------------------

band_results = {}

for band in TARGET_BANDS:

    mask_im = np.abs(offset_im - band) < BAND_HALF_WIDTH
    mask_mo = np.abs(offset_mo - band) < BAND_HALF_WIDTH

    lengths_im = contiguous_lengths(mask_im)
    lengths_mo = contiguous_lengths(mask_mo)

    entries_im, exits_im = detect_entries_exits(mask_im)
    entries_mo, exits_mo = detect_entries_exits(mask_mo)

    band_results[band] = {
        "mask_im": mask_im,
        "mask_mo": mask_mo,
        "lengths_im": lengths_im,
        "lengths_mo": lengths_mo,
        "entries_im": entries_im,
        "exits_im": exits_im,
        "entries_mo": entries_mo,
        "exits_mo": exits_mo,
    }


# ---------------------------------------------------------
# PLOT PHASE OFFSETS
# ---------------------------------------------------------

plt.figure(figsize=(10,5))
plt.plot(time, offset_im, label="inner-middle")
plt.plot(time, offset_mo, label="middle-outer")

for band in TARGET_BANDS:
    plt.axhline(band, linestyle="--", alpha=0.4)

plt.title("Phase Offsets with Resonance Bands")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "resonance_offsets.png")
plt.close()


# ---------------------------------------------------------
# BAND WINDOWS PLOT
# ---------------------------------------------------------

plt.figure(figsize=(10,5))

for band in TARGET_BANDS:

    mask = band_results[band]["mask_im"].astype(int)

    plt.plot(time, mask + band, label=f"band {band} (inner-middle)")

plt.title("Resonance Band Occupancy")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "resonance_band_windows.png")
plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

report_path = OUTPUT_DIR / "resonance_band_report.txt"

with open(report_path, "w") as f:

    f.write("Resonance Band Report\n")
    f.write("=====================\n\n")
    f.write(f"Total timesteps: {steps}\n\n")

    for band in TARGET_BANDS:

        res = band_results[band]

        f.write(f"BAND {band}\n")
        f.write("-----------------\n")

        f.write("Inner-Middle\n")
        f.write(f"entries: {len(res['entries_im'])}\n")

        if res["lengths_im"]:
            f.write(f"mean duration: {np.mean(res['lengths_im']):.2f}\n")
            f.write(f"max duration: {np.max(res['lengths_im'])}\n")

        f.write("\nMiddle-Outer\n")
        f.write(f"entries: {len(res['entries_mo'])}\n")

        if res["lengths_mo"]:
            f.write(f"mean duration: {np.mean(res['lengths_mo']):.2f}\n")
            f.write(f"max duration: {np.max(res['lengths_mo'])}\n")

        f.write("\n\n")

print("Resonance band tracking complete.")
