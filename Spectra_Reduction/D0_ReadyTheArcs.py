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

#Output tag
data_dict = {'reduc_tag': 'arc_trim'}

#Loop through the arms
colors = ['Blue', 'Red']
for arm_color in colors:
    
    for target in dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']:
        
        target_arclist = map(float,dz.observation_dict[target + '_arc'])
                
        #Get object and global indeces
        idx_arc = (dz.reducDf.RUN.isin(target_arclist)) & (dz.reducDf.reduc_tag == 'biascorr') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)   
        
        File_Folder         = dz.reducDf.loc[idx_arc, 'file_location'].values[0]
        File_Name           = dz.reducDf.loc[idx_arc, 'file_name'].values[0]
        File_Name_flatcor   = File_Name[0:File_Name.find('.')] + '_f.fits'
        File_Name_trim      = File_Name[0:File_Name.find('.')] + '_t.fits'
        
        #Define flat
        idx_nflat_master    = (dz.reducDf.reduc_tag == 'nflatcombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
         
        #Define cropping region
        cropping            = dz.observation_dict[arm_color + '_cropping']
        cropping_region     = '[{rawA}:{rawB},{columnA}:{columnB}]'.format(rawA=cropping[0], rawB=cropping[1],columnA=cropping[2], columnB=cropping[3])
         
        #flat the arc
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = dz.reducFolders['arcs']
        dz.task_attributes['input']         = File_Folder + File_Name
        dz.task_attributes['output']        = File_Folder + File_Name_flatcor
        dz.task_attributes['flatcor']       = 'yes'
        dz.task_attributes['flat']          = dz.reducDf.file_location[idx_nflat_master].values[0] + dz.reducDf.file_name[idx_nflat_master].values[0]
        dz.run_iraf_task('ccdproc')        
        dz.object_to_dataframe(File_Folder + File_Name_flatcor, {'reduc_tag': 'arc_flatcor'})    
        
        #Crop the arc
        dz.reset_task_dict()
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = dz.reducFolders['arcs']
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['input']         = File_Folder + File_Name_flatcor + cropping_region
        dz.task_attributes['output']        = '{run_Folder}{output_name}'.format(run_Folder = dz.task_attributes['run folder'], output_name = File_Name_trim)   
        dz.run_iraf_task('imcopy')  
        dz.object_to_dataframe(File_Folder + File_Name_trim, {'reduc_tag': 'arc_trim'})    
 
#Generate pdf file
idx_print = (dz.reducDf.reduc_tag == 'arc_trim') & (dz.reducDf.valid_file)
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'arcs_trimmed', ext = 0, include_graph=True) 
 
print 'Data treated'
