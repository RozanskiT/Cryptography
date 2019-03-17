#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import hashlib
from Crypto import Random
from Crypto.Random.random import randint
from Crypto.Cipher import AES
import numpy as np
import itertools
"""
DESCRIPTION

"""
class AESCipher(object):
    """
    Implementation of AES cipher from:
    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    -------------------
    """
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8',errors='ignore')


    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class MerklePuzzleCrypto:
    def __init__(self,N=100,difficulty=10,constant="stala"):
        self.N=N
        self.privateKey="My private key"
        self.constant=constant
        self.puzzles=[]
        self.n=difficulty
        #---------------------------
        self.choosenID=None
        self.choosenKey=None
        self.choosenAESCipher=None
        #---------------------------

    #---------------------------------------------------------------------------
    # X
    def createBunchOfPuzzles(self):
        cipher=AESCipher(self.privateKey)
        for i in range(self.N):
            ID=str(cipher.encrypt(str(i)))
            KEY=str(cipher.encrypt(str(ID)))[0:self.n]
            puzzleCipher=AESCipher(KEY)
            ID=puzzleCipher.encrypt(ID)
            KEY=puzzleCipher.encrypt(KEY)
            CONSTANT=puzzleCipher.encrypt(self.constant)
            self.puzzles.append([ID,KEY,CONSTANT])
        #print(self.puzzles)

    def getPuzzles(self):
        return self.puzzles

    def getIDandFindKey(self,ID):
        cipher=AESCipher(self.privateKey)
        self.choosenID=str(ID)
        self.choosenKey=str( cipher.encrypt(self.choosenID) )[0:self.n]
        self.choosenAESCipher=AESCipher(self.choosenKey)

    def decrypt(self,decMessage):
        return self.choosenAESCipher.decrypt(decMessage)


    #---------------------------------------------------------------------------
    # Y
    def chooseRandomPuzzle(self):
        if self.puzzles!=[] and not None:
            i=Random.random.randint(0,self.N-1)
            ID,KEY,CONST=self.puzzles[i]
            #Try all possible keys of length self.readDifficulty
            allPossibleKeys=itertools.product(bytes(range(0,256)),repeat=self.n)
            for key in allPossibleKeys:
                key = ''.join(chr(x) for x in key)
                #print(key)
                if self.constant==AESCipher(key).decrypt(CONST):
                    #print(self.constant,AESCipher(key).decrypt(CONST))
                    #print("FOUND")
                    self.choosenID=AESCipher(key).decrypt(ID)
                    self.choosenKey=AESCipher(key).decrypt(KEY)
                    self.choosenAESCipher=AESCipher(self.choosenKey)
                    #print(len(self.choosenKey))
                    break

    def setPuzzles(self,puzzles):
        self.puzzles=puzzles

    def sendMessage(self,message="Hello world!"):
        return self.choosenAESCipher.encrypt(message)

    def sendID(self):
        return self.choosenID

#-------------------------------------------------------------------------------
def testAESCipher():
    key="Asdhaetdnasgdb#ardfsssssssssscvragfd$"
    message="Ala ma kota"
    cipher=AESCipher(key)
    enc=cipher.encrypt(message)
    print(enc)
    dec=cipher.decrypt(enc)
    print(dec)

def testMerklePuzzleCrypto():
    N=2**10
    MPC_X=MerklePuzzleCrypto(N=N,difficulty=2)
    MPC_Y=MerklePuzzleCrypto()
    #---------------------------------------
    MPC_X.createBunchOfPuzzles()
    #
    print("PUZZLES PREPARED")
    #
    puzzl=MPC_X.getPuzzles()
    const=MPC_X.constant
    n=MPC_X.n

    MPC_Y.constant=const
    MPC_Y.n=n
    MPC_Y.setPuzzles(puzzl)
    print("PUZZLES, CONSTANT AND ORYGINAL KEY LENGTH SEND")

    MPC_Y.chooseRandomPuzzle()
    print("RANDOM PUZZLE SOLVED")
    keyID=MPC_Y.sendID()
    MPC_X.getIDandFindKey(keyID)
    print("COMMUNICATION ESTABLISHED")
    #
    #- Wymieniono klucze, Y może bezpiecznie wysyłać wiadomości do X

    mess1=MPC_Y.sendMessage("Testowa wiadomosc numer jeden")
    # |
    print(MPC_X.decrypt(mess1))

    mess2=MPC_Y.sendMessage("Testowa wiadomosc numer dwa")
    # |
    print(MPC_X.decrypt(mess2))


def main():
    #testAESCipher()
    testMerklePuzzleCrypto()


if __name__ == '__main__':
	main()
