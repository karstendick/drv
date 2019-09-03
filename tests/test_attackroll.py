import unittest
from fractions import Fraction

from drv.attackroll import *

class TestAttackroll(unittest.TestCase):
    def test_get_probs(self):
        expected = {Outcome.MISS: Fraction(9,20),
                    Outcome.HIT: Fraction(1,2),
                    Outcome.CRIT: Fraction(1,20)}
        self.assertEqual(expected, get_probs(15,5))
