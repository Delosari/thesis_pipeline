import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction import spectra_reduction

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/H0_CleanNarrow.py
'''

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms--
colors = ['Red']

data_dict = {'reduc_tag' : 'clean_narrow'}

tag_stars_calibration = dz.observation_dict['stars_calibration_tag'][0] 

for arm_color in colors:
     
    indeces_Stars   = dz.reducDf.frame_tag.isin(dz.observation_dict['Standard_stars']) & (dz.reducDf.ISISLITW < 2) & (dz.reducDf.reduc_tag == tag_stars_calibration) & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
 
    Files_Folders   = dz.reducDf.loc[indeces_Stars, 'file_location'].values
    Files_Names     = dz.reducDf.loc[indeces_Stars, 'file_name'].values
    objects         = dz.reducDf.loc[indeces_Stars, 'frame_tag'].values
    number_objects  = len(Files_Names)
    
    for i in range(number_objects):
                  
        print '{idx}/{total_files}: {Current_File}:'.format(idx=i, total_files=number_objects, Current_File=Files_Names[i]) 
         
        if i >= 0:
                         
            #Names configuration
            initial_name    = Files_Folders[i] + Files_Names[i]
            Clean_Name      = Files_Folders[i] + objects[i] + '_clean.fits'
             
            #Delete them if already there:
            for output_names in [Clean_Name]:
                if os.path.isfile(output_names):
                    os.remove(output_names)                
        
            #-----Clean the spectra
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['objects'])
            dz.task_attributes['input']         = initial_name
            dz.task_attributes['output']        = '""'
             
            #Change the folder so the fit is saved at the right folder
            os.chdir(Files_Folders[i]) 
             
            #Run the task
            print
            print 'REMOVE points:', 'x twice between edges'
            print 'press "i" to save:', Clean_Name
            print
            dz.run_iraf_task('splot', run_externally=False)
                
            #Add objects to data frame with the new frame_tag
            dz.object_to_dataframe(Clean_Name, data_dict)        
    
indeces_print = (dz.reducDf.reduc_tag == 'clean_narrow')
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'cleaned_narrow_stars', plots_type = 'spectra', ext = 0)        
                            
print 'Data treated'



