from os import environ
environ["MKL_THREADING_LAYER"] = "GNU"
import theano
import theano.tensor as tt
import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer
import pymc as pm2

specS = SpectraSynthesizer()

# synth_data = {'spectra_components'      :['emission', 'nebular', 'stellar'],
#               'wavelengh_limits'        :[4200,6900],
#               'resample_inc'            :1,
#               'norm_interval'           :[5100,5150],
#               'input_ions'              :['H1r','He1r','He2r','O2','O3','Ar3','Ar4','S2','S3','N2'],
#               'output_folder'           :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
#               'obs_name'                :'ObsHIIgalaxySynth',
#               'obj_lines_file'          :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objlines.txt',
#               'obj_properties_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_objProperties.txt',
#               'ssp_lib_type'            :'starlight',  # TODO In here we will add "test" for the pip
#               'data_folder'             :'/home/vital/Starlight/Bases/',
#               'data_file'               :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
#               'obj_ssp_coeffs_file'     :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt',
#               'error_stellarContinuum'  :0.01,
#               'error_lines'             :0.02}
#
# specS.gen_synth_obs(**synth_data)

# Import observation
data_address = '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/' + 'ObsHIIgalaxySynth' + '_objParams.txt'
obsData = specS.load_obsData(data_address, 'ObsHIIgalaxySynth')

# Import stellar library data
starlight_ssp = {'ssp_lib_type'         :'starlight',  # TODO In here we will add "test" for the pip
                'data_folder'           :'/home/vital/Starlight/Bases/',
                'data_file'             :'/home/vital/Starlight/Bases/Dani_Bases_Extra_short.txt',
                'wavelengh_limits'      :[4200,6900],
                'resample_inc'          :1,
                'norm_interval'         :[5100, 5150]}

ssp_starlight = specS.load_ssp_library(**starlight_ssp)

# Simulation Data
fit_conf = {'obs_data'                  :obsData,
            'ssp_data'                  :ssp_starlight,
            'output_folder'             :'/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/',
            'spectra_components'        :['emission', 'nebular', 'stellar'],  # ,['emission', 'nebular', 'stellar'],
            'input_lines'               :'all',
            'prefit_ssp'                :False,
            'prefit_data'               :None,
            'wavelengh_limits'          :[4200,6900],
            'resample_inc'              :1,
            'norm_interval'             :[5100,5150]}

# Prepare fit data
specS.prepareSimulation(**fit_conf)
myMask = np.ones( specS.obj_data['flux_norm'].size)
specS.prepareContinuaData(ssp_starlight['wave_resam'], ssp_starlight['flux_norm'],  ssp_starlight['normFlux_coeff'],
                          specS.obj_data['wave_resam'], specS.obj_data['flux_norm'],
                          obsData['continuum_sigma'], myMask,
                          nebularFlux = None, mainPopulationsFile = '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt')

specS.inputContinuumEr = 0.05
err_synth = np.random.normal(0, specS.inputContinuumEr, size=specS.inputContinuum.size)
inputMio = specS.sspPrefitCoeffs.dot(specS.onBasesFluxNorm)
inputMioWitherr = specS.sspPrefitCoeffs.dot(specS.onBasesFluxNorm) + err_synth
weights_list = ['w_i__0','w_i__1','w_i__2','w_i__3','w_i__4']

start_values = dict(zip(weights_list, specS.sspPrefitCoeffs))


print specS.sspPrefitCoeffs
print specS.nBases

basesFlux_tt = theano.shared(specS.onBasesFluxNorm)
with pm.Model() as model:

    w_i = pm.Uniform('w_i', lower=0, upper=5, shape=specS.nBases)
    err = pm.Uniform('err', lower = 0.0, upper = 20.0)
    flux_i = w_i.dot(basesFlux_tt)

    Y = pm.Normal('Y', mu=flux_i, sd=err, observed=inputMio)

    for RV in model.basic_RVs:
        print(RV.name, RV.logp(model.test_point))

    # Launch model
    step = pm.NUTS()
    trace = pm.sample(10000, tune=1000, start=start_values, step=step)

# Output trace data
print pm.summary(trace)
pm.traceplot(trace)
plt.show()


