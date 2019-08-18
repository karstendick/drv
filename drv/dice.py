from collections import defaultdict
from copy import deepcopy
from fractions import Fraction

from drv.drv import Drv


class Dice(defaultdict):
    """A Dice object is a defaultdict of int to int, mapping a die size to the
    number of those dice.
    E.g. {4: 2, 6: 3} is 2d4 + 3d6
    """
    def __init__(self, d):
        defaultdict.__init__(self, int, d)

    def add(self, d):
        result = deepcopy(defaultdict(int, self))
        for k, v in d.items():
            result[k] += v
        self = Dice(defaultdict(int, result))
        return self

    def double(self):
        self = Dice(defaultdict(int, {k: 2*v for k,v in self.items()}))
        return self

    def to_drv(self):
        result = Drv({0:1}) # the "identity" Drv to use as an accumulator
        for dice_denom, dice_num in self.items():
            for i in range(dice_num):
                result += die_pmf(dice_denom)
        return result
