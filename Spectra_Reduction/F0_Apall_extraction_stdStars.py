import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/F0_Apall_extraction_stdStars.py
'''

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms
colors  = ['Blue']

data_dict = {'reduc_tag' : 'extracted_spectrum'}

#Setting the standar stars folders to save the reference files
os.chdir(dz.reducFolders['objects'])

for arm_color in colors:
                 
    indeces_targetframes    = (dz.reducDf.frame_tag.isin(dz.observation_dict['Standard_stars'])) & (dz.reducDf.reduc_tag == 'wave_calibrated') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check()) 
             
    Files_Folders           = dz.reducDf.loc[indeces_targetframes, 'file_location'].values
    Files_Names             = dz.reducDf.loc[indeces_targetframes, 'file_name'].values
    objects                 = dz.reducDf.loc[indeces_targetframes, 'frame_tag'].values
    colors                  = dz.reducDf.loc[indeces_targetframes, 'ISIARM'].values
    Cropping_key            = dz.observation_dict['{Color}_cropping'.format(Color=arm_color)]
    cropping_area           = map(int, Cropping_key) 
        
    for i in range(len(objects)):
                
        if objects[i] in ['BD33']:
            output_name                         = Files_Names[i][0:Files_Names[i].find('.')] + '_e.fits'
            dz.task_attributes['run folder']    = Files_Folders[i]
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = Files_Folders[i] + Files_Names[i]
            dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.task_attributes['run folder'], output_name = output_name)   
            dz.task_attributes['extras']        = 'no'
            dz.task_attributes['gain_key']      = 'GAIN'
            dz.task_attributes['readnois_key']  = 'READNOIS'
            dz.task_attributes['backgro']       = 'median'
            dz.task_attributes['trace']         = 'yes'
            dz.task_attributes['edit']          = 'yes'
            dz.task_attributes['resize']        = 'no'
            dz.task_attributes['nsum']          = 10
            dz.task_attributes['referen']       = '""'   
            dz.task_attributes['line']          = '2600'
            dz.task_attributes['ylevel']        = 0.05    
            dz.task_attributes['b_order']       = 1
            dz.task_attributes['order']         = "increasing"
            dz.task_attributes['b_sample']      = '-{outer_blimit}:-{inner_blimit},{inner_blimit}:{outer_blimit}'.format(outer_blimit = int((cropping_area[1] - cropping_area[0])/4 * 1.4), inner_blimit = int((cropping_area[1] - cropping_area[0])/ 4 * 0.9))
            print dz.task_attributes['b_sample']
            print cropping_area
            print (cropping_area[1] - cropping_area[0])/4
            print (cropping_area[1] - cropping_area[0])/4 * 1.4
            
            
            #Run the task
            dz.run_iraf_task('apall', run_externally=False)
                          
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(dz.task_attributes['output'], data_dict)        

idx_print = (dz.reducDf.reduc_tag == 'extracted_spectrum') & (dz.reducDf.frame_tag.isin(dz.observation_dict['Standard_stars']))
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'extracted_stars', plots_type = 'extraction', ext = 0)
   
print 'Data treated'


