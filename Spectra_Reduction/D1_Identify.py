import os
import sys
from pandas import set_option
from os.path import isfile
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction import spectra_reduction
from shutil import copyfile

'''
Run outside
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/D1_Identify.py
'''

#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Output tag
data_dict = {'reduc_tag': 'arc_trim'}

#Loop through the arms
colors = ['Blue','Red']
for arm_color in colors:

    idx_arcs        = (dz.reducDf.reduc_tag == 'arc_trim') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)   
    File_Folders    = dz.reducDf.loc[idx_arcs, 'file_location'].values
    File_Names      = dz.reducDf.loc[idx_arcs, 'file_name'].values
    
    for i in range(len(File_Names)):
                
        #Identify the arc
        dz.task_attributes['run folder']    = dz.reducFolders['arcs']
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['input']         = File_Folders[i] + File_Names[i]
        database_folder                     = '{arcs_folder}database/'.format(arcs_folder = dz.reducFolders['arcs'])
        dz.task_attributes['database']      = database_folder
                
        #Create the database folder if it does not exist
        if not os.path.exists(database_folder):
            os.makedirs(database_folder)
                     
        #Run the task
        os.chdir(dz.task_attributes['run folder'])
        dz.run_iraf_task('identify', run_externally=False)
                          
print 'Data treated'
