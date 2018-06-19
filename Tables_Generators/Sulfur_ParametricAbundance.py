from numpy                               import linspace, ones, log10, power
from collections                         import OrderedDict
from scipy.optimize                      import minimize, curve_fit, leastsq
# from Plotting_Libraries.dazer_plotter    import Plot_Conf
import pyneb as pn

def Emissivity_parametrization(Temp_Range, A, B, C):
        
    return 12 + A + B/Temp_Range + C * log10(Temp_Range)

def Fitting_Emissivity(Temp_Range, PyNeb_Emissivity,  A, B, C):
    
    p_1, conv_curFit = curve_fit(Emissivity_parametrization, Temp_Range, PyNeb_Emissivity, [A, B, C])
    
    return p_1, conv_curFit

def He_Emissivity_parametrization(Temp_Range, A, B):
        
    return A * power(Temp_Range,B)

def He_Fitting_Emissivity(Temp_Range, PyNeb_Emissivity,  A, B):
    
    p_1, conv_curFit = curve_fit(He_Emissivity_parametrization, Temp_Range, PyNeb_Emissivity, [A, B])
    
    return p_1, conv_curFit

def Emissivity_parametrization_backup(Temp_Range, A, B, C):
        
    return 12 + A + B/Temp_Range + C * log10(Temp_Range)


# # SULFUR III 9069--------------------------------
#
# A_0 = -6.5768
# B_0 = - 0.6293
# C_0 = + 0.6463
#
# #Declare Classes
# dz = Plot_Conf()
#
# #Define figure format
# dz.FigConf()
#
# print 'Tell me the files', pn.atomicData.getAllAvailableFiles('S4')
#
# #Line codes to solve the slow pyneb issue
# pn.atomicData.setDataFile('h_i_rec_SH95.hdf5', 'H1', 'rec')
# pn.atomicData.setDataFile('he_ii_rec_SH95.hdf5', 'He2', 'rec')
#
# #Change atomic data for Sulfur
# # pn.atomicData.includeFitsPath()
# pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
#
# #Atom creation and definition of physical conditions
# HI = pn.RecAtom('H', 1)
# S4 = pn.Atom('S', 4)
# He = pn.RecAtom('He',1)
# # print 'S4 sources', S4.printSources()
#
# #Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = '4_2'
# Wave_dict['S3_10.5m']   = 105000
#
# #Define physical conditions
# tem         = 10000
# tem_range   = linspace(5000, 25000, 1000)
# den         = 100
#
# #Emissivities ranges
# Hbeta_emis    = HI.getEmissivity(tem = tem_range, den = den, label = Wave_dict['Hbeta'])
# S4_105m_emis  = S4.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['S3_10.5m'])
# t4_range      = tem_range/10000
#
# #Plotting Pyneb Emis vs Temp
# S4_emis_vector_pyneb    = log10((S4_105m_emis)/Hbeta_emis)
# dz.data_plot(tem_range, S4_emis_vector_pyneb, label='PyNeb value: S4')
#
# #Fitting characteristics
# p_1, conv_curFit = Fitting_Emissivity(t4_range, S4_emis_vector_pyneb, A_0, B_0, C_0)
#
# print 'Initial values', A_0, B_0, C_0
# print 'Guessed values', p_1
#
# #New fitting values
# Vit_Emis = p_1[0] + p_1[1]/t4_range + p_1[2] * log10(t4_range)
# dz.data_plot(tem_range, Vit_Emis, label='Vital fitting')
#
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'$log\left(\frac{E_{\left[SIII\right]9069}}{E_{H\beta}}\right)$'
# title   = r'Sulfur emissivity comparison: 9069$\AA$ line, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)
#
# A_1 = p_1[0]
# B_1 = p_1[1]
# C_1 = p_1[2]
#
# formula = r"$12+log\left(\frac{S^{+3}}{H^{+}}\right)=log\left(\frac{I\left(10.5m\right)}{I\left(H\beta\right)}\right)+"+str(round(A_1*-1,4))+r"+\frac{"+str(round(B_1*-1,4))+r"}{t_{e}}"+str(round(C_1*-1,4))+r"\cdot log\left(t_{e}\right)$"
# # print 'The formula is'
# # print formula
#
# dz.Axis.text(0.15, 0.30, formula, transform=dz.Axis.transAxes, fontsize=20)
#
# Abund                   = 0.085
# Te_test                 = 20000
# t4_test                 = Te_test / 10000
# ne_test                 = 100
# Line_dict               = OrderedDict()
# Line_dict['10.51m']     = S4.getEmissivity(tem = Te_test, den = ne_test, wave = Wave_dict['S3_10.5m'])
# Line_dict['4861.36A']   = HI.getEmissivity(tem = Te_test, den = ne_test, label = Wave_dict['Hbeta'])
# The_Ratio               = Abund * Line_dict['10.51m'] / Line_dict['4861.36A']
# S3_abund_pyneb          = S4.getIonAbundance(int_ratio = The_Ratio, tem = Te_test, den = ne_test, wave = 105000, Hbeta = 1)
# Abun_formula            = log10(The_Ratio) + 6.3956 + 0.0416/t4_test - 0.4216 * log10(t4_test) - 12
# Emis_formula            = 12 + p_1[0] + p_1[1]/t4_range + p_1[2] * log10(t4_range)
# print 'Comparing abund', S3_abund_pyneb, 10**Abun_formula
#
#
# #Display figure
# dz.display_fig()


