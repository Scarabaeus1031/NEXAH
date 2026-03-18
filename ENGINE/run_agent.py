# ENGINE/run_agent.py

from analysis.stability_landscape_generator import generate_stability_landscape


def main():
    print("NEXAH Agent started")
    print("Initializing system...")

    for step in range(3):
        print(f"\nStep {step}")
        print("Calling analysis layer...")

        # 🔥 echter Call
        landscape = generate_stability_landscape()

        # minimal interpretieren
        summary = {
            "min": float(landscape.min()),
            "max": float(landscape.max()),
            "mean": float(landscape.mean())
        }

        print("Landscape summary:", summary)

        # einfache Entscheidung
        if summary["max"] > 0.8:
            print("→ High stability region detected")
        else:
            print("→ Exploring further...")

    print("\nAgent finished.")


if __name__ == "__main__":
    main()
