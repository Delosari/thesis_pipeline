'''
Created on May 24, 2016

@author: vital
'''

import pandas as pd
from collections            import OrderedDict
from numpy                  import array, log10 as np_log10, linspace, zeros, exp, power, absolute, hstack, min as np_min, max as np_max, clip, argmin, abs, pi
from user_conf.ManageFlow   import DataToTreat
from dazer_methods          import Dazer
from lmfit.models           import LinearModel
from lmfit                  import Parameters, minimize, report_fit
import pymc




def find_closest(A, target):
    idx_array = zeros(len(target))
    #A must be sorted
    for i in range(len(target)):

        idx_array[i] = argmin(abs(A - target[i]))
        
    return idx_array

#Import model classes
dz = Dazer()

#Define figure format
size_dict = {'axes.labelsize':20, 'legend.fontsize':18, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)

#Locate the data
Catalogue_Dic           = DataToTreat()
Pattern                 = Catalogue_Dic['Datatype'] + '.fits'
AbundancesFileExtension = '_' + Catalogue_Dic['Datatype'] + '_linesLog_reduc.txt'
FilesList               = dz.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)

#Dictionary to store the objects frames
Logs_dict = OrderedDict()

#Loop through the files
for i in range(len(FilesList)):

    #Analyze file address
    CodeName, FileName, FileFolder  = dz.Analyze_Address(FilesList[i])
    Log_address = FileFolder + CodeName + AbundancesFileExtension
    
    Logs_dict[CodeName] = pd.read_csv(Log_address, delim_whitespace = True, header=0, index_col=0)
    
#Generate the physical parameters panel
Catalogue_LinesPanel = pd.Panel(Logs_dict)
Eqw_Frame   = Catalogue_LinesPanel.minor_xs('eqw')
Flux_Frame  = Catalogue_LinesPanel.minor_xs('flux_intg')

#Load the PopStar grids
FilesFolder                 = '/home/vital/Dropbox/Astrophysics/Lore/PopStar/' 
TableAddressn10             = 'mnras0403-2012-SD1_clusterTable1.txt'
TableAddressn100            = 'mnras0403-2012-SD2_clusterTable2.txt'
TableRecombination_Emission = 'mnras0398-0451-sm_TableS7_EquivalentWidths.txt'
 
#Load the tables
Frame_HydrogenEmission      = pd.read_csv(FilesFolder + TableRecombination_Emission, delim_whitespace = True)
Frame_MetalsEmission        = pd.read_csv(FilesFolder + TableAddressn10, delim_whitespace = True)
 
#Get grid values
Grid1_ages   = Frame_HydrogenEmission.lage.unique()
Grid1_IMF    = Frame_HydrogenEmission.imf.unique()
Grid1_Z      = Frame_HydrogenEmission.Zmet.unique()
Grid1_mups   = Frame_HydrogenEmission.mup.unique()
Grid1_mlow   = Frame_HydrogenEmission.mlow.unique()
 
Grid2_ages   = Frame_MetalsEmission.t.unique()
Grid2_masses = Frame_MetalsEmission.M_Msun.unique()
Grid2_Z      = Frame_MetalsEmission.Z.unique()
Grid2_logRs  = Frame_MetalsEmission.logR.unique()
Grid2_logU   = Frame_MetalsEmission.logU.unique()

print 'Headers 1', Frame_HydrogenEmission.columns.values
print 'Grid ages 1', Grid1_ages
print 'Grid IMF 1', Grid1_IMF
print 'Grid Z 1', Grid1_Z
print 'Grid mup 1', Grid1_mups
print 'Grid mlow 1', Grid1_mlow

print 'Headers 2', Frame_MetalsEmission.columns.values
print 'Grid ages 2', Grid2_ages
print 'Grid masses 2', Grid2_masses
print 'Grid Z', Grid2_Z
# print 'Grid Rs (pc)', Grid2_logRs
# print 'Grid log(U)', Grid2_logU

nH  = 10.0 #cm^-3
c   = 29979245800.0 #cm/s
pc_to_cm = 3.0856776e18 

