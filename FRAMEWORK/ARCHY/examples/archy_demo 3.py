from __future__ import annotations

from FRAMEWORK.ARCHY.stability_models.archy_system_model import (
    ArchySystemInput,
    analyze_archy_system,
    pretty_print,
)


def cave_system():
    return ArchySystemInput(
        name="cave",

        outside={
            "thermal": 20,
            "pressure": 1,
            "acoustic": 1,
            "humidity": 1,
        },

        inside={
            "thermal": 5,
            "pressure": 0.1,
            "acoustic": 0.2,
            "humidity": 0.6,
        },

        domain_weights={
            "thermal": 1.2,
            "pressure": 1.0,
            "acoustic": 1.0,
            "humidity": 0.8,
        },

        active_elements={
            "mass": 1,
            "medium": 1,
            "geometry": 0.7,
            "location": 0.8,
            "layering": 0.6,
        },

        base_orientation=0,
        architectural_delta=0.05,
        environmental_delta=0.02,
    )


def igloo_system():
    return ArchySystemInput(
        name="igloo",

        outside={
            "thermal": 25,
            "pressure": 1,
            "acoustic": 1,
            "humidity": 0.8,
        },

        inside={
            "thermal": 2,
            "pressure": 0.2,
            "acoustic": 0.3,
            "humidity": 0.5,
        },

        domain_weights={
            "thermal": 1.3,
            "pressure": 1.0,
            "acoustic": 0.8,
            "humidity": 0.7,
        },

        active_elements={
            "mass": 0.8,
            "medium": 0.7,
            "geometry": 1.0,
            "location": 0.8,
            "layering": 0.6,
            "orientation": 0.6,
        },

        base_orientation=5,
        architectural_delta=0.03,
        environmental_delta=0.02,
    )


def city_block():
    return ArchySystemInput(
        name="city_block",

        outside={
            "thermal": 18,
            "pressure": 1,
            "acoustic": 4,
            "humidity": 1,
        },

        inside={
            "thermal": 8,
            "pressure": 0.3,
            "acoustic": 1,
            "humidity": 0.7,
        },

        domain_weights={
            "thermal": 1.0,
            "pressure": 0.8,
            "acoustic": 1.2,
            "humidity": 0.6,
        },

        active_elements={
            "mass": 0.7,
            "geometry": 0.8,
            "location": 0.9,
            "layering": 0.5,
            "orientation": 0.7,
            "urban_form": 1.0,
        },

        base_orientation=10,
        architectural_delta=0.08,
        environmental_delta=0.05,
    )


def run_demo():

    systems = [
        cave_system(),
        igloo_system(),
        city_block(),
    ]

    results = []

    for system in systems:
        result = analyze_archy_system(system)
        results.append(result)

    print()
    print("ARCHY SYSTEM COMPARISON")
    print("=" * 50)
    print()

    for r in results:
        print(pretty_print(r))
        print()
        print("-" * 50)
        print()


if __name__ == "__main__":
    run_demo()
