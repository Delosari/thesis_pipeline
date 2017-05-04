import pandas       as pd
from os             import makedirs
from astropy.io     import fits
from os.path        import isdir
from dazer_methods  import Dazer
from shutil         import rmtree, copy
from collections    import OrderedDict
  
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
   
dz = Dazer()
 
#Input and output locations
input_folders = [
    '/home/vital/Astrodata/WHT_2008_01/Night2/',
    '/home/vital/Astrodata/WHT_2009_07/Night1/',
    '/home/vital/Astrodata/WHT_2009_07/Night2/',
    '/home/vital/Astrodata/WHT_2011_11/Night1/',
    '/home/vital/Astrodata/WHT_2011_11/Night2/',
    '/home/vital/Astrodata/WHT_2016_04/Night1/',
    '/home/vital/Astrodata/WHT_2016_04/Night2/']
output_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/'

#Delete the folder contents
if isdir(output_folder):
    rmtree(output_folder)
 
catalogue_df        = pd.DataFrame()
catalogue_colums    = ['codename', 'objCode', 'folder_address', 'file_name', 'folder_code','night', 'time_obs', 'arm_color', 'aperture', 'parent_file_address', 'reduc_tag', 'telluric_star', 'telluric_file', 'chemistry_valid', ]
   
#--Load the data in the data frame
for data_folder in input_folders:
        
    dz.reducDf = dz.load_reduction_dataframe(data_folder)
    dz.observation_dict = dz.load_observation_dict(data_folder + 'observation_properties.txt')
    
    #Move the objects
    for target_object in dz.observation_dict['objects']:
                    
        code_name = target_object.translate(None, "[]")
                                  
        #Move the files to their folder
        for arm_color in ['Blue', 'Red']:
            for calibration in ['flocal', 'fglobal']:
                 
                reduction_tag   = 'flux_calibrated_objects_' + calibration
                idx_target      = (dz.reducDf.frame_tag == target_object) & (dz.reducDf.reduc_tag == reduction_tag) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))           
                fits_address    = dz.reducDf.file_location[idx_target].values[0] + dz.reducDf.file_name[idx_target].values[0]
                 
                wavelength, Flux_array, Header_0 = dz.get_spectra_data(fits_address)
                 
                if 'NAXIS2' in Header_0:
                    appertures_n = int(Header_0['NAXIS2'])
                else:
                    appertures_n = 1

                night_obs   = Header_0['DATE-OBS']
                time_obs    = pd.to_datetime('{}T{}'.format(night_obs, Header_0['UTSTART']))
                
                if (night_obs == '2011-12-02') and (code_name == '4'): #Trick in for observations which are set to a new night
                    night_obs = '2011-12-01'
                
                for aperture in range(appertures_n):
                                                    
                    properties_dict = OrderedDict().fromkeys(catalogue_colums)
                    properties_dict['objCode']              = code_name
                    properties_dict['night']                = night_obs
                    properties_dict['time_obs']             = time_obs
                    properties_dict['arm_color']            = arm_color
                    properties_dict['aperture']             = aperture + 1
                    properties_dict['parent_file_address']  = fits_address
                    properties_dict['reduc_tag']            = reduction_tag
                         
                    catalogue_df = catalogue_df.append(properties_dict, ignore_index=True)
                   
catalogue_df            = catalogue_df.ix[:,catalogue_colums] #Organize columns by initial format
catalogue_df.aperture   = catalogue_df.aperture.astype(int)

#--Define spectra and file folders
catalogue_objects = catalogue_df.objCode.unique()

for obj in catalogue_objects:
    
    idcs            = (catalogue_df.objCode == obj) 
    nights          = list(catalogue_df.night[idcs].unique())
    appertures      = catalogue_df.aperture[idcs].unique()
    
    match_idcs  = catalogue_df.loc[idcs].index.tolist()
        
    for i in range(len(match_idcs)):
        ind_fits = match_idcs[i]
        
        #Get the night of the observation
        if len(nights) == 1:
            extension_night = ''
        else:
            extension_night = '_n{}'.format(nights.index(catalogue_df.night[ind_fits]) + 1)
        
        #Get the color of the observatoin
        extension_color         = '_' + catalogue_df.arm_color[ind_fits]
        
        #Get the calibration extension
        extension_calibration   = '_flocal' if 'flocal' in catalogue_df.parent_file_address[ind_fits] else '_fglobal'

        #Get the apperture extension
        if len(appertures) == 1:
            extension_appertures    = ''
        else: 
            extension_appertures    = '_A{}'.format(catalogue_df.aperture[ind_fits])

        #Load the data to the table
        label_name = obj + extension_night + extension_appertures + extension_color + extension_calibration
        catalogue_df.loc[ind_fits, 'codename']          = label_name
        catalogue_df.loc[ind_fits, 'folder_address']    = output_folder + obj + extension_night + extension_appertures +'/'
        catalogue_df.loc[ind_fits, 'file_name']         = label_name + '.fits'
        catalogue_df.loc[ind_fits, 'folder_code']       = obj + extension_night + extension_appertures
                
#Change the indeces to the code name
catalogue_df = catalogue_df.set_index('codename')      

#Move the files
for idx in catalogue_df.index.tolist():
    src_file            = catalogue_df.parent_file_address[idx]
    current_object      = catalogue_df.objCode[idx]

    appertures_forObject = catalogue_df.loc[catalogue_df.objCode == current_object].aperture.unique()
        
    #Case with one apperture
    if len(appertures_forObject) == 1:
        target_file = catalogue_df.folder_address[idx] + catalogue_df.file_name[idx]
         
        if not isdir(catalogue_df.folder_address[idx]):
            makedirs(catalogue_df.folder_address[idx])
         
        copy(src_file, target_file)
        print src_file, '->', target_file
     
    #Case with several apperatures we only copy the one we want
    else:
        if not isdir(catalogue_df.folder_address[idx]):
            makedirs(catalogue_df.folder_address[idx])
         
        target_file = catalogue_df.folder_address[idx] + catalogue_df.file_name[idx]
                 
        wavelength, Flux_array, Header_0 = dz.get_spectra_data(src_file) #This header is not the same...
 
        data_apperture  = Flux_array[catalogue_df.aperture[idx] - 1]
         
        fits.writeto(target_file, data_apperture, Header_0)
         
        print src_file, '->', target_file
    
print catalogue_df.folder_code

#Store the dataframe
frame_address = output_folder.replace('objects/', 'reduction_export_df')
catalogue_df.to_pickle(frame_address)
  
            