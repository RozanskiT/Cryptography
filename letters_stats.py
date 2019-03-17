#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
DESCRIPTION

"""
import numpy as np
import matplotlib.pyplot as plt
def letterStats(fileName):
    freqTable=np.zeros(256)
    with open(fileName,'r') as f:
        readData = f.read()
        #print(readData)
    for ch in readData:
        freqTable[ord(ch)]+=1
    freqTable/=sum(freqTable)
    return freqTable

def main():
    freqTable=letterStats('../letters.txt')
    print(freqTable)
    plt.plot(freqTable)
    plt.show()


if __name__ == '__main__':
	main()