#--------------------------------Helium I Lines--------------------------------

#The formula has the shape: E_HeII / E_Hbeta = A * t_4 ^ B

HI = pn.RecAtom('H', 1)
He1 = pn.RecAtom('He', 1)

A_0 = 1 / 2.04
B_0 = - 0.13

C_0 = 1 / 0.783
D_0 = - 0.23

E_0 = 1 / 2.58
F_0 = - 0.25

# #Declare Classes
# dz = Plot_Conf()
#
# #Define figure format
# dz.FigConf()

print 'I am using this atomic data'
print He1.printSources()

#Define lines:
Wave_dict               = OrderedDict()
Wave_dict['Hbeta']      = '4_2'
Wave_dict['He1_4472A']  = 4471.0
Wave_dict['He1_5876A']  = 5876.0
Wave_dict['He1_6678A']  = 6678.0

#Define physical conditions
tem         = 10000
tem_range   = linspace(5000, 25000, 100)
den         = 100

#Emissivities ranges
Hbeta_emis      = HI.getEmissivity(tem = tem_range, den = den, label = Wave_dict['Hbeta'])
He1_emis        = He1.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['He1_5876A'])
t4_range        = tem_range/10000

#Plotting Pyneb Emis vs Temp
He1_emis_pyneb  = He1_emis / Hbeta_emis
# dz.data_plot(tem_range, He1_emis_pyneb, label='PyNeb value: PFHM 2012')

#Fitting characteristics
p_1, conv_curFit = He_Fitting_Emissivity(t4_range, He1_emis_pyneb, E_0, F_0)

print 'Initial value', p_1[0]**-1, -1*p_1[1]

# #Plotting Hagele Emis vs temp
# Fabian_Emis = A_0 * power(t4_range, B_0)
# dz.data_plot(tem_range, Fabian_Emis, label='Fabian fitting')
#
# #New fitting values
# Vit_Emis = p_1[0] * power(t4_range, p_1[1])
# dz.data_plot(tem_range, Vit_Emis, label='Vital fitting ' + str(p_1[0]) + ' ' + str(p_1[1]))
#
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'$\frac{E_{\left[HeII\right]4686}}{E_{H\beta}}$'
# title   = r'Helium II emissivity comparison, 4686$\AA$, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)


