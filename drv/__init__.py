from collections import defaultdict
from fractions import Fraction

import matplotlib.pyplot as plt

from drv.drv import Drv
from drv.dice import Dice
from drv.attackroll import *


def plot_drv(drv):
    plt.bar(drv.keys(), drv.values())
    plt.xticks(drv.support())
    # plt.show()

def plot_weapons(crits_on=None, roll_type=None):
    shortsword = Dice({6:1})
    greataxe = Dice({12:1})
    greatsword = Dice({6:2})

    shortsword_attack_roll = attack_dmg_pmf(15, 5, shortsword, 3, crits_on=crits_on, roll_type=roll_type)
    print(shortsword_attack_roll)
    plt.subplot(1, 3, 1)
    plot_drv(shortsword_attack_roll)

    greataxe_attack_roll = attack_dmg_pmf(15, 5, greataxe, 3, crits_on=crits_on, roll_type=roll_type)
    print(greataxe_attack_roll)
    plt.subplot(1, 3, 2)
    plot_drv(greataxe_attack_roll)

    greatsword_attack_roll = attack_dmg_pmf(15, 5, greatsword, 3, crits_on=crits_on, roll_type=roll_type)
    print(greatsword_attack_roll)
    plt.subplot(1, 3, 3)
    plot_drv(greatsword_attack_roll)

    plt.show()


    f, axarr = plt.subplots(3, sharex=True)
    axarr[0].bar(shortsword_attack_roll.keys(), shortsword_attack_roll.values())
    axarr[0].set_title('Shortsword')
    axarr[1].bar(greataxe_attack_roll.keys(), greataxe_attack_roll.values())
    axarr[1].set_title('Greataxe')
    axarr[2].bar(greatsword_attack_roll.keys(), greatsword_attack_roll.values())
    axarr[2].set_title('Greatsword')

    plt.show()

def main():
    probs = get_probs(15,5)
    print(probs)

    adv_probs = get_probs(15,5, roll_type=RollType.ADV)
    print(adv_probs)

    disadv_probs = get_probs(15,5, roll_type=RollType.DISADV)
    print(disadv_probs)

    elven_accuracy_probs = get_probs(15,5, roll_type=RollType.ELVEN_ACCURACY)
    print(elven_accuracy_probs)

    champion_adv_probs = get_probs(15,5, crits_on=CritsOn.C19, roll_type=RollType.ADV)
    print(champion_adv_probs)

    champion_elven_accuracy_probs = get_probs(15,5, crits_on=CritsOn.C19, roll_type=RollType.ELVEN_ACCURACY)
    print(champion_elven_accuracy_probs)

    champion18_elven_accuracy_probs = get_probs(15,5, crits_on=CritsOn.C18_19, roll_type=RollType.ELVEN_ACCURACY)
    print(champion18_elven_accuracy_probs)

    plot_weapons(CritsOn.C19, RollType.ADV)

    import pdb; pdb.set_trace()
    print('done')


if __name__ == "__main__":
    main()
