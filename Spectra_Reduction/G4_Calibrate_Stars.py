import os
import sys
from pyfits import getval
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

# data_dict = {'reduc_tag' : 'flux_calibrated_stars_local'}


#Which slit to use WARNING no me gusta
slit_minimum = float(dz.observation_dict['slit_minimum'][0])  #Normally this should be 2
if slit_minimum < 2.0:
    slit_for_calibration = ['narrow']
else:
    slit_for_calibration = ['wide']


#Loop through the arms
colors  = ['Blue','Red']
for arm_color in colors:
        
    indeces_Stars   = (dz.reducDf.frame_tag.isin(dz.observation_dict['Standard_stars'])) & (dz.reducDf.reduc_tag == 'extracted_spectrum') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.target_validity_check()) 
  
    Files_Folders   = dz.reducDf.loc[indeces_Stars, 'file_location'].values
    Files_Names     = dz.reducDf.loc[indeces_Stars, 'file_name'].values
    slit_width      = dz.reducDf.loc[indeces_Stars, 'ISISLITW'].values
    objects         = dz.reducDf.loc[indeces_Stars, 'frame_tag'].values
    slit_size       = slit_for_calibration[0]                   
    
    #Calibrate with own function
    for i in range(len(Files_Names)):

        sensfunc_file = '{run_folder}sen_{starcode}_{color}_{slit_size}.fits'.format(run_folder = dz.reducFolders['objects'], starcode = objects[i], color = arm_color, slit_size = slit_size)

        output_name                             = Files_Names[i][0:Files_Names[i].find('.')] + '_flocal.fits'
        dz.task_attributes['run folder']        = Files_Folders[i]
        dz.task_attributes['color']             = arm_color
        dz.task_attributes['input']             = Files_Folders[i] + Files_Names[i]
        dz.task_attributes['output']            = Files_Folders[i] + output_name
        dz.task_attributes['senstivityCurve']   = sensfunc_file
        dz.task_attributes['airmass']           = getval(Files_Folders[i] + Files_Names[i], 'AIRMASS', 0)
        dz.task_attributes['exptime']           = getval(Files_Folders[i] + Files_Names[i], 'EXPTIME', 0)                                                       
           
        #Run the task
        dz.run_iraf_task('calibrate')
        
        #Store in dataframe       
        dz.object_to_dataframe(dz.task_attributes['output'], {'reduc_tag' : 'flux_calibrated_stars_local'})        

    #Calibrate with global function
    for i in range(len(Files_Names)):

        sensfunc_file = '{run_folder}sen_{color}_{slit_size}.fits'.format(run_folder = dz.reducFolders['objects'], starcode = objects[i], color = arm_color, slit_size = slit_size)

        output_name                             = Files_Names[i][0:Files_Names[i].find('.')] + '_fglobal.fits'
        dz.task_attributes['run folder']        = Files_Folders[i]
        dz.task_attributes['color']             = arm_color
        dz.task_attributes['input']             = Files_Folders[i] + Files_Names[i]
        dz.task_attributes['output']            = Files_Folders[i] + output_name
        dz.task_attributes['senstivityCurve']   = sensfunc_file
        dz.task_attributes['airmass']           = getval(Files_Folders[i] + Files_Names[i], 'AIRMASS', 0)
        dz.task_attributes['exptime']           = getval(Files_Folders[i] + Files_Names[i], 'EXPTIME', 0)                                                       
           
        #Run the task
        dz.run_iraf_task('calibrate')
        
        #Store in dataframe       
        dz.object_to_dataframe(dz.task_attributes['output'], {'reduc_tag' : 'flux_calibrated_stars_global'})    

indeces_print = (dz.reducDf.reduc_tag == 'flux_calibrated_stars_local') | (dz.reducDf.reduc_tag == 'flux_calibrated_stars_global')
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'calibrated_stars', plots_type = 'spectra', ext = 0)
   
print 'Data treated'


