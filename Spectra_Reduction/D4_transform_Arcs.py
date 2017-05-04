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
 
#Arm colors
data_dict = {'reduc_tag': 'arcs_wave_calibrated'}
 
#Loop through the arms
colors = ['Blue', 'Red'] 
for arm_color in colors:
                 
    #Get object and global indeces
    #indeces_arcGlobal   = (dz.reducDf.reduc_tag == 'trim_image') & (dz.reducDf.frame_tag == 'arc') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)  
    #indeces_arcs        = indeces_arcGlobal
    index_arcframe      = (dz.reducDf.RUN.isin(List_arc_runs)) & (dz.reducDf.reduc_tag == 'biascorr') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)  
    indeces_arcs = index_arcframe
 
    Files_Folder        = dz.reducDf.loc[indeces_arcs, 'file_location'].values
    Files_Name          = dz.reducDf.loc[indeces_arcs, 'file_name'].values  
    Arc_colors          = dz.reducDf.loc[indeces_arcs, 'ISIARM'].values
    Arc_dict            = dict(zip([w.replace(' arm', '') for w in Arc_colors], Files_Name))
         
    for j in range(len(Files_Name)):  
 
        arc_frame   = Arc_dict[arm_color]
        arc_name    = arc_frame[0:arc_frame.rfind('.')]
                                  
        dz.task_attributes['run folder']    = Files_Folder[j]
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['input']         = Files_Folder[j] + Files_Name[j]
        dz.task_attributes['output']        = Files_Folder[j] + Files_Name[j].replace('.fits', '_w.fits')
        dz.task_attributes['fitnames']      = arc_name
     
        #Moving the data base to the obj/standard folder
        if not os.path.exists(dz.task_attributes['run folder'] + 'database/'):
            os.makedirs(dz.task_attributes['run folder'] + 'database/')            
                 
        #Run the task
        dz.run_iraf_task('transform')
     
        #Add objects to data frame with the new frame_tag
        dz.object_to_dataframe(dz.task_attributes['output'], data_dict)
     
#Generate pdf file
dz.generate_step_pdf((dz.reducDf.reduc_tag == 'arcs_wave_calibrated') , file_address = dz.reducFolders['reduc_data'] + 'arcs_wave_calibrated', ext = 0, plots_type = 'arcs_calibration')
 
print 'Data treated'
 
 # #Preload objects arcs
# List_arc_runs = []
# for obj_target in dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']:
#     List_arc_runs += dz.observation_dict[obj_target + '_arc']
#  
# #Clean repeated objects and only treat 
# List_arc_runs = map(float, sorted(set(List_arc_runs)))
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


