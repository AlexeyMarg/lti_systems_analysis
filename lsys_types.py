import numpy as np


class SSC:
    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray):
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
    def __init__(self, lsys_tf: np.ndarray):
        if len(lsys_tf) == 2 and len(lsys_tf[0]) <= len(lsys_tf[1]):
            self.num = lsys_tf[0]
            self.den = lsys_tf[1]
        else:
            print("Wrong input data")

class TFD:
    def __init__(self, lsys_dtf: np.ndarray, sampletime: float):
        if len(lsys_dtf) == 2 and len(lsys_dtf[0]) <= len(lsys_dtf[1]):
            self.num = lsys_dtf[0]
            self.den = lsys_dtf[1]
            self.sampletime = sampletime
        else:
            print("Wrong input data")