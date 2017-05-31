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
size_dict = {'axes.labelsize':24, 'legend.fontsize':24, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':22, 'ytick.labelsize':22}
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

nH          = 10.0 #cm^-3
c           = 29979245800.0 #cm/s
pc_to_cm    = 3.0856776e18 
markers     = ['o','s','^'] 


#Plot ionization parameters versus EqW
x_array = array([])
y_array = array([])
 
Sulfur_Ratio = (Flux_Frame.loc['S2_6716A'] + Flux_Frame.loc['S2_6731A']) / (Flux_Frame.loc['S3_9069A'] + Flux_Frame.loc['S3_9531A'])
obj_SIIbySIII = np_log10(Sulfur_Ratio.astype('float64'))
  
colors_list = ['#CC79A7', '#D55E00', '#bcbd22']
metals_list = [0.0001, 0.004, 0.02]
for i in range(len(metals_list)):
    Z = metals_list[i]
    indeces = (Frame_MetalsEmission["Z"] == Z)
    x = np_log10((Frame_MetalsEmission.loc[indeces, '[SII]6716'] + Frame_MetalsEmission.loc[indeces, '[SII]6731']) / (Frame_MetalsEmission.loc[indeces, '[SIII]9069'] + Frame_MetalsEmission.loc[indeces, '[SIII]9532']))
    y = Frame_MetalsEmission.loc[indeces, 'logU']
    dz.data_plot(x, y, label='z = {Z}'.format(Z = Z), markerstyle=markers[i], color=colors_list[i])
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
dz.FigWording(r'$log(I([SII]\lambda\lambda6716+6731\AA)/I([SIII]\lambda\lambda9069+9531\AA))$', r'$log(U)$', '')
dz.Axis.set_xlim(-1.55, 2)
# dz.display_fig()
dz.savefig(output_address = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/logU_vs_Sratio')

