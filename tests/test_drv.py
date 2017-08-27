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
