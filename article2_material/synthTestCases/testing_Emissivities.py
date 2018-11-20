import pyneb as pn
import numpy as np
from lib.Astro_Libraries.spectrum_fitting.extinction_tools import ReddeningLaws

def emisEquation_Te(temp_range, den_range, a, b, c):
    return a + b / (temp_range / 10000.0) + c * np.log10(temp_range / 10000)

O3 = pn.Atom('O', 3)
S3 = pn.Atom('S', 3)
H1 = pn.RecAtom('H', 1)
redFunc = ReddeningLaws()
ne_true = 255.0

Atoms_list = [O3, O3, O3, S3, S3, S3]
temps_list = [14824.15,14824.15,14824.15,14500.0,14500.0,14500.0]
waves_list = [4363, 4959, 5007, 6312, 9069, 9531]
emisCoeffs = np.array([[ 4.93971547, -2.67389618,  0.5704052 ],
                        [ 5.20667399, -1.23030651,  0.60467635],
                        [ 5.68146828, -1.2303065,   0.60467637],
                        [ 5.26198474, -1.64855539,  0.6903541 ],
                        [ 5.4236323,  -0.63216556,  0.64281555],
                        [ 5.81612196, -0.63216556,  0.64281554]])
for i in range(len(Atoms_list)):
    pyneb_measure = Atoms_list[i].getEmissivity(tem=temps_list[i], den=ne_true, wave=waves_list[i])/H1.getEmissivity(tem=temps_list[i], den=ne_true, wave = 4861)
    fit_measure = emisEquation_Te(temps_list[i], ne_true, emisCoeffs[i][0], emisCoeffs[i][1], emisCoeffs[i][2])

    print np.log10(pyneb_measure), fit_measure, (1 - fit_measure/np.log10(pyneb_measure)) * 100

# cHbeta_true = 0.125
# O3_abund_trueLog = 8.05
#
# coeffs =
#
# Odict = {'Te':14824.15, 'ne': 255.0, '4363': np.array([ 4.93971547, -2.67389618,  0.5704052]), 'flambda' : 0.1290772165678573}
# Sdict = {'Te':14500.0, 'ne': 255.0, '6312': np.array([5.26198474, -1.64855539, 0.6903541]), 'flambda' : -0.28123633158905226}
#
#
# O3_abund_true = 10**(O3_abund_trueLog - 12)
#
# waves = np.array([4363, 4959, 5007])
#
# Hbeta_true = H1.getEmissivity(tem=Te_true, den=ne_true, wave = 4861)
# exctinFlambda = redFunc.gasExtincParams(waves,3.4, 'G03 LMC')
#
# # 'S3_6312A': array([5.26198474, -1.64855539, 0.6903541]),
# # 'S3_9069A': array([5.4236323, -0.63216556, 0.64281555]),
# # 'S3_9531A': array([5.81612196, -0.63216556, 0.64281554])}
# # 'O3_4363A': array([4.93971547, -2.67389618, 0.5704052]),
# # 'O3_4959A': array([5.20667399, -1.23030651, 0.60467635]),
# # 'O3_5007A': array([5.68146828, -1.2303065, 0.60467637]),
#
# print np.log10(O3.getEmissivity(tem=Te_true, den=ne_true, wave=waves[0])/Hbeta_true)
# print emisEquation_Te(Te_true, ne_true, 4.93971547, -2.67389618, 0.5704052)
#
# print exctinFlambda
#
# abund + emis_ratio - flambda * cHbeta - 12
#
# for i in range(waves.size):
#     print O3_abund_true * (O3.getEmissivity(tem=Te_true, den=ne_true, wave=waves[i])/Hbeta_true) * 10**(-cHbeta_true * exctinFlambda[i])