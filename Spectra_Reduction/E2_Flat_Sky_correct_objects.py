import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()
  
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Output files flag
data_dict = {'reduc_tag': 'flat_cor'}

#Loop through the arms
colors = ['Blue', 'Red']
for arm_color in colors:
 
    #Same illumination frame for all the objects
    index_illumination  = (dz.reducDf.reduc_tag == 'illumFrame') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
    illum_address       = dz.reducDf.loc[index_illumination, 'file_location'].values[0] + dz.reducDf.loc[index_illumination, 'file_name'].values[0]
     
    for obj_target in dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']:
                   
        #Get the right flat
        index_objflat    = (dz.reducDf.reduc_tag == obj_target + '_flatobj_n') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) 
        obj_flat_address = dz.reducDf.loc[index_objflat, 'file_location'].values[0] + dz.reducDf.loc[index_objflat, 'file_name'].values[0]
        
        #Get the targets indeces
        if obj_target in dz.observation_dict['objects']:
            idx_target  = (dz.reducDf.frame_tag == obj_target) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal_imComb') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)             
        elif obj_target in dz.observation_dict['Standard_stars']:
            idx_target  = (dz.reducDf.frame_tag == obj_target) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file) 

        #List of files belonging to that target
        Target_folders  = dz.reducDf.loc[idx_target, 'file_location'].values 
        Target_names    = dz.reducDf.loc[idx_target, 'file_name'].values
        
        #We may have more than one frame at different conditions
        for i in range(len(Target_names)):
            input_file = Target_names[i]
            if obj_target in dz.observation_dict['objects']:
                output_file = Target_folders[i] + input_file[0:input_file.rfind('.')] + '_f.fits' 
            elif obj_target in dz.observation_dict['Standard_stars']:
                if dz.reducDf.loc[(dz.reducDf.file_name == input_file), 'ISISLITW'].values > 2:
                    slt_Width = 'Wide'
                else:
                    slt_Width = 'Narrow'
                output_file = '{run_folder}{CodeName}_{color}_{width_slit}_f.fits'.format(run_folder = Target_folders[i], CodeName = obj_target, color=arm_color, width_slit=slt_Width)        
                 
            #Task configuration
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['run folder']    = Target_folders[i]
            dz.task_attributes['input']         = Target_folders[i] + input_file
            dz.task_attributes['output']        = output_file    
            dz.task_attributes['flatcor']       = 'yes'
            dz.task_attributes['flat']          = obj_flat_address
            dz.task_attributes['illumco']       = 'yes' 
            dz.task_attributes['illum']         = illum_address
              
            #Run the task
            dz.run_iraf_task('ccdproc')
                       
            #Add objects to data frame with the new reduc_tag
            dz.object_to_dataframe(output_file, data_dict)
      
#Generate pdf file
idx_print = (dz.reducDf.reduc_tag == 'flat_cor') | (dz.reducDf.frame_tag.isin(dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal_imComb'))
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'target_frames_flatcor', plots_type='flat_calibration', ext = 0)
         
print 'Data treated'
