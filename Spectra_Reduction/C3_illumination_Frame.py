import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

'''
Run in terminal
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/C3_illumination_Frame.py
'''

#Load iraf pypeline object
dz = spectra_reduction()
  
#Entries for new files
data_dict = {'reduc_tag': 'illumFrame'}

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

illumination_source = dz.observation_dict['illumination_source'][0]

if illumination_source == 'sky':

    #Loop through the arms
    colors = ['Blue', 'Red']
    
    for arm_color in colors:
    
        #Get the files we are going to treat
        indeces_skyCombine_n  = (dz.reducDf.reduc_tag == 'skycombine_f') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
    
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['flat sky'])
        dz.task_attributes['input']         = dz.reducDf.loc[indeces_skyCombine_n, 'file_location'].values[0] + dz.reducDf.loc[indeces_skyCombine_n, 'file_name'].values[0]
        dz.task_attributes['output']        = '{folder_run}illumflat_{color}.fits'.format( folder_run = dz.task_attributes['run folder'], color = dz.task_attributes['color'])
     
        #Run the task
        dz.run_iraf_task('illumination', run_externally=False)
             
        #Add objects to data frame with the new reduc_tag
        dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
         
    #Generate pdf file
    indeces_print = (dz.reducDf.reduc_tag == 'illumFrame')
    dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'illumination_frames', plots_type = 'fits_compare', ext = 0, include_graph=True) 

elif illumination_source == 'lamp':
    
    #Loop through the arms
    colors = ['Blue', 'Red']
    
    for arm_color in colors:
    
        #Get the files we are going to treat
        indeces_skyCombine_n  = (dz.reducDf.reduc_tag == 'flatcombine_f') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
    
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['flat lamp'])
        dz.task_attributes['input']         = dz.reducDf.loc[indeces_skyCombine_n, 'file_location'].values[0] + dz.reducDf.loc[indeces_skyCombine_n, 'file_name'].values[0]
        dz.task_attributes['output']        = '{folder_run}illumflat_{color}.fits'.format( folder_run = dz.task_attributes['run folder'], color = dz.task_attributes['color'])
     
        #Run the task
        dz.run_iraf_task('illumination', run_externally=False)
             
        #Add objects to data frame with the new reduc_tag
        dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
         
    #Generate pdf file
    indeces_print = (dz.reducDf.reduc_tag == 'illumFrame')
    dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'illumination_frames', plots_type = 'fits_compare', ext = 0, include_graph=True)     
    
print 'Data treated'