# #--------------------------------Helium II 4863--------------------------------
#  
# #The formula has the shape: E_HeII / E_Hbeta = A * t_4 ^ B
#  
# A_0 = 1 / 0.084
# B_0 = - 0.14
#       
# #Declare Classes
# dz = Plot_Conf() 
#         
# #Define figure format
# dz.FigConf()
#       
# print 'Tell me the files', pn.atomicData.getAllAvailableFiles('He2')
#       
# #Atom creation and definition of physical conditions
# HI = pn.RecAtom('H', 1)
# HeII = pn.RecAtom('He', 2)
#  
# print 'These sources are'
# HeII.printSources()  
#    
# #Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = '4_2' 
# Wave_dict['HeII_4686']  = 4686.0 
#    
# #Define physical conditions
# tem         = 10000
# tem_range   = linspace(5000, 25000, 100)
# den         = 100
#    
# #Emissivities ranges
# Hbeta_emis    = HI.getEmissivity(tem = tem_range, den = den, label = Wave_dict['Hbeta'])
# He2_4686_emis = HeII.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['HeII_4686'])
# t4_range      = tem_range/10000
#    
# #Plotting Pyneb Emis vs Temp
# He2_4686_emis_pyneb  = He2_4686_emis / Hbeta_emis
# dz.data_plot(tem_range, He2_4686_emis_pyneb, label='PyNeb value: PFHM 2012')
#    
# #Fitting characteristics
# p_1, conv_curFit = He_Fitting_Emissivity(t4_range, He2_4686_emis_pyneb, A_0, B_0)
#    
# print 'Initial value', p_1
#    
# #Plotting Hagele Emis vs temp
# Fabian_Emis = A_0 * power(t4_range, B_0)
# dz.data_plot(tem_range, Fabian_Emis, label='Fabian fitting')
#    
# #New fitting values
# Vit_Emis = p_1[0] * power(t4_range, p_1[1])
# dz.data_plot(tem_range, Vit_Emis, label='Vital fitting ' + str(p_1[0]) + ' ' + str(p_1[1]))
#    
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'$\frac{E_{\left[HeII\right]4686}}{E_{H\beta}}$'
# title   = r'Helium II emissivity comparison, 4686$\AA$, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)

# A_1 = p_1[0]
# B_1 = p_1[1]
# C_1 = p_1[2]
    
# formula = r"$12+log\left(\frac{S^{+2}}{H^{+}}\right)=log\left(\frac{I\left(9069+9532\right)}{I\left(H\beta\right)}\right)+"+str(round(A_1*-1,4))+r"+\frac{"+str(round(B_1*-1,4))+r"}{t_{e}}"+str(round(C_1*-1,4))+r"\cdot log\left(t_{e}\right)$"
# print 'The formula is'
# print formula
#   
# dz.Axis.text(0.15, 0.30, formula, transform=dz.Axis.transAxes, fontsize=20) 
#    
#Display figure
# dz.display_fig()

