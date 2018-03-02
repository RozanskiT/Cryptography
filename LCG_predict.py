#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Assignment 1.

Construct and implement an efficient statistical test that predicts (with
non-negligible probability) next bits of linear congruencial generator.
"""

def LCG(modulus,multiplier,increment,seed):
    """
    Linear congruential generator,
    https://en.wikipedia.org/wiki/Linear_congruential_generator
    """
    while True:
        seed=(multiplier*seed+increment)%modulus
        yield seed

def crackLCG(lcgSequence):
    """
    Learned from:
    https://tailcall.net/blog/cracking-randomness-lcgs/
    """
    modulus=findModulus(lcgSequence)
    multiplier=findMultiplier(lcgSequence)
    increment=findIncrement(lcgSequence)
    return modulus,multiplier,increment


def findModulus(lcgSequence):
    from fractions import gcd
    from functools import reduce
    diffs = [s1 - s0 for s0, s1 in zip(lcgSequence, lcgSequence[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return modulus

def findMultiplier(lcgSequence):
    multiplier=0
    return multiplier

def findIncrement(lcgSequence):
    increment=0
    return increment


def main():
    import random
    # MMIX by Donald Knuth
    modulus=2**64
    multiplier=6364136223846793005
    increment=1442695040888963407
    #seed=0
    seed=random.randint(1, modulus)
    lcgGenerator=LCG(modulus,multiplier,increment,seed)
    # Get n numbers from generator
    n=5
    lcgSequence=[next(lcgGenerator) for _ in range(n)]
    #print(lcgSequence)

    #Computed paramters:
    print(crackLCG(lcgSequence))
    #set paramters
    print((modulus,multiplier,increment))


if __name__ == '__main__':
	main()
