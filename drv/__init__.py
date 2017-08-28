from collections import defaultdict
from fractions import Fraction

class Pmf(defaultdict):
    """pmf is a defaultdict of int to Fraction, mapping values to
    probabilities

    """
    def __init__(self, mapping):
        probability_sum = sum(mapping.values())
        if probability_sum != 1:
            raise ValueError("Pmf sum must be 1; received invalid value {}"
                             .format(probability_sum))
        defaultdict.__init__(self, int, mapping)

class Drv:
    def __init__(self, pmf):
        self._pmf = pmf
    def expected_value(self):
        return sum([value * probability for value, probability in self._pmf.items()])

def die_pmf(n):
    return Pmf({k: Fraction(1,n) for k in range(1, n+1)})

def main():
    pmf = Pmf({1: Fraction(1,2),
               2: Fraction(1,2)})

    import pdb; pdb.set_trace()
    print('done')

if __name__ == "__main__":
    main()
