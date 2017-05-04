import  numpy as np
import  matplotlib.pyplot as plt
from    lmfit.models import GaussianModel, ExponentialModel, LinearModel
from    lmfit import Parameters, minimize, report_fit
from    collections import OrderedDict
from    scipy.signal import argrelextrema
from scipy.stats.mstats_basic import skew

def Observational_data():
    
    #Since we know the emision line is Halpha we may declare the their locations
    mu_Emissions = np.array([6548.0, 6563.0, 6584.0])
    
    #Wavelengths marking the blue continuum, line region and red continuum
    Wavelength_regions = np.array([6490.55, 6524.84, 6539.56, 6592.46, 6594.82, 6615.0])

    #Halpha line
    Spectrum = np.array([[ 6478.64 , 8.44735e-17 ],
                        [ 6480.38 , 8.72528e-17 ],
                        [ 6482.11 , 8.64812e-17 ],
                        [ 6483.85 , 8.56387e-17 ],
                        [ 6485.58 , 8.30909e-17 ],
                        [ 6487.32 , 8.13269e-17 ],
                        [ 6489.05 , 7.95901e-17 ],
                        [ 6490.79 , 8.54554e-17 ],
                        [ 6492.52 , 8.04148e-17 ],
                        [ 6494.26 , 7.956e-17 ],
                        [ 6495.99 , 8.30647e-17 ],
                        [ 6497.73 , 7.7904e-17 ],
                        [ 6499.46 , 8.87215e-17 ],
                        [ 6501.2 , 8.64422e-17 ],
                        [ 6502.93 , 8.16061e-17 ],
                        [ 6504.67 , 8.65604e-17 ],
                        [ 6506.4 , 8.31527e-17 ],
                        [ 6508.14 , 8.30319e-17 ],
                        [ 6509.87 , 8.63514e-17 ],
                        [ 6511.61 , 8.71934e-17 ],
                        [ 6513.34 , 9.19315e-17 ],
                        [ 6515.08 , 8.56164e-17 ],
                        [ 6516.81 , 8.59196e-17 ],
                        [ 6518.55 , 9.06681e-17 ],
                        [ 6520.28 , 8.68873e-17 ],
                        [ 6522.02 , 8.20436e-17 ],
                        [ 6523.75 , 8.25962e-17 ],
                        [ 6525.49 , 9.21053e-17 ],
                        [ 6527.22 , 9.26558e-17 ],
                        [ 6528.96 , 9.78202e-17 ],
                        [ 6530.69 , 8.98786e-17 ],
                        [ 6532.43 , 9.69294e-17 ],
                        [ 6534.16 , 9.45276e-17 ],
                        [ 6535.9 , 9.68097e-17 ],
                        [ 6537.63 , 9.49528e-17 ],
                        [ 6539.37 , 9.91305e-17 ],
                        [ 6541.1 , 1.08216e-16 ],
                        [ 6542.84 , 1.29092e-16 ],
                        [ 6544.57 , 2.15399e-16 ],
                        [ 6546.31 , 3.5338e-16 ],
                        [ 6548.04 , 3.83513e-16 ],
                        [ 6549.78 , 2.93025e-16 ],
                        [ 6551.52 , 2.42892e-16 ],
                        [ 6553.25 , 2.6806e-16 ],
                        [ 6554.99 , 4.25984e-16 ],
                        [ 6556.72 , 8.69919e-16 ],
                        [ 6558.46 , 3.12376e-15 ],
                        [ 6560.19 , 1.05061e-14 ],
                        [ 6561.93 , 1.72276e-14 ],
                        [ 6563.66 , 1.45295e-14 ],
                        [ 6565.4 , 7.38004e-15 ],
                        [ 6567.13 , 2.50114e-15 ],
                        [ 6568.87 , 8.43756e-16 ],
                        [ 6570.6 , 3.74166e-16 ],
                        [ 6572.34 , 2.25341e-16 ],
                        [ 6574.07 , 1.77545e-16 ],
                        [ 6575.81 , 1.53118e-16 ],
                        [ 6577.54 , 1.72322e-16 ],
                        [ 6579.28 , 3.17761e-16 ],
                        [ 6581.01 , 7.27118e-16 ],
                        [ 6582.75 , 9.71497e-16 ],
                        [ 6584.48 , 7.37653e-16 ],
                        [ 6586.22 , 4.04425e-16 ],
                        [ 6587.95 , 1.87279e-16 ],
                        [ 6589.69 , 1.24133e-16 ],
                        [ 6591.42 , 1.11212e-16 ],
                        [ 6593.16 , 9.87069e-17 ],
                        [ 6594.89 , 9.51901e-17 ],
                        [ 6596.63 , 8.85843e-17 ],
                        [ 6598.36 , 9.26498e-17 ],
                        [ 6600.1 , 9.4736e-17 ],
                        [ 6601.83 , 8.44449e-17 ],
                        [ 6603.57 , 9.11648e-17 ],
                        [ 6605.3 , 8.95719e-17 ],
                        [ 6607.04 , 8.81881e-17 ],
                        [ 6608.77 , 8.77689e-17 ],
                        [ 6610.51 , 8.31259e-17 ],
                        [ 6612.24 , 8.37382e-17 ],
                        [ 6613.98 , 7.99306e-17 ],
                        [ 6615.71 , 9.14558e-17 ],
                        [ 6617.45 , 8.54267e-17 ]])

    #The method returns the wavelength, flux, and spectrum regions        
    return Spectrum[:,0], Spectrum[:,1], Wavelength_regions, mu_Emissions

