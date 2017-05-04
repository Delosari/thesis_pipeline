import pandas as pd
from dazer_methods import Dazer

#Create class object
dz = Dazer()
script_code = dz.get_script_code()

#Load catalogue dataframe
catalogue_dict      = dz.import_catalogue()
catalogue_df        = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
lineslog_extension  = '_' + catalogue_dict['Datatype'] + '_linesLog_emission_2nd.txt'#First data log for reduced spectra
lickIndcs_extension = '_lick_indeces.txt'
fits_file_Ext       = '_Emission_2nd.fits'


# Forcing the remake of new files
dz.RemakeFiles = True

n_objects = len(catalogue_df.index)

#Loop through the objects
for objName in catalogue_df.index:
        
    #Object
    objName             = catalogue_df.loc[objName].name
    fits_file           = objName + fits_file_Ext
    ouput_folder        = '{}{}/'.format(catalogue_dict['Obj_Folder'], objName) 
    
    #Output lines log dataframe
    lineslog_df         = pd.DataFrame(columns=dz.saving_parameters_list)
    lines_log_address   = ouput_folder + objName + lineslog_extension
   
    print '\n-- Treating {} @ {}'.format(objName, fits_file), catalogue_df.index.get_loc(objName), '/', n_objects

    #Spectrum data
    wave, flux, header_0 = dz.get_spectra_data(ouput_folder + fits_file)
            
    lick_idcs_df = pd.read_csv(ouput_folder + objName + lickIndcs_extension, delim_whitespace = True, header = 0, index_col = 0, comment='L') #Dirty trick to avoid the Line_label row
     
    #Start to loop through recorded line 
    for i in range(len(lick_idcs_df.index)):
         
        try:
            
            print '-- Treating line:', lick_idcs_df.iloc[i].name  
                      
            #Establish current line
            dz.Current_Label    = lick_idcs_df.iloc[i].name
            dz.Current_Ion      = lick_idcs_df.iloc[i].Ion
            dz.Current_TheoLoc  = lick_idcs_df.iloc[i].lambda_theo
            selections = lick_idcs_df.iloc[i][3:9].values
            
            #Proceed to measure
            line_data = dz.measure_line(wave, flux, selections, lineslog_df, Measuring_Method = 'MC_lmfit', store_data = True)
            
        except:
            dz.log_emLine_error(objName, dz.Current_Label)
            
    dz.save_lineslog_dataframe(lineslog_df, lines_log_address)
    print '-', lines_log_address, 'saving'
                                                                 
print "\nAll data treated", dz.display_errors('emLine measurement', extra_verbose=True)