# print 
# 
# 
# #Line intensity ratios for different metallicities 
# x_array = array([])
# y_array = array([])
# 
# #Adding a new column with the data we want
# Frame_MetalsEmission['Q'] = np_log10(power(10, Frame_MetalsEmission['logU']) * 4 * pi * c * nH * power(Frame_MetalsEmission['logR'] * pc_to_cm, 2))
# 
# for Z in [0.008]:
#     indeces     = (Frame_MetalsEmission["Z"] == Z) & (Frame_MetalsEmission["M_Msun"] == 40000)
#     tabulated   = Frame_MetalsEmission.loc[indeces, 'logU'].values
#     calculated  = power(10, Frame_MetalsEmission.loc[indeces, 'logU']) * 4 * pi * c * nH * power(Frame_MetalsEmission.loc[indeces, 'logR'] * pc_to_cm, 2)
#     
#     print 'ionizations', Frame_MetalsEmission.loc[indeces, 'logU'].values
#     print 'Q(H)', np_log10(calculated).values
#     print 'Q(H) 2', Frame_MetalsEmission.loc[indeces, 'Q'].values
#  
#     
# index =   (Frame_MetalsEmission["Z"] == Z) & (Frame_MetalsEmission["M_Msun"] == 40000) & (Frame_MetalsEmission["t"] == 5.00)
# print 'These values', Frame_MetalsEmission.loc[index, 'logU'].values, Frame_MetalsEmission.loc[index, 'logR'].values
# print 'These values', Frame_MetalsEmission.loc[index, 'logU'].values[0], Frame_MetalsEmission.loc[index, 'logR'].values[0]

    

#     print (Frame_MetalsEmission.loc[indeces, '[SII]6716'] + Frame_MetalsEmission.loc[indeces, '[SII]6731']) / (Frame_MetalsEmission.loc[indeces, '[SIII]9069'] + Frame_MetalsEmission.loc[indeces, '[SIII]9532']))
#     y = np_log10((Frame_MetalsEmission.loc[indeces, '[OII]3727']) / (Frame_MetalsEmission.loc[indeces, '[OIII]5007'] + Frame_MetalsEmission.loc[indeces, '[OIII]4959']))
#     dz.data_plot(x, y, label='z = {Z}'.format(Z = Z), markerstyle='o')
#     x_array = hstack([x_array, x])
#     y_array = hstack([y_array, y])
#  
# #Displaying the figure
# dz.FigWording(r'$log([SII]/[SIII])$', r'$log\left(\frac{[OII]}{[OIII]}\right)$', r'PopStar models: $log\left(\frac{[OII]}{[OIII]}\right)$ vs $log\left(\frac{[SII]}{[SIII]}\right)$ for $M_{cluster} = 60000M\odot$, IMF = Salpeter', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.04)
# # dz.savefig(output_address = FilesFolder + 'Plots/' + 'IonizationParameter_Z_evolution_Obsevational_Data')
# dz.display_fig()



# #Line intensity ratios for different metallicities 
# x_array = array([])
# y_array = array([])
#   
# for Z in [0.008, 0.004, 0.0004]:
#     indeces = (Frame_MetalsEmission["Z"] == Z) & (Frame_MetalsEmission["M_Msun"] == 60000)
#     x = np_log10((Frame_MetalsEmission.loc[indeces, '[SII]6716'] + Frame_MetalsEmission.loc[indeces, '[SII]6731']) / (Frame_MetalsEmission.loc[indeces, '[SIII]9069'] + Frame_MetalsEmission.loc[indeces, '[SIII]9532']))
#     y = np_log10((Frame_MetalsEmission.loc[indeces, '[OII]3727']) / (Frame_MetalsEmission.loc[indeces, '[OIII]5007'] + Frame_MetalsEmission.loc[indeces, '[OIII]4959']))
#     dz.data_plot(x, y, label='z = {Z}'.format(Z = Z), markerstyle='o')
#     x_array = hstack([x_array, x])
#     y_array = hstack([y_array, y])
# 
# #Displaying the figure
# dz.FigWording(r'$log([SII]/[SIII])$', r'$log\left(\frac{[OII]}{[OIII]}\right)$', r'PopStar models: $log\left(\frac{[OII]}{[OIII]}\right)$ vs $log\left(\frac{[SII]}{[SIII]}\right)$ for $M_{cluster} = 60000M\odot$, IMF = Salpeter', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.04)
# # dz.savefig(output_address = FilesFolder + 'Plots/' + 'IonizationParameter_Z_evolution_Obsevational_Data')
# dz.display_fig()

