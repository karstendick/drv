import unittest
from fractions import Fraction

from drv.attackroll import *

class TestAttackroll(unittest.TestCase):
    def test_get_probs(self):
        expected = {Outcome.MISS: Fraction(9,20),
                    Outcome.HIT: Fraction(1,2),
                    Outcome.CRIT: Fraction(1,20)}
        self.assertEqual(expected, get_probs(15,5))

    def test_get_probs_adv(self):
        expected = {Outcome.MISS: Fraction(81,400),
                    Outcome.HIT: Fraction(7,10),
                    Outcome.CRIT: Fraction(39,400)}
        self.assertEqual(expected, get_probs(15,5, roll_type=RollType.ADV))

    def test_get_probs_disadv(self):
        expected = {Outcome.MISS: Fraction(279,400),
                    Outcome.HIT: Fraction(3,10),
                    Outcome.CRIT: Fraction(1,400)}
        self.assertEqual(expected, get_probs(15,5, roll_type=RollType.DISADV))

    def test_get_probs_elven_accuracy(self):
        expected = {Outcome.MISS: Fraction(729,8000),
                    Outcome.HIT: Fraction(613,800),
                    Outcome.CRIT: Fraction(1141,8000)}
        self.assertEqual(expected, get_probs(15,5, roll_type=RollType.ELVEN_ACCURACY))
