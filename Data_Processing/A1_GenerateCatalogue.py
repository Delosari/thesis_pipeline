import pandas as pd
from numpy import loadtxt
from dazer_methods import Dazer
from collections import OrderedDict

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#Generate dazer object
dz = Dazer()

format_file = '/home/vital/git/Dazer/Dazer/dazer/bin/catalogue_dataframe_format.dz'

#We load the export dataframe
objects_folder  = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/'
export_df       = pd.read_pickle('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/transition_df')

key_codes, description, latex_format = loadtxt(format_file, dtype=str, delimiter=';', unpack=True)

#Rows indeces and columns from the dataframe
objlist_exported   = list(OrderedDict.fromkeys(export_df.folder_code.values)) #trick to keep the order
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

for objcode in objlist_exported:
    
    #Data from arm
    for color in ['Blue', 'Red']:
     
        calibration = 'fglobal'
        file_address = '{root_folder}{obj_folder}/{code_obj}_{color}_{calib}.fits'.format(root_folder=objects_folder, obj_folder=objcode, code_obj=objcode, color=color, calib=calibration) 
        wavelength, Flux_array, Header_0 = dz.get_spectra_data(file_address)
 
        catalogue_df.loc[objcode, 'calibration'] = calibration
        catalogue_df.loc[objcode, '{}_file'.format(color)] = file_address
        catalogue_df.loc[objcode, 'Wmin_{}'.format(color)] = wavelength[0]
        catalogue_df.loc[objcode, 'Wmax_{}'.format(color)] = wavelength[-1]
        catalogue_df.loc[objcode, '{}_Grating'.format(color)] = Header_0['ISIGRAT']
        catalogue_df.loc[objcode, '{}_CENWAVE'.format(color)] = Header_0['CENWAVE']
    
    #Data from night
    catalogue_df.loc[objcode, 'Dichroic']   = Header_0['ISIDICHR']
    catalogue_df.loc[objcode, 'RA']         = Header_0['RA']
    catalogue_df.loc[objcode, 'DEC']        = Header_0['DEC']
    catalogue_df.loc[objcode, 'UT_OBS']     = pd.to_datetime('{}T{}'.format(Header_0['DATE-OBS'], Header_0['UTSTART']))
    
    #Data from export
    idx = (export_df.folder_code == objcode)
    catalogue_df.loc[objcode, 'objcode']            = export_df.objcode.loc[idx].values[0]
    catalogue_df.loc[objcode, 'obsfolder']          = export_df.loc[idx, 'obsfolder'].values[0]
    catalogue_df.loc[objcode, 'Standard_stars']     = ';'.join(export_df.loc[idx, 'Standard_stars'].values[0])
    catalogue_df.loc[objcode, 'obscode']            = export_df.loc[idx, 'obscode'].values[0]
    catalogue_df.loc[objcode, 'calibration_star']   = ';'.join(export_df.loc[idx, 'calibration_star'].values[0])
    catalogue_df.loc[objcode, 'reduc_tag']          = export_df.loc[idx, 'reduc_tag'].values[0]
    catalogue_df.loc[objcode, 'aperture']           = export_df.loc[idx, 'aperture'].values[0]
       
#Output catalogue
print catalogue_df.columns
dz.save_excel_DF(catalogue_df, '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx', df_sheet_format = 'catalogue_data')

# #Store the dataframe
# frame_address = objects_folder.replace('objects/', 'catalogue_df')
# dz.save_dataframe(catalogue_df, frame_address)


# import pandas as pd
# from numpy import loadtxt
# from dazer_methods import Dazer
# from collections import OrderedDict
# 
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# 
# #Generate dazer object
# dz = Dazer()
# 
# format_file = '/home/vital/git/Dazer/Dazer/dazer/bin/catalogue_dataframe_format.dz'
# 
# #We load the export dataframe
# objects_folder  = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/'
# export_df       = pd.read_pickle('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/transition_df')
# 
# key_codes, description, latex_format = loadtxt(format_file, dtype=str, delimiter=';', unpack=True)
# 
# #Rows indeces and columns from the dataframe
# list_exported   = list(OrderedDict.fromkeys(export_df.folder_code.values)) #trick to keep the order
# catalogue_df    = pd.DataFrame(columns = key_codes)
# 
# print list_exported
# 
# for objcode in list_exported:
#     
#     #Data from arm
#     for color in ['Blue', 'Red']:
#      
#         calibration = 'fglobal'
#         file_address = '{root_folder}{obj_folder}/{code_obj}_{color}_{calib}.fits'.format(root_folder=objects_folder, obj_folder=objcode, code_obj=objcode, color=color, calib=calibration) 
#         wavelength, Flux_array, Header_0 = dz.get_spectra_data(file_address)
#  
#         catalogue_df.loc[objcode, 'calibration'] = calibration
#         catalogue_df.loc[objcode, '{}_file'.format(color)] = file_address
#         catalogue_df.loc[objcode, 'Wmin_{}'.format(color)] = wavelength[0]
#         catalogue_df.loc[objcode, 'Wmax_{}'.format(color)] = wavelength[-1]
#         catalogue_df.loc[objcode, '{}_Grating'.format(color)] = Header_0['ISIGRAT']
#         catalogue_df.loc[objcode, '{}_CENWAVE'.format(color)] = Header_0['CENWAVE']
#     
#     #Data from night
#     catalogue_df.loc[objcode, 'Dichroic']   = Header_0['ISIDICHR']
#     catalogue_df.loc[objcode, 'RA']         = Header_0['RA']
#     catalogue_df.loc[objcode, 'DEC']        = Header_0['DEC']
#     catalogue_df.loc[objcode, 'UT_OBS']     = pd.to_datetime('{}T{}'.format(Header_0['DATE-OBS'], Header_0['UTSTART']))
#     
#     #Data from export
#     idx = (export_df.folder_code == objcode)
#     catalogue_df.loc[objcode, 'objcode']            = export_df.objcode.loc[idx].values[0]
#     catalogue_df.loc[objcode, 'obsfolder']          = export_df.loc[idx, 'obsfolder'].values[0]
#     catalogue_df.loc[objcode, 'Standard_stars']     = export_df.loc[idx, 'Standard_stars'].values[0]
#     catalogue_df.loc[objcode, 'obscode']            = export_df.loc[idx, 'obscode'].values[0]
#     catalogue_df.loc[objcode, 'calibration_star']   = export_df.loc[idx, 'calibration_star'].values[0]
#     catalogue_df.loc[objcode, 'reduc_tag']          = export_df.loc[idx, 'reduc_tag'].values[0]
#     catalogue_df.loc[objcode, 'aperture']           = export_df.loc[idx, 'aperture'].values[0]
#        
# #Output catalogue
# print catalogue_df
# 
# #Store the dataframe
# frame_address = objects_folder.replace('objects/', 'catalogue_df')
# dz.save_dataframe(catalogue_df, frame_address)




