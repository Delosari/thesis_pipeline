import pyfits
from numpy                      import zeros, median, mean, empty, argsort
from DZ_observation_reduction   import spectra_reduction
from astropy.visualization      import ZScaleInterval

#Load iraf pypeline object
dz = spectra_reduction()
  
#Entries for new files
data_dict = {'reduc_tag': 'obj_combine'}

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Frames to combine
tag_to_combine = dz.observation_dict['tag_to_combine'][0]

#Loop through the arms
colors = ['Blue', 'Red']
for arm_color in colors:
           
    obj_scaling_key = '{Color}_scale_region'.format(Color=arm_color)
    stats_section   = map(int, dz.observation_dict[obj_scaling_key])
         
    for obj_target in dz.observation_dict['objects']:
           
        #Get the right flat        
        indeces_objframes = (dz.reducDf.frame_tag == obj_target) & (dz.reducDf.reduc_tag == tag_to_combine) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check())
      
        #Frames properties
        Files_Folders   = dz.reducDf.loc[indeces_objframes, 'file_location'].values
        Files_Names     = dz.reducDf.loc[indeces_objframes, 'file_name'].values
        frame_number    = len(Files_Names)
        
        if frame_number > 1:
                           
            #Getting the effective air mass from each frame
            air_eff_array   = zeros(frame_number)
            median_values   = empty(frame_number)
            for i in range(len(Files_Names)):
                File_Address        = Files_Folders[i] + Files_Names[i]
                frame_data          = pyfits.getdata(File_Address, 0)
                air_eff_array[i]    = pyfits.getval(File_Address, 'AIRMASS', 0)
                median_values[i]    = median(frame_data[stats_section[2]:stats_section[3],stats_section[0]:stats_section[1]])
                     
            #Calculate effective airmass
            if frame_number == 2:
                Airmass_combine = (air_eff_array[0] + air_eff_array[1]) / 2            
            if frame_number == 3:
                Airmass_combine = (air_eff_array[0] + 4 * air_eff_array[1] + air_eff_array[2]) / 6
            else:
                Airmass_combine = air_eff_array.mean()
                
            #Sort names according to max median
            Files_Names     = Files_Names[median_values.argsort()[::-1]]
            Sorted_median   = median_values[median_values.argsort()[::-1]]
                
            #Ready task configuration
            output_name                         = '{CodeName}_{color}.fits'.format(CodeName = obj_target.replace('[','').replace(']',''), color = arm_color)
            dz.task_attributes['run folder']    = dz.reducFolders['objects']
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = ','.join(list(Files_Folders + Files_Names))
            dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.reducFolders['objects'], output_name = output_name)     
            dz.task_attributes['combine']       = 'median'
            dz.task_attributes['scale']         = 'none'
            dz.task_attributes['statsec']       = '[{XA}:{XB},{YA}:{YB}]'.format(XA=stats_section[0],XB=stats_section[1],YA=stats_section[2],YB=stats_section[3])
            dz.task_attributes['reject']        = 'crreject'
            dz.task_attributes['weight']        = '""'             
            dz.task_attributes['gain']          = 'GAIN'
            dz.task_attributes['snoise']        = 'READNOIS'
                                       
            #Run the task
            dz.run_iraf_task('imcombine', run_externally=False)
                           
            #Pause to check task output   
            #raw_input("\nPress Enter to continue...")
                                
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
                             
            #Setting the new airmass value
            pyfits.setval(filename = dz.task_attributes['output'], keyword = 'AIRMASS', value = Airmass_combine)
                              
#New files
if tag_to_combine == 'frame_shifted':
    idx_print = (dz.reducDf.reduc_tag == 'obj_combine') | ((dz.reducDf.reduc_tag == 'frame_shifted') & (dz.reducDf.frame_tag.isin(dz.observation_dict['objects'])) & (dz.target_validity_check()))
    dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'target_combined_shiftedframes', ext = 0, plots_type = 'frame_combine_shifted')
else:
    idx_print = (dz.reducDf.reduc_tag == 'obj_combine') | ((dz.reducDf.reduc_tag == 'cosmic_ray_removal') & (dz.reducDf.frame_tag.isin(dz.observation_dict['objects'])) & (dz.target_validity_check()))
    dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'target_combinedframes', ext = 0, plots_type = 'frame_combine')

   
print 'Data treated'


