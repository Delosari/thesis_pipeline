import pyneb as pn
import numpy as np

H1 = pn.RecAtom('H', 1)
atom = pn.Atom('O', 3)
T_calc = 16342
ne =145
emis = np.log10(atom.getEmissivity(T_calc, ne, wave=5007, product=False) / H1.getEmissivity(T_calc, ne, wave=4861, product=False))
# emis = atom.getEmissivity(T_calc, ne, wave=5007, product=False) / H1.getEmissivity(T_calc, ne, wave=4861, product=False)
abund = 8.0
red = -0.03336211345166251* 0.11
print emis
print abund
print red
print
fluxes = abund + emis - red - 12
print fluxes

#abund_dict[ions_array[i]] + line_emis - f_lambda * cHbeta_true - 12

# abund + emis_ratio - flambda * cHbeta - 12
#
# abund
# Out[16]: 5.029786740430777
# emis_ratio
# Out[17]: 0.11
# flambda
# Out[18]: -0.03336211345166251
# cHbeta
# Out[19]: 8.05

# import numpy as np
# import pyneb as pn
# import matplotlib.pyplot as plt
# from lib.Astro_Libraries.spectrum_fitting.plot_tools import MCMC_printer
# from lib.Astro_Libraries.spectrum_fitting.gasEmission_functions import EmissivitySurfaceFitter
# from mpl_toolkits.mplot3d import Axes3D
# import os
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as tt
#
#
# ef = EmissivitySurfaceFitter()
# te = tt.matrix('te')
# ne = tt.matrix('ne')
# a = tt.dscalar('a')
# b = tt.dscalar('b')
# c = tt.dscalar('c')
# d = tt.dscalar('d')
# emisHeI = (a + b * ne) * tt.log10(te / 10000.0) - tt.log10(c + d * ne)
# emisHeI_tt = theano.function([te, ne, a, b, c, d], emisHeI)
#
# Te_range = np.linspace(7500, 25000, 20)
# ne_array = np.linspace(0, 500, 20)
# ne_array[0] = 1.0
# X, Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
#
# emisHeI_tt(10000.0)

