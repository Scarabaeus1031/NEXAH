import math
import unittest

import run_experiment as experiment


class ArithmeticTests(unittest.TestCase):
    def test_first_primes_include_finite_exceptions(self):
        self.assertEqual(
            experiment.first_n_primes(10),
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
        )

    def test_mod6_prime_support(self):
        primes = experiment.first_n_primes(1_000)
        self.assertTrue(all(prime % 6 in (1, 5) for prime in primes if prime > 3))

    def test_crt_roundtrip_for_every_mod42_state(self):
        for value in range(42):
            self.assertEqual(
                experiment.crt_encode_6_7(*experiment.crt_decode_42(value)),
                value,
            )

    def test_crt_coordinates_have_declared_residues(self):
        for residue6 in range(6):
            for residue7 in range(7):
                encoded = experiment.crt_encode_6_7(residue6, residue7)
                self.assertEqual(encoded % 6, residue6)
                self.assertEqual(encoded % 7, residue7)

    def test_wheel_invariants(self):
        self.assertEqual(experiment.radical(360), 30)
        self.assertEqual(experiment.euler_phi(280), 96)
        self.assertEqual(experiment.euler_phi(360), 96)
        self.assertEqual(math.lcm(20, 24, 30), 120)

    def test_mod360_has_twelve_lifts_per_mod30_unit(self):
        units30 = [value for value in range(30) if math.gcd(value, 30) == 1]
        units360 = [
            value for value in range(360) if math.gcd(value, 360) == 1
        ]
        for residue in units30:
            self.assertEqual(
                sum(value % 30 == residue for value in units360),
                12,
            )


class ModelTests(unittest.TestCase):
    def test_markov_detects_alternating_dual_sequence(self):
        train = [1, 5] * 100
        test = [1, 5] * 20
        result = experiment.evaluate_prediction(
            test,
            experiment.fit_markov(train),
            experiment.fit_marginal(train, 6),
            6,
        )
        self.assertGreater(result["information_gain_bits"], 0.9)

    def test_reflection_tv_is_zero_for_reflection_symmetric_edges(self):
        residues = [1, 5, 1, 5, 1]
        self.assertEqual(experiment.reflection_tv(residues, 6), 0.0)

    def test_scan_contains_predeclared_spaces(self):
        for modulus in (6, 7, 30, 31, 32, 33, 42, 120, 210, 280, 360):
            self.assertIn(modulus, experiment.SCAN_MODULI)


if __name__ == "__main__":
    unittest.main()
