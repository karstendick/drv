from enum import Enum
from functools import partial, reduce
from collections import defaultdict
from fractions import Fraction

from drv.drv import Drv
from drv.dice import Dice

class Outcome(Enum):
    MISS = 0
    HIT = 1
    CRIT = 2

def constant_probability_multiply(k, x):
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


def roll_to_outcome(ac, attack_mod, roll):
    # TODO: crits on 19/18
    if roll == 1:
        return Outcome.MISS
    if roll == 20:
        return Outcome.CRIT
    if roll + attack_mod >= ac:
        return Outcome.HIT
    return Outcome.MISS

def get_probs(ac, attack_mod):
    this_roll_to_outcome = partial(roll_to_outcome, ac, attack_mod)
    rolls = range(1,21)
    outcomes = map(this_roll_to_outcome, rolls)
    def outcome_reducer(accum, elem):
        accum[elem] += Fraction(1, len(rolls))
        return accum
    outcome_map = reduce(outcome_reducer, outcomes, defaultdict(int))
    return outcome_map

def attack_dmg_pmf(ac, attack_mod, dmg_pmf, dmg_mod):
    outcome_probs = get_probs(ac, attack_mod)

    attack_hit_results_wo_mod = constant_probability_multiply(outcome_probs[Outcome.HIT], dmg_pmf.to_drv())
    attack_hit_results = constant_outcome_add(dmg_mod, attack_hit_results_wo_mod)

    crit_results_wo_mod = constant_probability_multiply(outcome_probs[Outcome.CRIT], dmg_pmf.double().to_drv())
    crit_results = constant_outcome_add(dmg_mod, crit_results_wo_mod)

    result = defaultdict(int, {})
    result = piecewise_add(attack_hit_results, crit_results)
    result[0] = outcome_probs[Outcome.MISS]

    return Drv(result)