def Gaussian_Curve(A, mu, sigma, x, zerolev):
    
    return A * np.exp(-(x-mu)*(x-mu)/(2*sigma*sigma)) + zerolev

def GaussHermit_Curve(A, mu, sigma, skew, kurt, x, zerolev):
    
    c1      =   -np.sqrt(3); 
    c2      =   -np.sqrt(6) 
    c3      =   2/np.sqrt(3) 
    c4      =   np.sqrt(6)/3 
    c5      =   np.sqrt(6)/4    
    
    return A*np.exp(-.5*((x-mu)/sigma)**2)*(1+skew*(c1*((x-mu)/sigma)+c3*((x-mu)/sigma)**3)+kurt*(c5+c2*((x-mu)/sigma)**2+c4*((x-mu)/sigma)**4)) + zerolev

def CompositeModel_zerolev(params, x, zerolev, Ncomps):

    y_model = 0.0
    for i in range(Ncomps):
        index   = str(i + 1)
#         print 'index', index
        A       = params['A' + index].value 
        mu      = params['mu' + index].value 
        sigma   = params['sigma' + index].value 
        y_model       = y_model + A * np.exp(-(x-mu)*(x-mu)/(2*sigma*sigma))
        
    return y_model + zerolev
                       
def CompResid_zerolev(params, x, y, zerolev, Ncomps, err):

    return (CompositeModel_zerolev(params, x, zerolev, Ncomps) - y) / err

def CompResid_zerolev_gh(params, x, y, zerolev, Ncomps, err):

    return (gaussfunc_gh(params, x, zerolev, Ncomps) - y) / err

