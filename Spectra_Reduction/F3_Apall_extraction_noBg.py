import os
import sys
from shutil import copy
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

'''
Run
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/F3_Apall_extraction_noBg.py
'''

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Setting the standar stars folders to save the reference files
os.chdir(dz.reducFolders['objects'])

#Output data tag
data_dict = {'reduc_tag' : 'extracted_spectrum'}

#Loop through the arms
colors  = ['Red']

slit_minimum = float(dz.observation_dict['slit_minimum'][0])  #Normally this should be 2

for arm_color in colors:
           
    indeces_targetframes    = (dz.reducDf.frame_tag.isin(dz.observation_dict['objects'])) & (dz.reducDf.reduc_tag == 'background_removed') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check())
       
    Files_Folders           = dz.reducDf.loc[indeces_targetframes, 'file_location'].values
    Files_Names             = dz.reducDf.loc[indeces_targetframes, 'file_name'].values
    objects                 = dz.reducDf.loc[indeces_targetframes, 'frame_tag'].values
    colors                  = dz.reducDf.loc[indeces_targetframes, 'ISIARM'].values
     
    star_reference          = dz.observation_dict['{color}_ref_star'.format(color=arm_color)][0]
    index_reference_star    = (dz.reducDf.frame_tag == star_reference) & (dz.reducDf.reduc_tag == 'wave_calibrated') & (dz.reducDf.ISISLITW > slit_minimum) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))    
    reference_star          = dz.reducDf.loc[index_reference_star, 'file_location'].values + dz.reducDf.loc[index_reference_star, 'file_name'].values
    reference_star          = reference_star[0]
       
    reference_folder        = dz.reducFolders['objects'] + 'database/'
    reference_name          = 'ap_' + dz.reducFolders['objects'][1:].replace('/','_') +  dz.reducDf.loc[index_reference_star, 'file_name'].values[0].replace('.fits', '')
        
    #Copy reference file to the folder
#     copy(reference_folder + reference_name,  dz.reducFolders['objects'] + 'database/' + reference_name)
            
    for i in range(len(objects)):
               
        if objects[i] in ['IZW18']:
                      
            #Plotting reference line
            object_reference    = '{CodeName}_refline_{Color}'.format(CodeName=objects[i], Color=arm_color)
            Store_cords         = dz.observation_dict[object_reference]
            x_peak, y_peak      = int(Store_cords[0]), int(Store_cords[1])
                
            #Getting the crop region
            Cropping_key    = dz.observation_dict['{Color}_cropping'.format(Color=arm_color)]
            cropping_area   = map(int, Cropping_key) 
            line_location   = y_peak - cropping_area[2]    
                
            print '--',  Files_Names[i], x_peak, y_peak, 'reference line:', line_location    
                
            output_name                         = Files_Names[i][0:Files_Names[i].find('.')] + '_e.fits'
            dz.task_attributes['run folder']    = Files_Folders[i]
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = Files_Folders[i] + Files_Names[i]
            dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.task_attributes['run folder'], output_name = output_name)   
            dz.task_attributes['extras']        = 'no'
            dz.task_attributes['gain_key']      = 'GAIN'
            dz.task_attributes['readnois_key']  = 'READNOIS'
            dz.task_attributes['backgro']       = 'none'
            dz.task_attributes['trace']         = 'no'
            dz.task_attributes['edit']          = 'yes'
            dz.task_attributes['resize']        = 'yes'        
            dz.task_attributes['nsum']          = 10
            dz.task_attributes['line']          = line_location
            dz.task_attributes['referen']       = reference_star
            dz.task_attributes['ylevel']        = 0.05    
            dz.task_attributes['b_order']       = 1
            dz.task_attributes['order']         = 'increasing'
            dz.task_attributes['b_sample']      = '-{outer_blimit}:-{inner_blimit},{inner_blimit}:{outer_blimit}'.format(outer_blimit = int((cropping_area[1] - cropping_area[0])/4 * 1.8), inner_blimit = int((cropping_area[1] - cropping_area[0])/ 4 * 1.2))
            
            #Run the task
            dz.run_iraf_task('apall', run_externally=False)
                      
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)        
    
idx_print = (dz.reducDf.reduc_tag == 'extracted_spectrum') & (dz.reducDf.ISIARM == 'Red arm') & (dz.reducDf.frame_tag.isin(dz.observation_dict['objects']))
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'extracted_red_objects', plots_type = 'extraction', ext = 0)
   
print 'Data treated'


