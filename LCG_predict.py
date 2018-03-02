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
    modulus=findModulus(lcgSequence)
    multiplier=findMultiplier(lcgSequence)
    increment=findIncrement(lcgSequence)
    return modulus,multiplier,increment


def findModulus(lcgSequence):
    modulus=0
    return modulus

def findMultiplier(lcgSequence):
    multiplier=0
    return multiplier

def findIncrement(lcgSequence):
    increment=0
    return increment


def main():
    # MMIX by Donald Knuth
    modulus=2**64
    multiplier=6364136223846793005
    increment=1442695040888963407
    seed=0
    lcgGenerator=LCG(modulus,multiplier,increment,seed)
    # Get n numbers from generator
    n=10
    lcgSequence=[next(lcgGenerator) for _ in range(n)]
    print(lcgSequence)

    #Computed paramters:
    print(crackLCG(lcgSequence))


if __name__ == '__main__':
	main()
