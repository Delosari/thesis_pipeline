from dazer_methods import Dazer
from pandas import notnull
from numpy import median
from libraries.Astro_Libraries.Nebular_Continuum import NebularContinuumCalculator

#Declare objects
dz = Dazer()
nebCalc = NebularContinuumCalculator()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'

#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_reduc'

#Define plot frame and colors
dz.FigConf()
 
#Loop through files only if we are dealing the WHT data and only scientific objects:
for i in range(len(catalogue_df.index)):
    
        print '-- Treating {} @ {}'.format(catalogue_df.iloc[i].name, AbundancesFileExtension)
#     try:

        #Locate the objects
        objName             = catalogue_df.iloc[i].name
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        fits_file           = catalogue_df.iloc[i].reduction_fits
        lineslog_address = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
        
        #Load object data
        lineslog_frame = dz.load_lineslog_frame(lineslog_address)
        wave, flux, header_0 = dz.get_spectra_data(fits_file)
    
        #Perform the reddening correction
        cHbeta = catalogue_df.iloc[i][cHbeta_type]
        dz.deredden_lines(lineslog_frame, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
        spectrum_dered = dz.derreddening_spectrum(wave, flux, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

        #Import cHbeta coefficient
    #     Te          = catalogue_df.iloc[i].TeSIII if notnull(catalogue_df.iloc[i].TeSIII) else 10000.0
    #     nHeII_HII   = catalogue_df.iloc[i].HeII_HII_from_S if notnull(catalogue_df.iloc[i].HeII_HII_from_S) else 0.1
    #     nHeIII_HII  = catalogue_df.iloc[i].HeIII_HII_from_S if notnull(catalogue_df.iloc[i].HeIII_HII_from_S) else 0.0
    #     Hbeta_Flux  = lineslog_frame.loc['H1_4861A', 'line_Int']
    #     Halpha_Flux = lineslog_frame.loc['H1_6563A', 'line_Int']
    
        Te          = 10000.0
        nHeII_HII   = 0.1
        nHeIII_HII  = 0.01
        Hbeta_Flux  = lineslog_frame.loc['H1_4861A', 'line_Int']
        Halpha_Flux = lineslog_frame.loc['H1_6563A', 'line_Int']
        
        print '--Using physical parameters', Te, nHeII_HII, nHeIII_HII, Hbeta_Flux, Halpha_Flux
    
        #Extend the wavelength range to visualize the balmer jump
        NebWave = nebCalc.Extend_WavelengthRange(wave)
    
        #-- Calculate nebular continuum
        nebCalc.PropertiesfromUser(Te, Hbeta_Flux.nominal_value, nHeII_HII, nHeIII_HII, NebWave, Calibration = 'Zanstra')
    
        #-- Calculate continuous emissino coefficients:
        Gamma_Total, Gamma_lambda, Gamma_FB_HI, Gamma_FB_HeI, Gamma_FB_HeII, Gamma_2q, Gamma_FF = nebCalc.Calculate_Nebular_gamma()
    
        #-- Caculate nebular flux with different calibration methods
        NebularInt_Hbeta = nebCalc.Zanstra_Calibration('Hbeta', Hbeta_Flux.nominal_value, Gamma_Total)
        NebularInt_Halpha = nebCalc.Zanstra_Calibration('Halpha', Halpha_Flux.nominal_value, Gamma_Total)
        
        #-- Determine or predict the intensity of the balmer jump
        x_trendline, y_trendline, BalmerJump_Int = nebCalc.Estimate_BalmerJumpFlux(spectrum_dered)
    
        #Plotting the data
        dz.data_plot(wave,         spectrum_dered,      'Reduced spectrum')
        dz.data_plot(NebWave,      NebularInt_Hbeta,    'Nebular continuum - Hbeta calibration')
        dz.data_plot(NebWave,      NebularInt_Halpha,   'Nebular continuum - Halfa calibration')
        dz.data_plot(x_trendline,  y_trendline,         'Balmer jump regression', linestyle='--')
    
        #Format the graphs
        plotTitle = r'Object {} Nebular continuum calculation'.format(objName)
        dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', plotTitle)   
        mean_flux = spectrum_dered.mean()
        dz.Axis.set_ylim(-0.05*mean_flux, 15*mean_flux)
        dz.Axis.set_xlim(3500, 5250)
                    
        output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='NebularContinuum_Comparison')
        dz.save_manager(output_pickle, save_pickle = True)
    
#     except:
#         dz.log_error(objName) 
                   
print 'All data treated', dz.display_errors()

# from dazer_methods import Dazer
# from libraries.Astro_Libraries.Nebular_Continuum import NebularContinuumCalculator
# 
# def nebular_continua_calculation_plots():
# 
#     #Plotting the data
#     dz.data_plot(Wave,         Int,                'Reduced spectrum',                         dz.ColorVector[2][0])
#     dz.data_plot(NebWave,      NebularInt_Hbeta,    'Nebular continuum - Hbeta calibration',    dz.ColorVector[2][1])
#     dz.data_plot(NebWave,      NebularInt_Halpha,   'Nebular continuum - Halfa calibration',    dz.ColorVector[2][2])
#     dz.data_plot(x_trendline,  y_trendline,         'Balmer jump regression',                   dz.ColorVector[2][3],     linestyle='--')
# 
#     #Format the graphs
#     PlotTitle = r'Object '+ CodeName + ' Nebular continuum calculation'
#     dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   
#     
#     #Save the data to the Catalogue folder
#     dz.save_manager(FileFolder + dz.ScriptCode + '_' + CodeName + '_NebularContinuum_Comparison', reset_fig = True) 
# 
#     return
# 
# #Declare objects
# 
# dz      = Dazer()
# nebCalc = NebularContinuumCalculator()
# 
# #Define operation
# Catalogue_Dic       = dz.import_catalogue()
# pattern             = Catalogue_Dic['Datatype'] + '.fits'
# Lineslog_extension  = '_' + Catalogue_Dic['Datatype'] + '_LinesLog_v3.txt' 
# cHbeta_type         = 'cHBeta_red'
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
#         cHbeta                          = dz.GetParameter_ObjLog(CodeName, FileFolder, cHbeta_type,Assumption='float')
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
#         Halpha_Flux                     = lineslog_frame['line_Int']['H1_6563A']
#         print '--Using physical parameters', Te, nHeII_HII, nHeIII_HII, Hbeta_Flux, Halpha_Flux
# 
#         #Extend the wavelength range to visualize the balmer jump
#         NebWave = nebCalc.Extend_WavelengthRange(Wave)
# 
#         #-- Calculate nebular continuum
#         nebCalc.PropertiesfromUser(Te, Hbeta_Flux.nominal_value, nHeII_HII, nHeIII_HII, NebWave, Calibration = 'Zanstra')
# 
#         #-- Calculate continuous emissino coefficients:
#         Gamma_Total, Gamma_lambda, Gamma_FB_HI, Gamma_FB_HeI, Gamma_FB_HeII, Gamma_2q, Gamma_FF = nebCalc.Calculate_Nebular_gamma()
# 
#         #-- Caculate nebular flux with different calibration methods
#         NebularInt_Hbeta = nebCalc.Zanstra_Calibration('Hbeta', Hbeta_Flux.nominal_value, Gamma_Total)
#         NebularInt_Halpha = nebCalc.Zanstra_Calibration('Halpha', Hbeta_Flux.nominal_value, Gamma_Total)
#         
#         #-- Determine or predict the intensity of the balmer jump
#         x_trendline, y_trendline, BalmerJump_Int = nebCalc.Estimate_BalmerJumpFlux(Int)
# 
#         #Plotting Nebular continuum calculation
#         nebular_continua_calculation_plots()
#         
#     except:
#         dz.log_error(CodeName) 
#                    
# print 'All data treated', dz.display_errors()

