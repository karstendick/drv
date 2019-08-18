from collections import defaultdict
import itertools
from fractions import Fraction
from copy import deepcopy

import matplotlib.pyplot as plt

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
                result = add(result, die_pmf(dice_denom))
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

def constant_outcome_add(k, x):
    z = defaultdict(int, {})
    for value, prob in x.items():
        z[value + k] = prob
    return z

def support(x):
    return sorted([value for value, prob in x.items() if prob > 0])

def piecewise_add(x,y):
    z = defaultdict(int, {})
    for i in set().union(support(x), support(y)):
        z[i] = x[i] + y[i]
    return z


def attack_dmg_pmf(ac, attack_mod, dmg_pmf, dmg_mod):
    attack_hit_results_wo_mod = constant_probility_multiply(pr_hit(ac, attack_mod), dmg_pmf.to_drv())
    attack_hit_results = constant_outcome_add(dmg_mod, attack_hit_results_wo_mod)

    crit_results_wo_mod = constant_probility_multiply(pr_crit(ac, attack_mod), dmg_pmf.double().to_drv())
    crit_results = constant_outcome_add(dmg_mod, crit_results_wo_mod)

    result = defaultdict(int, {})
    result = piecewise_add(attack_hit_results, crit_results)
    result[0] = pr_miss(ac, attack_mod)

    return Drv(result)

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


def main():

    attack_roll = attack_dmg_pmf(15, 5, Dice({6:1}), 3)
    print(attack_roll)



    plt.bar(attack_roll.keys(), attack_roll.values())
    plt.xticks(attack_roll.support())
    plt.show()

    import pdb; pdb.set_trace()
    print('done')

if __name__ == "__main__":
    main()
