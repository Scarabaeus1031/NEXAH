import numpy as np

def generate_signal(n=100, transition=60):
    t = np.arange(n)
    x = np.sin(0.2 * t)

    # regime change
    x[transition:] += np.random.normal(0, 0.8, size=n-transition)

    return x


def switching_density(x):
    dx = np.diff(x)
    signs = np.sign(dx)
    switches = np.abs(np.diff(signs)) > 0
    density = np.convolve(switches, np.ones(5)/5, mode='same')
    return density


def variance_proxy(x):
    return np.convolve(x**2, np.ones(10)/10, mode='same')


def detect_time(signal, threshold):
    for i, val in enumerate(signal):
        if val > threshold:
            return i
    return np.nan


runs = 50

switch_times = []
var_times = []

for r in range(runs):
    np.random.seed(r)

    x = generate_signal()

    sd = switching_density(x)
    var = variance_proxy(x)

    # simple detection thresholds
    t_switch = detect_time(sd, 0.5)
    t_var = detect_time(var, 0.5)

    switch_times.append(t_switch)
    var_times.append(t_var)


print("\n--- V19 RESULTS ---")

print("Switching detection:")
print(f"mean = {np.nanmean(switch_times):.2f}, std = {np.nanstd(switch_times):.2f}")

print("\nVariance detection:")
print(f"mean = {np.nanmean(var_times):.2f}, std = {np.nanstd(var_times):.2f}")

diff = np.array(var_times) - np.array(switch_times)

print("\nDetection delay (variance - switching):")
print(f"mean = {np.nanmean(diff):.2f}, std = {np.nanstd(diff):.2f}")
