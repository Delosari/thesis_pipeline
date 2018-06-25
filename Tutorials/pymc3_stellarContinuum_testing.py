from os import environ
environ["MKL_THREADING_LAYER"] = "GNU"
import theano.tensor as tt
import pymc3 as pm
import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt
from scipy.integrate import quad

def planck_radiation(wav, T, h, c, k):
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a / ((np.power(wav,5)) * (np.exp(b) - 1.0))
    return intensity

def planck_radiation_tt(wav, T, h, c, k):
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a / ((tt.power(wav,5)) * (tt.exp(b) - 1.0))
    return intensity

def gaussian(wave, A, mu, sig):
    return A * np.exp(-np.power(wave - mu, 2.) / (2 * np.power(sig, 2.)))

# Physical constants
h = 6.626e-34
c = 3.0e+8
k = 1.38e-23

# Observed wavelength range
obs_wave = np.arange(400,500)

# Compute stellar continuum
T_true = 10000.0
continuum_true = planck_radiation(obs_wave * 1e-9, T_true, h, c, k)

# Calculate line true shape and area
A_true, mu_true, sig_true = 1e15, 460, 1
sqrt2pi = np.sqrt((2 * np.pi))
emline_true = gaussian(obs_wave, A_true, mu_true, sig_true)
emLineArea_true = A_true*sig_true*sqrt2pi
emLineArea_err = emLineArea_true * 0.05

# Mask for the line region
idcs_mask = (obs_wave > mu_true-5) & (obs_wave < mu_true+5)
mask = np.ones(obs_wave.size)
mask[idcs_mask] = 0

# Observed flux with noise
err_continuum = np.mean(continuum_true) * 0.05
obs_flux = continuum_true + emline_true + np.random.normal(0, err_continuum, obs_wave.size)

# Observed line area
obs_line_area = simps(obs_flux[idcs_mask], obs_wave[idcs_mask])


# Pymc3 model
with pm.Model() as model:

    temp = pm.Normal('temp', mu=5000.0, sd=1000.0)
    A_norm  = pm.HalfNormal('A_norm', sd=5)
    sig = pm.HalfNormal('sigma', sd=5)
    sig2 = pm.HalfNormal('sigma2', sd=5)

    # Model continuum
    continuum_flux = planck_radiation_tt(obs_wave * 1e-9, temp, h, c, k) * mask

    # Likelihood model continuum (masking the line)
    Y_continuum = pm.Normal('Y_continuum', mu=continuum_flux, sd=err_continuum, observed=obs_flux*mask)

    # Remove from the observation the proposed continuum
    emission_obs = obs_flux - continuum_flux

    # Integrate area under line continuum
    continuum_contribution = simps(continuum_flux[idcs_mask], obs_wave[idcs_mask]) / 1e15

    # Model line area
    line_area = A_norm*sig*sqrt2pi + continuum_contribution

    # Global multivariable likelihood for all lines
    Y_line = pm.Normal('Y_line', mu=line_area, sd=emLineArea_err, observed=obs_line_area)

    for RV in model.basic_RVs:
        print(RV.name, RV.logp(model.test_point))

    # Launch model
    trace = pm.sample(8000, tune=2000)

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