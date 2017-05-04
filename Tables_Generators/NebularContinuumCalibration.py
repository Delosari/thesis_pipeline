#!/usr/bin/env python

from numpy                                      import hstack, linspace, vstack, zeros, log10
from CodeTools.PlottingManager                  import myPickle
from    ManageFlow                              import DataToTreat
from Astro_Libraries.Nebular_Continuum          import NebularContinuumCalculator
from Plotting_Libraries.dazer_plotter           import Plot_Conf
from matplotlib                                 import image
from scipy.interpolate                          import interp1d
from matplotlib._png                            import read_png
from matplotlib.offsetbox                       import OffsetImage, AnnotationBbox

#---------------------Spectrum Continuum comparisons------------------------------
pv                      = myPickle()
dz                      = Plot_Conf() 
nebCalc                 = NebularContinuumCalculator()
nebCalc.DataRoot        = '/home/vital/Dropbox/Astrophysics/Lore/NebularContinuum/'
 
#Define operation
Catalogue_Dic           = DataToTreat()
Pattern                 = Catalogue_Dic['Datatype'] + '_dered.fits'
Lineslog_extension      = '_' + Catalogue_Dic['Datatype'] + '_dered_LinesLog_v3.txt' 
 
#Find and organize files from terminal command or .py file
FilesList               = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
 
#Define figure format
dz.FigConf(FigWidth =16 , FigHeight = 9)
 
for i in range(len(FilesList)):
 
    #Analyze file address
    CodeName, FileName, FileFolder      = pv.Analyze_Address(FilesList[i])
 
    #Extract the data from fits files
    Wave, Flux, ExtraData               = pv.File_to_data(FileFolder, FileName)
                    
    #Import data coefficient
    Te                                  = pv.GetParameter_ObjLog(CodeName, FileFolder,  'TOIII',        Assumption='Min_Temp')
    nHeII_HII                           = pv.GetParameter_ObjLog(CodeName, FileFolder,  'HeII_HII',     Assumption='Min_HeII')
    nHeIII_HII                          = pv.GetParameter_ObjLog(CodeName, FileFolder,  'HeIII_HII',    Assumption='Min_HeIII')
    Hbeta_Flux                          = pv.GetParameter_LineLog(CodeName, FileFolder, 'H1_4861A',     'FluxGauss',   Lineslog_extension)
     
    #Calculate nebular continuum
    nebCalc.PropertiesfromUser(Te, Hbeta_Flux, nHeII_HII, nHeIII_HII, Wave, Calibration = 'Zanstra')
 
    #Calculate continuous emissino coefficients:
    Gamma_Total, Gamma_lambda, Gamma_FB_HI, Gamma_FB_HeI, Gamma_FB_HeII, Gamma_2q, Gamma_FF = nebCalc.Calculate_Nebular_gamma()
     
    #Caculate nebular flux with different calibration methods
    NebularFlux = nebCalc.Zanstra_Calibration('Hbeta', Hbeta_Flux, Gamma_Total)
     
    #Get stellar continuum
    StellarContinuumFits = CodeName + '_StellarContinuum.fits'
    Wave_Stellar, Int_Stellar, ExtraData        = pv.File2Data(FileFolder, StellarContinuumFits)
     
    Wave_StellarExtension                       = linspace(3000.0,3399.0,200)
    Int_StellarExtension                        = zeros(len(Wave_StellarExtension))
     
    Int_Stellar                                 = hstack((Int_StellarExtension,      Int_Stellar))
    Wave_Stellar                                = hstack((Wave_StellarExtension,    Wave_Stellar))
     
    Interpolation                               = interp1d(Wave_Stellar, Int_Stellar, kind = 'slinear')        
    Int_Stellar_Resampled                       = Interpolation(Wave)
     
    #Plotting the data:
    dz.data_plot(Wave, Flux, label = 'Dereddened spectrum')
    dz.data_plot(Wave, NebularFlux, label = 'Nebular spectrum')
    dz.data_plot(Wave_Stellar, Int_Stellar, label = 'Stellar spectrum', linestyle='--')
    dz.data_plot(Wave, Int_Stellar_Resampled + NebularFlux, label = 'Stellar + Nebular components')
    
