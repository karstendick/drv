from collections import defaultdict
import itertools
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

    def __str__(self):
        m = {value: round(float(prob), 5) for value, prob in self.items() if prob > 0}
        l = ["{0: >3} {1: >8.2%}".format(value, prob) for value, prob in m.items()]
        return "\n".join(l)

    def __repr__(self):
        return self.__str__()

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

def multiply(x, y):
    z = defaultdict(int, {})
    for x_i, y_i in itertools.product(x.support(), y.support()):
        z_i = x_i * y_i
        z[z_i] += x[x_i]*y[y_i]
    return Pmf(z)

# TODO: debug this so that it never returns negative probabilities, e.g.:
# attack_pmf(1, 5)
# defaultdict(<class 'int'>, {0: Fraction(-1, 4), 1: Fraction(6, 5), 2: Fraction(1, 20)})
# attack_pmf(30, 5)
# defaultdict(<class 'int'>, {0: Fraction(6, 5), 1: Fraction(-1, 4), 2: Fraction(1, 20)})
#
# TODO: Bug: don't just double damage on a crit; instead, roll more dice
# i.e.: 2d6, NOT 2*(1d6)
def attack_pmf(ac, attack_mod):
    atk_pmf = Pmf({0: Fraction(ac - attack_mod -1, 20),
                    1: Fraction(20-ac + attack_mod, 20),
                    2: Fraction(1,20)})
    return atk_pmf
# TODO: Likewise, e.g.:
# attack_dmg_mod_pmf(1, 5)
# defaultdict(<class 'int'>, {0: Fraction(-1, 4), 1: Fraction(5, 4)})
# attack_dmg_mod_pmf(30, 5)
# defaultdict(<class 'int'>, {0: Fraction(6, 5), 1: Fraction(-1, 5)})
def attack_dmg_mod_pmf(ac, attack_mod):
    atk_pmf = Pmf({0: Fraction(ac - attack_mod -1, 20),
                    1: Fraction(20-ac + attack_mod+1, 20)})
    return atk_pmf


def attack_dmg_pmf(ac, attack_mod, dmg_pmf, dmg_mod):
    #prob_miss = ac - attack_mod -2
    atk_pmf = attack_pmf(ac, attack_mod)
    total_dmg = add(dmg_pmf, const_pmf(dmg_mod))
    result = multiply(atk_pmf, total_dmg)
    return result

def main():
    pmf = Pmf({1: Fraction(1,2),
               2: Fraction(1,2)})
    d6 = die_pmf(6)
    d6_2 = die_pmf(6)
    d6_plus_3 = add(d6, const_pmf(3))
    d4 = die_pmf(4)
    four_d4 = add(d4, add(d4, add(d4, d4)))
    drv = Drv(four_d4)
    attack_roll = attack_dmg_pmf(13, 5, d6, 3)
    import pdb; pdb.set_trace()
    print('done')

if __name__ == "__main__":
    main()
