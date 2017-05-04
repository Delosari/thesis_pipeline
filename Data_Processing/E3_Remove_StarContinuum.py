#!/usr/bin/env python

import numpy as np
from dazer_methods import Dazer
from scipy.interpolate import interp1d

#Declare code classes
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict          = dz.import_catalogue()
catalogue_df            = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
cHbeta_type             = 'cHbeta_reduc'
nebular_exten           = '_NebularContinuum.fits'
Stellar_ext             = '_StellarContinuum.fits'
emitting_ext            = '_Emission.fits'
BasesLimit              = 7000.0

#Define plot frame and colors
dz.FigConf()

#Reddening properties
R_v = 3.4
red_curve = 'G03'
cHbeta_type = 'cHbeta_reduc'

#Loop through files
for i in range(len(catalogue_df.index)):
                    
        print '-- Treating {}'.format(catalogue_df.iloc[i].name)
        
        #Locate the objects
        objName             = catalogue_df.iloc[i].name
        ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        fits_file           = catalogue_df.iloc[i].reduction_fits
    
        #Get reduce spectrum data
        Wave_T, Int_T, ExtraData_T = dz.get_spectra_data(fits_file)
        Wave_N, Int_N, ExtraData_N = dz.get_spectra_data(ouput_folder + objName + nebular_exten)
        Wave_S, Int_S, ExtraData_S = dz.get_spectra_data(ouput_folder + objName + Stellar_ext)    

        #Perform the reddening correction
        cHbeta = catalogue_df.iloc[i][cHbeta_type]
        Int_T_dered = dz.derreddening_spectrum(Wave_T, Int_T, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)

        #Increase the range of Wave_S so it is greater than the observational range
        Wave_StellarExtension = np.linspace(3000.0,3399.0,200)
        Int_StellarExtension  = np.zeros(len(Wave_StellarExtension))
    
        #Increase the range of Wave_S so it is greater than the observational range
        Int_S = np.hstack((Int_StellarExtension, Int_S))
        Wave_S = np.hstack((Wave_StellarExtension, Wave_S))
    
        #Resampling stellar spectra
        Interpolation               = interp1d(Wave_S, Int_S, kind = 'slinear')        
        Int_Stellar_Resampled       = Interpolation(Wave_T)
    
        #Remove the continua
        Int_E = Int_T_dered - Int_N - Int_Stellar_Resampled
    
        #Plot the data
        dz.data_plot(Wave_S, Int_S,                     'Stellar fitting')
        dz.data_plot(Wave_T, Int_Stellar_Resampled,     'Resampled stellar fitting')
        dz.data_plot(Wave_T, Int_T_dered,                'Reduced spectra - derreds')
        dz.data_plot(Wave_T, Int_E,                     'Emitting component')
        
        #Focus on the blue region
        mean_flux = Int_T.mean()
        dz.Axis.set_ylim(-0.1*mean_flux, 15*mean_flux)
        dz.Axis.set_xlim(3500, 5250)    
    
        #Set titles and legend
        PlotTitle = r'Object {} Stellar continuum substraction'.format(objName)
        dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', PlotTitle)   
         
        #Save data  
        output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='StellarContinuum_substraction')
        dz.save_manager(output_pickle, save_pickle = True)
    
        #Export fits
        Int_E_redd = dz.reddening_spectrum(Wave_T, Int_E, reddening_curve=red_curve, cHbeta=cHbeta.nominal_value, R_v=R_v)
        dz.Data_2_Fits(ouput_folder, objName + emitting_ext, ExtraData_T, Wave_T, Int_E_redd, NewKeyWord = ['EMISSPEC', 'only emission lines'])
        catalogue_df.loc[objName, 'emission_fits'] = ouput_folder + objName + emitting_ext
        

#Store the dataframe
dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')
