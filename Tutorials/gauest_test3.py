import numpy as np
import matplotlib.pyplot as plt
from kapteyn.profiles import gauest
from scipy import optimize
from kapteyn import kmpfit

def local_maxima(xval, yval):
    xval = np.asarray(xval)
    yval = np.asarray(yval)

    sort_idx = np.argsort(xval)
    yval = yval[sort_idx]
    gradient = np.diff(yval)
    maxima = np.diff((gradient > 0).view(np.int8))
    return np.concatenate((([0],) if gradient[0] < 0 else ()) +
                          (np.where(maxima == -1)[0] + 1,) +
                          (([len(yval)-1],) if gradient[-1] > 0 else ()))

def CurveData():
    x = np.array([3963.67285156,  3964.49560547,  3965.31835938,  3966.14111328,  3966.96362305,
         3967.78637695,  3968.60913086,  3969.43188477,  3970.25463867,  3971.07714844,
         3971.89990234,  3972.72265625,  3973.54541016,  3974.36791992,  3975.19067383])
    y = np.array([1.75001533e-16,   2.15520995e-16,   2.85030769e-16,   4.10072843e-16, 7.17558032e-16,
         1.27759917e-15,   1.57074192e-15,   1.40802933e-15, 1.45038722e-15,  1.55195653e-15,
         1.09280316e-15,   4.96611341e-16, 2.68777266e-16,  1.87075114e-16,   1.64335999e-16])
    return x, y

def CombineGaussiansModel(p, x, ncomp):
    #-----------------------------------------------------------------------
    # This describes the model and its parameters for which we want to find
    # the best fit. 'p' is a sequence of parameters (array/list/tuple).
    #-----------------------------------------------------------------------
    y = 0.0
    zerolev = p[-1]   # Last element
    for i in range(ncomp):
        A, mu, sigma = p[i*3:(i+1)*3]
        y += A * np.exp(-(x-mu)*(x-mu)/(2.0*sigma*sigma))
    return y + zerolev

def Residuals_Kmpfit(p, data):
    #-----------------------------------------------------------------------
    # This function is the function called by the fit routine in kmpfit
    # It returns a weighted residual. De fit routine calculates the
    # square of these values.
    #-----------------------------------------------------------------------
    x, y, err, ncomp = data
    return (y-CombineGaussiansModel(p,x,ncomp)) / err

def model2(p,x):
    A,x1,sig1,B,x2,sig2 = p
    return A*np.exp(-(x-x1)**2/sig1**2) + B*np.exp(-(x-x2)**2/sig2**2)

def res2(p,x,y):
    return model2(p,x) - y

Wave, Flux  = CurveData()

err = 7.5e-18

NumperExpectedlines = 2

# Find maxima
Maxima_Index    =   local_maxima(Wave, Flux)
print 'local maxima', Maxima_Index
    
# A typical simplistic way to fit:

# A, mu, sigma 
A_0, A_1        = Flux[Maxima_Index[0]]/NumperExpectedlines, Flux[Maxima_Index[1]]/NumperExpectedlines
mu_0, mu_1      = Wave[Maxima_Index[0]], Wave[Maxima_Index[1]]
sig_0, sig_1    = Wave[-1] - Wave[0]/2, Wave[-1] - Wave[0]/2
p0_mine         = [A_0, mu_0, 1,  A_1,  mu_1, 1]

#Mduran method
# p0 = [1e-15,3968,2,1e-15,3972,2]
p0 = p0_mine 
p1,conv = optimize.leastsq(res2,p0[:],args=(Wave,Flux))
print 'Output Mduran', p1

p1_mine,conv_mine = optimize.leastsq(res2,p0[:],args=(Wave,Flux))



Fig    = plt.figure(figsize = (16, 10))  
Axis1  = Fig.add_subplot(111) 

Axis1.plot(Wave, Flux, label='Emission line')
# Axis1.plot(Wave, CombineGaussiansModel(fitobj.params,Wave, ncomps), 'b', lw=2, label="Fit with kmpfit")
Axis1.set_xlabel( r'Wavelength $(\AA)$',)
Axis1.set_ylabel('Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$')
# plot(Wave,Flux,'+') # data
#fitted function
Axis1.plot(np.arange(3962,3976,0.1),model2(p1,np.arange(3962,3976,0.1)),'-')


Axis1.plot([Wave[Maxima_Index[0]], Wave[Maxima_Index[1]]],[Flux[Maxima_Index[0]], Flux[Maxima_Index[1]]],'ro')

#Kmpfit method
fitobj = kmpfit.Fitter(residuals=Residuals_Kmpfit, data=(Wave, Flux, err, NumperExpectedlines))
try:
    fitobj.fit(params0=p1)
    Axis1.plot(Wave, CombineGaussiansModel(fitobj.params,Wave,NumperExpectedlines), 'b', lw=2, label="Fit with kmpfit")
except Exception, mes:
    print "Something wrong with fit: ", mes
    raise SystemExit

print 'Los parametros del kmpfit', fitobj.params


plt.show() 