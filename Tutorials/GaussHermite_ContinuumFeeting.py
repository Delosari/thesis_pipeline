
# import numpy as np
# import pylab as pl
# from scipy.optimize import minimize
# 
# points = 500
# xlim = 3.
# 
# def f(x,*p):
#     a1,a2,a3,a4,a5 = p
#     x = x.astype(complex) # cast x explicitly to complex, to ensure complex valued f
#     return a1*(x-a2)**a3 * np.exp(-a4 * x**a5)
# 
# # generate noisy data with known coefficients
# p0 = [1.4,-.8,1.1,1.2,2.2]
# x = (np.random.rand(points) * 2. - 1.) * xlim
# x.sort()
# y = f(x,*p0)
# y_noise = y + np.random.randn(points) * .05 + np.random.randn(points) * 1j*.05
# 
# # error function chosen as mean of squared absolutes
# err = lambda p: np.mean(np.abs(f(x,*p)-y_noise)**2)
# 
# # "L-BFGS-B" # this method supports bounds
# 
# # bounded optimization using scipy.minimize
# p_init = [1.,-1.,.5,.5,2.]
# p_opt = minimize(
#     err, # minimize wrt to the noisy data
#     p_init, 
#     bounds=[(None,None),(-1,1),(None,None),(0,None),(None,None)], # set the bounds
#     method="L-BFGS-B").x
# 
# print 'sin x',  minimize( err, p_init, bounds=[(None,None),(-1,1),(None,None),(0,0),(None,None)], method="L-BFGS-B")
# print 'con x', minimize( err, p_init, bounds=[(None,None),(-1,1),(None,None),(0,None),(None,None)], method="L-BFGS-B").x
# 
# # plot everything
# pl.scatter(x, np.real(y_noise), c='b',alpha=.2, label="re(f) + noise")
# pl.scatter(x, np.imag(y_noise), c='r',alpha=.2, label="im(f) + noise")
# 
# pl.plot(x, np.real(y), c='b', lw=1., label="re(f)")
# pl.plot(x, np.imag(y), c='r', lw=1., label="im(f)")
# 
# pl.plot(x, np.real(f(x,*p_opt)) ,'--', c='b', lw=2.5, label="fitted re(f)")
# pl.plot(x, np.imag(f(x,*p_opt)) ,'--', c='r', lw=2.5, label="fitted im(f)")
# 
# pl.xlabel("x")
# pl.ylabel("f(x)")
# 
# pl.legend(loc="best")
# pl.xlim([-xlim*1.01,xlim*1.01])
# 
# pl.show()



import  numpy
from    kapteyn import kmpfit
from    CodeTools.PlottingManager import myPickle
from scipy.interpolate  import interp1d
from scipy.optimize import minimize

def SingleGaussHermit_Continuum(Ind_Variables, A, mu, sigma, skew, kutor):
 
    GHcoeffs = {}
    GHcoeffs['c0'] = numpy.sqrt(6.0) / 4.0
    GHcoeffs['c1'] = -numpy.sqrt(3.0)
    GHcoeffs['c2'] = -numpy.sqrt(6.0)
    GHcoeffs['c3'] = 2.0 * numpy.sqrt(3.0) / 3.0
    GHcoeffs['c4'] = numpy.sqrt(6.0) / 3.0
 
    F = (Ind_Variables[0] - mu) / sigma
 
    E =  A * numpy.exp(-0.5*F*F) * ( 1.0 + skew * F * (GHcoeffs['c3'] * F * F + GHcoeffs['c1']) + kutor *( GHcoeffs['c0'] + F * F * (GHcoeffs['c2'] + GHcoeffs['c4'] * F * F)))
 
    return E + Ind_Variables[1]
 
def residualsGH(p, data):
    # Return weighted residuals of Gauss-Hermite
    x, y, err, zerolevel = data
    return (y-funcGH(p,x,zerolevel)) / err
 
def funcGH(p, x, zerolevel):
    # Model is a Gauss-Hermite function
    A, xo, s, h3, h4 = p
    return gausshermiteh3h4(x, A, xo, s, h3, h4) + zerolevel
 
def gausshermiteh3h4(x, A, x0, s, h3, h4):
    #------------------------------------------------------------
    # The Gauss-Hermite function is a superposition of functions of the form
    # F = (x-xc)/s                                            
    # E =  A.Exp[-1/2.F^2] * {1 + h3[c1.F+c3.F^3] + h4[c5+c2.F^2+c4.F^4]} 
    #------------------------------------------------------------
    c0 =     numpy.sqrt(6.0)/4.0
    c1 =    -numpy.sqrt(3.0)
    c2 =    -numpy.sqrt(6.0)
    c3 = 2.0*numpy.sqrt(3.0)/3.0
    c4 =     numpy.sqrt(6.0)/3.0
     
    F = (x-x0)/s
    E = A*numpy.exp(-0.5*F*F)*( 1.0 + h3*F*(c3*F*F+c1) + h4*(c0+F*F*(c2+c4*F*F)) )
    return E
 