# def model(a_matrix, b_vector):
#     x_coeffs = np.array([pm.Uniform('w__i_%i' % i, 0.0, 5.00) for i in range(specS.nBases)])
#
#     @pm.deterministic(plot=False)
#     def linear_sytem(x_coeffs=x_coeffs, basesSpectra=a_matrix):
#         return x_coeffs.dot(basesSpectra)
#
#     @pm.stochastic(observed=True)
#     def likelihood(value=b_vector, fit_results=linear_sytem, sigma=specS.inputContinuumEr):
#         chiSq = np.sum(np.square(fit_results - value) / np.square(sigma))
#         return - chiSq / 2
#
#     return locals()
#
# # Bayesian
# MDL1 = pm.MCMC(model(specS.onBasesFluxNorm, inputMio))
# MDL1.sample(5000, 1000, 1)
#
# # Compare
# for i in range(specS.sspPrefitCoeffs.size):
#     bayesian_fit_coeff = MDL1.stats()['w__i_' + str(i)]['mean']
#     print specS.sspPrefitCoeffs[i], bayesian_fit_coeff


fig, ax = plt.subplots(1, 1, figsize=(16, 10))
# ax.plot(specS.inputWave, specS.inputContinuum, label='Input object')
ax.plot(specS.inputWave, inputMioWitherr, label='Input object')
ax.plot(specS.inputWave, inputMio, label='my Input object', lineStyle = '--')

# plt.fill_between(specS.inputWave, specS.inputContinuum-specS.inputContinuumEr, specS.inputContinuum+specS.inputContinuumEr, alpha = 0.5)
ax.update({'xlabel': 'Wavelength (nm)', 'ylabel': 'Flux (normalised)'})
ax.legend()
plt.show()



# # Get populations for the stellar continua
# bases_idx, bases_coeff, bases_coeff_err = np.loadtxt('/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/synth_stellarPop.txt', usecols=[0, 1, 2], unpack=True)
#
# inputWave = ssp_starlight['wave_resam']
# inputContinuum = bases_coeff.dot(ssp_starlight['flux_norm'])
# sigma_cont = 0.2
#
# # Pymc3 model
# basesFlux_tt = theano.shared(ssp_starlight['flux_norm'])
# with pm.Model() as model:
#
#     w_i = pm.Uniform('w_i', lower=0, upper=20, shape=bases_coeff.size)
#
#     flux_i = w_i.dot(basesFlux_tt)
#
#     start= pm.find_MAP()
#
#     Y = pm.Normal('Y', mu=flux_i, sd=sigma_cont, observed=inputContinuum)
#
#     for RV in model.basic_RVs:
#         print(RV.name, RV.logp(model.test_point))
#
#     # Launch model
#     trace = pm.sample(10000, tune=5000)

# Output trace data
# print pm.summary(trace)
# pm.traceplot(trace)
# plt.show()

# fig, ax = plt.subplots(1, 1, figsize=(16, 10))
# # ax.plot(specS.inputWave, specS.inputContinuum, label='Input object')
# ax.plot(inputWave, inputContinuum, label='Input object')
# plt.fill_between(inputWave, inputContinuum-sigma_cont, inputContinuum+sigma_cont, alpha = 0.5)
# ax.update({'xlabel': 'Wavelength (nm)', 'ylabel': 'Flux (normalised)'})
# ax.legend()
# plt.show()




# wave_bases = specS.obj_data['wave_resam']

# self.prepareContinuaData()
#
# basesWave, basesFlux, basesFluxCoeffs, obj_WaveObs, obsFlux, obsFluxEr, objMask,
# nebularFlux = None, mainPopulationsFile = self.obj_data['obj_ssp_coeffs_file']):







