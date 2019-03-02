import numpy as np
import uncertainties as unc

logSI_OI_Gradient = unc.ufloat(-1.53, 0.05)
OI_SI_un = 1.0 / unc.umath.pow(10, -logSI_OI_Gradient)

print OI_SI_un
# O2_abund = 0.00000648
# O3_abund = 0.00004578
#
# logO2_abund = 12 + np.log10(O2_abund)
# logO3_abund = 12 + np.log10(O3_abund)
#
# print logO2_abund
# print logO3_abund
#
# print 12 + np.log10(O2_abund + O3_abund)
# print logO2_abund + logO3_abund



# from lib.Astro_Libraries.spectrum_fitting.tensor_tools import EmissionTensors
#
# def corO2_7319(emis_ratio, cHbeta, flambda, O2_abund, O3_abund, Te_high):
#     fluxCorr = np.power(10, O2_abund + emis_ratio - flambda * cHbeta - 12) + \
#                np.power(10, O3_abund + 0.9712758487381 + np.log10(np.power(Te_high/10000.0, 0.44)) - flambda * cHbeta - 12)
#
#     return fluxCorr
#
# emisTT = EmissionTensors()
#
# O2_abund = 0.00648
# O3_abund = 0.04578
# logO2abund = 12 + np.log10(O2_abund)
# logO3abund = 12 + np.log10(O3_abund)
# O2_emis = 0.6
# logO2_emis = np.log10(O2_emis)
# cHbeta = 0.12
# flambda = - 0.25
# temp = 12000.0
#
# f_O2 = O2_abund * O2_emis * np.power(10, -cHbeta * flambda)
# flog_O2 = np.power(10, logO2abund + np.log10(O2_emis) - flambda * cHbeta - 12)
#
# f_O2_rec = (O3_abund * 9.36 * np.power(temp/10000.0, 0.44)) * np.power(10, -cHbeta * flambda)
# flog_O2_rec = np.power(10, logO3abund + np.log10(9.36) + np.log10(np.power(temp/10000.0, 0.44)) - flambda * cHbeta - 12)
#
# f_O2_tot = f_O2 + f_O2_rec
#
#
# print f_O2
# print flog_O2
# print
# print f_O2_rec
# print flog_O2_rec
# print
# print f_O2 + f_O2_rec
# print flog_O2 + flog_O2_rec
# print
# print emisTT.emFluxTensors['O2_7319A_b'](np.log10(O2_emis), cHbeta, flambda, logO2abund, logO3abund, temp)
# print corO2_7319(np.log10(O2_emis), cHbeta, flambda, logO2abund, logO3abund, temp)

