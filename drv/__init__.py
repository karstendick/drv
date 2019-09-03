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

def plot_weapons():
    shortsword = Dice({6:1})
    greataxe = Dice({12:1})
    greatsword = Dice({6:2})

    shortsword_attack_roll = attack_dmg_pmf(15, 5, shortsword, 3)
    print(shortsword_attack_roll)
    plt.subplot(1, 3, 1)
    plot_drv(shortsword_attack_roll)

    greataxe_attack_roll = attack_dmg_pmf(15, 5, greataxe, 3)
    print(greataxe_attack_roll)
    plt.subplot(1, 3, 2)
    plot_drv(greataxe_attack_roll)

    greatsword_attack_roll = attack_dmg_pmf(15, 5, greatsword, 3)
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

    plot_weapons()

    import pdb; pdb.set_trace()
    print('done')


if __name__ == "__main__":
    main()