# from os import environ
# environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as tt
# import pymc3 as pm
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal.signaltools import convolve2d
# from scipy.interpolate.interpolate import interp1d
# from scipy.ndimage import gaussian_filter1d
# from numpy import ceil, max, sum, arange, zeros, exp, square, empty
#
# def convolution_fit3D(sigma, wave, flux):
#
#     # Calculate stellar broadening kernel
#     r_sigma         = sigma / (wave[1] - wave[0])
#
#     # Kernel matrix
#     box             = 2 #np.int64(3 * r_sigma) if np.int64(3 * r_sigma) < 3 else 3
#     kernel_len      = 2 * box + 1
#     kernel          = np.zeros((1, kernel_len))
#     kernel_range    = np.arange(0, 2 * box + 1)
#
#     # Generating gaussian kernel with sigma (the norm factor is the sum of the gaussian)
#     kernel[0, :]    = np.exp(-0.5 * ((np.square(kernel_range - box) / r_sigma)))
#     norm            = np.sum(kernel[0, :])
#     kernel          = kernel / norm
#
#     #Perform convolution
#     flux_convolved  = convolve2d(flux, kernel, mode='same', boundary='symm')
#
#     return flux_convolved
#
# def gaussian_filter1d_ppxf(spec, sig):
#     """
#     Convolve a spectrum by a Gaussian with different sigma for every pixel.
#     If all sigma are the same this routine produces the same output as
#     scipy.ndimage.gaussian_filter1d, except for the border treatment.
#     Here the first/last p pixels are filled with zeros.
#     When creating a template library for SDSS data, this implementation
#     is 60x faster than a naive for loop over pixels.
#
#     :param spec: vector with the spectrum to convolve
#     :param sig: vector of sigma values (in pixels) for every pixel
#     :return: spec convolved with a Gaussian with dispersion sig
#
#     """
#     sig = sig.clip(0.01)  # forces zero sigmas to have 0.01 pixels
#     p = int(np.ceil(np.max(3*sig)))
#     m = 2*p + 1  # kernel size
#     x2 = np.linspace(-p, p, m)**2
#
#     n = spec.size
#     a = np.zeros((m, n))
#     # fig, ax = plt.subplots(1, 1, figsize=(16, 10))
#
#     for j in range(m):   # Loop over the small size of the kernel
#         #print j, n-m+j+1
#         indices = n-m+j+1
#         a[j,:] = spec
#         a[j, p:-p] = spec[j:n-m+j+1]
#         # ax.plot(waveData, a[j,:], label=j)
#
#     # ax.update({'xlabel': 'Wavelength (nm)', 'ylabel': 'Flux (normalised)'})
#     # ax.legend()
#     # plt.show()
#
#     gau = np.exp(-x2[:, None]/(2*sig**2))
#     gau /= np.sum(gau, 0)[None, :]  # Normalize kernel
#
#     conv_spectrum = np.sum(a*gau, 0)
#
#     return conv_spectrum
#
# def gaussian_filter1d_vital(sigma, wave, flux):
#
#     # Kernel matrix
#     box             = int(ceil(max(3*sigma)))
#     kernel_len      = 2 * box + 1
#     kernel          = np.zeros((1, kernel_len))
#     kernel_range    = np.arange(0, 2 * box + 1)
#
#     # Generating gaussian kernel with sigma (the norm factor is the sum of the gaussian)
#     kernel[0, :]    = np.exp(-0.5 * ((np.square(kernel_range - box) / sigma**2)))
#     norm            = np.sum(kernel[0, :])
#     kernel          = kernel / norm
#
#     #Perform convolution
#     flux_convolved  = convolve2d(flux, kernel, mode='same', boundary='symm')
#
#     p = int(np.ceil(np.max(3*sigma)))
#     m = 2*p + 1  # kernel size
#     x2 = np.linspace(-p, p, m)**2
#     n = flux.size
#     a = np.zeros((m, n))
#     for j in range(m):   # Loop over the small size of the kernel
#         a[j, p:-p] = flux[j:n-m+j+1]
#     gau = np.exp(-x2[:, None]/(2*sigma**2))
#     gau /= np.sum(gau, 0)[None, :]  # Normalize kernel
#     myKernel = np.exp(-0.5 * ((np.square(kernel_range - box) / sigma**2)))
#     myKernelN = myKernel / np.sum(myKernel)
#     flux_convolved = convolve2d(np.array([flux]), myKernelN, mode='same', boundary='symm')
#
#     print
#     print 'box', box
#     print 'p', p
#     print
#     print 'kernel (initial)', np.zeros((1, kernel_len)).shape
#     print 'a (initial)', np.zeros((m, n)).shape
#     print
#     print 'kernel_len', kernel_len
#     print 'm', m
#     print
#     print 'kernel_range', kernel_range
#     print 'x2', x2
#     print 'np.square(kernel_range - box)', np.square(kernel_range - box)
#     print
#     print 'x2[:, None]',x2[:, None]
#     print 'np.square(kernel_range - box)', np.square(kernel_range - box)
#     print
#     print 'np.exp(-x2[:, None]/(2*sig**2))', np.exp(-x2[:, None]/(2*sigma**2))
#     print 'np.exp(-0.5 * ((np.square(kernel_range - box) / sigma)))', myKernel
#     print
#     print 'myKernelN', myKernelN
#     print 'gau_N', gau
#     print
#     print 'kernel', kernel
#     print 'gau', gau
#     print
#
#     return flux_convolved
#
# def convolve_dazer(sigma, wave, flux):
#
#     # Kernel matrix
#     box             = int(ceil(max(3*sigma)))
#     kernel_len      = 2 * box + 1
#     kernel_range    = arange(0, 2 * box + 1)
#     kernel          = empty((1, kernel_len))
#
#     # Filling gaussian values (the norm factor is the sum of the gaussian)
#     kernel[0, :]    = exp(-0.5 * (square((kernel_range - box)/sigma)))
#     kernel          /= sum(kernel[0, :])
#
#     #Perform convolution
#     flux_convolved  = convolve2d(flux, kernel, mode='same', boundary='symm')
#
#     return flux_convolved
#
# # Model data
# waveData = np.arange(401, 550, 1)
# fluxData = np.array([1.303, 1.345, 1.3  , 1.352, 1.334, 1.33 , 1.294, 1.269, 1.18 ,
#        0.717, 1.069, 1.22 , 1.237, 1.298, 1.276, 1.283, 1.263, 1.257,
#        1.25 , 1.237, 1.279, 1.273, 1.263, 1.26 , 1.212, 1.21 , 1.208,
#        1.23 , 1.17 , 1.113, 1.125, 1.16 , 1.055, 0.596, 1.045, 1.17 ,
#        1.166, 1.196, 1.143, 1.197, 1.211, 1.205, 1.203, 1.182, 1.194,
#        1.181, 1.147, 1.158, 1.171, 1.19 , 1.21 , 1.178, 1.142, 1.163,
#        1.132, 1.182, 1.148, 1.144, 1.14 , 1.156, 1.166, 1.143, 1.162,
#        1.141, 1.136, 1.164, 1.143, 1.123, 1.151, 1.138, 1.113, 1.136,
#        1.108, 1.125, 1.16 , 1.13 , 1.128, 1.133, 1.109, 1.134, 1.12 ,
#        1.11 , 1.1  , 1.078, 1.002, 0.672, 0.982, 1.061, 1.075, 1.104,
#        1.08 , 1.039, 1.12 , 1.064, 1.093, 1.084, 1.098, 1.078, 1.072,
#        1.041, 1.055, 1.044, 1.064, 0.993, 1.026, 1.04 , 1.053, 1.008,
#        1.078, 1.017, 1.023, 1.036, 1.042, 1.023, 1.031, 1.042, 0.957,
#        1.041, 1.039, 1.022, 1.001, 1.023, 1.031, 1.04 , 1.022, 1.032,
#        0.963, 1.019, 1.033, 0.993, 1.023, 1.004, 0.972, 0.988, 1.013,
#        1.028, 0.977, 1.007, 1.002, 0.985, 0.974, 0.999, 0.955, 1.017,
#        0.999, 0.982, 0.994, 0.962, 0.981])
#
# # Generating synthetic observation
# sigma_star = 0.5
# # fluxConv_fit3D = convolution_fit3D(sigma_star, waveData, np.array([fluxData]))
# # fluxConv_ppxf = gaussian_filter1d_ppxf(fluxData, np.ones(fluxData.size) * sigma_star)
# fluxConv_scipy = gaussian_filter1d(fluxData, sigma_star)
# #fluxConv_vital = gaussian_filter1d_vital(sigma_star, waveData, fluxData)
# fluxConv_vital = convolve_dazer(sigma_star, waveData, np.array([fluxData]))
#
#
#
# # Plot input data
# fig, ax = plt.subplots(1, 1, figsize=(16,10))
# ax.plot(waveData, fluxData, label='Model spectrum')
# # ax.plot(waveData, fluxConv_fit3D[0], label='Fit3D convolution', color = 'tab:green')
# ax.plot(waveData, fluxConv_scipy, label='scipy convolution', color = 'tab:red', linestyle=':')
# # ax.plot(waveData, fluxConv_ppxf, label='ppxf convolution', color = 'tab:orange')
#
# ax.plot(waveData, fluxConv_vital[0], label='vital convolution', color = 'tab:orange')
#
# ax.update({'xlabel':'Wavelength (nm)', 'ylabel':'Flux (normalised)'})
# ax.legend()
# plt.show()





