import os
import sys
from numpy import in1d
from pyfits import getval
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction
from shutil import copyfile

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms
colors = ['Blue','Red']
first_time_running = True


#Which slit to use WARNING no me gusta
slit_minimum = float(dz.observation_dict['slit_minimum'][0])  #Normally this should be 2
if slit_minimum < 2.0:
    slit_for_calibration = ['narrow']
else:
    slit_for_calibration = ['wide']

#---Delete global files #THESE FILES SHOULD BE INCLUDED IN THE DATAFRAME
default_standard_files = ['std_Blue_narrow.txt', 'std_Blue_wide.txt', 'std_Red_narrow.txt', 'std_Red_wide.txt']
for standard_file in default_standard_files:
    if os.path.isfile(dz.reducFolders['objects'] + standard_file):
        os.remove(dz.reducFolders['objects'] + standard_file) 

#---Delete individual files
for arm_color in colors:
    for slit_size in slit_for_calibration:
        for star in dz.observation_dict['Standard_stars']:
            standard_file_local   = '{run_folder}std_{starcode}_{color}_{slit_size}.txt'.format(run_folder = dz.reducFolders['objects'], starcode = star, color = arm_color, slit_size = slit_size)
            if os.path.isfile(standard_file_local):
                os.remove(standard_file_local) 

#---Run the standard task
for arm_color in colors:
     
    for slit_size in slit_for_calibration:
                
        standard_file_global = '{run_folder}std_{color}_{slit_size}.txt'.format(run_folder = dz.reducFolders['objects'], color = arm_color, slit_size = slit_size)
 
        slit_indeces = (dz.reducDf.ISISLITW > slit_minimum) 
 
        indeces_Stars   = dz.reducDf.index[in1d(dz.reducDf['frame_tag'], dz.observation_dict['Standard_stars']) &
                                           (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) &
                                           (dz.reducDf.reduc_tag == 'extracted_spectrum') & slit_indeces &
                                           (dz.reducDf.valid_file)]
     
        Files_Folders   = dz.reducDf.loc[indeces_Stars, 'file_location'].values
        Files_Names     = dz.reducDf.loc[indeces_Stars, 'file_name'].values
        slit_width      = dz.reducDf.loc[indeces_Stars, 'ISISLITW'].values
        objects         = dz.reducDf.loc[indeces_Stars, 'frame_tag'].values
     
        for i in range(len(Files_Names)):
              
            #Change the current folder
            os.chdir(Files_Folders[i])
                     
            print '\n--GOING FOR', objects[i]
             
            standard_file_local   = '{run_folder}std_{starcode}_{color}_{slit_size}.txt'.format(run_folder = dz.reducFolders['objects'], starcode = objects[i], color = arm_color, slit_size = slit_size)
             
            calibration_dict = dz.standar_stars_calibrationFile(objects[i])
                  
            if calibration_dict['file name'] != None:
                         
                dz.task_attributes['run folder']    = Files_Folders[i]
                dz.task_attributes['color']         = arm_color
                dz.task_attributes['input']         = Files_Names[i]
                dz.task_attributes['output']        = standard_file_local  
         
                dz.task_attributes['star_name']     = calibration_dict['file name']
                dz.task_attributes['caldir']        = calibration_dict['calibration_folder']
                dz.task_attributes['bandwidth']     = calibration_dict['bandwidth']
                dz.task_attributes['bandsep']       = calibration_dict['bandsep']
                dz.task_attributes['airmass']       = getval(Files_Folders[i] + Files_Names[i], 'AIRMASS', 0)
                dz.task_attributes['exptime']       = getval(Files_Folders[i] + Files_Names[i], 'EXPTIME', 0)
                                                                      
                #Run the task
                dz.run_iraf_task('standard', run_externally=False, overwrite=False)
             
            #If global file does not exist, create and fill it with the data from the first star
            if os.path.isfile(standard_file_global) == False:
                copyfile(standard_file_local, standard_file_global)
             
            #otherwise append lines from current star to the global file
            else:
                with open(standard_file_global, "a") as outfile:
                    with open(standard_file_local, "rb") as infile:
                        outfile.write(infile.read())                
                 
         
print 'Data treated'


