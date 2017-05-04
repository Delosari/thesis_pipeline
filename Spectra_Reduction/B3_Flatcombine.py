from DZ_observation_reduction   import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()

#Entries for new files
data_dict = {'reduc_tag': 'flatcombine'}
 
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms
colors = ['Blue', 'Red']
  
for arm_color in colors:
  
    #Get the files we are going to treat
    indeces_arm  = (dz.reducDf.reduc_tag == 'biascorr') & (dz.reducDf.frame_tag == 'flat') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
      
    file_location   = dz.reducDf[indeces_arm].file_location.values.astype(str)
    file_names      = dz.reducDf[indeces_arm].file_name.values.astype(str)
      
    dz.task_attributes['color']         = arm_color
    dz.task_attributes['input array']   = dz.reducDf.loc[indeces_arm, 'file_location'].values + dz.reducDf.loc[indeces_arm, 'file_name'].values
    dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['flat lamp'])
    dz.task_attributes['in_list_name']  = 'in_files_to_flatCombine_{color}.list'.format(color = dz.task_attributes['color'])
    dz.task_attributes['input']         = '@{folder_run}{list_name}'.format( folder_run = dz.task_attributes['run folder'], list_name = dz.task_attributes['in_list_name'])
    dz.task_attributes['output']        = '{folder_output}flat_combine_{color}.fits'.format(folder_output = dz.task_attributes['run folder'], color = dz.task_attributes['color'])
    dz.task_attributes['combine']       = 'median'
    dz.task_attributes['reject']        = 'crreject'
    dz.task_attributes['scale']         = 'mode'
    dz.task_attributes['ccdtype']       = '""'
    dz.task_attributes['gain']          = 'gain'
    dz.task_attributes['snoise']        = 'readnois'
          
    #Run the task
    dz.run_iraf_task('flatcombine')
        
    #Add objects to data frame with the new frame_tag
    dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
    
#Generate pdf file
idx_print = (dz.reducDf.reduc_tag == 'flatcombine') | ((dz.reducDf.reduc_tag == 'biascorr') & (dz.reducDf.frame_tag == 'flat'))
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'flat_combines', ext = 0, include_graph=True, sorting_pattern = ['ISIARM', 'reduc_tag'])

dz.beep_alarmn()

print 'Data treated'


