import numpy as np


class SSC:
    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray):
        (nA, mA) = np.shape(a)
        (nB, mB) = np.shape(b)
        (nC, mC) = np.shape(c)
        (nD, mD) = np.shape(d)
        if nA != mA:
            print('Matrix A should be square')
            exit()
        elif (nB != nA) or (mB > nA) or (nC > nA) or (mC != nA) or (nD != nC) or (mD > mB):
            print('Matrices dimensions must agree')
            exit()
        self.A = a
        self.B = b
        self.C = c
        self.D = d


class SSD:
    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray, sampletime: float):
        (nA, mA) = np.shape(a)
        (nB, mB) = np.shape(a)
        (nC, mC) = np.shape(a)
        (nD, mD) = np.shape(a)
        if nA != mA:
            print('Matrix A should be square')
            exit()
        elif (nB != nA) or (mB > nA) or (nC > nA) or (mC != nA) or (nD != nC) or (mD > mB):
            print('Matrices dimensions must agree')
            exit()
        self.A = a
        self.B = b
        self.C = c
        self.D = d
        self.sampletime = sampletime

class TFC:
    def __init__(self, lsys_num: np.ndarray, lsys_den: np.ndarray):
        if len(np.shape(lsys_num)) == 1 and len(np.shape(lsys_den)) == 1 and len(lsys_num) <= len(lsys_den):
            self.num = lsys_num
            self.den = lsys_den
        else:
            print("Wrong input data")

class TFD:
    def __init__(self, lsys_dnum: np.ndarray, lsys_dden: np.ndarray, sampletime: float):
        if len(np.shape(lsys_dnum)) == 1 and len(np.shape(lsys_dden)) == 1 and len(lsys_dnum) <= len(lsys_dden):
            self.num = lsys_dnum
            self.den = lsys_dden
            self.sampletime = sampletime
        else:
            print("Wrong input data")