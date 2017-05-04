import os
import sys
os.environ['TK_LIBRARY']    = '/home/vital/anaconda/python27/lib/tk8.5'
os.environ['TCL_LIBRARY']   = '/home/vital/anaconda/python27/lib/tcl8.5'
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
from DZ_observation_reduction import spectra_reduction

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/D3_Fitcoords.py
'''
 
#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
  
#Loop through the arms
colors = ['Blue','Red']
for arm_color in colors:

    #Get object and global indeces
    indeces_arc         = (dz.reducDf.reduc_tag == 'arc_trim') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)  
    Files_Folder        = dz.reducDf.loc[indeces_arc, 'file_location'].values
    Files_Name          = dz.reducDf.loc[indeces_arc, 'file_name'].values
    
    #Loop through the files        
    for i in range(len(Files_Name)):
        
        input_file                          = Files_Folder[i] + Files_Name[i]
        input_file_noExt                    = input_file[0:input_file.rfind('.')]
                                                             
        dz.task_attributes['run folder']    = dz.reducFolders['arcs']
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['input']         = input_file_noExt
        dz.task_attributes['fitname']       = '""'
        
        #Run the task
        dz.run_iraf_task('fitcoords', run_externally=False)

print 'Data treated'