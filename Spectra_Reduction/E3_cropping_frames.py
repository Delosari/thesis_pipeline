from DZ_observation_reduction   import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()
  
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms
colors = ['Blue', 'Red']

data_dict = {'reduc_tag' : 'trim_image'}

for arm_color in colors:
    
    cropping                = dz.observation_dict[arm_color + '_cropping']
    cropping_region         = '[{rawA}:{rawB},{columnA}:{columnB}]'.format(rawA=cropping[0], rawB=cropping[1],columnA=cropping[2], columnB=cropping[3])

    indeces_targetframes    = (dz.reducDf.reduc_tag == 'flat_cor') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check())  
  
    Files_Folders           = dz.reducDf.loc[indeces_targetframes, 'file_location'].values
    Files_Names             = dz.reducDf.loc[indeces_targetframes, 'file_name'].values
 
    for i in range(len(Files_Names)):
        
        output_name                         = Files_Names[i][0:Files_Names[i].find('.')] + '_t.fits'
        dz.task_attributes['run folder']    = Files_Folders[i]
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['input']         = Files_Folders[i] + Files_Names[i] + cropping_region
        dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.task_attributes['run folder'], output_name = output_name)   
    
        #Run the task
        dz.run_iraf_task('imcopy')
            
        #Add objects to data frame with the new frame_tag
        dz.object_to_dataframe(dz.task_attributes['output'], data_dict)        
            
#Print pdfs
indeces_print = (dz.reducDf.reduc_tag == 'trim_image')
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'trim_images', ext = 0, include_graph=False)  
     
print 'Data treated'


