from uncertainties                      import ufloat
from uncertainties.umath                import pow as uma_pow

#Sulfur O/H ratio
logSI_OI_Gradient = ufloat(-1.53, 0.05)                
OI_SI = uma_pow(10, -logSI_OI_Gradient)

HeII_HI = ufloat(0.105926246317, 1.38777878078e-17)

OI_HI  = ufloat(0.000129583794561, 1.354535563e-06)

SI_HI = ufloat(3.58051262182e-06, 8.61374827027e-08)

HeIII_HeII = ufloat(0.000577309209945, 7.63955464343e-05)

HeI_HI = HeII_HI + HeIII_HeII

print 'HeI_HI', HeI_HI
Y_mass_InferenceO = (4 * HeI_HI * (1 - 20 * OI_HI)) / (1 + 4 * HeI_HI)
Y_mass_InferenceS = (4 * HeI_HI * (1 - 20 * OI_SI * SI_HI)) / (1 + 4 * HeI_HI)

print 'este radio', OI_SI.nominal_value
print OI_SI.nominal_value * 3.58051262182e-06, 'comparado con', 0.000129583794561

print 'Via single lines'
print (4 * 0.109697250692 * (1 - 20 * 0.000129583794561)) / (1 + 4 * 0.109697250692)
print (4 * 0.109697250692 * (1 - 20 * 33.8844156139 * 3.58051262182e-06)) / (1 + 4 * 0.109697250692)

print 'Via inference'
print Y_mass_InferenceO
print Y_mass_InferenceS