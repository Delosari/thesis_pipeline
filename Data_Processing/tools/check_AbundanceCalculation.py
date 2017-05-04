import pyneb as pn
from collections import OrderedDict
from timeit import default_timer as timer
from numpy import random, mean, std, zeros, power
from dazer_methods  import Dazer
from pandas import Series
from libraries.Math_Libraries.sigfig import round_sig

def generate_lines_dict(ion, Te, den, param_dict, lines_dict, MC_size = 2, error = 0.05):
 
    lines_matrix = OrderedDict()
    print ion, 'using', param_dict[ion + '_abund']
    abund_dist   = random.normal(param_dict[ion + '_abund'], error * param_dict[ion + '_abund'], MC_size)      
    for line in param_dict[ion + '_lines']:
         
        #Special cases:
        if line == 'O2_3726A':
            line_emiss = zeros(MC_size)
             
            for line_blend in ['O2_3726A', 'O2_3729A']:
                wave_line = float(line_blend[line_blend.find('_')+1:-1])
                emis_line = param_dict[ion + '_atom'].getEmissivity(tem=Te, den=den, wave = wave_line, product = False)
                line_emiss += emis_line
            line_label = line + '+'    
             
        elif line == 'O2_7319A':
            line_emiss = zeros(MC_size)
             
            for line_blend in ['O2_7319A', 'O2_7330A']:
                wave_line = float(line_blend[line_blend.find('_')+1:-1])
                emis_line = param_dict[ion + '_atom'].getEmissivity(tem=Te, den=den, wave = wave_line, product = False)                
                line_emiss += emis_line
                hbeta_flux = dz.H1_atom.getEmissivity(tem=Te, den=den, label = '4_2', product = False)
            recomb_contr = (9.36 * power((Te/10000.0), 0.44)) * hbeta_flux
            line_emiss += recomb_contr 
            line_label = line + '+'    
         
        #Common case 
        else: 
            line_label = line
            wave       = float(line[line.find('_')+1:-1])
            line_emiss = param_dict[ion + '_atom'].getEmissivity(tem=Te, den=den, wave = wave, product = False)
         
        line_flux = abund_dist * line_emiss
        lines_matrix[line_label] = line_flux
     
    lines_dict.update(lines_matrix)
     
    return
 
dz = Dazer()
dz.load_elements()
 
param_dict = {}
param_dict['ne_true']   = 150.0
param_dict['Te_low']    = 12000.0
param_dict['Te_high']   = 14000.0
param_dict['H1_abund']  = 1.0
param_dict['S2_abund']  = 1.2e-6
param_dict['S3_abund']  = 2.4e-6
param_dict['O2_abund']  = 1.2e-5
param_dict['O3_abund']  = 2.4e-5
param_dict['Ar3_abund'] = 2.4e-6
param_dict['Ar4_abund'] = 4.8e-6
param_dict['N2_abund']  = 1.2e-6
param_dict['He2_abund'] = 1.2e-4


param_dict['H1_atom']   = dz.H1_atom
param_dict['H1_lines']  = ['H1_4861A']
param_dict['S2_atom']   = dz.S2_atom
param_dict['S2_lines']  = ['S2_6716A', 'S2_6731A']
param_dict['S3_atom']   = dz.S3_atom
param_dict['S3_lines']  = ['S3_6312A', 'S3_9069A', 'S3_9531A']
param_dict['O2_atom']   = dz.O2_atom
param_dict['O2_lines']  = ['O2_3726A', 'O2_3729A', 'O2_7319A', 'O2_7330A']
param_dict['O3_atom']   = dz.O3_atom
param_dict['O3_lines']  = ['O3_4363A', 'O3_4959A', 'O3_5007A']
param_dict['Ar3_atom']  = dz.Ar3_atom
param_dict['Ar3_lines'] = ['Ar3_7136A', 'Ar3_7751A']
param_dict['Ar4_atom']  = dz.Ar4_atom
param_dict['Ar4_lines'] = ['Ar4_4711A']
param_dict['N2_atom']   = dz.N2_atom
param_dict['N2_lines']  = ['N2_6548A', 'N2_6584A']
param_dict['He2_atom']  = dz.He2_atom
param_dict['He2_lines'] = ['He2_4686A']

