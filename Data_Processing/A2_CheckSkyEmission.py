from dazer_methods import Dazer
from DZ_observation_reduction import spectra_reduction
from numpy import isnan
import os.path

dz = Dazer()
dz_reduc = spectra_reduction()
script_code = dz.get_script_code()

catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

dz.FigConf(Figtype = 'Grid_size', n_columns = 1, n_rows = 2)

for i in range(len(catalogue_df.index)):

    #print '\n-- Treating {} @ {}'.format(catalogue_df.iloc[i].name, catalogue_df.iloc[i].Red_file)
   
    codeName            = catalogue_df.iloc[i].name
    fits_file           = catalogue_df.iloc[i].Red_file
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], codeName)
    redshift_factor     = 1 + catalogue_df.iloc[i].z_Red
    
    star                = catalogue_df.iloc[i].telluric_star
    calibration_star    = catalogue_df.iloc[i].calibration_star.split(';')[0]
      
    if os.path.isfile('{reduc_folder}objects/{calibStar}_Red_slit5.0_n.fits'.format(reduc_folder = catalogue_df.iloc[i].obsfolder, calibStar = calibration_star)):
        star_file = '{reduc_folder}objects/{calibStar}_Red_slit5.0_n.fits'.format(reduc_folder = catalogue_df.iloc[i].obsfolder, calibStar = calibration_star)
    
    elif os.path.isfile('{reduc_folder}objects/{calibStar}_Red_slit8.0_n.fits'.format(reduc_folder = catalogue_df.iloc[i].obsfolder, calibStar = calibration_star)):
        star_file = '{reduc_folder}objects/{calibStar}_Red_slit8.0_n.fits'.format(reduc_folder = catalogue_df.iloc[i].obsfolder, calibStar = calibration_star)
    
    else:
        star_file = '{reduc_folder}objects/{calibStar}_Red_slit1.0_n.fits'.format(reduc_folder = catalogue_df.iloc[i].obsfolder, calibStar = calibration_star)
    
    print 

    #Spectra data
    wave_obs, flux_obs, header_0_obs = dz.get_spectra_data(fits_file, ext=0)  
    wave_star, flux_star, header_0_star = dz.get_spectra_data(star_file, ext=0)  
 
    print '---Telluric star',  codeName, os.path.isfile(fits_file), len(flux_star.shape)
    
    if  len(flux_star.shape) == 3:
        flux_star = flux_star[0][0]
 
    #Plot data
    dz.data_plot(wave_obs, flux_obs, label= 'Observed spectrum', linestyle='step', graph_axis=dz.ax1)
    dz.data_plot(wave_star, flux_star, label= 'Calibration star spectrum', linestyle='step', graph_axis=dz.ax2)
    dz.ax1.set_ylim(bottom=0)
    
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', r'Object {} Star {}'.format(codeName, calibration_star), loc='best', graph_axis=dz.ax1) 
    dz.FigWording(r'Wavelength $(\AA)$', 'Normalized flux', '', loc='lower center', graph_axis=dz.ax2)
     
    output_pickle = '{objFolder}{stepCode}_{objCode}_{ext}'.format(objFolder=ouput_folder, stepCode=script_code, objCode=codeName, ext='check sky emission')
    dz.save_manager(output_pickle, save_pickle = True, reset_fig=True) 
    
    dz.ax1.cla()
    dz.ax2.cla()        