def Residuals_GaussHermite(p, data):
    # Return weighted residuals of Gauss-Hermite
    x_true, y, zerolev, sigma_zerolev = data[0], data[1], data[2], data[3]
    return (y - (SingleGaussHermit_Continuum((x_true, zerolev), p[0], p[1], p[2], p[3], p[4]))) / sigma_zerolev
 
def loadObsData():
     
    xnorm =         numpy.array([ -5.07766641e+00,  -3.38526641e+00,  -1.69286641e+00,  -4.66406250e-04, 1.69193359e+00,   3.38473359e+00,   5.07713359e+00,   6.76953359e+00])
    ynorm =         numpy.array([ 0.13052058,  0.25424442,  0.78959614,  1.,          0.97449845,  0.58909029, 0.24163596,  0.19020805])    
    zero_level =    numpy.array([ 0.16437745,  0.16392456,  0.16347182,  0.16301893,  0.16256604,  0.16211314, 0.16166025,  0.16120736])
    sig_zerolevel = 0.0145931
     
    return xnorm, ynorm, zero_level, sig_zerolevel
 
# pv = myPickle()
# pv.FigFormat_One(ColorConf='Night1')
#  
# GHcoeffs = {}
# GHcoeffs['c0'] = numpy.sqrt(6.0) / 4.0
# GHcoeffs['c1'] = -numpy.sqrt(3.0)
# GHcoeffs['c2'] = -numpy.sqrt(6.0)
# GHcoeffs['c3'] = 2.0 * numpy.sqrt(3.0) / 3.0
# GHcoeffs['c4'] = numpy.sqrt(6.0) / 3.0
#  
# x                       = numpy.linspace(3, 9, 30)
# x_resample              = numpy.linspace(3, 9, 100)
#  
# A1  = 2.18
# X1  = 5.54
# S1  = 0.55
# h31 = -1
# h41                     = 0.0
# zerolevel               = 0.1 * x + 2
# zerolevel_resample      = 0.1 * x_resample + 2
# err                     = numpy.ones(len(x))
#  
# y           = SingleGaussHermit_Continuum((x, zerolevel), A1, X1, S1, h31, h41)
# y           += numpy.random.normal(0.0, 0.05, len(y))
# y_resample  = SingleGaussHermit_Continuum((x_resample, zerolevel_resample), A1, X1, S1, h31, h41)
# 
# pv.DataPloter_One(x_resample, y_resample, LineLabel='Gaussian prediction', LineColor= 'White', LineStyle = '--')
# pv.DataPloter_One(x_resample, zerolevel_resample, LineLabel='Continua', LineColor= 'yellow', LineStyle = '--')
# pv.Labels_Legends_One(Plot_Title = 'Testing Gauss hermit gaussian')
# pv.DisplayFigure()

pv = myPickle()
pv.FigFormat_One(ColorConf='Night1')
 
x, y, zerolevel, err = loadObsData()
x_resample =  numpy.linspace(x[0], x[-1], 100)
Interpolation           = interp1d(x, zerolevel, kind = 'slinear')
zerolevel_resample   = Interpolation(x_resample)
 
#Initial guesses
A_0     = numpy.max(y)
mu_0    = x[numpy.argmax(y)]
sigma_0 = 1
h_31_0  = 0 
h_41_0 = 0
p0 = [A_0, mu_0, sigma_0, h_31_0, h_41_0]
# args_dict = {'data' : (x, y, zerolevel, err)}
#  
# Minimize_Output = minimize(Residuals_GaussHermite(p, ), x0 = p0, args = (args_dict,), bounds=[(None,None),(None,None),(None,None),(None,None),(None,None)], method="L-BFGS-B")
#  
# print Minimize_Output
 
#We try the kapteyn methodology first
fitting_example = kmpfit.Fitter(residuals=residualsGH, data=(x,y,err, zerolevel))
fitting_example.fit(params0=p0)
print 'example prediction'
print fitting_example.params
y_example = funcGH(fitting_example.params, x_resample, zerolevel_resample)
#Then mine
fitobj = kmpfit.Fitter(residuals=Residuals_GaussHermite, data=([x, y, zerolevel, err]))
fitobj.parinfo = [{}, {}, {}, {'Fixed':0}, {'limits':(0,0.00001)}]
fitobj.fit(params0 = p0)
print 'My prediction'
print fitobj.params
y_mine = SingleGaussHermit_Continuum((x_resample, zerolevel_resample), fitobj.params[0], fitobj.params[1], fitobj.params[2], fitobj.params[3], fitobj.params[4])
 
pv.DataPloter_One(x, y, LineLabel="input data", LineColor= pv.Color_Vector[1], LineStyle=None)
# pv.DataPloter_One(x_resample, y_resample, LineLabel='Gauss Hermite curve', LineColor= pv.Color_Vector[2][2])
pv.DataPloter_One(x_resample, y_example, LineLabel='Example prediction', LineColor= 'Orange', LineStyle = ':')
pv.DataPloter_One(x_resample, y_mine, LineLabel='Gaussian prediction', LineColor= 'Red', LineStyle = '--')
pv.DataPloter_One(x_resample, zerolevel_resample, LineLabel='Continua', LineColor= 'yellow', LineStyle = '--')
 
pv.Labels_Legends_One(Plot_Title = 'Testing Gauss hermit gaussian')
pv.DisplayFigure()