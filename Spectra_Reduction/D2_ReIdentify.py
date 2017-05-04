import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction import spectra_reduction
 
#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
  
#Loop through the arms
colors = ['Blue', 'Red']
for arm_color in colors:
    
    #Get object and global indeces
    indeces_arc     = (dz.reducDf.reduc_tag == 'arc_trim') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)  
    Files_Folder    = dz.reducDf.loc[indeces_arc, 'file_location'].values
    Files_Name      = dz.reducDf.loc[indeces_arc, 'file_name'].values

    for i in range(len(Files_Name)):
                                                               
        dz.task_attributes['run folder']    = dz.reducFolders['arcs']
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['referenc']      = Files_Folder[i] + Files_Name[i]
        dz.task_attributes['input']         = Files_Folder[i] + Files_Name[i]
                     
        #Run the task
        dz.run_iraf_task('reidentify', run_externally=False)
        
            
print 'Data treated'