def Load_lmfit_parameters(N_comps, Initial_guesses_dic, wide_component = False, mu_precission = 1):

    params = Parameters()

    for i in range(N_comps):
        index = str(i + 1)
        print 'we go', i, Initial_guesses_dic['skew'][i], Initial_guesses_dic['skew']
        params.add('A'      + index, value = Initial_guesses_dic['A'][i])
        params.add('mu'     + index, value = Initial_guesses_dic['mu'][i], min = Initial_guesses_dic['mu'][i] - mu_precission, max = Initial_guesses_dic['mu'][i] + mu_precission) #One angstrom tolerance for min and max value of mu
        params.add('sigma'  + index, value = Initial_guesses_dic['sigma'][i], min = Initial_guesses_dic['min_sigma'][i], max = 5.0)
        params.add('skew'   + index, value = Initial_guesses_dic['skew'][i], vary=True)
        params.add('kutor'  + index, value = Initial_guesses_dic['kutor'][i], vary=True)
        
        params.add('fwhm'   + index, expr = '2.354820045 * {sigma}'.format(sigma = 'sigma'  + index))
        params.add('FWHM'   + index, expr = '({fwhm}/{mu}) * 2.99792458e5'.format(fwhm = 'fwhm' + index, mu = 'mu' + index))
        params.add('Flux'   + index, expr = '({A}*{fwhm})/(2.35*0.3989)'.format(A = 'A'  + index, fwhm = 'fwhm' + index))

    #Set all sigmas to the same value
    for i in range(1, N_comps):
        index = str(i + 1)
        params['skew'      + index].expr='skew1'
        params['kutor'      + index].expr='kutor1'
        
    #Set flux in N2_6548A as 1/3 N2_6584A
    params.add('Flux1', expr = 'Flux3 / 3')

    if wide_component:
        index = str(N_comps + 1)
        params.add('A'      + index, value = Initial_guesses_dic['A'][N_comps])
        params.add('mu'     + index, expr = 'mu2')
        params.add('sigma'  + index, value = Initial_guesses_dic['sigma'][N_comps], min = Initial_guesses_dic['min_sigma'][N_comps], max = 8.0)
        params.add('skew'   + index, value = Initial_guesses_dic['skew'][i], vary=True)
        params.add('kutor'  + index, value = Initial_guesses_dic['kutor'][i], vary=True)            
        params.add('fwhm'   + index, expr = '2.354820045 * {sigma}'.format(sigma = 'sigma'  + index))
        params.add('FWHM'   + index, expr = '({fwhm}/{mu}) * 2.99792458e5'.format(fwhm = 'fwhm' + index, mu = 'mu' + index))
        params.add('Flux'   + index, expr = '({A}*{fwhm})/(2.35*0.3989)'.format(A = 'A'  + index, fwhm = 'fwhm' + index))

    return params

def gaussfunc_gh(params, x, zerolev, Ncomps):
    
    y_model = 0.0
    for i in range(Ncomps):
        index   = str(i + 1)    
        amp     =   params['A' + index].value
        center  =   params['mu' + index].value
        sig     =   params['sigma' + index].value
        c1      =   -np.sqrt(3); 
        c2      =   -np.sqrt(6) 
        c3      =   2/np.sqrt(3) 
        c4      =   np.sqrt(6)/3 
        c5      =   np.sqrt(6)/4
        skew    =   params['skew' + index].value
        kurt    =   params['kutor' + index].value
     
        y_model = amp*np.exp(-.5*((x-center)/sig)**2)*(1+skew*(c1*((x-center)/sig)+c3*((x-center)/sig)**3)+kurt*(c5+c2*((x-center)/sig)**2+c4*((x-center)/sig)**4))
        
    return y_model + zerolev

Wavelength, Flux, Spectrum_regions, mu_Emissions = Observational_data()


#Variables to improve the initial guesses
Halpha_Peak             = np.max(Flux)
mu_precission           = 1 #Maximun tolerance on the lines center (Angtroms)

#We stablish the continuum blue and red regions (for the linear component calculation)
#and we stablish the line region (for the gaussian components calculation)
line_region             = (Wavelength >= Spectrum_regions[2]) & (Wavelength <= Spectrum_regions[3])
blue_region, red_region = (Wavelength >= Spectrum_regions[0]) & (Wavelength <= Spectrum_regions[1]), (Wavelength >= Spectrum_regions[4]) & (Wavelength <= Spectrum_regions[5])
line_wave, line_flux    = Wavelength[line_region], Flux[line_region]
blue_wave, blue_flux    = Wavelength[blue_region], Flux[blue_region]
red_wave, red_flux      = Wavelength[red_region], Flux[red_region]

