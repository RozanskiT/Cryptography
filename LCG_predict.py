#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np

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
        yield seed
        seed=(multiplier*seed+increment)%modulus


def crackLCG(lcgSequence):
    """
    Learned from:
    https://tailcall.net/blog/cracking-randomness-lcgs/
    """
    modulus=findModulus(lcgSequence)
    multiplier=findMultiplier(lcgSequence, modulus)
    increment=findIncrement(lcgSequence, modulus, multiplier)
    return modulus,multiplier,increment


def findModulus(lcgSequence):
    from fractions import gcd
    from functools import reduce
    diffs = [s1 - s0 for s0, s1 in zip(lcgSequence, lcgSequence[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return modulus

def findMultiplier(lcgSequence, modulus):
    multiplier = (lcgSequence[2] - lcgSequence[1]) * modinv(lcgSequence[1] - lcgSequence[0], modulus) % modulus
    return multiplier

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modinv(b, n):
    g, x, _ = egcd(b, n)
    #if g == 1:
    #    return x % n
    return g * x % n

def findIncrement(lcgSequence, modulus, multiplier):
    return (lcgSequence[1] - lcgSequence[0]*multiplier) % modulus


def testAccuracy(lcgGenerator,numberOfTests,sequenceLength,generatorValues):
    """
    Procedure tests accuracy of finding LCG paramteters
    """
    num=0
    for _ in range(numberOfTests):
        lcgSequence=[next(lcgGenerator) for _ in range(sequenceLength)]
        num+=np.array_equal(generatorValues,crackLCG(lcgSequence))
    return num*100./numberOfTests



def main():
    import random
    # MMIX by Donald Knuth
    modulus=2**64
    multiplier=6364136223846793005
    increment=1442695040888963407
    #seed=10
    seed=random.randint(1, modulus)
    LCGGenerator=LCG(modulus,multiplier,increment,seed)
    # Get n numbers from generator
    sequenceLength=4
    MakeTest=True
    if MakeTest:
        numberOfTests=10000
        print("Accuracy in %i tests is : %5.2f %s"% \
        (numberOfTests, \
        testAccuracy(LCGGenerator,numberOfTests,sequenceLength,(modulus,multiplier,increment)), \
        '%'))
    else:
        #generate sequence
        LCGSequence=[next(LCGGenerator) for _ in range(sequenceLength)]

        #try to compute unknown parameters:
        foundParameters=crackLCG(LCGSequence)
        foundLCGGenerator=LCG(*foundParameters,LCGSequence[0])
        move=[next(foundLCGGenerator) for _ in range(sequenceLength)]

        #compare:
        print('=========================================================')
        print((modulus,multiplier,increment), '\n ?= \n',foundParameters)
        print('=========================================================')
        for _ in range(5):
            print(next(LCGGenerator),' ?= ',next(foundLCGGenerator))

if __name__ == '__main__':
	main()
