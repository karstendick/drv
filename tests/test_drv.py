import unittest
from fractions import Fraction
from math import sqrt

from drv.drv import *

class TestDrv(unittest.TestCase):
    def test_probability_sum(self):
        bad_pmf = {1: Fraction(1,2),
                   2: Fraction(1,2),
                   3: Fraction(1,2)}
        self.assertRaises(ValueError, Drv, bad_pmf)
        good_pmf = {1: Fraction(1,2),
                    2: Fraction(1,2)}
        self.assertEqual(Drv(good_pmf), Drv(good_pmf))

    def test_die_pmf(self):
        d4 = {1: Fraction(1,4),
              2: Fraction(1,4),
              3: Fraction(1,4),
              4: Fraction(1,4)}
        self.assertEqual(d4, die_pmf(4))

    def test_expected_value(self):
        drv = Drv(die_pmf(6))
        self.assertEqual(Fraction(7,2), drv.expected_value())

    def test_die_variance(self):
        # the variance of any fair die of n sides is:
        # (n^2 - 1)/12
        for n in range(1,11):
            drv = Drv(die_pmf(n))
            self.assertEqual(Fraction(n*n-1, 12), drv.variance())

    def test_zero_variance(self):
        drv = Drv(Drv({1: 1}))
        self.assertEqual(0, drv.variance())

    def test_std_dev(self):
        drv = Drv(die_pmf(6))
        self.assertEqual(sqrt(Fraction(35,12)), drv.std_dev())

    def test_add(self):
        d4 = die_pmf(4)
        d6 = die_pmf(6)
        expected = Drv({2: Fraction(1,24),
                        3: Fraction(2,24),
                        4: Fraction(3,24),
                        5: Fraction(4,24),
                        6: Fraction(4,24),
                        7: Fraction(4,24),
                        8: Fraction(3,24),
                        9: Fraction(2,24),
                        10: Fraction(1,24)})
        self.assertEqual(expected, d4 + d6)
        self.assertEqual(expected, d6 + d4)

    def test_add_const(self):
        d4 = die_pmf(4)
        const3 = const_pmf(3)
        expected = Drv({4: Fraction(1,4), 5: Fraction(1,4),
                        6: Fraction(1,4), 7: Fraction(1,4)})
        self.assertEqual(expected, d4 + const3)
        self.assertEqual(expected, const3 + d4)
