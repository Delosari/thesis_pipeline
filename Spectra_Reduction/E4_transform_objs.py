import os
import sys
from shutil import copyfile
from numpy.core import defchararray as np_f
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
from DZ_observation_reduction import spectra_reduction
 
#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Arm colors
data_dict = {'reduc_tag': 'wave_calibrated'}

#Loop through the arms
colors = ['Blue', 'Red'] 
for arm_color in colors:
    
    for obj_target in dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']:
    
        #Get the arc
        arc_run         = map(float ,dz.observation_dict[obj_target + '_arc'])  #This must be changed to a df
        arc_idx         = (dz.reducDf.reduc_tag == 'arc_trim') & (dz.reducDf.RUN.isin(arc_run)) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)  
        arc_filename    = dz.reducDf.loc[arc_idx, 'file_name'].values[0]
        arc_code        = arc_filename[0:arc_filename.rfind('.')]
    
        #Get the object
        index_object    = (dz.reducDf.reduc_tag == 'trim_image') & (dz.reducDf.frame_tag == obj_target) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check())    
        Files_Folder    = dz.reducDf.loc[index_object, 'file_location'].values
        Files_Name      = dz.reducDf.loc[index_object, 'file_name'].values
        output_names    = np_f.replace(Files_Name.astype(str), '.fits', '_w.fits')
        
        for j in range(len(Files_Name)):  
            dz.task_attributes['run folder']    = Files_Folder[j]
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = Files_Folder[j] + Files_Name[j]
            dz.task_attributes['output']        = Files_Folder[j] + output_names[j]
            dz.task_attributes['fitnames']      = arc_code
  
            #Moving the data base to the obj/standard folder
            if not os.path.exists(dz.task_attributes['run folder'] + 'database/'):
                os.makedirs(dz.task_attributes['run folder'] + 'database/') 
            
            input_arc_code  = '{in_folder}database/fc{arc_code}'.format(in_folder = dz.reducFolders['arcs'], arc_code = arc_code)
            output_arc_code = '{out_folder}database/fc{arc_code}'.format(out_folder = dz.task_attributes['run folder'], arc_code = arc_code)           
            copyfile(input_arc_code, output_arc_code)
            
            #Run the task
            dz.run_iraf_task('transform')
 
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)

            #Clear the dict
            dz.reset_task_dict()

print 'Data treated'
