import pandas       as pd
from os             import makedirs
from astropy.io     import fits
from os.path        import isdir
from dazer_methods  import Dazer
from shutil         import rmtree, copy
from collections    import OrderedDict
from numpy          import loadtxt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
   
dz = Dazer()
 
#Input and output locations
input_folders = OrderedDict()
input_folders['WHT_2016_10_n1'] = '/home/vital/Astrodata/WHT_2016_10/'     
  
input_folders['WHT_2016_04_n1'] = '/home/vital/Astrodata/WHT_2016_04/Night1/'
input_folders['WHT_2016_04_n2'] = '/home/vital/Astrodata/WHT_2016_04/Night2/'                

input_folders['WHT_2011_11_n1'] = '/home/vital/Astrodata/WHT_2011_11/Night1/'
input_folders['WHT_2011_11_n2'] = '/home/vital/Astrodata/WHT_2011_11/Night2/'

input_folders['WHT_2011_09_n1'] = '/home/vital/Astrodata/WHT_2011_09/Night1/'
input_folders['WHT_2011_09_n2'] = '/home/vital/Astrodata/WHT_2011_09/Night2/'

input_folders['WHT_2011_01_n2'] = '/home/vital/Astrodata/WHT_2011_01/Night2/'

input_folders['WHT_2009_07_n1'] = '/home/vital/Astrodata/WHT_2009_07/Night1/'
input_folders['WHT_2009_07_n2'] = '/home/vital/Astrodata/WHT_2009_07/Night2/'           

input_folders['WHT_2008_01_n2'] = '/home/vital/Astrodata/WHT_2008_01/Night2/'

output_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/objects/'

#Set figure format
dz.FigConf()

#Create the catalogue dataframe 
key_codes = ['codename', 'objcode', 'obscode', 'obsfolder', 'Standard_stars', 'time_obs', 'arm_color', 'aperture', 'parent_file_address', 'reduc_tag', 'calibration_star'] #Codename will become the index in the final dataframe

transition_catalogue = pd.DataFrame()
   
#--Load the data in the data frame
for obs in input_folders:
    
    data_folder = input_folders[obs]
    dz.reducDf = dz.load_reduction_dataframe(data_folder)
    dz.observation_dict = dz.load_observation_dict(data_folder + 'observation_properties.txt')
    standard_stars = dz.observation_dict['Standard_stars']
    
    #Move the objects
    for target_object in dz.observation_dict['objects']:
               
        objcode = target_object.translate(None, "[]")
        calibration_stars = dz.observation_dict['{}_calibration_star'.format(target_object)]
                
        print '--', objcode
                                 
        #Move the files to their folder
        for arm_color in ['Blue', 'Red']:
            for calibration in ['flocal', 'fglobal']:
                
                #Locate the file
                reduction_tag   = 'flux_calibrated_objects_' + calibration
                idx_target      = (dz.reducDf.frame_tag == target_object) & (dz.reducDf.reduc_tag == reduction_tag) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))           
                fits_address    = dz.reducDf.file_location[idx_target].values[0] + dz.reducDf.file_name[idx_target].values[0]

                #Get header
                wavelength, Flux_array, Header_0 = dz.get_spectra_data(fits_address)
                 
                #Data to store
                night_obs       = Header_0['DATE-OBS']
                time_obs        = pd.to_datetime('{}T{}'.format(night_obs, Header_0['UTSTART']))
                appertures_n    = int(Header_0['NAXIS2']) if 'NAXIS2' in Header_0 else 1
                
                #Create one entry for each apperture
                for aperture in range(appertures_n):
                                                    
                    properties_dict = {}
                    properties_dict['objcode']              = objcode
                    properties_dict['obscode']              = obs
                    properties_dict['obsfolder']            = data_folder
                    properties_dict['time_obs']             = time_obs
                    properties_dict['arm_color']            = arm_color
                    properties_dict['aperture']             = aperture + 1
                    properties_dict['parent_file_address']  = fits_address
                    properties_dict['reduc_tag']            = reduction_tag
                    properties_dict['Standard_stars']       = standard_stars
                    properties_dict['calibration_star']     = calibration_stars

                    transition_catalogue = transition_catalogue.append(properties_dict, ignore_index=True)
                    
