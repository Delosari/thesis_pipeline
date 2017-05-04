from pyfits import getval
from DZ_observation_reduction import spectra_reduction
 
#Load iraf pypeline object
dz = spectra_reduction()
   
#Entries for new files
data_dict = {'reduc_tag':'master bias'}
 
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms
colors = ['Blue', 'Red']
for arm_color in colors:
     
    #Get the files to treat
    indx = (dz.reducDf.reduc_tag == 'bias') & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color)) & (dz.reducDf.valid_file)
    list_file_names = dz.reducDf.loc[indx, 'file_name'].values
     
    #Task configuration
    dz.task_attributes['input array']   = dz.reducFolders['raw data'] + list_file_names + '[1]'
    dz.task_attributes['color']         = arm_color
    dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['bias'])
    dz.task_attributes['in_list_name']  = 'bias_{color}.list'.format(color = dz.task_attributes['color'])
    dz.task_attributes['input']         = '@{folder_run}{in_list_name}'.format( folder_run = dz.task_attributes['run folder'], in_list_name = dz.task_attributes['in_list_name'])
    dz.task_attributes['output']        = '{folder_output}master_bias_{color}.fits'.format(folder_output = dz.task_attributes['run folder'], color = dz.task_attributes['color'])
    dz.task_attributes['combine']       =  'median'
    
    #Run the task
    dz.run_iraf_task('zerocombine')
    dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
   
#Display biassec, trimsec data
indeces_print = (dz.reducDf.reduc_tag == 'master bias')
list_mBias = dz.reducDf.loc[indeces_print].file_location.values + dz.reducDf.loc[indeces_print].file_name.values
for bias_file in list_mBias:
    print getval(bias_file, 'ISIARM', 0)
    print 'BIASSEC',  getval(bias_file, 'BIASSEC', 0)
    print 'TRIMSEC',  getval(bias_file, 'TRIMSEC', 0),'\n'    

#Generating pdf output
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'global_bias', plots_type = 'fits_compare', ext = 0, include_graph=True) 
 
dz.beep_alarmn()
 
print 'Data treated'

   
