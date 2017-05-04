#!/usr/bin/env python
from dazer_methods import Dazer
from numpy import linspace, zeros, hstack
from scipy.interpolate import interp1d

#Declare code classes
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
nebular_exten           = '_NebularContinuum_emis.fits'
Stellar_ext             = '_StellarContinuum_emis.fits'
emitting_ext            = '_Emission_2nd.fits'

#Define plot frame and colors
dz.FigConf()

#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_emis'

#Loop through files
for i in range(len(catalogue_df.index)):
    
    print '-- Treating {}'.format(catalogue_df.iloc[i].name)
 
    #Locate the objects
    objName             = catalogue_df.iloc[i].name
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    fits_file           = catalogue_df.iloc[i].reduction_fits

    #Get reduce spectrum data
    Wave_O, Int_O, ExtraData_T = dz.get_spectra_data(fits_file)
    Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + nebular_exten)
    Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + Stellar_ext)    
    Wave_E, Int_E, ExtraData_E = dz.get_spectra_data(ouput_folder + objName + emitting_ext)    
    
    #Increase the range of Wave_S so it is greater than the observational range
    Wave_StellarExtension = linspace(3000.0,3399.0,200)
    Int_StellarExtension  = zeros(len(Wave_StellarExtension))
 
    #Increase the range of Wave_S so it is greater than the observational range
    Int_S   = hstack((Int_StellarExtension, Int_S))
    Wave_S  = hstack((Wave_StellarExtension, Wave_S))
 
    #Resampling stellar spectra
    Interpolation               = interp1d(Wave_S, Int_S, kind = 'slinear')        
    Int_Stellar_Resampled       = Interpolation(Wave_O)

    #Perform the reddening correction
    cHbeta = catalogue_df.iloc[i][cHbeta_type]
    IntObs_dered = dz.derreddening_spectrum(Wave_O, Int_O, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
    IntEmi_dered = dz.derreddening_spectrum(Wave_E, Int_E, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

    Int_Sum = IntEmi_dered + Int_Stellar_Resampled + Int_N

    dz.data_plot(Wave_O, IntObs_dered, 'Observed spectrum')
    dz.data_plot(Wave_N, Int_N, 'Nebular continuum')
    dz.data_plot(Wave_S, Int_S, 'Stellar continuum')

    #Set titles and legend
    PlotTitle = r'{} continua comparison'.format(objName)
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle, loc='upper right')   
    
    mean_flux = Int_O.mean()
    dz.Axis.set_ylim(-0.05*mean_flux, 15*mean_flux)
    dz.Axis.set_xlim(3550, 5250)
        
    #Save data  
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='comparison_spectra')
    dz.save_manager(output_pickle, save_pickle = True)

#-----------------------------------------------------------------------------------------------------
print 'All data treated', dz.display_errors()

