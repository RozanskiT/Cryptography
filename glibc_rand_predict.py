#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Assignment 2.
Construct and implement an efficient statistical test that predicts (with
non-negligible probability) next bits of glibc’s random().
---------------------------
for details in glibc check:
    rand.c
    random.c
    random_r.c
    stdlib.h
"""

def glibcPRGN(seed):
    """
    glibc random generator, based on:
    https://www.mathstat.dal.ca/~selinger/random/
    and
    https://github.com/qbx2/python_glibc_random/blob/master/glibc_prng.py
    """
    int32 = lambda x: x&0xffffffff-0x100000000 if x&0xffffffff>0x7fffffff else x&0xffffffff
    int64 = lambda x: x&0xffffffffffffffff-0x10000000000000000 if x&0xffffffffffffffff>0x7fffffffffffffff else x&0xffffffffffffffff

    r = [0] * 34
    r[0] = seed

    for i in range(1, 31):
        r[i] = int32(int64(16807 * r[i-1]) % 0x7fffffff)

        if r[i] < 0:
            r[i] = int32(r[i] + 0x7fffffff)

    for i in range(31, 34):
        r[i] = int32(r[i-31])

    for i in range(34, 344):
        r.pop(0)
        r.append(int32(r[2] + r[30]))

    while True:
        r.pop(0)
        r.append(int32(r[2] + r[30]))
        yield int32((r[-1]&0xffffffff) >> 1)


def crackGlibcRandom(glibcRandomSequence):
    """
    To finish!
    """
    diffs = [(o2, o30,o33) for o2, o30,o33 in zip(glibcRandomSequence[2:], glibcRandomSequence[30:],glibcRandomSequence[33:])]
    print([ o33-(o30+o2)%0x80000000 for o2, o30,o33 in diffs])
    return 0

def getNextGlibcRandom(glibcRandomSequence):
    """
    With 75% gives correct next random
    """
    o1,o2=glibcRandomSequence[-3],glibcRandomSequence[-31]
    return (o1+o2)%0x80000000

def main():
    """
    Test accuracy of predicting next number
    """
    sequenceLength=34
    probability=0
    noTest=10000
    for i in range(noTest):
        rng=glibcPRGN(i)
        glibcRandomSequence=[r for _,r in zip(range(sequenceLength),rng)]
        if(getNextGlibcRandom(glibcRandomSequence)==next(rng)):
            probability+=1
    probability*=100./noTest
    print("Accuracy: ",probability, '%')



if __name__ == '__main__':
	main()
