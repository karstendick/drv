import unittest
from fractions import Fraction

from drv import *

class TestPmf(unittest.TestCase):
    def test_probability_sum(self):
        bad_pmf = {1: Fraction(1,2),
                   2: Fraction(1,2),
                   3: Fraction(1,2)}
        self.assertRaises(ValueError, Pmf, bad_pmf)
        good_pmf = {1: Fraction(1,2),
                    2: Fraction(1,2)}
        self.assertEqual(Pmf(good_pmf), Pmf(good_pmf))

    def test_die_pmf(self):
        d4 = {1: Fraction(1,4),
              2: Fraction(1,4),
              3: Fraction(1,4),
              4: Fraction(1,4)}
        self.assertEqual(d4, die_pmf(4))

class TestDrv(unittest.TestCase):
    def test_expected_value(self):
        drv = Drv(die_pmf(6))
        self.assertEqual(Fraction(7,2), drv.expected_value())