# #Get observational data frame
# Eqw_Hbeta = absolute(Eqw_Frame.loc['H1_4861A'].values)
# 
# print Eqw_Hbeta
# 
# #Plotting Eqw(Hbeta) versus age for Z values, IMF = Kroupa
# for i in range(len([0.0001,  0.0004,  0.004,   0.008,   0.02])):
#     
#     Z = [0.0001,  0.0004,  0.004,   0.008,   0.02][i]
#     
#     indeces = (Frame_HydrogenEmission["Zmet"] == Z) & (Frame_HydrogenEmission["imf"] == 'SAL') & (Frame_HydrogenEmission["mlow"] == 0.15) & (Frame_HydrogenEmission["mup"] == 100)
#     x = Frame_HydrogenEmission.loc[indeces, 'lage']
#     y = Frame_HydrogenEmission.loc[indeces, 'EWHB']
#     idx_targets = find_closest(y.values, Eqw_Hbeta)
# #     idx_targets = argmin(abs(y.values - Eqw_Hbeta))
# #     print 'pero estos...', x.loc[0].values
#     print  dz.ColorVector[2][i]
#     line = dz.data_plot(x, y, label='z = {Z}'.format(Z = Z), color = dz.ColorVector[2][i], linestyle='-', linewidth =  2)
#     dz.data_plot(x.iloc[idx_targets].values, Eqw_Hbeta, label='Catalogue objects', color = dz.ColorVector[2][i], markerstyle='o')
# 
# 
# Eqw_Hbeta = Eqw_Frame.loc['H1_4861A']
# 
# dz.Axis.set_xlim(5, 8)
# dz.FigWording(r'$log(age)$', r'$Eqw(H\beta)\,(\AA)$', r'PopStar models: $H\beta$ equivalent width vs Cluster age $\left(IMF=Salpeter_{0.15\,M_{\odot}}^{100\,M_{\odot}}\right)$', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.02)
# dz.savefig(output_address = FilesFolder + 'Plots/' + 'EqwHbeta_Z_evolution_Obsevational_Data')#  dz.savefig(output_address = FilesFolder + 'Plots/' + 'IonizationParameter_Z_evolution')
# dz.display_fig()


#Plot ionization parameters versus EqW
x_array = array([])
y_array = array([])
 
Sulfur_Ratio = (Flux_Frame.loc['S2_6716A'] + Flux_Frame.loc['S2_6731A']) / (Flux_Frame.loc['S3_9069A'] + Flux_Frame.loc['S3_9531A'])
obj_SIIbySIII = np_log10(Sulfur_Ratio.astype('float64'))
  
colors_list = ['#CC79A7', '#D55E00', '#bcbd22']
metals_list = [0.008, 0.004, 0.02]
for i in range(len(metals_list)):
    Z = metals_list[i]
    indeces = (Frame_MetalsEmission["Z"] == Z)
    x = np_log10((Frame_MetalsEmission.loc[indeces, '[SII]6716'] + Frame_MetalsEmission.loc[indeces, '[SII]6731']) / (Frame_MetalsEmission.loc[indeces, '[SIII]9069'] + Frame_MetalsEmission.loc[indeces, '[SIII]9532']))
    y = Frame_MetalsEmission.loc[indeces, 'logU']
    dz.data_plot(x, y, label='z = {Z}'.format(Z = Z), markerstyle='o', color=colors_list[i])
    x_array = hstack([x_array, x])
    y_array = hstack([y_array, y])
     
