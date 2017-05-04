import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction import spectra_reduction

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/H2_NormWide.py
'''

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms--
colors = ['Red']

data_dict = {'reduc_tag' : 'norm_stars'}
 
for arm_color in colors:
       
    indeces_Stars   = dz.reducDf.frame_tag.isin(dz.observation_dict['Standard_stars']) & (dz.reducDf.reduc_tag == 'flux_calibrated_stars_local') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
   
    Files_Folders   = dz.reducDf.loc[indeces_Stars, 'file_location'].values
    Files_Names     = dz.reducDf.loc[indeces_Stars, 'file_name'].values
    objects         = dz.reducDf.loc[indeces_Stars, 'frame_tag'].values
    slitwidths      = dz.reducDf.loc[indeces_Stars, 'ISISLITW'].values
    number_objects  = len(Files_Names)
        
    for i in range(number_objects):
                                              
        #Names configuration
        initial_name    = Files_Folders[i] + Files_Names[i]
        Normalize_Name  = '{folder}{object}_{color}_slit{width}_n.fits'.format(folder = Files_Folders[i], object=objects[i], color=arm_color, width=round(slitwidths[i],1))
                
        #-----Clean the spectra
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['objects'])
        dz.task_attributes['input']         = initial_name
        dz.task_attributes['output']        = Normalize_Name
            
        #Run the task
        dz.run_iraf_task('continuum', run_externally=False)
               
        #Add objects to data frame with the new frame_tag
        dz.object_to_dataframe(Normalize_Name, data_dict)        
      
indeces_print = (dz.reducDf.reduc_tag == 'norm_stars')
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'normalized_stars', plots_type = 'spectra', ext = 0)        
                              
print 'Data treated'







# import os
# import sys
# sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
# os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
# os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
# from DZ_observation_reduction   import spectra_reduction
# 
# '''
# Run externally
# python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/G0_TelluricCorrection.py
# '''
# 
# #Load iraf pypeline object
# dz = spectra_reduction()
# 
# #Load reduction data frame
# dz.declare_catalogue(dz.Catalogue_folder)
# 
# #Loop through the arms--
# colors      = ['Red']
# data_dict   = {'reduc_tag' : 'telluric_corrected'}
# 
# for arm_color in colors:
#      
#     indeces_obj             = dz.reducDf.frame_tag.isin(dz.observation_dict['objects']) & (dz.reducDf.reduc_tag == 'flux_calibrated_objects_fglobal') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
#  
#     Files_Folders           = dz.reducDf.loc[indeces_obj, 'file_location'].values
#     Files_Names             = dz.reducDf.loc[indeces_obj, 'file_name'].values
#     slit_width              = dz.reducDf.loc[indeces_obj, 'ISISLITW'].values
#     objects                 = dz.reducDf.loc[indeces_obj, 'frame_tag'].values
#     
#     for i in range(len(Files_Names)):
#         
#         color_order         = dz.plots_dict[arm_color]
#         Calibration_star    = dz.observation_dict[objects[i] + '_calibration_star'][color_order]
#         Normalize_Name      = '{run_folder}{starcode}_clean_n.fits'.format(run_folder = dz.reducFolders['objects'], starcode = Calibration_star)
#               
#         #-----Divide the spectrum
#         dz.task_attributes['color']         = arm_color
#         dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['objects'])
#         dz.task_attributes['input1']        = Files_Folders[i] + Files_Names[i]
#         dz.task_attributes['op']            = '/'
#         dz.task_attributes['input2']        = Normalize_Name
#         dz.task_attributes['output']        = Files_Folders[i] + Files_Names[i].replace('.fits', '_tell.fits')
#          
#         #Run the task
#         dz.run_iraf_task('sarith', run_externally=False)
#                
#         #Add objects to data frame with the new frame_tag
#         dz.object_to_dataframe(dz.task_attributes['output'], data_dict)      
#          
# print 'Printing these files'
# indeces_print = (dz.reducDf.reduc_tag == 'telluric_corrected')
# dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'telluric_corrected_spectra', plots_type = 'spectra', ext = 0)
#  
# print 'Data treated'



