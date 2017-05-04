from dazer_methods import Dazer

#Create class object
dz = Dazer()

#Set figure format
dz.FigConf()


extracted_files = ['/home/vital/Astrodata/WHT_2016_04/Night1/objects/MRK36_Blue_cr_f_t_w_e.fits',
'/home/vital/Astrodata/WHT_2016_04/Night1/objects/MRK36_Red_cr_f_t_w_bg_e.fits']

flux_calibrated = ['/home/vital/Astrodata/WHT_2016_04/Night1/objects/MRK36_Blue_cr_f_t_w_e_fglobal.fits',
'/home/vital/Astrodata/WHT_2016_04/Night1/objects/MRK36_Red_cr_f_t_w_bg_e_fglobal.fits']

# flux_calibrated = ['/home/vital/Astrodata/WHT_2016_04/Night1/objects/MRK36_Blue_cr_f_t_w_e_fglobal.fits',
# '/home/vital/Astrodata/WHT_2016_04/Night1/objects/MRK36_Red_cr_f_t_w_bg_e_fglobal.fits']

flux_calibrated = [
                   '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/MRK36_A1/MRK36_A1_Blue_fglobal.fits',
                   '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/MRK36_A2/MRK36_A2_Blue_fglobal.fits',
                   '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/MRK36_A1/MRK36_A1_Red_fglobal.fits',
                   '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/MRK36_A2/MRK36_A2_Red_fglobal.fits',
                   ]

for i in range(len(flux_calibrated)):
    
#     color = 'Blue' if 'Blue' in extracted_files[i] else 'Red'
    
    
    CodeName, FileName, FileFolder  = dz.Analyze_Address(flux_calibrated[i])
    
    wavelength, Flux_array, Header_0 = dz.get_spectra_data(flux_calibrated[i])
    
#     for j in range(Header_0['NAXIS2']):
#         
#         color_plot = 'orangish' if j == 0 else 'dark blue'
#         dz.data_plot(wavelength, Flux_array[j], label = 'Apperture {} {}'.format(j, color), color=dz.colorVector[color_plot])        

    dz.data_plot(wavelength, Flux_array, label = FileName)        


dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'MRK36')

dz.display_fig()