import os
import sys
from collections import OrderedDict
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction
from shutil import copyfile

'''
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/B6_FastCombine.py
'''

#Load iraf pypeline object
dz = spectra_reduction()
  
#Entries for new files
data_dict = {'reduc_tag': 'objTest_combine'}

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms
colors          = ['Blue', 'Red']
for arm_color in colors:
                
    obj_scaling_key = '{Color}_scale_region'.format(Color=arm_color)
           
    for obj_target in dz.observation_dict['objects']:
             
        indeces_objframes = (dz.reducDf.frame_tag == obj_target) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check())
                     
        #Frames properties
        Files_Folders   = dz.reducDf.loc[indeces_objframes, 'file_location'].values
        Files_Names     = dz.reducDf.loc[indeces_objframes, 'file_name'].values
        obj_code        = dz.reducDf.loc[indeces_objframes, 'file_name'].values
        frame_number    = len(Files_Names)
                     
        if (frame_number > 1):
                                       
            dz.task_attributes['run folder']    = dz.reducFolders['objects']
            output_name                         = '{CodeName}_{color}_testComb.fits'.format(CodeName = obj_target.replace('[','').replace(']',''), color = arm_color)
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = ','.join(list(Files_Folders + Files_Names))
            dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.reducFolders['objects'], output_name = output_name)   
            dz.task_attributes['combine']       = 'median'
            dz.task_attributes['scale']         = 'median'
            dz.task_attributes['reject']        = 'crreject'
            dz.task_attributes['weight']        = '""'
            dz.task_attributes['gain']          = 'GAIN'
            dz.task_attributes['snoise']        = 'READNOIS'
            dz.task_attributes['axis']          = 1
            dz.task_attributes['statsec']       = '""'
                                   
            #Run the task
            print 'output_1', dz.task_attributes['output']
            dz.run_iraf_task('imcombine', run_externally=False)
               
            #Proceed to a background substraction
            dz.task_attributes                  = OrderedDict()
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['run folder']    = dz.reducFolders['objects']
            dz.task_attributes['input']         = '{run_Folder}{output_name}'.format(run_Folder = dz.reducFolders['objects'], output_name = output_name)  
            dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.reducFolders['objects'], output_name = output_name.replace('.fits', '_Bg.fits'))  
            dz.task_attributes['axis']          = 1
            dz.task_attributes['order']         = 1

            print 'output_2', dz.task_attributes['output']
  
  
            #Printing reference line reference line
            try:
                object_reference    = '{CodeName}_refline_{Color}'.format(CodeName=obj_target, Color=arm_color)
                Store_cords         = dz.observation_dict[object_reference]
                x_peak, y_peak      = int(Store_cords[0]), int(Store_cords[1])
                print '-------------------------',  obj_target, 'reference line:', y_peak
            except:
                print '-------------------------No reference line'
  
                     
            #Run the task
            if arm_color == 'Red': 
                dz.run_iraf_task('background', run_externally=False)
            else:
                copyfile(dz.task_attributes['input'], dz.task_attributes['output'])
                                
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
                  
#New files
idx_to_print = (dz.reducDf.reduc_tag == 'objTest_combine')
dz.generate_step_pdf(idx_to_print, file_address = dz.reducFolders['reduc_data'] + 'test_target_combined', plots_type = 'fast_combine', ext = 0)

dz.beep_alarmn()
      
print 'Data treated'


