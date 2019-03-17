#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
EX 3

"""
import re
import numpy as np

def loadEncryptedMessage(fileName):
    ciphertexts=[]
    with open(fileName,'r') as f:
        readData = f.readlines()
    for line in readData:
        if line[0] =='0' or line[0] =='1':
            line=line[:-2]
            ciphertext=line.split(" ")
            ciphertext=list(map(lambda x: int(x,2),ciphertext))
            ciphertexts.append(ciphertext)
    return ciphertexts

def XOR(L1,L2):
    return [ i^j for (i,j) in zip(L1,L2)]

def listToString(L):
    return ''.join(chr(i) for i in L)

def only_letters(tested_string):
    match = re.match("^[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM ,]*$", tested_string)
    return match is not None

def basic_letters(tested_string):
    match = re.match("^[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM :\- ;,\.!\?']*$", tested_string)
    return match is not None

def extended_letters(tested_string):
    match = re.match("^[qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,;:'!&/ \. \^ \* \+ \? \{ \} \[ \] \\ \| \( \)]*$", tested_string)
    return match is not None

def asciiRange(tested_string):
    for c in tested_string:
        if not (ord(c) >= ord(" ") and ord(c) <= ord("~")):
            return False
    return True


def findKey(ct):
    maxL=max([len(x) for x in ct])
    key=[]
    for n in range(0,maxL-1):
        k=0
        num=0
        potentialKeyElement=[]
        for i in range(0,255):
            a=""
            for c in ct:
                if len(c)> n:
                    a+=chr(c[n]^i)
            if basic_letters(a) and " " in a:
                num+=1
                k=i
                potentialKeyElement.append(i)
        if not num:
            for i in range(0,255):
                a=""
                for c in ct:
                    if len(c)> n:
                        a+=chr(c[n]^i)
                if asciiRange(a) or extended_letters(a):
                    num+=1
                    k=i
                    potentialKeyElement.append(i)
                else:
                    potentialKeyElement.append(0)
        key.append(potentialKeyElement[0])
    return key

def findKey2(ct):
    maxL=max([len(x) for x in ct])
    key=[]
    for n in range(0,maxL-1):
        k=0
        num=0
        goodnessOfKey=np.zeros(256)
        for i in range(0,255):
            for c in ct:
                if len(c)> n:
                    if only_letters(chr(c[n]^i)):
                        goodnessOfKey[i]+=1
        key.append(np.argmax(goodnessOfKey))
    return key


def main():
    ct=loadEncryptedMessage('../lab2.dat')
    ct=ct[0:-1]
    lastct=ct[-1]

    key=[33,234,92,163,27,173,94,76,124,144,120,167,163,180,165,87,99,250,95,125,\
        235,61,48,45,192,230,8,8,221,184,67,107,122,29,117,91,212,72,123,26,10,\
        224,243,89,107,160,52,120,171,100,97,183,6,189,35,114,57,99,124,41,37,\
        175,182,206,106,6,85,84,246,83,36,89,90,207,90,37,64,193,184,156,77,42,\
        200,142,43,87,219,42,225,26,187,18,245,63,249,44,62,136,231,216,23,197,\
        81,169,221,114,6,222,130,14,190,20,180,241,60,47,108,219,35,0,99,98,43,\
        208,26,105,85,57,80,157,84,52,151,25,121,228,19,54,107,150,250,11,196,\
        236,89,199,75,88,125,59,237,64,219,156,164,23,158,144,196,113,201,107,\
        176,167,203,23,2,112,135,32,48,227,83,136,194,160,20,52]

    if True:
        bestAutoKey=findKey2(ct)
    else:
        bestAutoKey=findKey(ct)

    if False:
        for i,c in enumerate(ct):
            print("\n\n\n",i, "\n")
            text=XOR(c,key)
            print(listToString(text))
    if False:
        for i,c in enumerate(ct):
            print("\n\n",i, "\n")
            text=XOR(c,bestAutoKey)
            print(listToString(text))

    if True:
        print("\n\nLAST Cipher text: ")
        text=XOR(lastct,key)
        print(listToString(text))
        print("\n\n--------------------------------------------------------------------")
        print("KEY:")
        print(listToString(key))

    else:
        print("\n\nLAST Cipher text: ")
        text=XOR(lastct,bestAutoKey)
        print(listToString(text))
        print("\n\n--------------------------------------------------------------------")
        print("KEY:")
        print(listToString(bestAutoKey))

if __name__ == '__main__':
	main()
