from collections import defaultdict
import itertools
from fractions import Fraction
from math import sqrt
from copy import deepcopy
import operator


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
        return result

    def double(self):
        return {k: 2*v for k,v in self.items()}

    def to_drv(self):
        result = Drv({0:1}) # the "null" Drv to use as an accumulator
        for dice_denom, dice_num in self.items():
            for i in range(dice_num):
                result = add(result, die_pmf(dice_denom))
        return result

def add_dice(d1, d2):
    result = defaultdict(int)
    result = deepcopy(defaultdict(int, d1))
    for k, v in d2.items():
        result[k] += v
    return result

def die_pmf(n):
    return Drv({k: Fraction(1, n) for k in range(1, n+1)})

def const_pmf(c):
    return Drv({c: Fraction(1, 1)})

def add(x, y):
    """Takes two Drvs, x and y, and adds them to get z, the convolution. This
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
    return Drv(z)

def multiply(x, y):
    z = defaultdict(int, {})
    for x_i, y_i in itertools.product(x.support(), y.support()):
        z_i = x_i * y_i
        z[z_i] += x[x_i] * y[y_i]
    return Drv(z)

def constant_probility_multiply(k, x):
    z = defaultdict(int, {})
    for value, prob in x.items():
        z[value] = prob * k
    return z

def support(x):
    return sorted([value for value, prob in x.items() if prob > 0])

def piecewise_add(x,y):
    z = defaultdict(int, {})
    for i in set().union(support(x), support(y)):
        z[i] = x[i] + y[i]
    return z


# TODO: debug this so that it never returns negative probabilities, e.g.:
# attack_pmf(1, 5)
# defaultdict(<class 'int'>, {0: Fraction(-1, 4), 1: Fraction(6, 5), 2: Fraction(1, 20)})
# attack_pmf(30, 5)
# defaultdict(<class 'int'>, {0: Fraction(6, 5), 1: Fraction(-1, 4), 2: Fraction(1, 20)})
#
# TODO: Bug: don't just double damage on a crit; instead, roll more dice
# e.g.: 2d6, NOT 2*(1d6)
def attack_pmf(ac, attack_mod):
    atk_pmf = Drv({0: Fraction(ac - attack_mod - 1, 20),
                   1: Fraction(20 - ac + attack_mod, 20),
                   2: Fraction(1, 20)})
    return atk_pmf
# TODO: Likewise, e.g.:
# attack_dmg_mod_pmf(1, 5)
# defaultdict(<class 'int'>, {0: Fraction(-1, 4), 1: Fraction(5, 4)})
# attack_dmg_mod_pmf(30, 5)
# defaultdict(<class 'int'>, {0: Fraction(6, 5), 1: Fraction(-1, 5)})
def attack_dmg_mod_pmf(ac, attack_mod):
    atk_pmf = Drv({0: Fraction(ac - attack_mod - 1, 20),
                   1: Fraction(20 - ac + attack_mod + 1, 20)})
    return atk_pmf


def attack_dmg_pmf(ac, attack_mod, dmg_pmf, dmg_mod):
    #prob_miss = ac - attack_mod -2
    # atk_pmf = attack_pmf(ac, attack_mod)
    # total_dmg = add(dmg_pmf, const_pmf(dmg_mod))
    # result = multiply(atk_pmf, total_dmg)

    attack_hit_results = constant_probility_multiply(pr_hit(ac, attack_mod), Dice(dmg_pmf).to_drv())
    crit_results = constant_probility_multiply(pr_crit(ac, attack_mod), Dice(Dice(dmg_pmf).double()).to_drv())
    result = defaultdict(int, {})
    result = piecewise_add(attack_hit_results, crit_results)
    result[0] = pr_miss(ac, attack_mod)

    # return Drv(result)
    return result

def pr_crit(ac, attack_mod):
    # TODO: Advantage and disadvantage
    # TODO: Hafling Lucky trait to re-roll 1's
    return Fraction(1,20)

def pr_hit(ac, attack_mod):
    # TODO: crits on 19s
    count_of_hits = max(0, min(18, 20 - ac + attack_mod))
    return Fraction(count_of_hits, 20)

def pr_miss(ac, attack_mod):
    return 1 - pr_crit(ac, attack_mod) - pr_hit(ac, attack_mod)

def attack_roll(ac, attack_mod, dmg_dice, dmg_mod):
    pass

def main():
    pmf = Drv({1: Fraction(1, 2),
               2: Fraction(1, 2)})
    d6 = die_pmf(6)
    d6_2 = die_pmf(6)
    d6_plus_3 = add(d6, const_pmf(3))
    d4 = die_pmf(4)
    four_d4 = add(d4, add(d4, add(d4, d4)))
    drv = Drv(four_d4)
    attack_roll = attack_dmg_pmf(15, 5, Dice({6:1}), 3)

    dd = Dice({4:2, 6:3})
    # d2 = add_dice(d, {6:1})
    dd.add({6:1})

    import pdb; pdb.set_trace()
    print('done')

if __name__ == "__main__":
    main()
