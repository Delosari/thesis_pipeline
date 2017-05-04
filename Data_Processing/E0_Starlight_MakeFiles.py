#!/usr/bin/env python

from dazer_methods import Dazer
from os.path import basename
#Declare code classes
dz = Dazer()

#Declare data to treat
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
nebular_fits_exten      = '_NebularContinuum.fits'

#Generate plot frame and colors
dz.FigConf()

#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_reduc'

#Loop through files
for i in range(len(catalogue_df.index)):
    
    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_file           = catalogue_df.iloc[i].reduction_fits
    nebular_fits        = ouput_folder + objName + nebular_fits_exten
    
    Wave_T, Int_T, header_T = dz.get_spectra_data(fits_file)
    Wave_N, Int_N, header_T = dz.get_spectra_data(ouput_folder + objName + nebular_fits_exten)

    #Perform the reddening correction
    cHbeta = catalogue_df.iloc[i][cHbeta_type]
    Obs_spectrum_dered = dz.derreddening_spectrum(Wave_T, Int_T, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
    spectrum_dered = Obs_spectrum_dered - Int_N
    
    #Generating the starlight files
    FileName = basename(fits_file)
    Grid_FileName, Sl_OutputFile, Sl_OutputFolder, X_1Angs, Y_1Angs = dz.GenerateStarlightFiles(ouput_folder, FileName, objName, catalogue_df.iloc[i], Wave_T, spectrum_dered)
    
    print '--Output file ', Sl_OutputFile
    
    #Plot the data
    dz.data_plot(Wave_T,    spectrum_dered, "Reduced spectrum")
    dz.data_plot(X_1Angs,   Y_1Angs,  "Resampled spectrum", linestyle='--')       
    
    # Set titles and legend  
    PlotTitle = 'Object {} Resampled spectrum for starlight'.format(objName)
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   

    # Save data  
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='Resampled_Spectrum')
    dz.save_manager(output_pickle, save_pickle = True)

print 'Data treated'

#-----------------------------------------------------------------------------------------------------

# print "All data treated"
# 
# 
# #!/usr/bin/env python
# 
# from dazer_methods import Dazer
# 
# #Declare code classes
# dz = Dazer()
# 
# #Declare data to treat
# Catalogue_Dic       = dz.import_catalogue()
# nebular_fits_exten  = '_NebularContinuum.fits'
# pattern             =  Catalogue_Dic['Datatype'] + '.fits'
# cHbeta_type         = 'cHBeta_red'
# 
# #Find and organize files from terminal command or .py file
# FilesList           = dz.Folder_Explorer(pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
# 
# #Generate plot frame and colors
# dz.FigConf(n_colors=5)
# 
# #Loop through files
# for i in range(len(FilesList)):
#     
#     #Analyze file address
#     CodeName, FileName, FileFolder  = dz.Analyze_Address(FilesList[i])
#     
#     #Import fits files
#     Wave_T, Int_T, ExtraData_T      = dz.File_to_data(FileFolder, FileName)
#     Wave_N, Int_N, ExtraData_N      = dz.File_to_data(FileFolder, CodeName + nebular_fits_exten)
#     
#     cHbeta                          = dz.GetParameter_ObjLog(CodeName, FileFolder, cHbeta_type,Assumption='cHbeta_min')
#     Int_Derred                      = dz.derreddening_continuum(Wave_T, Int_T - Int_N , cHbeta.nominal_value)
#     
#     #Generating the starlight files
#     Grid_FileName, Sl_OutputFile, Sl_OutputFolder, X_1Angs, Y_1Angs = dz.GenerateStarlightFiles(FileFolder, FileName, CodeName, Wave_T, Int_Derred)
#     
#     print '--Output file ', Sl_OutputFile
#     
#     #Plot the data
#     dz.data_plot(Wave_T,    Int_Derred,   "Reduced spectrum",     dz.ColorVector[2][0])
#     dz.data_plot(X_1Angs,   Y_1Angs,      "Resampled spectrum",   dz.ColorVector[2][1],     linestyle='--')       
#     
#     # Set titles and legend  
#     PlotTitle = 'Object ' + CodeName + 'Resampled spectrum for starlight'
#     dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   
# 
#     # Save data  
#     dz.save_manager(FileFolder + dz.ScriptCode + '_' + CodeName + '_Resampled_Spectrum')
#              
#     print i+1, '/' , len(FilesList)
# 
# #-----------------------------------------------------------------------------------------------------
# 
# print "All data treated"