# from os import environ
# environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as tt
# import pymc3 as pm
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate.interpolate import interp1d
#
# # Model data
# waveData = np.arange(401, 550, 1)
# fluxData = np.array([1.303, 1.345, 1.3  , 1.352, 1.334, 1.33 , 1.294, 1.269, 1.18 ,
#        0.717, 1.069, 1.22 , 1.237, 1.298, 1.276, 1.283, 1.263, 1.257,
#        1.25 , 1.237, 1.279, 1.273, 1.263, 1.26 , 1.212, 1.21 , 1.208,
#        1.23 , 1.17 , 1.113, 1.125, 1.16 , 1.055, 0.596, 1.045, 1.17 ,
#        1.166, 1.196, 1.143, 1.197, 1.211, 1.205, 1.203, 1.182, 1.194,
#        1.181, 1.147, 1.158, 1.171, 1.19 , 1.21 , 1.178, 1.142, 1.163,
#        1.132, 1.182, 1.148, 1.144, 1.14 , 1.156, 1.166, 1.143, 1.162,
#        1.141, 1.136, 1.164, 1.143, 1.123, 1.151, 1.138, 1.113, 1.136,
#        1.108, 1.125, 1.16 , 1.13 , 1.128, 1.133, 1.109, 1.134, 1.12 ,
#        1.11 , 1.1  , 1.078, 1.002, 0.672, 0.982, 1.061, 1.075, 1.104,
#        1.08 , 1.039, 1.12 , 1.064, 1.093, 1.084, 1.098, 1.078, 1.072,
#        1.041, 1.055, 1.044, 1.064, 0.993, 1.026, 1.04 , 1.053, 1.008,
#        1.078, 1.017, 1.023, 1.036, 1.042, 1.023, 1.031, 1.042, 0.957,
#        1.041, 1.039, 1.022, 1.001, 1.023, 1.031, 1.04 , 1.022, 1.032,
#        0.963, 1.019, 1.033, 0.993, 1.023, 1.004, 0.972, 0.988, 1.013,
#        1.028, 0.977, 1.007, 1.002, 0.985, 0.974, 0.999, 0.955, 1.017,
#        0.999, 0.982, 0.994, 0.962, 0.981])
#
# # Generating synthetic observation
# z_True = 1.225
# waveObs = np.arange(420, 500, 1) * z_True
# fluxObs = interp1d(waveData, fluxData, bounds_error=True)(np.arange(420, 500, 1))
# sigma_cont = 0.05
#
# # Limits to the redshift
# z_min_ssp = np.around((waveObs[-1] / waveData[-1]), decimals=2)
# z_max_ssp = np.around((waveObs[0] / waveData[0]), decimals=2)
#
# # Declare data tensors
# waveObs_tt = theano.shared(waveData)
# waveData_tt = theano.shared(waveData)
# fluxData_tt = theano.shared(fluxData)
#
# # Pymc3 model
# with pm.Model() as model:
#
#     # Prior redshift
#     z = pm.Uniform('z', lower=z_min_ssp, upper=z_max_ssp)
#
#     # Proposal wavelength
#     wave_i = waveData_tt * z
#
#     # Interpolate model flux at observed wavelength range
#     flux_i = interp1d(wave_i, fluxData_tt, bounds_error=True)(waveObs_tt)
#
#     # Likelihood
#     Y = pm.Normal('Y', mu=flux_i, sd=sigma_cont, observed=fluxObs)
#
#     for RV in model.basic_RVs:
#         print(RV.name, RV.logp(model.test_point))
#
#     # Launch model
#     trace = pm.sample(5000, tune=1000)
#
# # Plot input data
# fig, ax = plt.subplots(1,1)
# ax.plot(waveData, fluxData, label='Model spectrum')
# ax.plot(waveObs, fluxObs, label='Observed spectrum', color = 'tab:green')
# ax.annotate('', xy=(532, 0.6), xytext=(434.0, 0.6),arrowprops=dict(facecolor='black', color='tab:orange', lw=0.5, alpha=1), color='tab:orange')
# ax.annotate('Doppler shift (z)', xy=(532, 0.6), xytext=(465.0, 0.62), arrowprops=dict(facecolor='black', color='tab:orange', lw=0.5, alpha=0), color='tab:orange')
# ax.legend()
# ax.update({'xlabel':'Wavelength (nm)', 'ylabel':'Flux (normalised)'})
# plt.show()



