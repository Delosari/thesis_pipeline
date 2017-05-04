from numpy                      import empty
from DZ_observation_reduction   import spectra_reduction
from shutil import copy as shu_copy
  
#Load iraf pypeline object
dz = spectra_reduction()
   
#Entries for new files
data_dict = {'reduc_tag': 'biascorr'}
 
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
 
#Search for objects we want to treat for bias
list_for_bias   = dz.observation_dict['Standard_stars'] + dz.observation_dict['objects'] + ['flat', 'arc', 'sky']
 
#Loop through the arms
colors = ['Blue', 'Red']
for arm_color in colors:
   
    #Get the files to bias correct
    indeces_arm     = (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.file_location.str.contains('raw_fits')) & dz.reducDf.frame_tag.isin(list_for_bias) & (dz.reducDf.valid_file)
    frames_type     = dz.reducDf.loc[indeces_arm, 'frame_tag'].values
    files_folders   = dz.reducDf.loc[indeces_arm, 'file_location'].values
    files_names     = dz.reducDf.loc[indeces_arm, 'file_name'].values
    
    #Get the correction files
    idx_zerofile    = (dz.reducDf.reduc_tag == 'master bias') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
    biasfile        = dz.reducDf.file_location[idx_zerofile].values[0] + dz.reducDf.file_name[idx_zerofile].values[0]
    fixfile         = '{folder_input}badpix_{color}mask'.format(folder_input = dz.Catalogue_folder, color = arm_color)
    print 'damelo', dz.observation_dict['biassec_regions']
    biassec_region  = '[{columnA}:{columnB},{rowA}:{rowB}]'.format(columnA=dz.observation_dict['biassec_regions'][0],columnB=dz.observation_dict['biassec_regions'][1],rowA=dz.observation_dict['biassec_regions'][2],rowB=dz.observation_dict['biassec_regions'][3])
    trimsec_region  = '[{columnA}:{columnB},{rowA}:{rowB}]'.format(columnA=dz.observation_dict['trimsec_regions'][0],columnB=dz.observation_dict['trimsec_regions'][1],rowA=dz.observation_dict['trimsec_regions'][2],rowB=dz.observation_dict['trimsec_regions'][3])

    #Make a security copy of the bias file
    backup_file     = biasfile[0:biasfile.rfind('.')] + '_backup.fits'
    shu_copy(biasfile, backup_file)
  
    #Generate the list of input and output files
    input_array     = files_folders + files_names + '[1]'
    input_list_name = 'in_files_to_biasCorrect_{color}.list'.format(color = arm_color)

    #Generate the output array
    output_array = empty(len(frames_type), dtype=object)
    for i in range(len(frames_type)):
        frame_object = frames_type[i]
        if frame_object in dz.observation_dict['objects']:
            output_folder = dz.reducFolders['objects']
        elif frame_object in dz.observation_dict['Standard_stars']:
            output_folder = dz.reducFolders['objects']
            
        elif frame_object == 'flat':
            output_folder = dz.reducFolders['flat lamp']
        elif frame_object == 'sky':
            output_folder = dz.reducFolders['flat sky']
        elif frame_object == 'arc':
            output_folder = dz.reducFolders['arcs']
    
        ouput_address = output_folder + files_names[i]
        if ouput_address.endswith('.fit'):
            ouput_address = ouput_address.replace('.fit', '_b.fits')
        elif ouput_address.endswith('.fits'):
            ouput_address = ouput_address.replace('.fits', '_b.fits')    
        output_array[i] = ouput_address
    
    #Set the task attributes
    dz.task_attributes['color']         = arm_color
    dz.task_attributes['run folder']    = dz.reducFolders['bias']
    dz.task_attributes['input array']   = input_array   
    dz.task_attributes['in_list_name']  = 'in_files_to_biasCorrect_{color}.list'.format(color = arm_color)

    dz.task_attributes['input']         = '@{folder_run}{list_name}'.format(folder_run = dz.task_attributes['run folder'], list_name = dz.task_attributes['in_list_name'])
    dz.task_attributes['output array']  = output_array
    dz.task_attributes['out_list_name'] = 'out_files_to_biasCorrect_{color}.list'.format(color = arm_color)
    dz.task_attributes['output']        = '@{folder_run}{list_name}'.format(folder_run = dz.task_attributes['run folder'], list_name = dz.task_attributes['out_list_name'])
    
    dz.task_attributes['fixpix']        = 'yes'
    dz.task_attributes['fixfile']       = fixfile
    dz.task_attributes['oversca']       = 'yes'
    dz.task_attributes['biassec']       = biassec_region
    dz.task_attributes['trim']          = 'yes'
    dz.task_attributes['trimsec']       = trimsec_region
    dz.task_attributes['zerocor']       = 'yes'     
    dz.task_attributes['zero']          = biasfile

    #Run the task
    dz.run_iraf_task('ccdproc', run_externally=False)
        
    #Add objects to data frame with the new frame_tag
    dz.object_to_dataframe(dz.task_attributes['output array'], data_dict)     

    #Save the ccdproc treated bias frame the bias file
    ccdproc_bias = biasfile.replace('.fits', '_b.fits')
    shu_copy(biasfile, ccdproc_bias)
    dz.object_to_dataframe(ccdproc_bias, {'reduc_tag': 'ccdproc_bias'})
    
    #Recover the bias file
    shu_copy(backup_file, biasfile)
    
#Generate pdf file
idx_print = (dz.reducDf.reduc_tag == 'biascorr')
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'bias_corrected', verbose=True, ext = 0)

dz.beep_alarmn()

print 'Data treated'