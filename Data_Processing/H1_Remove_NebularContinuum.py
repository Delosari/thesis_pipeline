from pandas import notnull
from dazer_methods import Dazer
from libraries.Astro_Libraries.Nebular_Continuum import NebularContinuumCalculator

#Declare objects
dz = Dazer()
nebCalc = NebularContinuumCalculator()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_emission.txt'
nebular_fits_exten      = '_NebularContinuum_emis.fits'

#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_emis'

#Define plot frame and colors
dz.FigConf()
 
#Loop through files only if we are dealing the WHT data and only scientific objects:
for objName in catalogue_df.index:
    
    print '-- Treating {} @ {}'.format(objName, AbundancesFileExtension)

    #Locate the objects
    objName                 = catalogue_df.loc[objName].name
    ouput_folder            = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_file               = catalogue_df.loc[objName].reduction_fits
    lineslog_address        = '{objfolder}{codeName}{lineslog_extension}'.format(objfolder = ouput_folder, codeName=objName, lineslog_extension=AbundancesFileExtension)
        
    #Load object data
    object_data             = catalogue_df.loc[objName]
    lineslog_frame          = dz.load_lineslog_frame(lineslog_address)
    wave, flux, header_0    = dz.get_spectra_data(fits_file)

    #Perform the reddening correction
    cHbeta = catalogue_df.loc[objName, cHbeta_type]
    dz.deredden_lines(lineslog_frame, reddening_curve=red_curve, cHbeta=cHbeta, R_v=R_v)
    spectrum_dered = dz.derreddening_spectrum(wave, flux, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

    #Import physical data    
    Tlow_key    = catalogue_df.loc[objName, 'T_high'] + '_emis'
    nHeII_HII   = 'HeII_HII_from_O' + '_emis'
    nHeIII_HII  = 'HeIII_HII_from_O' + '_emis'
    
    Te          = object_data[Tlow_key].nominal_value if notnull(object_data[Tlow_key]) else 10000.0  
    nHeII_HII   = object_data[nHeII_HII].nominal_value if notnull(object_data[nHeII_HII]) else 0.1
    nHeIII_HII  = object_data[nHeIII_HII].nominal_value if notnull(object_data[nHeIII_HII]) else 0.0 
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

