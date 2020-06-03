import math

import matplotlib.pyplot as plt

from lsys_transform import *
from lsys_types import *


def data(lsys):
    if isinstance(lsys, SSC):
        return lsys.A, lsys.B, lsys.C, lsys.D
    elif isinstance(lsys, SSD):
        return lsys.A, lsys.B, lsys.C, lsys.D, lsys.sampletime
    elif isinstance(lsys, TFC):
        return lsys.num, lsys.den
    elif isinstance(lsys, TFD):
        return lsys.num, lsys.den, lsys.sampletime
    else:
        print("Wrong data type")
        raise ValueError


def poles(lsys):
    if isinstance(lsys, SSC) or isinstance(lsys, SSD):
        return np.linalg.eigvals(lsys.A)
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        return np.linalg.eigvals(plant.A)
    else:
        print("Wrong data type")
        raise ValueError


def controlable(lsys):
    if isinstance(lsys, SSC) or isinstance(lsys, SSD):
        U = lsys.B
        for i in range(1, len(lsys.A)):
            temp = np.linalg.matrix_power(lsys.A, i)
            temp = np.dot(temp, lsys.B)
            U = np.concatenate((U, temp), axis=1)
        if np.linalg.matrix_rank(U) == len(lsys.A):
            return True
        else:
            return False
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        controlable(plant)
    else:
        print("Wrong data type")
        raise ValueError


def observable(lsys):
    if isinstance(lsys, SSC) or isinstance(lsys, SSD):
        Q = lsys.C
        for i in range(1, len(lsys.A)):
            temp = np.linalg.matrix_power(lsys.A, i)
            temp = np.dot(lsys.C, temp)
            Q = np.concatenate((Q, temp), axis=0)
        if np.linalg.matrix_rank(Q) == len(lsys.A):
            return True
        else:
            return False
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        observable(plant)
    else:
        print("Wrong data type")
        raise ValueError


def stable(lsys):
    if isinstance(lsys, SSC):
        temp = list(np.linalg.eigvals(lsys.A))
        if temp.count(0) > 1:
            # print('System is unstable')
            return False
        else:
            for i in temp:
                if i.real > 0:
                    # print('System is unstable')
                    return False
            if temp.count(0) == 1:
                # print('System is on the edge of stability')
                return False
            else:
                flag = 0
                for i in temp:
                    if i.real == 0:
                        flag += 1
                if flag > 0:
                    # print('System is on the edge of stability')
                    return False
                else:
                    for i in range(len(temp)):
                        temp[i] = temp[i].real
                    return True
    elif isinstance(lsys, SSD):
        temp = list(np.linalg.eigvals(lsys.A))
        temp2 = [abs(x) for x in temp]
        if (temp.count(1) + temp.count(-1) > 1) or (temp2.count(1) - temp.count(1) - temp.count(-1) > 2):
            # print('System is unstable')
            return False
        else:
            for i in temp2:
                if i > 1:
                    # print('System is unstable')
                    return False
        if temp.count(1) + temp.count(-1) == 1 or temp2.count(1) - temp.count(1) - temp.count(-1) == 2:
            # print('System is on the edge of stability')
            return False
        else:
            return True
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        if stable(plant):
            return True
        else:
            return False
    else:
        # print("Wrong data type")
        raise ValueError


def transient_time(lsys):
    if isinstance(lsys, SSC) or isinstance(lsys, SSD):
        if stable(lsys):
            temp = list(np.linalg.eigvals(lsys.A))
            if isinstance(lsys, SSC):
                for i in range(len(temp)):
                    temp[i] = temp[i].real
                return 3 / abs(min(temp))
            elif isinstance(lsys, SSD):
                for i in range(len(temp) - 1):
                    temp[i] = abs(temp[i])
                return -3 * lsys.sampletime / math.log(max(temp))
        else:
            return None
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        return transient_time(plant)
    else:
        # print("Linear system is not stable or wrong data type")
        raise ValueError


