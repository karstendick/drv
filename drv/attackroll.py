from enum import Enum
from functools import partial, reduce
from collections import defaultdict
from fractions import Fraction
from itertools import product

from drv.drv import Drv
from drv.dice import Dice

class Outcome(Enum):
    MISS = 0
    HIT = 1
    CRIT = 2

class RollType(Enum):
    DISADV = 0
    ADV = 1
    ELVEN_ACCURACY = 2

class CritsOn(Enum):
    C19 = 1
    C18_19 = 2

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


def roll_to_outcome(ac, attack_mod, crits_on, roll):
    if crits_on == CritsOn.C19:
        crits = [19, 20]
    elif crits_on == CritsOn.C18_19:
        crits = [18, 19, 20]
    else:
        crits = [20]

    if roll == 1:
        return Outcome.MISS
    if roll in crits:
        return Outcome.CRIT
    if roll + attack_mod >= ac:
        return Outcome.HIT
    return Outcome.MISS

def get_probs(ac, attack_mod, crits_on=None, roll_type=None):
    if not roll_type:
        rolls = range(1,21)
    elif roll_type == RollType.ADV:
        roll_pairs = product(range(1,21), repeat=2)
        rolls = list(map(max, roll_pairs))
    elif roll_type == RollType.DISADV:
        roll_pairs = product(range(1,21), repeat=2)
        rolls = list(map(min, roll_pairs))
    elif roll_type == RollType.ELVEN_ACCURACY:
        roll_pairs = product(range(1,21), repeat=3)
        rolls = list(map(max, roll_pairs))

    this_roll_to_outcome = partial(roll_to_outcome, ac, attack_mod, crits_on)
    outcomes = map(this_roll_to_outcome, rolls)
    def outcome_reducer(accum, elem):
        accum[elem] += Fraction(1, len(rolls))
        return accum
    outcome_map = reduce(outcome_reducer, outcomes, defaultdict(int))
    return outcome_map

def attack_dmg_pmf(ac, attack_mod, dmg_pmf, dmg_mod, crits_on=None, roll_type=None):
    outcome_probs = get_probs(ac, attack_mod, crits_on, roll_type)

    attack_hit_results_wo_mod = constant_probability_multiply(outcome_probs[Outcome.HIT], dmg_pmf.to_drv())
    attack_hit_results = constant_outcome_add(dmg_mod, attack_hit_results_wo_mod)

    crit_results_wo_mod = constant_probability_multiply(outcome_probs[Outcome.CRIT], dmg_pmf.double().to_drv())
    crit_results = constant_outcome_add(dmg_mod, crit_results_wo_mod)

    result = defaultdict(int, {})
    result = piecewise_add(attack_hit_results, crit_results)
    result[0] = outcome_probs[Outcome.MISS]

    return Drv(result)
