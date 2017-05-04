# from CodeTools.PlottingManager              import myPickle
# import pyfits
# from Plotting_Libraries.dazer_plotter       import Plot_Conf
# import numpy as np
# 
# dz = Plot_Conf()
# pv = myPickle()
# 
# Pattern     = '.fits'
# FileFolder  = '/home/vital/Desktop/Standard_Traditional/'
# 
# #Locate files on hard drive
# FilesList = pv.Folder_Explorer(Pattern, FileFolder, CheckComputer=False)
# 
# #Define figure format
# dz.FigConf()
# 
# #Loop through files
# for i in range(len(FilesList)):
#     
#     CodeName, FileName, FileFolder = pv.Analyze_Address(FilesList[i])
#     Name = FileName[0:FileName.find('_')]
#     
#     print 'Going for: ', Name, '(',FileName, ')'
#             
#     FitsFile = pyfits.open(FileFolder + FileName)
#     
#     Header_0    = FitsFile[0].header
#     Header_1    = FitsFile[1].header
#     Data_0      = FitsFile[0].data
#     Data_1      = FitsFile[1].data
#     Wave, Flux  = [], []
#     
#     for coso in Data_1:
#         Wave.append(coso[0])
#         Flux.append(coso[1])
#     
#     linestyle = '-'
#     if Name in ['bd17', 'bd28', 'feige34', 'bd33', 'g191']:
#         linestyle = '--'
#     
#     dz.data_plot(Wave, Flux/np.max(Flux), label = Name, linestyle=linestyle, linewidth=2)
# 
# #     dz.data_plot(Wave, Flux, label = Name, linestyle='--')
#     dz.Axis.set_xlim(3500, 11000)
# 
# dz.FigWording( xlabel = r'Wave', ylabel = r'Flux',title = 'Standard star calibration (dashed lines belong to objects already observed)', legend_loc='lower left')    
# # dz.Axis.set_xscale('log')
# # dz.Axis.set_yscale('log')
# 
# dz.display_fig()
# 
# # Wave_, Int, ExtraData = pv.File2Data(FileFolder, FileName)



import os
import urllib2
from Plotting_Libraries.dazer_plotter       import Plot_Conf
import pylab as pl
from matplotlib import image
import math, ephem, pandas as pd
from numpy import int64
from astroquery.sdss                        import SDSS
from astroquery.alfalfa                     import Alfalfa
from collections                            import OrderedDict
from ManageFlow                             import DataToTreat
from CodeTools.PlottingManager              import myPickle
from uncertainties                          import ufloat
from astropy                                import coordinates as coords
from astroquery.sdss                        import SDSS
from astroquery.simbad import Simbad
 
 
#Recover objects list
Table_Address   = '/home/vital/Desktop/WHT_CandiatesObjects_2016A/Data/Standar_star_calspec'
Candiates_frame = pd.read_csv(Table_Address, delimiter = '; ', header = 0, index_col = 0)
Object, Ra, dec = [], [], []
  
for i in range(len(Candiates_frame.index)):
 
    name = Candiates_frame.index[i]
 
    result_table = Simbad.query_object(name)
 
 
    if result_table != None:
        Object.append(name)
        Ra.append( result_table['RA'][0])
        dec.append( result_table['DEC'][0])
        print name, result_table['RA'][0], result_table['DEC'][0]
 
print '\nList of objects'       
for i in range(len(Object)):
    print Object[i].replace(' ', '_'), Ra[i].replace(' ',':'), dec[i].replace(' ',':')
 
 
# for i in range(len(Candiates_frame.index)):
#     
#     
#     #Get the frame row
#     row = Candiates_frame.iloc[[i]]
#     
#     #Get the object SDSS parameters
#     Name, Star_type, V, B_V, CDBS_name = Candiates_frame.index[i], row['Star type'].values[0], row['Vmag'].values[0], row['B-Vmag'].values[0], row['CDBS name'].values[0] 
#     
#     #Query the object
#     result_table = Simbad.query_object(Name)
# 
#     #Plot the output
#     print result_table[0]['RA']