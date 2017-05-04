import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

'''
Run from terminal
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/F1_BackgroundRed.py
'''

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Output tag
data_dict = {'reduc_tag' : 'background_removed'}

#Loop through the arms
colors  = ['Red']

for arm_color in colors:
       
    indeces_targetframes    = (dz.reducDf.frame_tag.isin(dz.observation_dict['objects'])) & (dz.reducDf.reduc_tag == 'wave_calibrated') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check()) 
   
    Files_Folders           = dz.reducDf.loc[indeces_targetframes, 'file_location'].values
    Files_Names             = dz.reducDf.loc[indeces_targetframes, 'file_name'].values
    objects                 = dz.reducDf.loc[indeces_targetframes, 'frame_tag'].values
    
    for i in range(len(objects)):
        
#         if objects[i] == '[8]':
        
            #Plotting reference line
            object_reference    = '{CodeName}_refline_{Color}'.format(CodeName=objects[i], Color=arm_color)
            Store_cords         = dz.observation_dict[object_reference]
            x_peak, y_peak      = int(Store_cords[0]), int(Store_cords[1])
     
            #Getting the crop region
            Cropping_key    = dz.observation_dict['{Color}_cropping'.format(Color=arm_color)]
            cropping_area   = map(int, Cropping_key) 
     
            print cropping_area
            print '--',  Files_Names[i], 'reference line:', y_peak - cropping_area[2]
     
            output_name                         = Files_Names[i][0:Files_Names[i].find('.')] + '_bg.fits'
            dz.task_attributes['run folder']    = Files_Folders[i]
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = Files_Folders[i] + Files_Names[i]
            dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.task_attributes['run folder'], output_name = output_name)
            dz.task_attributes['order']         = 1
            dz.task_attributes['axis']          = 1
                     
            #Run the task
            dz.run_iraf_task('background', run_externally=True)
               
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)        
  
print 'Printing these files'
indeces_print = (dz.reducDf.reduc_tag == 'background_removed')
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'background_objects', ext = 0, plots_type = 'fits_compare', include_graph=False)  
  
print 'Data treated'
