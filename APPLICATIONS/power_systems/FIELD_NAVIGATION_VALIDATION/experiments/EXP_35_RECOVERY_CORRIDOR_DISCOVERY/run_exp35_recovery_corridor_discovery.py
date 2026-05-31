# ============================================================
# Summary
# ============================================================

summary = f"""
EXP_35 RECOVERY CORRIDOR DISCOVERY
========================================

States: {len(df)}
Recovery Paths: {len(paths)}

Mean Corridor Length:
{np.mean(path_lengths):.2f}

Max Corridor Length:
{np.max(path_lengths)}

Min Corridor Length:
{np.min(path_lengths)}
"""

with open(
    OUTPUT_DIR
    / "exp35_summary.txt",
    "w"
) as f:

    f.write(summary)

print(summary)

print(
    "\nEXP_35 completed."
)
