from dazer_methods import Dazer
from numpy import log10
dz = Dazer()
dz.load_elements()

dz.S3_atom
S3_abund = 0.5

S3_emis1    = S3_abund * (1 + dz.S3_ratio) * dz.S3_atom.getEmissivity(10000, 100, wave = 9069)
S3_6312     = S3_abund *  dz.S3_atom.getEmissivity(10000, 100, wave = 6312)

Hbeta_emis = dz.H1_atom.getEmissivity(tem=10000, den=100, label = '4_2', product = False)

S3_1 = dz.S3_atom.getIonAbundance(S3_emis1, tem=10000, den=100, to_eval='L(9069)+L(9531)', Hbeta=Hbeta_emis)

S3_emis2 = S3_abund * (1 + dz.S3_ratio) * 0.9 * dz.S3_atom.getEmissivity(10000, 100, wave = 9069)
S3_emis3 = S3_abund * (1 + dz.S3_ratio) * 1.1 * dz.S3_atom.getEmissivity(10000, 100, wave = 9069)

S3_2 = dz.S3_atom.getIonAbundance(S3_emis2, tem=10000, den=100, to_eval='L(9069)+L(9531)', Hbeta=Hbeta_emis)
S3_3 = dz.S3_atom.getIonAbundance(S3_emis3, tem=10000, den=100, to_eval='L(9069)+L(9531)', Hbeta=Hbeta_emis)

S3_4 = dz.S3_atom.getIonAbundance(S3_emis1, tem=10500, den=100, to_eval='L(9069)+L(9531)', Hbeta=Hbeta_emis)
S3_5 = dz.S3_atom.getIonAbundance(S3_emis1, tem=9500, den=100, to_eval='L(9069)+L(9531)', Hbeta=Hbeta_emis)

Temp_predicted = dz.S3_atom.getTemDen(S3_6312/S3_emis1, den=100, to_eval='L(6312)/(L(9069)+L(9531))')

print S3_1
print S3_2, 1-S3_1/S3_2
print S3_3, 1-S3_1/S3_3

print Temp_predicted
print dz.S3_atom.getTemDen(S3_6312/S3_emis2, den=100, to_eval='L(6312)/(L(9069)+L(9531))')
print dz.S3_atom.getTemDen(S3_6312/S3_emis3, den=100, to_eval='L(6312)/(L(9069)+L(9531))')

print log10(S3_1)
print log10(S3_4)
print log10(S3_5)
print log10(S3_1) - log10(S3_4)
print log10(S3_1) - log10(S3_5)