# from os import environ
# environ["MKL_THREADING_LAYER"] = "GNU"
# import theano.tensor as tt
# import pymc3 as pm
# import numpy as np
# from scipy.integrate import simps
# import matplotlib.pyplot as plt
# from scipy.integrate import quad
#
# def planck_radiation(wav, T, h, c, k):
#     a = 2.0*h*c**2
#     b = h*c/(wav*k*T)
#     intensity = a / ((np.power(wav,5)) * (np.exp(b) - 1.0))
#     return intensity
#
# def planck_radiation_tt(wav, T, h, c, k):
#     a = 2.0*h*c**2
#     b = h*c/(wav*k*T)
#     intensity = a / ((tt.power(wav,5)) * (tt.exp(b) - 1.0))
#     return intensity
#
# def gaussian(wave, A, mu, sig):
#     return A * np.exp(-np.power(wave - mu, 2.) / (2 * np.power(sig, 2.)))
#
# # Physical constants
# h = 6.626e-34
# c = 3.0e+8
# k = 1.38e-23
#
# # Observed wavelength range
# obs_wave = np.arange(400,500)
#
# # Compute stellar continuum
# T_true = 10000.0
# continuum_true = planck_radiation(obs_wave * 1e-9, T_true, h, c, k)
#
# # Calculate line true shape and area
# A_true, mu_true, sig_true = 1e15, 460, 1
# sqrt2pi = np.sqrt((2 * np.pi))
# emline_true = gaussian(obs_wave, A_true, mu_true, sig_true)
# emLineArea_true = A_true*sig_true*sqrt2pi
# emLineArea_err = emLineArea_true * 0.05
#
# # Mask for the line region
# idcs_mask = (obs_wave > mu_true-5) & (obs_wave < mu_true+5)
# mask = np.ones(obs_wave.size)
# mask[idcs_mask] = 0
#
# # Observed flux with noise
# err_continuum = np.mean(continuum_true) * 0.05
# obs_flux = continuum_true + emline_true + np.random.normal(0, err_continuum, obs_wave.size)
#
# # Observed line area
# obs_line_area = simps(obs_flux[idcs_mask], obs_wave[idcs_mask])
#
#
# # Pymc3 model
# with pm.Model() as model:
#
#     temp = pm.Normal('temp', mu=5000.0, sd=1000.0)
#     A_norm  = pm.HalfNormal('A_norm', sd=5)
#     sig = pm.HalfNormal('sigma', sd=5)
#     sig2 = pm.HalfNormal('sigma2', sd=5)
#
#     # Model continuum
#     continuum_flux = planck_radiation_tt(obs_wave * 1e-9, temp, h, c, k) * mask
#
#     # Likelihood model continuum (masking the line)
#     Y_continuum = pm.Normal('Y_continuum', mu=continuum_flux, sd=err_continuum, observed=obs_flux*mask)
#
#     # Remove from the observation the proposed continuum
#     emission_obs = obs_flux - continuum_flux
#
#     # Integrate area under line continuum
#     continuum_contribution = simps(continuum_flux[idcs_mask], obs_wave[idcs_mask]) / 1e15
#
#     # Model line area
#     line_area = A_norm*sig*sqrt2pi + continuum_contribution
#
#     # Global multivariable likelihood for all lines
#     Y_line = pm.Normal('Y_line', mu=line_area, sd=emLineArea_err, observed=obs_line_area)
#
#     for RV in model.basic_RVs:
#         print(RV.name, RV.logp(model.test_point))
#
#     # Launch model
#     trace = pm.sample(8000, tune=2000)

