import unittest
from fractions import Fraction

from drv.dice import *

class TestDice(unittest.TestCase):
    def perform_add(self, a, b, expected):
        dice = Dice(a)
        dice = dice.add(b)
        self.assertEqual(dice, Dice(expected))

    def test_add(self):
        self.perform_add({4:2, 6:3}, {6:1}, {4:2, 6:4})

        self.perform_add({}, {}, {})
        self.perform_add({}, {6:1}, {6:1})
        self.perform_add({}, {6:1, 4:1}, {6:1, 4:1})

        # subtraction works, too
        self.perform_add({6:3}, {6:-1}, {6:2})

    def test_double(self):
        dice = Dice({12:1, 6:3})
        dice = dice.double()
        self.assertEqual(dice, Dice({12:2, 6:6}))
