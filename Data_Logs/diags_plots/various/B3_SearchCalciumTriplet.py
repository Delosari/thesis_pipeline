#!/usr/bin/python

from numpy import median, searchsorted, full, array, empty
from dazer_methods import Dazer

dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
dz.FigConf()

#Calcium triplet location
lambda_CaII     = array([8498.0, 8542.0, 8662.0])

#Limits for the plot
lambda_limits   = array([8300, 8900])  

#Loop through the objects
for i in range(len(catalogue_df.index)):
       
    #Object
    objName     = catalogue_df.iloc[i].name
    fits_file   = catalogue_df.iloc[i].reduction_fits
    
    print '-- Treating {} @ {}'.format(objName, fits_file)
    
    #Spectrum data
    wave, flux, header_0 = dz.get_spectra_data(fits_file)

    #Plot the regions of interest
    if wave[-1] > 8498:
        
        ind_low, ind_high = searchsorted(wave, lambda_limits)
        
        subWave, subFlux = wave[ind_low:ind_high], flux[ind_low:ind_high]
        medianFlux = full(3, median(subFlux), dtype=float)
        
        #Plot data    
        dz.data_plot(subWave, subFlux, '{} spectrum'.format(objName))
        dz.data_plot(lambda_CaII, medianFlux, 'CaII absorptions', markerstyle= 'o', color=dz.colorVector['orangish'])
                
        #Set titles and legend  
        dz.FigWording(r'Wavelength $(\AA)$', r'Flux $(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'Object {} CaII triplet region'.format(objName))         
        
        #Save data
        ouput_folder    = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
        output_pickle   = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=dz.ScriptCode, objCode=objName, ext='CalIIRegion')
        dz.save_manager(output_pickle, save_pickle = True)

print "\nAll data treated generated"