from dazer_methods import Dazer
from DZ_observation_reduction import spectra_reduction

#Create class object
dz = Dazer()
dz_reduc = spectra_reduction()
script_code = dz.get_script_code()

#Define operation
catalogue_dict = dz.import_catalogue()

#Load catalogue dataframe
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Set figure format
dz.FigConf()

#Loop through the objects
for i in range(len(catalogue_df.index)):
        
    #Treat each arm file
    for color in ['Blue', 'Red']:
        
        fits_file = catalogue_df.iloc[i]['{}_file'.format(color)]
        
        if (color == 'Red') and (str(catalogue_df.iloc[i].telluric_star) not in ['None', 'nan']):
            fits_file = catalogue_df.iloc[i].tellRed_file
          
        else:
            fits_file = catalogue_df.iloc[i]['{}_file'.format(color)]
            
        #Get file components
        CodeName, FileName, FileFolder  = dz.Analyze_Address(fits_file)

        print '--Treating:', CodeName, FileName, fits_file

        #Read the data
        redshift = catalogue_df.iloc[i]['z_{}'.format(color)]
        z_fits_file = fits_file.replace('.fits', '_z.fits')
                
        #IRAF task configuration
        dz_reduc.task_attributes['run folder']    = FileFolder
        dz_reduc.task_attributes['color']         = color
        dz_reduc.task_attributes['input']         = fits_file
        dz_reduc.task_attributes['output']        = z_fits_file
        dz_reduc.task_attributes['redshift']      = redshift
        dz_reduc.task_attributes['flux']          = 'yes'
        dz_reduc.run_iraf_task('dopcor')
          
        #Store file address in dataframe
        catalogue_df.loc[CodeName, 'z{}_file'.format(color)] = z_fits_file
                
        #Load spectrum
        wave, flux, ExtraData = dz.get_spectra_data(fits_file)
        wave_z, flux_z, ExtraData_z = dz.get_spectra_data(z_fits_file)
         
        dz.data_plot(wave, flux, label = '{} {} arm'.format(CodeName, color))
        dz.data_plot(wave_z, flux_z, label = '{} {} arm redshift corrected'.format(CodeName,color))
         
    #Wording for the figure  
    dz.FigWording(r'Wavelength $(\AA)$', 'Flux ' + r'$(erg\,cm^{-2} s^{-1} \AA^{-1})$', 'Redshift correction')
     
    #Store the figure
    output_address = FileFolder + script_code + '_' + CodeName + '_RedShiftCorrection'
    dz.save_manager(output_address, save_pickle = True)

dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')
 
print 'Data treated'