#     dz.InsertFigure(FileFolder,  CodeName + '.png')
    
    arr_hand = read_png(FileFolder + CodeName + '.png')
    Image_Frame = OffsetImage(arr_hand, zoom=3)
    ab = AnnotationBbox(Image_Frame, [0.865,0.8], xybox=(10,-10), xycoords='figure fraction', boxcoords="offset points")
    dz.Axis.add_artist(ab)    
    
    dz.Axis.set_xlim(3600.0, 3900)
    dz.Axis.set_ylim(0, 1e-15)
    #Set plot labels
    title   = r'SHOC579 spectrum components$'
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', title)    
     
    #Display figure
#     dz.display_fig()
    dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Elemental_RegressionsSulfur/Images/' + 'SHOC579_spectralComponents', extension='.png')

# #---------------------Zanstra calibration------------------------------
# 
# pv                      = myPickle()
# dz                      = Plot_Conf() 
# nebCalc                 = NebularContinuumCalculator()
# nebCalc.DataRoot        = '/home/vital/Dropbox/Astrophysics/Lore/NebularContinuum/'
#  
# #Define operation
# Catalogue_Dic           = DataToTreat()
# Pattern                 = Catalogue_Dic['Datatype'] + '_dered.fits'
# Lineslog_extension      = Catalogue_Dic['Datatype'] + '_dered_LinesLog_v3.txt' 
#  
# #Find and organize files from terminal command or .py file
# FilesList               = pv.Folder_Explorer(Pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
#  
# #Define figure format
# dz.FigConf(FigWidth = 4, FigHeight = 4)
#  
# for i in range(len(FilesList)):
#  
#     #Analyze file address
#     CodeName, FileName, FileFolder      = pv.Analyze_Address(FilesList[i])
#     
#     if CodeName == 'SHOC579':
#         
#         #Extract the data from fits files
#         Wave, Flux, ExtraData               = pv.File_to_data(FileFolder, FileName)
#                         
#         #Synthetic values for the plot
#         temp_ranges                         = linspace(5000, 20000, 10)
#          
#         nebCalc.Wavelength_Range            = linspace(912, 30000, 20000-912, endpoint=True)
#         nebCalc.HeII_HII                    = 0.01
#         nebCalc.HeIII_HII                   = 0.001
#           
#         alpha_eff_Matrix_Vector             = zeros(len(temp_ranges))
#         Gamma_Matrix                        = None
#          
#         for i in range(len(temp_ranges)):
#             nebCalc.Te                  = temp_ranges[i]
#             t4                          = nebCalc.Te / 10000    
#             alfa_eff_Hb_i               = 0.668e-13 * t4**-0.507 / (1 + 1.221*t4**0.653)
#              
#             alpha_eff_Matrix_Vector[i]  = alfa_eff_Hb_i
#             Gamma_Total_i, Gamma_lambda, Gamma_FB_HI, Gamma_FB_HeI, Gamma_FB_HeII, Gamma_2q, Gamma_FF = nebCalc.Calculate_Nebular_gamma()
#              
#             if i == 0:
#                 Gamma_Matrix = Gamma_Total_i/alfa_eff_Hb_i
#             else:
#                 Gamma_Matrix = vstack((Gamma_Matrix, Gamma_Total_i/alfa_eff_Hb_i))
#              
#         #Plot the data
#         dz.surface_plot(nebCalc.Wavelength_Range, temp_ranges, Gamma_Matrix)
#          
#         #Set plot labels
#         title   = r' $\gamma_{\nu,\,H} / \alpha^{eff}_{H\beta} $ ratio in a $T_{e}$ - $\lambda$ grid'
#         dz.FigWording(r'Wavelength $(\mathring{A})$', r'Temperature $(K)$', title)    
#          
#         #Display figure
#         dz.display_fig()
# #         dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Elemental_RegressionsSulfur/Images/' + 'NebularContinuumCalibration')
    
#-----------------------------------------------------------------------------------------------------

print "All data treated"