#!/usr/bin/python
from numpy import searchsorted, median, concatenate
from dazer_methods import Dazer

#Create class object
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
dz.FigConf()
 
#Loop through the objects
for i in range(len(catalogue_df.index)):
     
    #Object
    objName = catalogue_df.iloc[i].name
    
    if objName == '8':
    
        #Joining pointing
        joining_wavelength = catalogue_df.iloc[i].join_wavelength
     
        #Treat each arm file    
        blue_fits_file = catalogue_df.iloc[i]['zBlue_file'] 
        red_fits_file = catalogue_df.iloc[i]['zRed_file'] 
     
        CodeName_Blue, FileName_Blue, FileFolder_Blue = dz.Analyze_Address(blue_fits_file)
        CodeName_Red, FileName_Red, FileFolder_Red = dz.Analyze_Address(red_fits_file)
     
        wave_Blue, flux_Blue, ExtraData_Blue = dz.get_spectra_data(blue_fits_file)
        wave_Red, flux_Red, ExtraData_Red = dz.get_spectra_data(red_fits_file)
     
        idx_blue = searchsorted(wave_Blue, joining_wavelength) 
        idx_red  = searchsorted(wave_Red, joining_wavelength) 
         
        wave_comb = concatenate([wave_Blue[0:idx_blue], wave_Red[idx_red:-1]])
        flux_comb = concatenate([flux_Blue[0:idx_blue], flux_Red[idx_red:-1]])
     
        dz.data_plot(wave_Blue, flux_Blue, label = 'WHT blue arm')
        dz.data_plot(wave_Red, flux_Red, label = 'WHT red arm')
        dz.insert_image('/home/vital/Dropbox/Astrophysics/Seminars/Angeles_Seminar/8.png', Image_Coordinates = [0.85,0.70], Zoom=0.20, Image_xyCoords = 'axes fraction')
        dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'HII galaxy: SDSSJ024815.93-081716.5, WHT observation')
        dz.display_fig()
        #dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Angeles_Seminar/' + '8_WHT', extension='.png')

