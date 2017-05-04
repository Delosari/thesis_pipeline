import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction   import spectra_reduction

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/G2_sensfunc.py
'''

#Load iraf pypeline object
dz = spectra_reduction()
 
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
 
#Loop through the arms
colors      = ['Blue','Red']
os.chdir(dz.reducFolders['objects'])

#Which slit to use WARNING no me gusta
slit_minimum = float(dz.observation_dict['slit_minimum'][0])  #Normally this should be 2
if slit_minimum < 2.0:
    slit_for_calibration = ['narrow']
else:
    slit_for_calibration = ['wide']


#Fitting with individual standard files
for arm_color in colors:
         
    for width in slit_for_calibration:
            
        for star in dz.observation_dict['Standard_stars']:
                
            standard_file_local = 'std_{starcode}_{color}_{slit_size}.txt'.format(starcode = star, color = arm_color, slit_size = width)
                                              
            sensfunc_file   = '{run_folder}sen_{starcode}_{color}_{slit_size}.fits'.format(run_folder = dz.reducFolders['objects'], starcode = star, color = arm_color, slit_size = width)
                     
            dz.task_attributes['run folder']    = dz.reducFolders['objects']
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = standard_file_local
            dz.task_attributes['output']        = sensfunc_file  
            dz.task_attributes['functio']       = 'spline3' 
            dz.task_attributes['order']         = 40  
            dz.task_attributes['graphs']        = 'si'  
  
            #Run the task
            dz.run_iraf_task('sensfunc', run_externally=False)
                 
print 'Data treated'