# for local maxima
max_index = argrelextrema(line_flux, np.greater)[0]
peak_fluxes = line_flux[max_index]
peak_waves  = line_wave[max_index]

# for local minima
min_index = argrelextrema(line_flux, np.less)[0]
Minima_fluxes = line_flux[min_index]
Minima_waves  = line_wave[min_index]

# for local minima
min_index = argrelextrema(line_flux, np.less)[0]
Minima_fluxes = line_flux[min_index]
Minima_waves  = line_wave[min_index]

plt.plot(line_wave[max_index], line_flux[max_index], 'o', color = 'purple', label = 'Maxima')
plt.plot(line_wave[min_index], line_flux[min_index], 'o', color = 'orange', label = 'Minima')

#Lmfit parameters
Ncomps = 3
Initial_guesses_dic                     = OrderedDict()
Initial_guesses_dic['A']                = np.array([peak_fluxes[0], peak_fluxes[1], peak_fluxes[2], 4.25e-16])
Initial_guesses_dic['mu']               = np.array([peak_waves[0], peak_waves[1], peak_waves[2], peak_waves[1]])
Initial_guesses_dic['sigma']            = np.array([1.0, 1.0, 1.0, 5.0])
Initial_guesses_dic['skew']             = np.array([0.0, 0.0, 0.0, 0.0])
Initial_guesses_dic['kutor']            = np.array([0.0, 0.0, 0.0, 0.0])


Initial_guesses_dic['min_sigma']        = np.zeros(Ncomps + 1)
Initial_guesses_dic['min_sigma'][-1]    = 5
params = Load_lmfit_parameters(Ncomps, Initial_guesses_dic, wide_component = True, mu_precission = mu_precission)

#Declaring a linear continuum uppon which the line is located
lineal_mod                      = LinearModel(prefix='lineal_')
Continuum_wave, Continuum_flux  = np.hstack([blue_wave, red_wave]), np.hstack([blue_flux, red_flux])
Lineal_parameters               = lineal_mod.guess(Continuum_flux, x=Continuum_wave)
lineal_zerolev                  = Lineal_parameters['lineal_slope'].value * line_wave + Lineal_parameters['lineal_intercept'].value
err_continuum                   = np.std(Lineal_parameters['lineal_slope'].value * Continuum_wave + Lineal_parameters['lineal_intercept'].value - Continuum_flux)
print 'error', err_continuum

#Make the fitting
out = minimize(CompResid_zerolev_gh, params, args=(line_wave, line_flux, lineal_zerolev, Ncomps + 1, err_continuum))
report_fit(out.params)

#Make the plots
x_resample      = np.linspace(line_wave[0], line_wave[-1], 100)
lineal_resample = Lineal_parameters['lineal_slope'].value * x_resample + Lineal_parameters['lineal_intercept'].value
plt.plot(Wavelength, Flux,  '-', color= 'black', label = 'Complete spectrum')
plt.plot(x_resample, CompositeModel_zerolev(out.params, x_resample, lineal_resample, Ncomps + 1), 'r-', label = 'Fitted line')

for i in range(Ncomps + 1):    
    index   = str(i + 1)
    A       = out.params['A' + index].value 
    mu      = out.params['mu' + index].value 
    sigma   = out.params['sigma' + index].value
    skew    = out.params['skew' + index].value
    kurt    = out.params['kutor' + index].value 
    plt.plot(x_resample, GaussHermit_Curve(A, mu, sigma, skew, kurt, x_resample, lineal_resample), '--', color = 'blue', label = 'Components')
    
plt.plot(line_wave, lineal_zerolev, 'g:', label = 'Fitted line')
plt.legend(loc = 'best')

#Display graphs
plt.show()