# # #--------------------------------OXYGEN III--------------------------------
#   
# A_0 = - 6.1868
# B_0 = - 1.2491
# C_0 = + 0.5816
#   
# #Declare Classes
# dz = Plot_Conf() 
#     
# #Define figure format
# dz.FigConf()
#   
# print 'Tell me the files'
# print pn.atomicData.getDataFile('O3')
#   
# #Line codes to solve the slow pyneb issue
# pn.atomicData.setDataFile('h_i_rec_SH95.hdf5', 'H1', 'rec')
# pn.atomicData.setDataFile('he_ii_rec_SH95.hdf5', 'He2', 'rec')
#    
# #Atom creation and definition of physical conditions
# HI = pn.RecAtom('H', 1)
# O3 = pn.Atom('O', 3)
#   
# #Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = '4_2' 
# Wave_dict['O3_4959A']   = 4959 
# Wave_dict['O3_5007A']   = 5007 
#   
# #Define physical conditions
# tem         = 10000
# tem_range   = linspace(5000, 25000, 1000)
# den         = 100
#   
# #Emissivities ranges
# Hbeta_emis    = HI.getEmissivity(tem = tem_range, den = den, label = Wave_dict['Hbeta'])
# O3_4959A_emis = O3.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['O3_4959A'])
# O3_5007A_emis = O3.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['O3_5007A'])
# t4_range      = tem_range/10000
#    
# #Plotting Pyneb Emis vs Temp
# O3_emis_vector_pyneb    = log10((O3_4959A_emis + O3_5007A_emis)/Hbeta_emis)
# AtomicDataFile = str(pn.atomicData.getDataFile('O3')[1]).replace('_','')
#  
# dz.data_plot(tem_range, O3_emis_vector_pyneb, label='PyNeb value: ' + AtomicDataFile, linestyle=':')
#   
# #Fitting characteristics
# p_1, conv_curFit = Fitting_Emissivity(t4_range, O3_emis_vector_pyneb, A_0, B_0, C_0)
#   
# print 'Initial value', p_1
#  
# #Plotting Hagele Emis vs temp
# Hagele_Emis = 12 + A_0 + B_0/t4_range + C_0 * log10(t4_range)
# dz.data_plot(tem_range, Hagele_Emis, label='Hagele fitting formula: Lennon and Burke (1994)', linestyle=':', linewidth=2)
#  
# #Emissivity Epm
# EmisEpm = 12 - 6.1868 - 1.2491/t4_range + 0.5816 * log10(t4_range)
# dz.data_plot(tem_range, Hagele_Emis, label='EpMontero 2015 fitting: ' + AtomicDataFile)
#   
#   
# #New fitting values
# Vit_Emis = 12 + p_1[0] + p_1[1]/t4_range + p_1[2] * log10(t4_range)
# dz.data_plot(tem_range, Vit_Emis, label='New fitting: ' + AtomicDataFile)
#   
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'$log\left(\frac{E_{\left[OIII\right]4959}+E_{[OIII]5007}}{E_{H\beta}}\right)$'
# title   = r'Oxygen emissivity comparison, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)
#   
# A_1 = p_1[0]
# B_1 = p_1[1]
# C_1 = p_1[2]
#    
# formula = r"$12+log\left(\frac{O^{+2}}{H^{+}}\right)=log\left(\frac{I\left(4959+5007\right)}{I\left(H\beta\right)}\right)+"+str(round(A_1*-1,4))+r"+\frac{"+str(round(B_1*-1,4))+r"}{t_{e}}"+str(round(C_1*-1,4))+r"\cdot log\left(t_{e}\right)$"
#   
# dz.Axis.text(0.15, 0.30, formula, transform=dz.Axis.transAxes, fontsize=20) 
#    
# #Display figure
# dz.display_fig()
#  
# print 'Data treated'

#--------------------------------SULFUR III 9069--------------------------------
#   
# A_0 = -6.5768
# B_0 = - 0.6293
# C_0 = + 0.6463
#   
# #Declare Classes
# dz = Plot_Conf() 
#     
# #Define figure format
# dz.FigConf()
#   
# print 'Tell me the files', pn.atomicData.getAllAvailableFiles('S3')
#   
# #Line codes to solve the slow pyneb issue
# pn.atomicData.setDataFile('h_i_rec_SH95.hdf5', 'H1', 'rec')
# pn.atomicData.setDataFile('he_ii_rec_SH95.hdf5', 'He2', 'rec')
#   
# #Change atomic data for Sulfur
# # pn.atomicData.includeFitsPath()
# pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
#   
# #Atom creation and definition of physical conditions
# HI = pn.RecAtom('H', 1)
# S3 = pn.Atom('S', 3)
#   
# #Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = '4_2' 
# Wave_dict['S3_9069A']   = 9069 
# Wave_dict['S3_9531A']   = 9531 
#   
# #Define physical conditions
# tem         = 10000
# tem_range   = linspace(5000, 25000, 1000)
# den         = 100
#   
# #Emissivities ranges
# Hbeta_emis    = HI.getEmissivity(tem = tem_range, den = den, label = Wave_dict['Hbeta'])
# S3_9069A_emis = S3.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['S3_9069A'])
# t4_range      = tem_range/10000
#   
# #Plotting Pyneb Emis vs Temp
# S3_emis_vector_pyneb    = log10((S3_9069A_emis)/Hbeta_emis)
# dz.data_plot(tem_range, S3_emis_vector_pyneb, label='PyNeb value: Hudson et al 2012')
#   
# #Fitting characteristics
# p_1, conv_curFit = Fitting_Emissivity(t4_range, S3_emis_vector_pyneb, A_0, B_0, C_0)
#   
# print 'Initial value', p_1
#   
# #Plotting Marta fitting vs temp
# Marta_Emis = 12 + A_0 + B_0/t4_range + C_0 * log10(t4_range)
# dz.data_plot(tem_range, Marta_Emis, label='Marta fitting: Hudson et al 2012')
#   
# #New fitting values
# Vit_Emis = 12 + p_1[0] + p_1[1]/t4_range + p_1[2] * log10(t4_range)
# dz.data_plot(tem_range, Vit_Emis, label='Vital fitting: Hudson et al 2012')
#   
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'$log\left(\frac{E_{\left[SIII\right]9069}}{E_{H\beta}}\right)$'
# title   = r'Sulfur emissivity comparison: 9069$\AA$ line, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)
#   
# A_1 = p_1[0]
# B_1 = p_1[1]
# C_1 = p_1[2]
#    
# formula = r"$12+log\left(\frac{S^{+2}}{H^{+}}\right)=log\left(\frac{I\left(9069\right)}{I\left(H\beta\right)}\right)+"+str(round(A_1*-1,4))+r"+\frac{"+str(round(B_1*-1,4))+r"}{t_{e}}"+str(round(C_1*-1,4))+r"\cdot log\left(t_{e}\right)$"
# print 'The formula is'
# print formula
#   
# dz.Axis.text(0.15, 0.30, formula, transform=dz.Axis.transAxes, fontsize=20) 
#    
# #Display figure
# dz.display_fig()

