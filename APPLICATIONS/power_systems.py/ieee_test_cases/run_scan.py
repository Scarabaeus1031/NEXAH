from ieee_loader import load_ieee14
from stability_scan import run_stability_scan

def main():
    net = load_ieee14()
    results = run_stability_scan(net)

    for factor, stable in results:
        status = "Stable" if stable else "Unstable"
        print(f"Load factor: {factor:.2f} → {status}")

if __name__ == "__main__":
    main()
