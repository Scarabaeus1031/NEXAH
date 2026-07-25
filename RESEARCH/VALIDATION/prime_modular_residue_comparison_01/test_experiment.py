import unittest

import run_experiment as experiment


class PrimeGenerationTests(unittest.TestCase):
    def test_finite_exceptional_primes_are_present(self):
        self.assertEqual(
            experiment.first_n_primes(10),
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
        )

    def test_without_2_3_policy_removes_only_two_terms(self):
        primes = experiment.first_n_primes(10)
        self.assertEqual(
            experiment.policy_slice(primes, 10, "without_2_3"),
            [5, 7, 11, 13, 17, 19, 23, 29],
        )


class ModelTests(unittest.TestCase):
    def test_transition_rows_are_probabilities(self):
        model = experiment.transition_model([0, 1, 0, 1, 1], 2)
        for row in model:
            self.assertAlmostEqual(sum(row), 1.0)
            self.assertTrue(all(item > 0 for item in row))

    def test_information_gain_detects_deterministic_transition(self):
        train = [0, 1] * 100
        test = [0, 1] * 20
        result = experiment.evaluate_prediction(
            test,
            experiment.transition_model(train, 2),
            experiment.marginal_model(train, 2),
        )
        self.assertGreater(result["information_gain_bits"], 0.9)

    def test_fixed_bridge_uses_declared_formula(self):
        self.assertEqual(
            [(7 * residue + experiment.BRIDGE_DELTA) % 17
             for residue in range(7)],
            [8, 15, 5, 12, 2, 9, 16],
        )

    def test_affine_bridge_is_not_a_group_homomorphism(self):
        bridge = lambda residue: (
            7 * residue + experiment.BRIDGE_DELTA
        ) % 17
        self.assertNotEqual(bridge((1 + 1) % 7), (bridge(1) + bridge(1)) % 17)


class BoundaryTests(unittest.TestCase):
    def test_folds_are_chronological_and_disjoint(self):
        for train_fraction, test_fraction in experiment.FOLDS:
            train_end = int(experiment.N_PRIMES * train_fraction)
            test_end = int(experiment.N_PRIMES * test_fraction)
            self.assertLess(train_end, test_end)
            self.assertLessEqual(test_end, experiment.N_PRIMES)

    def test_stabilization_decision_is_never_inferred(self):
        self.assertIn(
            "No dynamical system",
            (
                "No dynamical system, intervention, perturbation or stability "
                "endpoint is part of this experiment."
            ),
        )


if __name__ == "__main__":
    unittest.main()