#Lineal model
lineal_mod          = LinearModel(prefix='lineal_')
Lineal_parameters   = lineal_mod.guess(y_array, x=x_array)
x_lineal            = linspace(np_min(x_array), np_max(x_array), 100)
y_lineal            = Lineal_parameters['lineal_slope'].value * x_lineal + Lineal_parameters['lineal_intercept'].value
dz.data_plot(x_lineal, y_lineal, label='', color = 'black', linestyle='--')
 
obj_u = Lineal_parameters['lineal_slope'].value * obj_SIIbySIII + Lineal_parameters['lineal_intercept'].value
dz.data_plot(obj_SIIbySIII, obj_u, label='Sample galaxies in linear fitting', color = 'black', markerstyle='x')
 
#Displaying the figure
dz.FigWording(r'$log([SII]/[SIII])$', r'$log(U)$', 'Ionization parameter versus sulfur lines ratio\n for a gas metallicity, mass and age cluster grid')
dz.Axis.set_xlim(-1.55, 2)
# dz.display_fig()

dz.savefig(output_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/data/' + 'logU_vs_Sratio')


# Luminosity_solar = 3.82e33 #erg s-1
# 
# # Plotting Eqw versus line intensity temporal evolution
# Eqw_Hbeta = Eqw_Frame.loc['H1_4861A']
# Int_Hbeta = Flux_Frame.loc['H1_4861A']
# dz.data_plot(Int_Hbeta.values / Luminosity_solar, absolute(Eqw_Hbeta.values), color='black', label= 'Catalogue values', markerstyle='o', linewidth =  2)
# 
# for j in range(len(Int_Hbeta.values)):
#     print Eqw_Hbeta.index.values[j], Eqw_Hbeta.values[j], Int_Hbeta.values[j]
# 
# for z in Grid2_Z:
#     x_halpha_empty = zeros(len(Grid2_ages))
#     y_halpha_empty = zeros(len(Grid2_ages))
#     x_hbeta_empty = zeros(len(Grid2_ages))
#     y_hbeta_empty = zeros(len(Grid2_ages))
#     
#     for i in range(len(Grid2_ages)):
#         age = Grid2_ages[i]
#     
#         indeces = (Frame_HydrogenEmission["lage"] == age) & (Frame_HydrogenEmission["Zmet"] == z) & (Frame_HydrogenEmission["imf"] == 'SAL') & (Frame_HydrogenEmission["mlow"] == 0.15) & (Frame_HydrogenEmission["mup"] == 100)
#     
#         y_hbeta_empty[i] = Frame_HydrogenEmission.loc[indeces, 'EWHB']
#         x_hbeta_empty[i] = Frame_HydrogenEmission.loc[indeces, 'Ihbeta']    
# 
#     dz.data_plot(x_hbeta_empty, y_hbeta_empty, label=r'z = {zvalue}'.format(zvalue = z), markerstyle='o', linewidth =  2)
# 
# dz.FigWording(r'$I(H\beta)$' '$(L_{\odot})$',  r'$Eqw(H\beta)\,(\AA)$', r'PopStar $H\beta$ equivalent width versus line intensity' '\n' r'$M_{cluster} = 1M_{\odot}$, IMF = Salpeter 2, $log(age) = 5-6.72$', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.04)
# # dz.savefig(output_address = FilesFolder + 'Plots/' + 'Eqw_vs_Ihbeta_Z_evolution')
# dz.display_fig()


#Plotting Intensity Hbeta intensity for both grids
# for mass in [60000]:
#     x_empty = zeros(len(Grid2_ages))
#     y_empty = zeros(len(Grid2_ages))
#     x_halpha = zeros(len(Grid2_ages))
#     y_halpha = zeros(len(Grid2_ages))
#     
#     for i in range(len(Grid2_ages)):
#         age = Grid2_ages[i]
#         indecesHydrogen = (Frame_HydrogenEmission["lage"] == age) & (Frame_HydrogenEmission["Zmet"] == 0.004) & (Frame_HydrogenEmission["imf"] == 'SAL') & (Frame_HydrogenEmission["mlow"] == 0.15) & (Frame_HydrogenEmission["mup"] == 100)
#         indecesMetals   = (Frame_MetalsEmission["M_Msun"] == mass) & (Frame_MetalsEmission["t"] == age) & (Frame_MetalsEmission["Z"] == 0.004)
#         x_empty[i]  = np_log10(Frame_HydrogenEmission.loc[indecesHydrogen, 'Ihbeta'] * mass * Luminosity_solar)
#         y_empty[i]  = Frame_MetalsEmission.loc[indecesMetals, 'Hb']
#         x_halpha[i] = np_log10(Frame_HydrogenEmission.loc[indecesHydrogen, 'Ihalpha'] * mass * Luminosity_solar)
#         y_halpha[i] = np_log10(power(10, Frame_MetalsEmission.loc[indecesMetals, 'Hb']) * Frame_MetalsEmission.loc[indecesMetals, 'Ha']) 
#         
# #         print Frame_HydrogenEmission.loc[indecesHydrogen, 'Ihalpha'].values[0], Frame_HydrogenEmission.loc[indecesHydrogen, 'Ihbeta'].values[0]
#         print Frame_HydrogenEmission.loc[indecesHydrogen, 'Ihalpha'].values[0] * mass * Luminosity_solar, Frame_MetalsEmission.loc[indecesMetals, 'Hb'].values[0] * Frame_MetalsEmission.loc[indecesMetals, 'Ha'].values[0] 
# 
#         
# #     for j in range(len(x_empty)):
# #         print x_empty[i], x_halpha[i]
# 
#     dz.data_plot(x_halpha, y_halpha, label=r'$H\beta$, cluster mass {mass} $M\odot$'.format(mass = mass), markerstyle='o')
#   
# # Make unity curve
# # x_unity = linspace(*dz.Axis.get_xlim())
# # dz.Axis.plot(x_unity, x_unity)   
# 
# dz.FigWording(r'$I(H\beta)$ Grid Popstar 1', r'$I(H\beta)$ Grid Popstar 2', r'PopStar $H\beta$ intensity comparison, $M_{cluster} = 60000M\odot$, IMF = Salpeter 2', axis_Size=30, title_Size=30, legend_size=10, legend_loc='best', Y_TitlePad=1.04)
# dz.display_fig()


# for i in range(len(Frame_HydrogenEmission.index)):
#       
#     #Get the frame row
#     row = Frame_HydrogenEmission.iloc[[i]]
#       
#     #Get the object SDSS parameters
#     print Frame_HydrogenEmission.index[i], row['Ihbeta'].values[0], row['Ihalpha'].values[0], row['Ihalpha'].values[0] / row['Ihbeta'].values[0]


#Plotting Eqw versus line intensity temporal evolution
# for z in Grid2_Z:
#     x_halpha_empty = zeros(len(Grid2_ages))
#     y_halpha_empty = zeros(len(Grid2_ages))
#     x_hbeta_empty = zeros(len(Grid2_ages))
#     y_hbeta_empty = zeros(len(Grid2_ages))
#     
#     for i in range(len(Grid2_ages)):
#         age = Grid2_ages[i]
#     
#         indeces = (Frame_HydrogenEmission["lage"] == age) & (Frame_HydrogenEmission["Zmet"] == z) & (Frame_HydrogenEmission["imf"] == 'SAL') & (Frame_HydrogenEmission["mlow"] == 0.15) & (Frame_HydrogenEmission["mup"] == 100)
#     
#         y_hbeta_empty[i] = Frame_HydrogenEmission.loc[indeces, 'EWHB']
#         x_hbeta_empty[i] = Frame_HydrogenEmission.loc[indeces, 'Ihbeta']    
# #     dz.data_plot(x_halpha_empty, y_halpha_empty, label=r'$H\alpha$, z = {zvalue}'.format(zvalue = z) , markerstyle='o', linewidth =  2)
#     dz.data_plot(x_hbeta_empty, y_hbeta_empty, label=r'z = {zvalue}'.format(zvalue = z), markerstyle='o', linewidth =  2)
# dz.FigWording(r'$I(H\beta)$' '$(L_{\odot})$',  r'$Eqw(H\beta)\,(\AA)$', r'PopStar $H\beta$ equivalent width versus line intensity' '\n' r'$M_{cluster} = 1M_{\odot}$, IMF = Salpeter 2, $log(age) = 5-6.72$', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.04)
# dz.savefig(output_address = FilesFolder + 'Plots/' + 'Eqw_vs_Ihbeta_Z_evolution')

# #Plotting Intensity Hbeta intensity for both grids
# for mass in Grid2_masses:
#     x_empty = zeros(len(Grid2_ages))
#     y_empty = zeros(len(Grid2_ages))
#     x_halpha = zeros(len(Grid2_ages))
#     y_halpha = zeros(len(Grid2_ages))    
#     
#     for i in range(len(Grid2_ages)):
#         age = Grid2_ages[i]
#         indecesHydrogen = (Frame_HydrogenEmission["lage"] == age) & (Frame_HydrogenEmission["Zmet"] == 0.004) & (Frame_HydrogenEmission["imf"] == 'SAL') & (Frame_HydrogenEmission["mlow"] == 0.15) & (Frame_HydrogenEmission["mup"] == 100)
#         indecesMetals   = (Frame_MetalsEmission["M_Msun"] == mass) & (Frame_MetalsEmission["t"] == age) & (Frame_MetalsEmission["Z"] == 0.004)
#      
#         x_empty[i]  = np_log10(Frame_HydrogenEmission.loc[indecesHydrogen, 'Ihbeta'] * Luminosity_solar * mass)
#         y_empty[i]  = Frame_MetalsEmission.loc[indecesMetals, 'Hb']
#         x_halpha[i] = np_log10(Frame_HydrogenEmission.loc[indecesHydrogen, 'Ihalpha'] * mass * Luminosity_solar)
#         y_halpha[i] = np_log10(power(10, Frame_MetalsEmission.loc[indecesMetals, 'Hb']) * Frame_MetalsEmission.loc[indecesMetals, 'Ha'])          
#                  
#     dz.data_plot(x_empty, y_empty, label=r'$H\beta$, cluster mass {mass} $M\odot$'.format(mass = mass), markerstyle='o')
#     dz.data_plot(x_halpha, y_halpha, label=r'$H\alpha$, cluster mass {mass} $M\odot$'.format(mass = mass), markerstyle='x')
# #  df.loc[len(df)]=['8/19/2014','Jun','Fly','98765'] 
# 
# # Make unity curve
# x_unity = linspace(*dz.Axis.get_xlim())
# dz.Axis.plot(x_unity, x_unity)   
# 
# dz.FigWording(r'$I(H\beta)$ Grid Popstar 1', r'$I(H\beta)$ Grid Popstar 2', r'PopStar $H\beta$ intensity comparison, $M_{cluster} = 60000M\odot$, IMF = Salpeter 2', axis_Size=30, title_Size=30, legend_size=10, legend_loc='best', Y_TitlePad=1.04)
# # dz.display_fig()
# dz.savefig(output_address = FilesFolder + 'Plots/' + 'IHbeta_comparison')

#Plotting Eqw(Hbeta) versus age for Z values, IMF = Salpeter, mup = 100, mlow = 0.15
# for Z in [0.008, 0.004, 0.02]:
#     indeces = (Frame_MetalsEmission["Z"] == Z)
#     x = np_log10((Frame_MetalsEmission.loc[indeces, '[SII]6716'] + Frame_MetalsEmission.loc[indeces, '[SII]6731']) / (Frame_MetalsEmission.loc[indeces, '[SIII]9069'] + Frame_MetalsEmission.loc[indeces, '[SIII]9532']))
#     y = Frame_MetalsEmission.loc[indeces, 'logU']
#     dz.data_plot(x, y, label='z = {Z}'.format(Z = Z), markerstyle='o')
# dz.FigWording(r'$log([SII]/[SIII])$', r'$log(U)$', r'PopStar models: Ionization parameter vs $log\left(\frac{[SII]}{[SIII]}\right)$ for several cluster massess, IMF = Salpeter', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.04)
# dz.savefig(output_address = FilesFolder + 'Plots/' + 'IonizationParameter_Z_evolution')


# #Plotting Eqw(Hbeta) versus age for Z values, Z = 0.04
# for imf in Grid1_IMF:
#     if imf  != 'SAL':
#         indeces = (Frame_HydrogenEmission["imf"] == imf) & (Frame_HydrogenEmission["Zmet"] == 0.004)
#         label = r'IMF = {imf}'.format(imf = imf)
#  
#         x = Frame_HydrogenEmission.loc[indeces, 'lage']
#         y = Frame_HydrogenEmission.loc[indeces, 'EWHB']
#         dz.data_plot(x, y, label=label, linestyle='-', linewidth = 2)
#  
# for mup in Grid1_mups:
#     for mlow in Grid1_mlow:
#         indeces = (Frame_HydrogenEmission["imf"] == 'SAL') & (Frame_HydrogenEmission["Zmet"] == 0.004) & (Frame_HydrogenEmission["mlow"] == mlow) & (Frame_HydrogenEmission["mup"] == mup)
#         label = r'IMF = SAL, $m_{{up}} = {mup}$, $m_{{low}} = {mlow}$'.format(mup = mup, mlow = mlow)
#          
#         x = Frame_HydrogenEmission.loc[indeces, 'lage']
#         y = Frame_HydrogenEmission.loc[indeces, 'EWHB']
#          
#         dz.data_plot(x, y, label=label, linestyle='--', linewidth =  2) 
#  
#       
# dz.FigWording(r' PopStar $log(age)$', r'$Eqw(H\beta)\,(\AA)$', r'PopStar models: $H\beta$ equivalent width vs Cluster age $(M_{Cluster} = 1M_{\odot})$, $z = 0.004$', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.04)
# dz.savefig(output_address = FilesFolder + 'Plots/' + 'EqwHbeta_IMF_evolution')
# 
# #Plotting Eqw(Hbeta) versus age for Z values, IMF = Kroupa
# for Z in Grid1_Z:
#     indeces = (Frame_HydrogenEmission["imf"] == 'KRO') & (Frame_HydrogenEmission["Zmet"] == Z)
#     x = Frame_HydrogenEmission.loc[indeces, 'lage']
#     y = Frame_HydrogenEmission.loc[indeces, 'EWHB']
#     dz.data_plot(x, y, label='z = {Z}'.format(Z = Z), linestyle='-', linewidth =  2)
#      
# dz.FigWording(r'$log(age)$', r'$Eqw(H\beta)\,(\AA)$', r'PopStar models: $H\beta$ equivalent width vs Cluster age $(M_{Cluster} = 1M_{\odot})$, IMF = Kroupa', axis_Size=30, title_Size=30, legend_size=25, legend_loc='best', Y_TitlePad=1.04)
# dz.savefig(output_address = FilesFolder + 'Plots/' + 'EqwHbeta_Z_evolution')

# print 'data treated'

# #Plotting Eqw(Hbeta) versus age Z = 0.004, M_Msun = 60000
# indeces = CompleteGrid['t']
# x = CompleteGrid['t'][indeces]
# x = CompleteGrid['t'][indeces]
# 
# for i in range(len(Grid_ages)):
#       
#     #Get the frame row
#     row = CompleteGrid.iloc[[i]]
#       
#     #Get the object SDSS parameters
#     print CompleteGrid.index[i], row['Z'].values[0], row['t'].values[0], row['M_Msun'].values[0]
# 
# # for i in range(len(CompleteGrid.index)):
# #      
# #     #Get the frame row
# #     row = CompleteGrid.iloc[[i]]
# #      
# #     #Get the object SDSS parameters
# #     print CompleteGrid.index[i], row['Z'].values[0], row['t'].values[0], row['M_Msun'].values[0]
#     
# 
# print 'data treated'

#Generate frame with all data
# CompleteGrid    = Table1_frame.append(Frame_MetalsEmission,ignore_index = True)