dz.lines_dict = OrderedDict()
generate_lines_dict('H1', param_dict['Te_low'], param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
# dz.Hbeta_flux = dz.lines_dict['H1_4861A']
 
generate_lines_dict('Ar3',  param_dict['Te_low'],   param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
generate_lines_dict('Ar4',  param_dict['Te_high'],  param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
generate_lines_dict('S2',   param_dict['Te_low'],   param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
generate_lines_dict('S3',   param_dict['Te_low'],   param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
generate_lines_dict('O2',   param_dict['Te_low'],   param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
generate_lines_dict('O3',   param_dict['Te_high'],  param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
generate_lines_dict('N2',   param_dict['Te_high'],  param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)
generate_lines_dict('He2',  param_dict['Te_high'],  param_dict['ne_true'], param_dict, MC_size=dz.MC_array_len, lines_dict=dz.lines_dict, error = 0.05)

dz.abunData, Data_TestObject = Series(), Series()
Data_TestObject['SIII_lines'] = 'BOTH'
 
dz.determine_electron_parameters(Data_TestObject)
 
dz.argon_abundance_scheme(dz.abunData['TeOIII'],    dz.abunData['TeSIII'],  dz.abunData['neSII'])
dz.sulfur_abundance_scheme(dz.abunData['TeSIII'],   dz.abunData['neSII'],   SIII_lines_to_use = Data_TestObject.SIII_lines)
dz.oxygen_abundance_scheme(dz.abunData['TeOIII'],   dz.abunData['TeSIII'],  dz.abunData['neSII'])
dz.nitrogen_abundance_scheme(dz.abunData['TeOIII'], dz.abunData['neSII'])

for parameter in dz.abunData.index:
    mean_value, std_value = mean(dz.abunData[parameter]), std(dz.abunData[parameter])
    scientfici_not = True if (mean_value < 1e-4) or (mean_value > 1e-5) else False
    print '--', parameter,'\t\t', round_sig(mean_value,5, scientfici_not), ' +/- ', round_sig(std_value, 5, scientfici_not)
    
# dz = Dazer()
# dz.load_elements()
# 
# param_dict = {}
# param_dict['ne_true']   = 150.0
# param_dict['Te_low']    = 12000.0
# param_dict['Te_high']   = 14000.0
# param_dict['Ar3_abund']  = 2.4e-6
# param_dict['Ar4_abund']  = 4.8e-6
# 
# Emis_Hbeta_Tlow = dz.H1_atom.getEmissivity(tem=param_dict['Te_low'], den=param_dict['ne_true'], label = '4_2', product = False)
# Emis_Hbeta_Thigh = dz.H1_atom.getEmissivity(tem=param_dict['Te_high'], den=param_dict['ne_true'], label = '4_2', product = False)
# 
# 
# Ar3_7136A_emis = param_dict['Ar3_abund'] * dz.Ar3_atom.getEmissivity(tem=param_dict['Te_low'], den=param_dict['ne_true'], wave = 7136)
# Ar3_7751A_emis = param_dict['Ar3_abund'] * dz.Ar3_atom.getEmissivity(tem=param_dict['Te_low'], den=param_dict['ne_true'], wave = 7751)
# Ar4_4740A_emis = param_dict['Ar4_abund'] * dz.Ar4_atom.getEmissivity(tem=param_dict['Te_high'], den=param_dict['ne_true'], wave = 4740)
# Ar4_4711A_emis = param_dict['Ar4_abund'] * dz.Ar4_atom.getEmissivity(tem=param_dict['Te_high'], den=param_dict['ne_true'], wave = 4711)
# 
# print dz.Ar3_atom.getIonAbundance(Ar3_7136A_emis, tem=param_dict['Te_low'], den=param_dict['ne_true'], wave = 7136, Hbeta=Emis_Hbeta_Tlow)
# print dz.Ar3_atom.getIonAbundance(Ar3_7751A_emis, tem=param_dict['Te_low'], den=param_dict['ne_true'], wave = 7751, Hbeta=Emis_Hbeta_Tlow)
# print dz.Ar4_atom.getIonAbundance(Ar4_4740A_emis, tem=param_dict['Te_high'], den=param_dict['ne_true'], wave = 4740, Hbeta=Emis_Hbeta_Thigh)
# print dz.Ar4_atom.getIonAbundance(Ar4_4711A_emis, tem=param_dict['Te_high'], den=param_dict['ne_true'], wave = 4711, Hbeta=Emis_Hbeta_Thigh)
# 
# #-New approach
# print 'New approach'
# Ar3_7136A_emis = Ar3_7136A_emis / Emis_Hbeta_Tlow * 100
# Ar3_7751A_emis = Ar3_7751A_emis / Emis_Hbeta_Tlow * 100
# Ar4_4740A_emis = Ar4_4740A_emis / Emis_Hbeta_Thigh * 100
# Ar4_4711A_emis = Ar4_4711A_emis / Emis_Hbeta_Thigh * 100
# 
# print dz.Ar3_atom.getIonAbundance(Ar3_7136A_emis, tem=param_dict['Te_low'], den=param_dict['ne_true'], wave = 7136, Hbeta=100)
# print dz.Ar3_atom.getIonAbundance(Ar3_7751A_emis, tem=param_dict['Te_low'], den=param_dict['ne_true'], wave = 7751, Hbeta=100)
# print dz.Ar4_atom.getIonAbundance(Ar4_4740A_emis, tem=param_dict['Te_high'], den=param_dict['ne_true'], wave = 4740, Hbeta=100)
# print dz.Ar4_atom.getIonAbundance(Ar4_4711A_emis, tem=param_dict['Te_high'], den=param_dict['ne_true'], wave = 4711, Hbeta=100)
#
#
# 
# print S3_9069A_emis/(S3_9069A_emis + S3_9531A_emis)
# print S2_6716A_emis/S2_6731A_emis
#  
# S2_6716A_emis = 2.64827e-15
# S2_6731A_emis = 1.95418e-15
# S3_6312A_emis = 5.05911e-16
# S3_9069A_emis = 5.12795e-15
# S3_9531A_emis = 1.34311e-14
# 
# print S3_9069A_emis/(S3_9069A_emis + S3_9531A_emis)
# print S2_6716A_emis/S2_6731A_emis
#  
# Te_obs,ne_obs = diags.getCrossTemDen(diag_tem = '[SIII] 6312/9200+', 
#                                       diag_den = '[SII] 6731/6716', 
#                                       value_tem = (S3_6312A_emis/(S3_9069A_emis + S3_9531A_emis)), 
#                                       value_den = S2_6731A_emis/S2_6716A_emis) 
#  
# # print 
#  
# print S2_atom.getIonAbundance(S2_6716A_emis, tem=Te_obs, den=ne_obs, wave = 6716, Hbeta=Emis_Hbeta)
# print S2_atom.getIonAbundance(S2_6731A_emis, tem=Te_obs, den=ne_obs, wave = 6731, Hbeta=Emis_Hbeta)
# print S3_atom.getIonAbundance(S3_9069A_emis, tem=Te_obs, den=ne_obs, wave = 9069, Hbeta=Emis_Hbeta)
# print S3_atom.getIonAbundance(S3_9531A_emis, tem=Te_obs, den=ne_obs, wave = 9531, Hbeta=Emis_Hbeta)