# import numpy as np
# import pyneb as pn
# import matplotlib.pyplot as plt
# from lib.Astro_Libraries.spectrum_fitting.plot_tools import MCMC_printer
# from lib.Astro_Libraries.spectrum_fitting.gasEmission_functions import EmissivitySurfaceFitter
# from mpl_toolkits.mplot3d import Axes3D
#
# ef = EmissivitySurfaceFitter()
#
# def emisHeI5876(param, a, b, c, d):
#     te, ne = param
#     return (a + b * ne) * np.power(te / 10000.0, c + d * ne)
#
#
# def emisHeI5876_inv(param, a, b, c, d):
#     te, ne = param
#     return np.power(te / 10000.0, c + d * ne) / (a + b * ne)
#
#
# def emisHeI5876_invNew(param, a, b, c, d):
#     te, ne = param
#     return np.power(te / 10000.0, a + b * ne) / (c + d * ne)
#
#
# def emisHeI5876_log(param, a, b, c, d):
#     te, ne = param
#     return (a + b * ne) * np.log10(te / 10000.0) - np.log10(c + d * ne)
#
#
# # Physical conditions
# tem, den = 12000.0, 100.0
# params = (tem, den)
#
# # Pyneb result
# H1 = pn.RecAtom('H', 1)
# He1 = pn.RecAtom('He', 1)
# emis_pn = He1.getEmissivity(tem, den, wave=5876) / H1.getEmissivity(tem, den, wave=4861)
# print 'Pyneb result', emis_pn
#
# # Epm 2017 result
# coeffsHeI5876_epm = np.array([0.745, -5.1e-5, 0.226, -0.0011])
# emis_param = emisHeI5876(params, *coeffsHeI5876_epm)
# print 'Epm 2017 result', 1.0 / emis_param
#
# # Epm 2017 invert result
# coeffsHeI5876_epmArranged = np.array([-0.226, 0.0011, 0.745, -5.1e-5])
# emis_param = emisHeI5876_invNew(params, *coeffsHeI5876_epmArranged)
# print 'Invert Epm 2017', emis_param
#
# # Epm 2017 invert result
# coeffsHeI5876_epmArranged = np.array([-0.226, 0.0011, 0.745, -5.1e-5])
# emis_param = emisHeI5876_log(params, *coeffsHeI5876_epmArranged)
# print 'log Epm 2017', 10 ** emis_param
#
# # Vit result
# coeffsHeI5876_specSynth = ef.epm2017_emisCoeffs['He1_5876A']
# emis_param = ef.ionEmisEq['He1_5876A'](params, *coeffsHeI5876_specSynth)
# print 'SpecSynth', 10 ** emis_param
#
# line_label, line_wave = 'He1_5876A', 5876
# #line_label, line_wave = 'He1_4026A', 4026
# #line_label, line_wave = 'He1_3889A', 3889
# #line_label, line_wave = 'He1_4471A', 4471
# #line_label, line_wave = 'He1_6678A', 6678
# #line_label, line_wave = 'He1_7065A', 7065
# #line_label, line_wave = 'O3_7330A', 7330
# atom = pn.RecAtom('He', 1)
#
# Te_range = np.linspace(7500, 25000, 20)
# ne_array = np.linspace(0, 500, 20)
# ne_array[0] = 1.0
# X, Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
# emisGrid_i = np.log10(atom.getEmissivity(XX, YY, wave=line_wave, product=False) / H1.getEmissivity(XX, YY, wave=4861, product=False))
#
# # print 'Antes', coeffsHeI5876_epmArranged
# # p1, p1_cov = ef.fitEmis(emisHeI5876_invNew, (XX, YY), emisGrid_i, p0 = coeffsHeI5876_epmArranged)
# # print 'Ahora', p1
# # p0_init = ef.epm2017_emisCoeffs[line_label] if line_label in ef.epm2017_emisCoeffs else None
# # p2, p2_cov = ef.fitEmis(emisHeI5876_log, (XX, YY), emisGrid_i, p0 = p0_init)
# # print 'Ahora2', p2
# p0_init = ef.epm2017_emisCoeffs[line_label] if line_label in ef.epm2017_emisCoeffs else None
# line_func = ef.ionEmisEq[line_label]
# p3, p3_cov = ef.fitEmis(line_func, (XX, YY), emisGrid_i, p0 = p0_init)
# print p3
#
# pt = MCMC_printer()
# #pt.emissivitySurfaceFit_2D(line_label, p2, emisGrid_i, emisHeI5876_invNew, (XX, YY))
# #pt.emissivitySurfaceFit_2D(line_label, p2, emisGrid_i, emisHeI5876_log, (XX, YY))
# #pt.emissivitySurfaceFit_3D(line_label, p2, emisGrid_i, emisHeI5876_log, (XX, YY))
# pt.emissivitySurfaceFit_2D(line_label, p3, emisGrid_i, line_func, (XX, YY))
# #pt.emissivitySurfaceFit_3D(line_label, p3, emisGrid_i, line_func, (XX, YY))
#
# plt.show()

# ef = EmissivitySurfaceFitter()
#
# line_label = 'He1_5876A'
# Te_range = np.linspace(7500, 25000, 20)
# ne_array = np.linspace(0, 500, 20)
# ne_array[0] = 1.0
# X, Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
# emisGrid_i = He1.getEmissivity(XX, YY, wave=5876, product=False) / H1.getEmissivity(XX, YY, wave=4861, product=False)
#
# print 'Antes', coeffsHeI5876_epmArranged
# p1, p1_cov = ef.fitEmis(emisHeI5876_invNew, (XX, YY), emisGrid_i, p0 = coeffsHeI5876_epmArranged)
# print 'Ahora', p1
#
# pt = MCMC_printer()
# pt.emissivitySurfaceFit_2D(line_label, p1, emisGrid_i, emisHeI5876_invNew, (XX, YY))
# #pt.emissivitySurfaceFit_3D(line_label, p1, emisGrid_i, emisHeI5876_invNew, (XX, YY))
#
# plt.show()


# pt = MCMC_printer()
#
# Te_range = np.linspace(7500, 25000, 20)
# ne_array = np.linspace(0, 500, 20)
# ne_array[0] = 1.0
# X, Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
#
# line_label = 'He1_5876A'
# emisGrid_i = He1.getEmissivity(XX, YY, wave=5876, product=False) / H1.getEmissivity(XX, YY, wave=4861, product=False)
#
# pt.emissivitySurfaceFit_2D(line_label, coeffsHeI5876_epmArranged, emisGrid_i, emisHeI5876_invNew, (XX, YY))
# pt.emissivitySurfaceFit_3D(line_label, coeffsHeI5876_epmArranged, emisGrid_i, emisHeI5876_invNew, (XX, YY))
#
# plt.show()
