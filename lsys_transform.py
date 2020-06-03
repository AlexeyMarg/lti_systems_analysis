import lsys_types
import numpy as np
import scipy.linalg as la
import sympy as sym


def tf2ss(lsys_tf):
    if not isinstance(lsys_tf, lsys_types.TFC) and not isinstance(lsys_tf, lsys_types.TFD):
        print("Wrong input data")
        raise ValueError
    if lsys_tf.den[0] != 1:
        for i in range(len(lsys_tf.num - 1)):
            lsys_tf.num[i] = lsys_tf.num[i] / lsys_tf.den[0]
        for i in range(len(lsys_tf.den - 1)):
            lsys_tf.num[i] = lsys_tf.num[i] / lsys_tf.den[0]
    n = len(lsys_tf.den)
    m = len(lsys_tf.num)
    A = np.concatenate([np.zeros((n - 2, 1)), np.eye(n - 2, n - 2)], axis=1)
    A = np.concatenate([A, np.zeros((1, n-1))], axis=0)
    for i in range(n - 1):
        A[n - 2, i] = -lsys_tf.den[n-1 - i]
    B = np.zeros((n-1, 1))
    B[n - 2, 0] = 1
    C = np.zeros((1, n-1))
    for i in range(m):
        C[0, i] = lsys_tf.num[m-1-i]
    if isinstance(lsys_tf, lsys_types.TFC):
        return lsys_types.SSC(A, B, C, np.array([[0.]]))
    elif isinstance(lsys_tf, lsys_types.TFD):
        return lsys_types.SSD(A, B, C, np.array([[0.]]), lsys_tf.sampletime)


def ss2tf(sys):
    if isinstance(sys, lsys_types.SSD) or isinstance(sys, lsys_types.SSC):
        s = sym.Symbol('s')
        temp = sym.Matrix(s * np.eye(len(sys.A)) - sys.A)
        temp = sys.C @ temp.inv() @ sys.B
        temp = sym.fraction(sym.simplify(temp[0, 0]))
        num = sym.Poly(temp[0], s).coeffs()
        den = sym.Poly(temp[1], s).coeffs()
        if isinstance(sys, lsys_types.SSD):
            return lsys_types.TFD(np.array(num), np.array(den), sys.sampletime)
        elif isinstance(sys, lsys_types.SSC):
            return lsys_types.TFC(np.array(num), np.array(den))
    else:
        print("Wrong input data")
        raise ValueError


def c2d(sys, T: float):
    if isinstance(sys, lsys_types.SSC):
        A = la.expm(sys.A*T)
        B = la.inv(sys.A) @ (la.expm(sys.A*T) - np.eye(len(sys.A))) @ sys.B
        C = sys.C
        D = sys.D
        return lsys_types.SSD(A, B, C, D, T)
    elif isinstance(sys, lsys_types.TFC):
        plant = tf2ss(sys)
        return c2d(plant, T)
    else:
        print("Wrong input data")
        raise ValueError


def d2c(sys):
    if isinstance(sys, lsys_types.SSD):
        A = la.logm(sys.A) / sys.sampletime
        B = la.inv(la.expm(A*sys.sampletime)-np.eye(len(A))) @ A @ sys.B
        C = sys.C
        D = sys.D
        return lsys_types.SSC(A, B, C, D)
    elif isinstance(sys, lsys_types.TFD):
        plant = tf2ss(sys)
        return d2c(plant)
    else:
        print("Wrong input data")
        raise ValueError
