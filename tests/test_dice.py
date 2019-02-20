import unittest
from fractions import Fraction

from drv import *

class TestDice(unittest.TestCase):
    def perform_add(self, a, b, expected):
        dice = Dice(a)
        dice = dice.add(b)
        self.assertEqual(dice, Dice(expected))

    def test_add(self):
        self.perform_add({4:2, 6:3}, {6:1}, {4:2, 6:4})
        # dice = Dice({4:2, 6:3})
        # dice = dice.add({6:1})
        # self.assertEqual(dice, Dice({4:2, 6:4}))
