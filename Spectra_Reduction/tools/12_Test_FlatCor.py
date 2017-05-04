import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()
  
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

data_dict = {'reduc_tag': 'test_flatCor'}

#Loop through the arms
colors = ['Blue', 'Red']

dz.verbose_output = False
for arm_color in colors:
   
    index_nflatcomb     = (dz.reducDf.reduc_tag == 'nflatcombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) 
    flat_address        = dz.reducDf.file_location[index_nflatcomb].values[0] + dz.reducDf.file_name[index_nflatcomb].values[0]
       
    for obj_target in dz.observation_dict['Standard_stars']:
   
        #Same illumination frame for all the objects
        idx_star = (dz.reducDf.frame_tag == obj_target) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file) 
           
        Target_folders  = dz.reducDf.loc[idx_star, 'file_location'].values 
        Target_names    = dz.reducDf.loc[idx_star, 'file_name'].values
        Target_isiarm   = dz.reducDf.loc[idx_star, 'ISIARM'].values
        Target_isislit   = dz.reducDf.loc[idx_star, 'ISISLITW'].values
  
        for i in range(len(Target_names)):
                                   
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['run folder']    = dz.reducFolders['flat sky']
            dz.task_attributes['input']         = Target_folders[i] + Target_names[i]
            dz.task_attributes['output']        = Target_folders[i] + Target_names[i].replace('.fits', '_testflatcor.fits')    
            dz.task_attributes['flatcor']       = 'yes'
            dz.task_attributes['flat']          = flat_address
  
            #Run the task
            dz.run_iraf_task('ccdproc')
        
            #Add objects to data frame with the new reduc_tag
            dz.object_to_dataframe(dz.task_attributes['output'] , data_dict)

idx_print = (dz.reducDf.reduc_tag == 'test_flatCor') | ((dz.reducDf.frame_tag.isin(dz.observation_dict['Standard_stars'])) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal')) 
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'testing_flats', plots_type='flat_calibration', include_graph=True, verbose=True, ext = 0)
      
dz.beep_alarmn()    
     
print 'Data treated'