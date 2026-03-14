from analysis.lorenz_ftle_map import main as run_ftle_map
from regimes.lorenz_parameter_atlas import main as run_parameter_atlas
from analysis.lorenz_switch_map import main as run_switch_map
from analysis.lorenz_unwrapped_return_map import main as run_unwrapped_return_map
from analysis.lorenz_symbolic_dynamics import main as run_symbolic_dynamics


def main():
    print("=== NEXAH Chaos Navigator :: Lorenz Tool ===")
    print("Running core Lorenz navigation analyses...")
    print()

    print("[1/5] FTLE map")
    run_ftle_map()

    print("[2/5] Parameter atlas")
    run_parameter_atlas()

    print("[3/5] Switch map")
    run_switch_map()

    print("[4/5] Unwrapped return map")
    run_unwrapped_return_map()

    print("[5/5] Symbolic dynamics")
    run_symbolic_dynamics()

    print()
    print("Done. Outputs were written to APPLICATIONS/outputs/lorenz_navigation/")


if __name__ == "__main__":
    main()
