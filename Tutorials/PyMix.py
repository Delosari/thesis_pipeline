import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def CurveData():
    x = np.array([3963.67285156,  3964.49560547,  3965.31835938,  3966.14111328,  3966.96362305,
         3967.78637695,  3968.60913086,  3969.43188477,  3970.25463867,  3971.07714844,
         3971.89990234,  3972.72265625,  3973.54541016,  3974.36791992,  3975.19067383])
    y = np.array([1.75001533e-16,   2.15520995e-16,   2.85030769e-16,   4.10072843e-16, 7.17558032e-16,
         1.27759917e-15,   1.57074192e-15,   1.40802933e-15, 1.45038722e-15,  1.55195653e-15,
         1.09280316e-15,   4.96611341e-16, 2.68777266e-16,  1.87075114e-16,   1.64335999e-16])
    return x, y

def FindMaxima(xval, yval):
    xval = np.asarray(xval)
    yval = np.asarray(yval)

    sort_idx = np.argsort(xval)
    yval = yval[sort_idx]
    gradient = np.diff(yval)
    maxima = np.diff((gradient > 0).view(np.int8))
    ListIndeces = np.concatenate((([0],) if gradient[0] < 0 else ()) + (np.where(maxima == -1)[0] + 1,) + (([len(yval)-1],) if gradient[-1] > 0 else ()))
    X_Maxima, Y_Maxima = [], []
        
    for index in ListIndeces:
        X_Maxima.append(xval[index])
        Y_Maxima.append(yval[index])
    
    return X_Maxima, Y_Maxima

def GaussianMixture_Model(p, x, ZeroLevel):
    y = 0.0
    N_Comps = int(len(p) / 3)
    for i in range(N_Comps):
        A, mu, sigma = p[i*3:(i+1)*3]
        y += A * np.exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma))
    Output =  y + ZeroLevel
    return Output

def Residuals_GaussianMixture(p, x, y, ZeroLevel):    
    return GaussianMixture_Model(p, x, ZeroLevel) - y

Wave, Flux  = CurveData()

Wave_Maxima, Flux_Maxima = FindMaxima(Wave, Flux)

EmLines_Number = len(Wave_Maxima)

ContinuumLevel = 1.64191e-16

# Define initial values
p_0 = []
for i in range(EmLines_Number):
    p_0.append(Flux_Maxima[i])
    p_0.append(Wave_Maxima[i])
    p_0.append(2.0)

p1, conv = optimize.leastsq(Residuals_GaussianMixture, p_0[:],args=(Wave, Flux, ContinuumLevel))

Fig    = plt.figure(figsize = (16, 10))  
Axis1  = Fig.add_subplot(111) 

Axis1.plot(Wave, Flux, label='Emission line')
Axis1.plot(Wave, GaussianMixture_Model(p1, Wave, ContinuumLevel), 'r', label='Fit with optimize.leastsq')
print p1
Axis1.plot(Wave, GaussianMixture_Model([p1[0],p1[1],p1[2]], Wave, ContinuumLevel), 'g:', label='Gaussian components')
Axis1.plot(Wave, GaussianMixture_Model([p1[3],p1[4],p1[5]], Wave, ContinuumLevel), 'g:')

Axis1.set_xlabel( r'Wavelength $(\AA)$',)
Axis1.set_ylabel('Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
plt.legend()

plt.show()