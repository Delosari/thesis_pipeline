#!/usr/bin/python
from numpy import searchsorted, median
from dazer_methods import Dazer

#Create class object
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
dz.FigConf()

color_dict = {'Blue':dz.colorVector['dark blue'],'Red':dz.colorVector['orangish']}

#Loop through the objects
for i in range(len(catalogue_df.index)):
    
    #Object
    objName = catalogue_df.iloc[i].name
    
    #Joining pointing
    joining_wavelength = catalogue_df.iloc[i].join_wavelength

    #Treat each arm file
    for color in ['Blue', 'Red']:
    
        fits_file = catalogue_df.iloc[i]['z{}_file'.format(color)] 
        
        print fits_file
        
        CodeName, FileName_Blue, FileFolder = dz.Analyze_Address(fits_file)
        
        wave, flux, ExtraData = dz.get_spectra_data(fits_file)

        dz.data_plot(wave, flux, label = '{} {} arm'.format(CodeName, color), color=color_dict[color])
        
        idx_point = searchsorted(wave, joining_wavelength) 
        
        if (wave[0] < joining_wavelength) and (joining_wavelength < wave[-1]):
            #dz.data_plot(wave[idx_point], flux[idx_point], label = 'Joining lambda {} $\AA$'.format(joining_wavelength), color=dz.colorVector['green'], markerstyle = 'o')
            dz.Axis.axvline(joining_wavelength, label = 'Joining lambda {} $\AA$'.format(joining_wavelength), color=dz.colorVector['green'])
        else:
            mean_continuum_flux = median(flux)
            #dz.data_plot(joining_wavelength, mean_continuum_flux, label = 'Joining lambda {} $\AA$'.format(joining_wavelength), color=dz.colorVector['green'], markerstyle = 'o')
            dz.Axis.axvline(joining_wavelength, label = 'Joining lambda {} $\AA$'.format(joining_wavelength), color=dz.colorVector['green'])
            
    mean_flux = median(flux)
    dz.Axis.set_ylim(mean_flux / 15, mean_flux * 10)
    dz.Axis.set_xlim(joining_wavelength-300, joining_wavelength+300)
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'Redshift correction')
        
    #Store the figure
    output_address = FileFolder + script_code + '_' + CodeName + '_joining_point'
    dz.save_manager(output_address, save_pickle = True)

print "\nAll data treated generated"