#--------------------------------SULFUR III 9531--------------------------------
  
# A_0 = -6.1843
# B_0 = - 0.6293
# C_0 = + 0.6463
#   
# #Declare Classes
# dz = Plot_Conf() 
#     
# #Define figure format
# dz.FigConf()
#   
# print 'Tell me the files', pn.atomicData.getAllAvailableFiles('S3')
#   
# #Line codes to solve the slow pyneb issue
# pn.atomicData.setDataFile('h_i_rec_SH95.hdf5', 'H1', 'rec')
# pn.atomicData.setDataFile('he_ii_rec_SH95.hdf5', 'He2', 'rec')
#   
# #Change atomic data for Sulfur
# # pn.atomicData.includeFitsPath()
# pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
#   
# #Atom creation and definition of physical conditions
# HI = pn.RecAtom('H', 1)
# S3 = pn.Atom('S', 3)
#   
# #Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = '4_2' 
# Wave_dict['S3_9069A']   = 9069 
# Wave_dict['S3_9531A']   = 9531 
#   
# #Define physical conditions
# tem         = 10000
# tem_range   = linspace(5000, 25000, 1000)
# den         = 100
#   
# #Emissivities ranges
# Hbeta_emis    = HI.getEmissivity(tem = tem_range, den = den, label = Wave_dict['Hbeta'])
# S3_9531A_emis = S3.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['S3_9531A'])
# t4_range      = tem_range/10000
#   
# #Plotting Pyneb Emis vs Temp
# S3_emis_vector_pyneb    = log10((S3_9531A_emis)/Hbeta_emis)
# dz.data_plot(tem_range, S3_emis_vector_pyneb, label='PyNeb value: Hudson et al 2012')
#   
# #Fitting characteristics
# p_1, conv_curFit = Fitting_Emissivity(t4_range, S3_emis_vector_pyneb, A_0, B_0, C_0)
#   
# print 'Initial value', p_1
#   
# #Plotting Marta fitting vs temp
# Marta_Emis = 12 + A_0 + B_0/t4_range + C_0 * log10(t4_range)
# dz.data_plot(tem_range, Marta_Emis, label='Marta fitting: Hudson et al 2012')
#   
# #New fitting values
# Vit_Emis = 12 + p_1[0] + p_1[1]/t4_range + p_1[2] * log10(t4_range)
# dz.data_plot(tem_range, Vit_Emis, label='Vital fitting: Hudson et al 2012')
#   
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'$log\left(\frac{E_{[SIII]9531}}{E_{H\beta}}\right)$'
# title   = r'Sulfur emissivity comparison: 9531$\AA$ line, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)
#   
# A_1 = p_1[0]
# B_1 = p_1[1]
# C_1 = p_1[2]
#    
# formula = r"$12+log\left(\frac{S^{+2}}{H^{+}}\right)=log\left(\frac{I\left(9531\right)}{I\left(H\beta\right)}\right)+"+str(round(A_1*-1,4))+r"+\frac{"+str(round(B_1*-1,4))+r"}{t_{e}}"+str(round(C_1*-1,4))+r"\cdot log\left(t_{e}\right)$"
# print 'The formula is'
# print formula
#   
# dz.Axis.text(0.15, 0.30, formula, transform=dz.Axis.transAxes, fontsize=20) 
#    
# #Display figure
# dz.display_fig()

