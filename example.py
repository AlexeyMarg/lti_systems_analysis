import lsys
import numpy as np

# Continuous state space plant
A = np.array([[0., 1.],
              [-1., -2.]])
B = np.array([[0.],
              [1.]])
C = np.array([[1., 0.]])
D = np.array([[0.]])
plant_ssc = lsys.SSC(A, B, C, D)
# Discrete state space plant
A = np.array([[0.9953, 0.09048],
              [-0.09048, 0.8144]])
B = np.array([ [0.004679],
               [0.09048]])
C = np.array([[1., 0.]])
D = np.array([[0.]])
plant_ssd = lsys.SSD(A, B, C, D, 0.1)
# Continuous transfer function
num = np.array([1.])
den = np.array([1., 2., 1.])
wc = lsys.TFC(num, den)
# Discrete transfer function
num = np.array([0.004679, 0.004377])
den = np.array([1., -1.81, 0.8187])
wd = lsys.TFC(num, den)

