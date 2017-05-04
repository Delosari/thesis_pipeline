from dazer_methods  import Dazer
from collections import OrderedDict

#Generate dazer object
dz = Dazer()
dz.load_elements()

Helium_linesNw = OrderedDict()
Helium_linesNw[4471] = 34.0
Helium_linesNw[6678] = 27.0
Helium_linesNw[7065] = 24.0

Helium_linesSe = OrderedDict()
Helium_linesSe[4471] = 38.0
Helium_linesSe[6678] = 30.0
Helium_linesSe[7065] = 25.0

nSII = 100.0
TOIII_nW = 23000.0
TOIII_sE = 19600.0

print 'Vilchez'
for line in Helium_linesNw:
    nwAbund = dz.He1_atom.getIonAbundance(Helium_linesNw[line], tem=TOIII_nW, den=nSII, wave=line, Hbeta=1000)
    seAbund = dz.He1_atom.getIonAbundance(Helium_linesSe[line], tem=TOIII_sE, den=nSII, wave=line, Hbeta=1000)
    print nwAbund, seAbund
    
Helium_linesmioNW = OrderedDict()
Helium_linesmioNW[4471] = 36.96
Helium_linesmioNW[5876] = 89.38
Helium_linesmioNW[6678] = 24.89
Helium_linesmioNW[7065] = 19.45

Helium_linesmioSe = OrderedDict()
Helium_linesmioSe[4471] = 21.96
Helium_linesmioSe[5876] = 65.64
Helium_linesmioSe[6678] = 22.93
Helium_linesmioSe[7065] = 19.44
print 'Vital'

for line in Helium_linesmioNW:
    nwAbund = dz.He1_atom.getIonAbundance(Helium_linesmioNW[line], tem=TOIII_nW, den=nSII, wave=line, Hbeta=1000)
    seAbund = dz.He1_atom.getIonAbundance(Helium_linesmioSe[line], tem=TOIII_sE, den=nSII, wave=line, Hbeta=1000)
    print nwAbund, seAbund