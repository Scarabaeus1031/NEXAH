# =========================
# V22 – TIME LAG ANALYSIS
# =========================

def compute_cross_correlation(a, b, max_lag=200):
    lags = np.arange(-max_lag, max_lag)
    corr = []

    a = (a - np.mean(a)) / (np.std(a) + 1e-8)
    b = (b - np.mean(b)) / (np.std(b) + 1e-8)

    for lag in lags:
        if lag < 0:
            c = np.corrcoef(a[:lag], b[-lag:])[0,1]
        elif lag > 0:
            c = np.corrcoef(a[lag:], b[:-lag])[0,1]
        else:
            c = np.corrcoef(a, b)[0,1]

        corr.append(c)

    return lags, np.array(corr)

# --- compute lag relationships

lags1, corr_curl_div = compute_cross_correlation(curl, div)
lags2, corr_div_curl = compute_cross_correlation(div, curl)

# =========================
# VISUALIZATION
# =========================

plt.figure(figsize=(10,6))

plt.plot(lags1, corr_curl_div, label="curl → div")
plt.plot(lags2, corr_div_curl, label="div → curl")

plt.axvline(0, linestyle="--", color="black")

plt.title("V22: Time Lag Coupling (Field Causality)")
plt.xlabel("Lag (timesteps)")
plt.ylabel("Correlation")
plt.legend()

out = os.path.join(OUTPUT_DIR, "v22_time_lag.png")
plt.savefig(out, dpi=150)

print(f"Saved: {out}")

# =========================
# PRINT RESULT
# =========================

best_lag_cd = lags1[np.argmax(corr_curl_div)]
best_lag_dc = lags2[np.argmax(corr_div_curl)]

print("\n--- TIME LAG RESULTS ---")
print(f"curl → div lag: {best_lag_cd}")
print(f"div → curl lag: {best_lag_dc}")
