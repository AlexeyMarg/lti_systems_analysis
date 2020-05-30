import lsys
import numpy as np

#       Objects declaration
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
den = np.array([1., 2., 3.])
wc = lsys.TFC(num, den)
# Discrete transfer function
numd = np.array([0.004679, 0.004377])
dend = np.array([1., -1.81, 0.8187])
wd = lsys.TFD(numd, dend, 0.1)

#       Functions examples
# lsys.data()
print('Matrices of continuous plant:\n{}'.format(lsys.data(plant_ssc)))
print('Matrices of discrete plant and sampling time:\n{}'.format(lsys.data(plant_ssd)))
print('Numerator and denominator of continuous plant:\n{}'.format(lsys.data(wc)))
print('Numerator, denominator and sample time of discrete plant:\n{}'.format(lsys.data(wd)))
# poles
print('Poles of continuous plant:\n{}'.format(lsys.poles(plant_ssc)))
print('Poles of discrete plant:\n{}'.format(lsys.poles(plant_ssd)))
print('Poles of continuous transfer function:\n{}'.format(lsys.poles(wc)))
print('Poles of discrete transfer function:\n{}'.format(lsys.poles(wd)))
# controlable
print('Is plant_ssc controlable?\n{}'.format(lsys.controlable(plant_ssc)))
# observable
print('Is plant_ssc observable?\n{}'.format(lsys.observable(plant_ssc)))
# stable
print('Is plant_ssc stable?\n{}'.format(lsys.stable(plant_ssc)))
# transient_time
print('Transient time of plant_ssd is {}'.format(lsys.transient_time(plant_ssd)))
# overshoot
print('Overshoot of wc is {}'.format(lsys.overshoot(wc)))
# oscillation_coef
print('Oscillation coefficient of wc is {}'.format(lsys.oscillation_coef(wc)))
# damping_coef
print('Damping coefficient of wc is {}'.format(lsys.damping_coef(wc)))
# step_response
y = lsys.step_response(plant_ssd)
# plot_step_response
lsys.plot_step_response(wc)
#       Plants transformation
# tf2ss
new_ss = lsys.tf2ss(wd)
print(lsys.data(new_ss))
# ss2tf
new_tf = lsys.ss2tf(plant_ssc)
print(lsys.data(new_tf))
# c2d
new_ss = lsys.c2d(plant_ssc, 0.1)
print(lsys.data(new_ss))
# d2c
new_tf = lsys.d2c(wd)
print(lsys.data(new_tf))


