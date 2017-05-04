import os
import sys
from pandas     import set_option
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
set_option('display.max_columns', None)
set_option('display.max_rows', None)
from DZ_observation_reduction import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Arm colors
data_dict       = {'reduc_tag': 'arc_combine'}
colors          = ['Blue', 'Red']

#Loop through the arms 
for arm_color in colors:
             
    indeces_arcs                        = (dz.reducDf.frame_tag == 'arc') & (dz.reducDf.reduc_tag == 'biascorr') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
    Arc_Folders                         = dz.reducDf.loc[indeces_arcs, 'file_location'].values
    Arc_Names                           = dz.reducDf.loc[indeces_arcs, 'file_name'].values  
    Arc_colors                          = dz.reducDf.loc[indeces_arcs, 'ISIARM'].values
    Arc_types                           = dz.reducDf.loc[indeces_arcs, 'OBJECT'].values
   
    output_name                         = 'Arc_{color}_combined.fits'.format(color = arm_color)
    dz.task_attributes['run folder']    = dz.reducFolders['arcs']
    dz.task_attributes['color']         = arm_color
    dz.task_attributes['in_list_name']  = 'arcs_{color}.list'.format(color = dz.task_attributes['color'])
    dz.task_attributes['input array']   = Arc_Folders + Arc_Names
    dz.task_attributes['input']         = '@{folder_run}{in_list_name}'.format( folder_run = dz.task_attributes['run folder'], in_list_name = dz.task_attributes['in_list_name']) 
    dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.reducFolders['arcs'], output_name = output_name)        
    dz.task_attributes['combine']       = 'sum'
    dz.task_attributes['scale']         = '""'
    dz.task_attributes['statsec']       = '""'
    dz.task_attributes['reject']        = 'crreject'
    dz.task_attributes['weight']        = '""'        
    dz.task_attributes['gain']          = 'GAIN'
    dz.task_attributes['snoise']        = 'READNOIS'    
    
    #Run the task
    dz.run_iraf_task('imcombine', run_externally=False)

    #Add objects to data frame with the new frame_tag
    dz.object_to_dataframe(dz.task_attributes['output'], data_dict) 
         
#Generating pdf output
indeces_print = (dz.reducDf.reduc_tag == 'arc_combine') | ((dz.reducDf.frame_tag == 'arc') & (dz.reducDf.reduc_tag == 'biascorr'))
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'arc_combinedframes', ext = 0, include_graph=True, sorting_pattern = ['ISIARM','reduc_tag'])

dz.beep_alarmn()
   
print 'Data treated'


