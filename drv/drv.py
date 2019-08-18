from collections import defaultdict
from fractions import Fraction
import itertools
import operator
from math import sqrt


def die_pmf(n):
    return Drv({k: Fraction(1, n) for k in range(1, n+1)})

def const_pmf(c):
    return Drv({c: Fraction(1, 1)})

class Drv(defaultdict):
    """A Drv (discrete random variable) is a defaultdict of int to Fraction,
    mapping values to probabilities.

    """
    def __init__(self, mapping):
        probability_sum = sum(mapping.values())
        if probability_sum != 1:
            raise ValueError("Probabilities must sum to 1; received invalid value {}"
                             .format(probability_sum))

        neg_probs = {value: prob for value, prob in mapping.items() if prob < 0}
        if neg_probs:
            raise ValueError("Probabilities must be non-negative; received invalid values {}"
                             .format(neg_probs))

        defaultdict.__init__(self, int, mapping)

    def support(self):
        return sorted([value for value, prob in self.items() if prob > 0])

    def min(self):
        return min(self.support())

    def max(self):
        return max(self.support())

    def expected_value(self):
        return sum([value * prob
                    for value, prob in self.items()])

    def mean(self):
        return self.expected_value()

    def variance(self):
        mean = self.mean()
        return sum([prob*value*value
                    for value, prob in self.items()]) \
                - mean*mean

    def std_dev(self):
        return sqrt(self.variance())

    def __str__(self):
        m = {value: round(float(prob), 5) for value, prob in self.items() if prob > 0}
        l = ["{0: >3} {1: >8.2%}".format(value, prob) for value, prob in sorted(m.items(), key=operator.itemgetter(0))]
        return "\n".join(l)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        """Adds two Drvs to get their convolution.
        This operation is commutative and associative.

        """
        # First, calculate the range of the support of the sum, z:
        z_min = self.min() + other.min()
        z_max = self.max() + other.max()

        z = defaultdict(int, {})
        # foreach value in pmf of z:
        for n in range(z_min, z_max+1):
            # calculate the convolution
            z[n] = sum([self[k] * other[n - k]
                        for k in range(n+1)])
        return Drv(z)

    def __mul__(self, other):
        z = defaultdict(int, {})
        for x_i, y_i in itertools.product(self.support(), other.support()):
            z_i = x_i * y_i
            z[z_i] += self[x_i] * other[y_i]
        return Drv(z)
