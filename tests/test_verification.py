"""Regression checks for verification failures and nonunique SVD bases."""
import contextlib
import io
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from check_simulation import check_assumptions, compare_svd, report


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)
        self.s = np.array([3., 3., 1.])
        self.reference = np.eye(3)
        angle = 0.7
        self.rotated = np.array([[np.cos(angle), -np.sin(angle), 0.],
                                 [np.sin(angle), np.cos(angle), 0.],
                                 [0., 0., 1.]])

    def test_failed_report_exits_unsuccessfully(self):
        for value in (2., np.nan, np.inf):
            with self.subTest(value=value), self.assertRaises(SystemExit) as caught:
                report("Injected failure", value, 1.)
            self.assertNotEqual(caught.exception.code, 0)

    def test_rotated_tied_basis_and_partial_tied_block_pass(self):
        for k in (1, 2, 3):
            self.assertTrue(compare_svd(self.s[:k], self.rotated[:, :k],
                                       self.rotated[:, :k], self.reference,
                                       self.s, self.reference))

    def test_sign_flips_pass(self):
        vectors = self.reference * np.array([-1., 1., -1.])
        self.assertTrue(compare_svd(self.s, vectors, vectors, self.reference,
                                   self.s, self.reference))

    def test_inconsistent_left_right_rotations_fail(self):
        with self.assertRaises(SystemExit):
            compare_svd(self.s, self.rotated, self.reference, self.reference,
                        self.s, self.reference)

    def test_wrong_spectrum_and_nonorthogonal_vectors_fail(self):
        with self.assertRaises(SystemExit):
            compare_svd(self.s + 1, self.reference, self.reference,
                        self.reference, self.s, self.reference)
        with self.assertRaises(SystemExit):
            compare_svd(self.s, 2 * self.reference, self.reference,
                        self.reference, self.s, self.reference)

    def test_distinct_values_cannot_rotate(self):
        with self.assertRaises(SystemExit):
            compare_svd(np.array([3., 2., 1.]), self.rotated, self.rotated,
                        self.reference, np.array([3., 2., 1.]), self.reference)

    def test_assumption_failure_exits_unsuccessfully(self):
        with self.assertRaises(SystemExit):
            check_assumptions(np.diag(self.s), self.s, 2 * self.reference,
                              self.reference, self.s)


if __name__ == "__main__":
    unittest.main()
