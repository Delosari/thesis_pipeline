'''
Created on Jan 29, 2016

@author: vital
'''
import math
import numpy as np
import matplotlib.pyplot as plt
import pyneb as pn

H1 = pn.RecAtom('H', 1)
O2 = pn.Atom('O', 2)
# O3 = pn.Atom('O', 3)
# N2 = pn.Atom('N', 2)
# S2 = pn.Atom('S', 2)
# Ar = pn.Atom('Ar', 2)
# Ar3 = pn.Atom('Ar', 3)

O2_abund = 0.03

tem = 11800
den = 100

O2_3726A    = O2.getEmissivity(tem, den, wave = 3726) * O2_abund
O2_3729A    = O2.getEmissivity(tem, den, wave = 3729) * O2_abund
O2_7319A    = O2.getEmissivity(tem, den, wave = 7319) * O2_abund
O2_7330A    = O2.getEmissivity(tem, den, wave = 7330) * O2_abund
Hbeta_flux  = H1.getEmissivity(tem, den, label = '4_2')

Abund_bothA = O2.getIonAbundance(O2_3726A, tem, den, wave = 3726, Hbeta = Hbeta_flux)
Abund_bothB = O2.getIonAbundance(O2_3729A, tem, den, wave = 3729, Hbeta = Hbeta_flux)
Abund_bothC = O2.getIonAbundance(O2_7319A, tem, den, wave = 7319, Hbeta = Hbeta_flux)
Abund_bothD = O2.getIonAbundance(O2_7330A, tem, den, wave = 7330, Hbeta = Hbeta_flux)
Abund_bothCD = O2.getIonAbundance(O2_7319A+O2_7330A, tem, den,  to_eval = 'L(7319)+L(7330)', Hbeta = Hbeta_flux)

print Abund_bothA
print Abund_bothB
print Abund_bothC
print Abund_bothD
print Abund_bothCD

print O2.getIonAbundance(54.68, 11800, 119,  to_eval = 'L(7319)+L(7330)',       Hbeta = 1000)
print O2.getIonAbundance(54.68/1000, tem=tem, den=den,  to_eval = 'L(7319)+L(7330)',  Hbeta = 1)
print O2.getIonAbundance(54.68/1000, tem=tem, den=den,  to_eval = 'L(7319)+L(7330)',   Hbeta = 1)
print O2.getIonAbundance(54.68/1000, tem=tem, den=den,  to_eval = 'L(7319)+L(7330)',   Hbeta = 1)



# O2_abund = 0.1
# Hbeta_flux  = H1.getEmissivity(10000, 100, label = '4_2')
# O2_3726A    = O2.getEmissivity(10000, 100, wave = 3726) * O2_abund
# O2_3729A    = O2.getEmissivity(10000, 100, wave = 3729) * O2_abund
# 
# Abund_bothA = O2.getIonAbundance(O2_3726A, 10000, 100, wave = 3726, Hbeta = Hbeta_flux)
# Abund_bothB = O2.getIonAbundance(O2_3729A, 10000, 100, wave = 3729, Hbeta = Hbeta_flux)
# Abund_both  = O2.getIonAbundance(O2_3726A + O2_3729A, 10000, 100, to_eval = 'L(3726)+L(3729)', Hbeta = Hbeta_flux)
# 
# print 'O2 abundance A', Abund_bothA
# print 'O2 abundance B', Abund_bothB
# print 'O2 abundance both lines', Abund_both
# 
# 
# Ar_Abund        = 0.2 
# Ar3_7136A       = Ar3.getEmissivity(10000, 100, wave = 7136) * Ar_Abund
# Ar3_7751A       = Ar3.getEmissivity(10000, 100, wave = 7751) * Ar_Abund
# 
# Abund_bothA         = Ar3.getIonAbundance(Ar3_7136A, 10000, 100, wave = 7136, Hbeta = Hbeta_flux)
# Abund_bothB         = Ar3.getIonAbundance(Ar3_7751A, 10000, 100, wave = 7751, Hbeta = Hbeta_flux)
# Abund_both          = Ar3.getIonAbundance(Ar3_7136A + Ar3_7751A, 10000, 100, to_eval = 'L(7751)+L(7136)', Hbeta = Hbeta_flux)
# Abund_both_Divid    = Ar3.getIonAbundance(Ar3_7751A / Ar3_7136A, 10000, 100, to_eval = 'L(7751)/L(7136)', Hbeta = Hbeta_flux)
# 
# print 'Ar3 abundance A', Abund_bothA
# print 'Ar3 abundance B', Abund_bothB
# print 'Ar3 abundance both lines', Abund_both
# print 'Ar3 abundance divide lines', Abund_both_Divid

