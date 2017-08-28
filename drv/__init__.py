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

    def support(self):
        return sorted([value for value, prob in self.items() if prob > 0])

    def min(self):
        return min(self.support())

    def max(self):
        return max(self.support())

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

def const_pmf(c):
    return Pmf({c: Fraction(1,1)})

def add(x, y):
    """Takes two pmfs, x and y, and adds them to get z, the convolution. This
    operation is commutative and associative.

    """
    # First, calculate the range of the support of the sum, z:
    z_min = x.min() + y.min()
    z_max = x.max() + y.max()

    z = defaultdict(int, {})
    # foreach value in pmf of z:
    for n in range(z_min, z_max+1):
        # calculate the convolution
        z[n] = sum([x[k] * y[n - k]
                    for k in range(n+1)])
    return Pmf(z)

def main():
    pmf = Pmf({1: Fraction(1,2),
               2: Fraction(1,2)})
    d6 = die_pmf(6)
    d6_2 = die_pmf(6)
    d6_plus_3 = add(d6, const_pmf(3))
    d4 = die_pmf(4)
    four_d4 = add(d4, add(d4, add(d4, d4)))
    drv = Drv(four_d4)
    import pdb; pdb.set_trace()
    print('done')

if __name__ == "__main__":
    main()
