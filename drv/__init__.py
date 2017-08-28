from collections import defaultdict
from fractions import Fraction
from math import sqrt

class Pmf(defaultdict):
    """A Pmf (probability mass function) is a defaultdict of int to Fraction,
    mapping values to probabilities.

    """
    def __init__(self, mapping):
        probability_sum = sum(mapping.values())
        if probability_sum != 1:
            raise ValueError("Pmf sum must be 1; received invalid value {}"
                             .format(probability_sum))
        defaultdict.__init__(self, int, mapping)

class Drv:
    """A Drv (discrete random variable) has a Pmf and provides methods for
    calculating statistics on it.

    """
    def __init__(self, pmf):
        self.pmf = pmf

    def expected_value(self):
        return sum([value * prob
                    for value, prob in self.pmf.items()])

    def mean(self):
        return self.expected_value()

    def variance(self):
        mean = self.mean()
        return sum([prob*value*value
                    for value, prob in self.pmf.items()]) \
                - mean*mean

    def std_dev(self):
        return sqrt(self.variance())


def die_pmf(n):
    return Pmf({k: Fraction(1,n) for k in range(1, n+1)})


def main():
    pmf = Pmf({1: Fraction(1,2),
               2: Fraction(1,2)})
    drv = Drv(die_pmf(6))
    import pdb; pdb.set_trace()
    print('done')

if __name__ == "__main__":
    main()
