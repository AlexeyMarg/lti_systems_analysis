import lsys_types
import numpy as np
import scipy.linalg as la
import sympy as sym


def tf2ss(lsys_tf):
    if not isinstance(lsys_tf, lsys_types.TFC) and not isinstance(lsys_tf, lsys_types.TFD):
        print("Wrong input data")
        return
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


def ss2tf(lsys):
    if isinstance(lsys, lsys_types.SSD) or isinstance(lsys, lsys_types.SSC):
        s = sym.Symbol('s')
        temp = sym.Matrix(s * np.eye(len(lsys.A)) - lsys.A)
        temp = lsys.C @ temp.inv() @ lsys.B
        temp = sym.fraction(sym.simplify(temp[0, 0]))
        num = sym.Poly(temp[0], s).coeffs()
        den = sym.Poly(temp[1], s).coeffs()
        if isinstance(lsys, lsys_types.SSD):
            return lsys_types.TFD(np.array([num, den]), lsys.sampletime)
        elif isinstance(lsys, lsys_types.SSC):
            return lsys_types.TFC(np.array([num, den]))
    else:
        print("Wrong input data")
        return


def c2d(lsys, T: float):
    if isinstance(lsys, lsys_types.SSC):
        A = la.expm(lsys.A*T)
        B = la.inv(lsys.A) @ (la.expm(lsys.A*T) - np.eye(len(lsys.A))) @ lsys.B
        C = lsys.C
        D = lsys.D
        return lsys_types.SSD(A, B, C, D, T)
    elif isinstance(lsys, lsys_types.TFC):
        plant = tf2ss(lsys)
        return c2d(plant, T)
    else:
        print("Wrong input data")
        return


def d2c(lsys):
    if isinstance(lsys, lsys_types.SSD):
        A = la.logm(lsys.A) / lsys.sampletime
        B = la.inv(la.expm(A*lsys.sampletime)-np.eye(len(A))) @ A @ lsys.B
        C = lsys.C
        D = lsys.D
        return lsys_types.SSC(A, B, C, D)
    elif isinstance(lsys, lsys_types.TFD):
        plant = tf2ss(lsys)
        return d2c(plant)
    else:
        print("Wrong input data")
        return