# #print O2,O3,N2,S2
# 
# diags   = pn.Diagnostics()
# Temp    = N2.getTemDen(0.02, den=444., to_eval = 'L(5755) / L(6548)')
# den         = S2.getTemDen(1.0, tem = 14000, to_eval = 'L(6731) / L(6716)') 
# Temp_Den = diags.getCrossTemDen(diag_tem='[NII] 5755/6548', diag_den='[SII] 6731/6716', value_tem=[0.02, 0.02], value_den=[1.0, 1.0])
# 
# 
# Ar_Abund        = 0.1 
# Ar3_7136A       = Ar3.getEmissivity(10000, 100, wave = 7136) * Ar_Abund
# Ar3_7751A       = Ar3.getEmissivity(10000, 100, wave = 7751) * Ar_Abund
# Hbeta           = H1.getEmissivity(tem=10000, den=100, wave=4861)
# Ar3_Meas_abund  = Ar3.getIonAbundance(int_ratio = Ar3_7751A / Hbeta, tem=10000, den=100, wave = 7136, Hbeta = 1)
# 
# print Ar3_Meas_abund
# 
# 
# 
# 
# 
# # TSIII_pn, nSII_pn = diags.getCrossTemDen(diag_tem = '[SIII] 6312/9200+',
# #                                          diag_den = '[SII] 6731/6716',
# #                                          value_tem = 0.2,
# #                                          value_den = 1) 
# # 
# # 
# # print 'Temp', Temp
# # print Temp_Den
# # print 'Density', den
# # 
# #                     
# # EmLine_List                 = ['R_SII_pn', 'R_SIIprime_pn', 'R_SIII_pn', 'R_NII_pn', 'R_OII_pn', 'R_OIII_pn']
# # Den_List                    = ['nSII_pn']
# # Temp_List                   = ['TOIII_pn', 'TOII_pn', 'TSII_pn', 'TSIII_pn','TNII_pn', 'TOII_approxfrom_TOIII_pn', 'TSIII_approxfrom_TOIII_pn', 'TOIII_approxfrom_TSIII_pn', 'TNII_approxfrom_TOIII_pn']
# # IonicAbund_List             = ['SII_HII_pn', 'SIII_HII_pn', 'SIV_HII_pn', 'OII_HII_pn', 'OII_HII_3279A_pn', 'OII_HII_7319A_pn', 'NII_HII_pn', 'HeII_HII_pn', 'HeIII_HII_pn', 'ArIII_HII_pn', 'ArIV_HII_pn']
# # Element_List                = ['SI_HI_pn', 'SI_HI_ArCorr_pn', 'OI_HI_pn', 'NI_OI_pn', 'NI_HI_pn', 'HeI_HI_pn']
# #     
# # Properties_dict        = dict.fromkeys(Element_List + IonicAbund_List + Den_List + Temp_List + EmLine_List)
# # 
# # print type(Properties_dict['R_SII_pn']) == type(None)
# # 
# # if Properties_dict.viewkeys() >= {'R_SII_pn', 'R_SIIprime_pn', 'coso', 'R_SIII_pn'}:
# #     print 'All in dict2'
# # else:
# #     print 'Not all in dict2'
# # 
# # if all (line in Properties_dict for line in ('R_SII_pn', 'R_SIIprime_pn', 'coso', 'R_SIII_pn')):
# #     print 'All in dict'
# # else:
# #     print 'Not all in dict '
# # 
# # if ('R_SII_pn' and 'R_SIIprime_pn' and 'R_SIII_pn' and 'coso') in Properties_dict:
# #     print 'bien jodido'
# # else:
# #     print 'Otro fallo'
# # 
# # if np.array([1,2,3,4]) is not None:
# #     print 'No lo es'
# 
# 
# H1 = pn.RecAtom('H', 1)
# 
# Halpha_emissivity = H1.getEmissivity(tem=10000, den=100, wave = 6563)
# 
# HPas8 = H1.getEmissivity(tem=10000, den=100, wave = 9545.969)
# HPas7 = H1.getEmissivity(tem=10000, den=100, wave = 9229.014)
# 
# print 'Hpas8', Halpha_emissivity/HPas8
# print 'Hpas7', Halpha_emissivity/HPas7