transition_catalogue = transition_catalogue.ix[:,key_codes] #Organize columns by initial format
transition_catalogue.aperture = transition_catalogue.aperture.astype(int) #This row must be integers

#--Define spectra and file folders for cases of different arms, appertures, nights...
catalogue_objects = transition_catalogue.objcode.unique()
 
for obj in catalogue_objects:
     
    idcs            = (transition_catalogue.objcode == obj) 
    observations    = list(transition_catalogue.obscode[idcs].unique())
    appertures      = transition_catalogue.aperture[idcs].unique()
    match_idcs      = transition_catalogue.loc[idcs].index.tolist()
         
    for i in range(len(match_idcs)):
        ind_fits = match_idcs[i]
         
        #Get the night of the observation
        if len(observations) == 1:
            extension_night = ''
        else:
            extension_night = '_n{}'.format(observations.index(transition_catalogue.obscode[ind_fits]) + 1)
         
        #Get the color of the observatoin
        extension_color         = '_' + transition_catalogue.arm_color[ind_fits]
         
        #Get the calibration extension
        extension_calibration   = '_flocal' if 'flocal' in transition_catalogue.parent_file_address[ind_fits] else '_fglobal'
 
        #Get the apperture extension
        if len(appertures) == 1:
            extension_appertures    = ''
        else: 
            extension_appertures    = '_A{}'.format(transition_catalogue.aperture[ind_fits])
  
        #Load the data to the table        
        label_name = obj + extension_night + extension_appertures + extension_color + extension_calibration
        transition_catalogue.loc[ind_fits, 'codename']          = label_name
        transition_catalogue.loc[ind_fits, 'folder_address']    = output_folder + obj + extension_night + extension_appertures +'/'
        transition_catalogue.loc[ind_fits, 'file_name']         = label_name + '.fits'
        transition_catalogue.loc[ind_fits, 'folder_code']       = obj + extension_night + extension_appertures
         

#Change the indeces to the code name
transition_catalogue = transition_catalogue.set_index('codename')      

print transition_catalogue

#Move the files
for idx in transition_catalogue.index.tolist():
    src_file            = transition_catalogue.parent_file_address[idx]
    current_object      = transition_catalogue.objcode[idx]
 
    appertures_forObject = transition_catalogue.loc[transition_catalogue.objcode == current_object].aperture.unique()
         
    #Case with one apperture
    if len(appertures_forObject) == 1:
        target_file = transition_catalogue.folder_address[idx] + transition_catalogue.file_name[idx]
          
        if not isdir(transition_catalogue.folder_address[idx]):
            makedirs(transition_catalogue.folder_address[idx])
          
        copy(src_file, target_file)
        print src_file, '->', target_file
      
    #Case with several apperatures we only copy the one we want
    else:
        if not isdir(transition_catalogue.folder_address[idx]):
            makedirs(transition_catalogue.folder_address[idx])
          
        target_file = transition_catalogue.folder_address[idx] + transition_catalogue.file_name[idx]
                  
        wavelength, Flux_array, Header_0 = dz.get_spectra_data(src_file) #This header is not the same...
        
        #Dirty trick for the WHT Change order
        if transition_catalogue.aperture[idx] == 1:
            number_for_apperture = 0
        elif transition_catalogue.aperture[idx] == 2:
            number_for_apperture = 1
            
        if 'Red' in target_file:
            number_for_apperture = 0 if number_for_apperture == 1 else 1
                    
        data_apperture  = Flux_array[number_for_apperture]
          
        fits.writeto(target_file, data_apperture, Header_0, overwrite=True)
         
        print src_file, '->', target_file
      
#Store the dataframe
frame_address = output_folder.replace('objects/', 'transition_df')
dz.save_dataframe(transition_catalogue, frame_address)
 
print 'Data treated'
 
 
 
 
 