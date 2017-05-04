from dazer_methods import Dazer
from libraries.Astro_Libraries.Nebular_Continuum import NebularContinuumCalculator

#Declare objects
dz = Dazer()
nebCalc = NebularContinuumCalculator()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
nebular_fits_exten      = '_NebularContinuum.fits'

#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_reduc'

#Define plot frame and colors
dz.FigConf()
 
#Loop through files only if we are dealing the WHT data and only scientific objects:
for i in range(len(catalogue_df.index)):
    
    print '-- Treating {} @ {}'.format(catalogue_df.iloc[i].name, AbundancesFileExtension)

    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_file           = catalogue_df.iloc[i].reduction_fits
    lineslog_address    = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
        
    #Load object data
    lineslog_frame = dz.load_lineslog_frame(lineslog_address)
    wave, flux, header_0 = dz.get_spectra_data(fits_file)

    #Perform the reddening correction
    cHbeta = catalogue_df.iloc[i][cHbeta_type]
    dz.deredden_lines(lineslog_frame, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
    spectrum_dered = dz.derreddening_spectrum(wave, flux, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

    Te          = 10000.0
    nHeII_HII   = 0.1
    nHeIII_HII  = 0.01
    Hbeta_Flux  = lineslog_frame.loc['H1_4861A', 'line_Int']
    Halpha_Flux = lineslog_frame.loc['H1_6563A', 'line_Int']
    
    print '--Using physical parameters', Te, nHeII_HII, nHeIII_HII, Hbeta_Flux, Halpha_Flux

    #-- Calculate nebular continuum
    nebCalc.PropertiesfromUser(Te, Hbeta_Flux.nominal_value, nHeII_HII, nHeIII_HII, wave, Calibration = 'Zanstra')

    #-- Calculate continuous emissino coefficients:
    Gamma_Total, Gamma_lambda, Gamma_FB_HI, Gamma_FB_HeI, Gamma_FB_HeII, Gamma_2q, Gamma_FF = nebCalc.Calculate_Nebular_gamma()

    #-- Caculate nebular flux with different calibration methods
    NebularInt_Hbeta = nebCalc.Zanstra_Calibration('Hbeta', Hbeta_Flux.nominal_value, Gamma_Total)

    #Removing nebular component
    Int_dedNeb  = spectrum_dered - NebularInt_Hbeta

    #nebularFlux_cont = dz.derreddening_continuum(wave, NebularInt_Hbeta, cHbeta.nominal_value)

    #Plotting the data
    dz.data_plot(wave, spectrum_dered,      'Reduced spectrum (without reddening)')
    dz.data_plot(wave, NebularInt_Hbeta,    'Nebular flux')
    dz.data_plot(wave, Int_dedNeb,          'Removed Nebular contribution')
    
    #Format the graphs
    PlotTitle = r'Object {} Nebular continuum substraction'.format(objName)
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   
    mean_flux = spectrum_dered.mean()
    dz.Axis.set_ylim(-0.05*mean_flux, 15*mean_flux)
    dz.Axis.set_xlim(3500, 5250)
            
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='NebularContinuum_substraction')
    dz.save_manager(output_pickle, save_pickle = True)

    #Export nebular continuum
    dz.Data_2_Fits(ouput_folder, objName + nebular_fits_exten, header_0, wave, NebularInt_Hbeta,  NewKeyWord = ['NEBUSPEC', 'zanstra_hbeta'])

print '\nAll data treated\n', dz.display_errors()

dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')


# from dazer_methods import Dazer
# from libraries.Astro_Libraries.Nebular_Continuum import NebularContinuumCalculator
# 
# #Declare objects
# dz      = Dazer()
# nebCalc = NebularContinuumCalculator()
# 
# #Define operation
# Catalogue_Dic       = dz.import_catalogue()
# pattern             = Catalogue_Dic['Datatype'] + '.fits'
# Lineslog_extension  = '_' + Catalogue_Dic['Datatype'] + '_LinesLog_v3.txt' 
# cHbeta_type         = 'cHBeta_red'
# nebular_fits_exten  = '_NebularContinuum.fits'
# 
# #Locate files on hard drive
# FilesList           = dz.Folder_Explorer(pattern, Catalogue_Dic['Obj_Folder'], CheckComputer=False)
# 
# #Define plot frame and colors
# dz.FigConf(n_colors=5)
#  
# #Loop through files only if we are dealing the WHT data and only scientific objects:
# for i in range(len(FilesList)):
#     try:
# 
#         #Analyze file address
#         CodeName, FileName, FileFolder  = dz.Analyze_Address(FilesList[i])
# 
#         #Extract the data from fits files
#         Wave, Flux, ExtraData           = dz.File_to_data(FileFolder, FileName)
# 
#         #Reddening correction on the whole spectrum
#         cHbeta                          = dz.GetParameter_ObjLog(CodeName, FileFolder, cHbeta_type, Assumption='float')
#         Int                             = dz.derreddening_continuum(Wave, Flux, cHbeta.nominal_value)
# 
#         #Load the object lines
#         lineslog_frame                  = dz.load_object_frame(FileFolder, CodeName, Lineslog_extension, chbeta_coef = cHbeta_type) 
# 
#         #Import cHbeta coefficient
#         Te                              = dz.GetParameter_ObjLog(CodeName, FileFolder,  'TSIII',        Assumption='Min_Temp')
#         nHeII_HII                       = dz.GetParameter_ObjLog(CodeName, FileFolder,  'HeII_HII',     Assumption='Min_HeII')
#         nHeIII_HII                      = dz.GetParameter_ObjLog(CodeName, FileFolder,  'HeIII_HII',    Assumption='Min_HeIII')
#         Hbeta_Flux                      = lineslog_frame['line_Int']['H1_4861A']
# 
#         #Calculate nebular continuum
#         nebCalc.PropertiesfromUser(Te, Hbeta_Flux.nominal_value, nHeII_HII, nHeIII_HII, Wave, Calibration = 'Zanstra')
# 
#         #-- Calculate continuous emission coefficients:
#         Gamma_Total, Gamma_lambda, Gamma_FB_HI, Gamma_FB_HeI, Gamma_FB_HeII, Gamma_2q, Gamma_FF = nebCalc.Calculate_Nebular_gamma()
# 
#         #-- Caculate nebular flux with different calibration methods
#         NebularInt_Hbeta = nebCalc.Zanstra_Calibration('Hbeta', Hbeta_Flux.nominal_value, Gamma_Total)
# 
#         #Removing nebular component
#         Int_dedNeb  = Int - NebularInt_Hbeta
#         Flux_deNeb  = dz.reddening_continuum(Wave, Int_dedNeb, cHbeta.nominal_value)
# 
#         nebularFlux_cont = dz.derreddening_continuum(Wave, NebularInt_Hbeta, cHbeta.nominal_value)
# 
#         #Plotting the data
#         dz.data_plot(Wave, Flux,                'Reduced spectrum',             dz.ColorVector[2][0])
#         dz.data_plot(Wave, Flux_deNeb,          'Removed Nebular continuum',    dz.ColorVector[2][1])
#         dz.data_plot(Wave, nebularFlux_cont,    'Nebular flux',                 dz.ColorVector[2][2])
#         
#         #Format the graphs
#         PlotTitle = r'Object '+ CodeName + ' Nebular continuum substraction'
#         dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   
# 
#         #Export nebular continuum
#         dz.Data_2_Fits(FileFolder, CodeName + nebular_fits_exten, ExtraData[0], Wave, nebularFlux_cont, NewKeyWord = ['NEBUSPEC', 'Resampled'])
# 
#         #Save the data to the Catalogue folder
#         dz.save_manager(FileFolder + dz.ScriptCode + '_' + CodeName + '_NebularContinuum_Removal', reset_fig = True)
#                 
#     except:
#         dz.log_error(CodeName) 
#  
# print '\nAll data treated\n', dz.display_errors()