def overshoot(sys):
    if stable(sys):
        y = step_response(sys)
        maxvar = y[0, 1]
        for i in range(1, len(y)):
            if y[i, 1] > maxvar:
                maxvar = y[i, 1]
        var = (maxvar - y[len(y) - 1, 1]) / y[len(y) - 1, 1] * 100
        return var
    else:
        # print("Linear system is unstable")
        return None


def oscillation_coef(lsys):
    if isinstance(lsys, SSC) or isinstance(lsys, SSD):
        if stable(lsys):
            temp = list(np.linalg.eigvals(lsys.A))
            temp_image = []
            temp_real = []
            for i in range(len(temp)):
                temp_image.append(temp[i].imag)
                temp_real.append(temp[i].real)
            beta = temp_image[0]
            pos = 0
            for i in range(len(temp_image)):
                if temp_image[i] > beta:
                    beta = temp_image[i]
                    pos = i
            alpha = abs(temp_real[pos])
            return beta / alpha
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        return oscillation_coef(plant)
    else:
        # print("Wrong data type")
        raise ValueError


def damping_coef(lsys):
    if isinstance(lsys, SSC) or isinstance(lsys, SSD):
        if stable(lsys):
            mu = oscillation_coef(lsys)
            if mu != 0:
                return 1 - math.exp(-2 * math.pi / mu)
            else:
                return None
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        return damping_coef(plant)
    else:
        # print("Wrong data type")
        raise ValueError


def step_response(lsys, step=0.01):
    if isinstance(lsys, SSC):
        if stable(lsys):
            time_max = 2 * transient_time(lsys)
        else:
            time_max = 10.0
        y = np.zeros((1, len(lsys.C)))
        time_array = np.array([[0]])
        for i in range(1, int(time_max / step)):
            time_array = np.concatenate([time_array, np.array([[i * step]])], axis=0)
            temp = la.expm(lsys.A * time_array[i])
            temp = np.dot(temp, np.zeros((len(lsys.A), 1)))
            temp = np.dot(lsys.C, temp)
            temp2 = + la.expm(lsys.A * (step * i)) - np.eye(len(lsys.A))
            temp2 = np.dot(temp2, lsys.B)
            temp2 = np.dot(la.inv(lsys.A), temp2)
            temp2 = np.dot(lsys.C, temp2)
            temp = temp + temp2
            temp = temp + lsys.D
            temp = np.transpose(temp)
            y = np.concatenate([y, temp], axis=0)
    elif isinstance(lsys, SSD):
        if stable(lsys):
            time_max = 2 * transient_time(lsys)
        else:
            time_max = 10.0
        y = np.zeros((1, len(lsys.C)))
        time_array = np.array([[0]])
        for i in range(1, int(time_max / lsys.sampletime)):
            time_array = np.concatenate([time_array, np.array([[i * lsys.sampletime]])], axis=0)
            temp = np.linalg.matrix_power(lsys.A, i)
            temp = np.dot(temp, np.zeros((len(lsys.A), 1)))
            temp = np.dot(lsys.C, temp)
            s = 0
            for j in range(i - 1):
                temp2 = np.linalg.matrix_power(lsys.A, i - j - 1)
                temp2 = np.dot(lsys.C, temp2)
                temp2 = np.dot(temp2, lsys.B)
                s = s + temp2
            temp = temp + s
            temp = temp + lsys.D
            temp = np.transpose(temp)
            y = np.concatenate([y, temp], axis=0)
    elif isinstance(lsys, TFC) or isinstance(lsys, TFD):
        plant = tf2ss(lsys)
        y = step_response(plant)
        return y
    else:
        print("Wrong data type")
        return False
    y = np.concatenate([time_array, y], axis=1)
    return y


def plot_step_response(lsys):
    y = step_response(lsys)
    plt.figure()
    if isinstance(lsys, SSC):
        for i in range(1, len(y[0])):
            plt.plot((y[:, 0]), (y[:, i]))
    else:
        for i in range(1, len(y[0])):
            plt.step((y[:, 0]), (y[:, i]))
    plt.grid(True)
    plt.show()
