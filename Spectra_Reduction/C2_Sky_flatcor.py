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

#Loop through the arms
colors = ['Blue', 'Red']

illumination_source = dz.observation_dict['illumination_source'][0]

print illumination_source

if illumination_source == 'sky':

    for arm_color in colors:
    
        #Same illumination frame for all the objects
        index_skycomb       = (dz.reducDf.reduc_tag == 'skycombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
        index_nflatcomb     = (dz.reducDf.reduc_tag == 'nflatcombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
        
        sky_folder          = dz.reducDf.file_location[index_skycomb].values[0]
        sky_file            = dz.reducDf.file_name[index_skycomb].values[0]
        
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = dz.reducFolders['flat sky']
        dz.task_attributes['input']         = sky_folder + sky_file
        dz.task_attributes['output']        = sky_folder + sky_file.replace('.fits', '_f.fits')    
        dz.task_attributes['flatcor']       = 'yes'
        dz.task_attributes['flat']          = dz.reducDf.file_location[index_nflatcomb].values[0] + dz.reducDf.file_name[index_nflatcomb].values[0]
          
        #Run the task
        dz.run_iraf_task('ccdproc')
    
        #Add objects to data frame with the new reduc_tag
        dz.object_to_dataframe(dz.task_attributes['output'] , {'reduc_tag': 'skycombine_f'})
    
    #Generate pdf file
    idx_print = (dz.reducDf.reduc_tag == 'skycombine_f') | (dz.reducDf.reduc_tag == 'skycombine')
    dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'skycombine_flatcorrected', plots_type='fits_compare', include_graph=True, verbose=True, ext = 0)
        
    dz.beep_alarmn()    

elif illumination_source == 'lamp':

    for arm_color in colors:

        #Same illumination frame for all the objects
        index_skycomb       = (dz.reducDf.reduc_tag == 'flatcombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
        index_nflatcomb     = (dz.reducDf.reduc_tag == 'nflatcombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
        
        sky_folder          = dz.reducDf.file_location[index_skycomb].values[0]
        sky_file            = dz.reducDf.file_name[index_skycomb].values[0]
        
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = dz.reducFolders['flat lamp']
        dz.task_attributes['input']         = sky_folder + sky_file
        dz.task_attributes['output']        = sky_folder + sky_file.replace('.fits', '_f.fits')    
        dz.task_attributes['flatcor']       = 'yes'
        dz.task_attributes['flat']          = dz.reducDf.file_location[index_nflatcomb].values[0] + dz.reducDf.file_name[index_nflatcomb].values[0]
          
        #Run the task
        dz.run_iraf_task('ccdproc')
    
        #Add objects to data frame with the new reduc_tag
        dz.object_to_dataframe(dz.task_attributes['output'] , {'reduc_tag': 'flatcombine_f'})
    
    #Generate pdf file
    idx_print = (dz.reducDf.reduc_tag == 'flatcombine_f') | (dz.reducDf.reduc_tag == 'flatcombine')
    dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'flatcombine_flatcorrected', plots_type='fits_compare', include_graph=True, verbose=True, ext = 0)
        
    dz.beep_alarmn()    

print 'Data treated'