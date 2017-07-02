#!/usr/bin/env python

from dazer_methods import Dazer
from numpy import loadtxt
from os.path import basename

#Declare dazer object
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
mask_extension          = '_Mask.lineslog'
dz.RootFolder           = '/home/vital/'

#Define plot frame and colors
dz.FigConf()


'''
MRK36_A1
MRK36_A2
MAR1324
MAR2071
4_n2
MAR1324
MAR2071
52319-521
51991-224
52235-602 SI
SHOC588
J2225'''

#Loop through files
for i in range(len(catalogue_df.index)):
    
    print '-- Treating {}'.format(catalogue_df.iloc[i].name)

    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_file           = catalogue_df.iloc[i].reduction_fits
        
    #Starlight output
    Sl_OutputFolder     = dz.RootFolder + 'Starlight/Output/'
    Sl_OutputFile       = basename(fits_file).replace('.fits', '.slOutput')
    Input_Wavelength, Input_Flux, Output_Flux, MaskPixels, ClippedPixels, FlagPixels, Parameters = dz.File_to_data(Sl_OutputFolder, Sl_OutputFile)
        
    #Import fits file    
    wave, flux, header_0 = dz.get_spectra_data(fits_file)
        
    #Getting the masks as a two lists with initial and final points            #WARNING the masks generated do not distinguish the absorptions
    InitialPoints, FinalPoints = loadtxt(ouput_folder + objName + mask_extension, usecols=(0,1) ,skiprows=1,unpack=True) #Change by new method 
    
    #Plot the data
    dz.data_plot(Input_Wavelength, Input_Flux, "Input spectrum")     
    dz.data_plot(Input_Wavelength, Output_Flux, 'Stellar fit')    
    dz.data_plot(ClippedPixels[0], ClippedPixels[1], 'Clipped pixels', color = dz.colorVector['green'], markerstyle='o')    
    dz.data_plot(FlagPixels[0], FlagPixels[1], 'Flagged pixels', color = dz.colorVector['pink'], markerstyle='o')     
 
    #Check flagged pixels
    dz.area_fill(InitialPoints, FinalPoints, 'Masks', color = dz.colorVector['orangish'], alpha = 0.2)
           
    # Set titles and legend
    PlotTitle = r'Object ' + objName + ' spectrum with masked and flagged pixels' 
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)
    dz.Axis.set_aspect(3)
    dz.display_fig()
    
#     # Save data  
#     output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='Sl_MasksFlags')
#     dz.save_manager(output_pickle, save_pickle = True)

#-----------------------------------------------------------------------------------------------------

# print "All data treated"
# 
# #!/usr/bin/env python
# 
# from dazer_methods import Dazer
# from numpy import loadtxt
# 
# #Declare code classes
# dz = Dazer()
# 
# #Declare data to treat
# Catalogue_Dic  = dz.import_catalogue()
# pattern        = Catalogue_Dic['Datatype'] + '.fits'
# 
# #Find and organize files from terminal command or .py file
# FilesList      = dz.Folder_Explorer(pattern,  Catalogue_Dic['Obj_Folder'], CheckComputer=False)
# 
# #Define plot frame and colors
# dz.FigConf(n_colors=5)
# 
# #Loop through files
# for i in range(len(FilesList)):
#     
#     #Analyze file address
#     CodeName, FileName, FileFolder  = dz.Analyze_Address(FilesList[i])
#     
#     #Import fits file    
#     Wave, Int, ExtraData            = dz.File_to_data(FileFolder,FileName)
#         
#     #Getting the masks as a two lists with initial and final points            #WARNING the masks generated do not distinguish the absorptions
#     MaskFileName                    = CodeName + '_Mask.lineslog'
#     InitialPoints, FinalPoints      = loadtxt(FileFolder + MaskFileName, usecols=(0,1) ,skiprows=1,unpack=True) #Change by new method 
#     
#     #Plot the data
#     dz.data_plot(Wave, Int, "Input spectrum", dz.ColorVector[2][1])               
#     dz.area_fill(InitialPoints, FinalPoints, 'Masks', dz.ColorVector[2][0], 0.2)
#            
#     # Set titles and legend
#     PlotTitle = r'Object ' + CodeName + ' spectrum with masked and flagged pixels' 
#     dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)
#        
#     # Save data  
#     dz.save_manager(FileFolder + dz.ScriptCode + '_' + CodeName + '_Sl_MasksFlags') 
# 
#     print i+1, '/' , len(FilesList)
# 
# #-----------------------------------------------------------------------------------------------------
# 
# print "All data treated"