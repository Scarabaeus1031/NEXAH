# threshold_pairs_2n_3n_analysis.py

import math
from sympy import isprime, factorint
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
MAX_N_2 = 12
MAX_N_3 = 9
MODS = [7, 17]

# -------------------------
# HELPERS
# -------------------------
def divisor_count(n: int) -> int:
    if n <= 0:
        return 0
    factors = factorint(n)
    count = 1
    for exp in factors.values():
        count *= (exp + 1)
    return count

def residue_signature(n: int, mods):
    return {m: n % m for m in mods}

def analyze_threshold(base: int, n: int, mods):
    m = base**n
    mp1 = m + 1

    return {
        "base": base,
        "n": n,
        "m": m,
        "m_plus_1": mp1,
        "m_is_prime": isprime(m),
        "m_plus_1_is_prime": isprime(mp1),
        "m_divisors": divisor_count(m),
        "m_plus_1_divisors": divisor_count(mp1),
        "m_residues": residue_signature(m, mods),
        "mp1_residues": residue_signature(mp1, mods),
    }

def print_block(rows, title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    for r in rows:
        print(
            f"base={r['base']}  n={r['n']:>2}  "
            f"m={r['m']:<8}  m+1={r['m_plus_1']:<8}  "
            f"prime(m)={r['m_is_prime']}  prime(m+1)={r['m_plus_1_is_prime']}  "
            f"div(m)={r['m_divisors']:<3}  div(m+1)={r['m_plus_1_divisors']:<3}  "
            f"mod7: {r['m_residues'][7]}→{r['mp1_residues'][7]}  "
            f"mod17: {r['m_residues'][17]}→{r['mp1_residues'][17]}"
        )

# -------------------------
# MAIN ANALYSIS
# -------------------------
rows_2n = [analyze_threshold(2, n, MODS) for n in range(1, MAX_N_2 + 1)]
rows_3n = [analyze_threshold(3, n, MODS) for n in range(1, MAX_N_3 + 1)]

print_block(rows_2n, "2^n -> 2^n + 1 THRESHOLD PAIRS")
print_block(rows_3n, "3^n -> 3^n + 1 THRESHOLD PAIRS")

# -------------------------
# SUMMARY COUNTS
# -------------------------
def summarize(rows, label):
    prime_hits = sum(1 for r in rows if r["m_plus_1_is_prime"])
    print(f"\n[{label}]")
    print(f"Total rows: {len(rows)}")
    print(f"(m+1) prime count: {prime_hits}")
    print(f"(m+1) prime ratio: {prime_hits / len(rows):.3f}")

summarize(rows_2n, "2^n + 1")
summarize(rows_3n, "3^n + 1")

# -------------------------
# PLOT 1: divisor count jump
# -------------------------
plt.figure(figsize=(10, 5))

x2 = [r["n"] for r in rows_2n]
y2_m = [r["m_divisors"] for r in rows_2n]
y2_mp1 = [r["m_plus_1_divisors"] for r in rows_2n]

x3 = [r["n"] for r in rows_3n]
y3_m = [r["m_divisors"] for r in rows_3n]
y3_mp1 = [r["m_plus_1_divisors"] for r in rows_3n]

plt.plot(x2, y2_m, marker="o", label="2^n divisors")
plt.plot(x2, y2_mp1, marker="o", label="2^n + 1 divisors")
plt.plot(x3, y3_m, marker="s", label="3^n divisors")
plt.plot(x3, y3_mp1, marker="s", label="3^n + 1 divisors")

plt.title("Threshold Pairs: Divisor Count Structure")
plt.xlabel("n")
plt.ylabel("Number of divisors")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 2: mod transitions
# -------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, mod in zip(axes, MODS):
    ax.plot(
        [r["n"] for r in rows_2n],
        [r["m_residues"][mod] for r in rows_2n],
        marker="o",
        label=f"2^n mod {mod}"
    )
    ax.plot(
        [r["n"] for r in rows_2n],
        [r["mp1_residues"][mod] for r in rows_2n],
        marker="o",
        linestyle="--",
        label=f"2^n+1 mod {mod}"
    )
    ax.plot(
        [r["n"] for r in rows_3n],
        [r["m_residues"][mod] for r in rows_3n],
        marker="s",
        label=f"3^n mod {mod}"
    )
    ax.plot(
        [r["n"] for r in rows_3n],
        [r["mp1_residues"][mod] for r in rows_3n],
        marker="s",
        linestyle="--",
        label=f"3^n+1 mod {mod}"
    )

    ax.set_title(f"Residue Transitions mod {mod}")
    ax.set_xlabel("n")
    ax.set_ylabel("Residue")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)

plt.tight_layout()
plt.show()

# -------------------------
# OPTIONAL: special hand-picked thresholds
# -------------------------
specials = [6, 7, 12, 13, 16, 17, 34]

print("\n" + "=" * 80)
print("SPECIAL THRESHOLD NUMBERS")
print("=" * 80)
for s in specials:
    print(
        f"n={s:<3} "
        f"prime={isprime(s)!s:<5} "
        f"divisors={divisor_count(s):<3} "
        f"mod7={s % 7:<2} "
        f"mod17={s % 17:<2}"
    )


# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