# #--------------------------------SULFUR III 9069 + 9531--------------------------------
#      
# A_0 = -5.80
# B_0 = - 0.77
# C_0 = + 0.22
#      
# #Declare Classes
# dz = Plot_Conf() 
#        
# #Define figure format
# dz.FigConf()
#      
# print 'Tell me the files', pn.atomicData.getAllAvailableFiles('S3')
#      
# #Line codes to solve the slow pyneb issue
# pn.atomicData.setDataFile('h_i_rec_SH95.hdf5', 'H1', 'rec')
# pn.atomicData.setDataFile('he_ii_rec_SH95.hdf5', 'He2', 'rec')
#   
# #Change atomic data for Sulfur
# # pn.atomicData.includeFitsPath()
# pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
#   
# #Atom creation and definition of physical conditions
# HI = pn.RecAtom('H', 1)
# S3 = pn.Atom('S', 3)
# 
# print 'For sulfur I am using'
# print S3.printSources()
# 
# #Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = '4_2' 
# Wave_dict['S3_9069A']   = 9069 
# Wave_dict['S3_9531A']   = 9531 
#   
# #Define physical conditions
# tem         = 10000
# tem_range   = linspace(5000, 25000, 1000)
# den         = 100
#   
# #Emissivities ranges
# Hbeta_emis    = HI.getEmissivity(tem = tem_range, den = den, label = Wave_dict['Hbeta'])
# S3_9069A_emis = S3.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['S3_9069A'])
# S3_9531A_emis = S3.getEmissivity(tem = tem_range, den = den, wave = Wave_dict['S3_9531A'])
# t4_range      = tem_range/10000
#   
# #Plotting Pyneb Emis vs Temp
# S3_emis_vector_pyneb    = log10((S3_9069A_emis + S3_9531A_emis)/Hbeta_emis)
# dz.data_plot(tem_range, S3_emis_vector_pyneb, label='PyNeb value: Hudson et al 2012')
#   
# #Fitting characteristics
# p_1, conv_curFit = Fitting_Emissivity(t4_range, S3_emis_vector_pyneb, A_0, B_0, C_0)
#   
# print 'Initial value', p_1
#   
# #Plotting Hagele Emis vs temp
# Hagele_Emis = 12 + A_0 + B_0/t4_range + C_0 * log10(t4_range)
# dz.data_plot(tem_range, Hagele_Emis, label='Hagele fitting: Tayal and Gupta 1999')
#   
# #New fitting values
# Vit_Emis = 12 + p_1[0] + p_1[1]/t4_range + p_1[2] * log10(t4_range)
# dz.data_plot(tem_range, Vit_Emis, label='Vital fitting: Hudson et al 2012')
#   
# #Plot wording
# xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'$log\left(\frac{E_{\left[SIII\right]9069}+E_{[SIII]9531}}{E_{H\beta}}\right)$'
# title   = r'Sulfur emissivity comparison, 9069$\AA$ + 9531$\AA$ lines, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)
#   
# A_1 = p_1[0]
# B_1 = p_1[1]
# C_1 = p_1[2]
#    
# formula = r"$12+log\left(\frac{S^{+2}}{H^{+}}\right)=log\left(\frac{I\left(9069+9532\right)}{I\left(H\beta\right)}\right)+"+str(round(A_1*-1,4))+r"+\frac{"+str(round(B_1*-1,4))+r"}{t_{e}}"+str(round(C_1*-1,4))+r"\cdot log\left(t_{e}\right)$"
# print 'The formula is'
# print formula
#   
# dz.Axis.text(0.15, 0.30, formula, transform=dz.Axis.transAxes, fontsize=20) 
#    
# #Display figure
# dz.display_fig()
