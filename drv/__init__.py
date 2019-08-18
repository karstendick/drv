from collections import defaultdict
from fractions import Fraction

import matplotlib.pyplot as plt

from drv.drv import Drv
from drv.dice import Dice


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
    d6 = Dice({6:1})
    attack_roll = attack_dmg_pmf(15, 5, d6, 3)
    print(attack_roll)



    plt.bar(attack_roll.keys(), attack_roll.values())
    plt.xticks(attack_roll.support())
    plt.show()

    import pdb; pdb.set_trace()
    print('done')

if __name__ == "__main__":
    main()