# # Output trace data
# print pm.summary(trace)
# pm.traceplot(trace)
# plt.show()
#
# #Plot input data
# fig, ax = plt.subplots(1,1)
# ax.plot(obs_wave, continuum_true)
# ax.plot(obs_wave, obs_flux, color = 'tab:green')
#
# ax.annotate('1st: Fit continuum', xy=(425.0, 3e14), xytext=(400.0, 8e14),
#             arrowprops=dict(facecolor='black', color='tab:blue', lw=0.5), color='tab:blue')
#
# ax.annotate('2nd: Integrate\n area under line', xy=(460.0, 1.2e14), xytext=(415.0, 1.25e14),
#             arrowprops=dict(facecolor='black', color='tab:green', lw=0.5), color='tab:green')
#
# ax.annotate('3rd: Remove from sample\n line area the continnum\n contribution', xy=(460.0, 4.3e14), xytext=(465.0, 8e14),
#             arrowprops=dict(facecolor='black', color='tab:red', lw=0.5), color='tab:red')
#
# ax.fill_between(obs_wave[idcs_mask], continuum_true[idcs_mask], obs_flux[idcs_mask], color='red', alpha=0.5, label='SelectionRegion')
#
# ax.fill_between(obs_wave[idcs_mask], np.zeros(np.sum(idcs_mask)), continuum_true[idcs_mask], color='tab:green', alpha=0.5, label='SelectionRegion')
#
# ax.update({'xlabel':'Wavelength', 'ylabel':'Flux'})
# plt.show()