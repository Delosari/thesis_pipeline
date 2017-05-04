import os
import sys
import pyfits
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction import spectra_reduction
from numpy import zeros, median, mean, empty, argsort

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/E0_Independent_Bg_Component.py
'''


#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Output tag
data_dict = {'reduc_tag': 'background_removed_component'}

targets_with_issues = ['52319-521', '52703-612']

#Loop through the arms
colors = ['Blue', 'Red']
for target in targets_with_issues:
 
    for arm_color in colors:
                     
        #Get object and global indeces
        indeces_objframes   = (dz.reducDf.frame_tag == target) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)   
      
        File_Folder         = dz.reducDf.loc[indeces_objframes, 'file_location'].values
        File_Name           = dz.reducDf.loc[indeces_objframes, 'file_name'].values
        File_Name_comb      = '{Folder_i}{code_name}_{color_arm}.fits'.format(Folder_i = File_Folder[0], code_name=target.replace('[','').replace(']',''), color_arm = arm_color)
        frame_number        = len(File_Name)
             
        #Define flat
        index_objflat       = (dz.reducDf.reduc_tag == target + '_flatobj_n') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) 
        obj_flat_address    = dz.reducDf.loc[index_objflat, 'file_location'].values[0] + dz.reducDf.loc[index_objflat, 'file_name'].values[0]
     
        #Same illumination frame for all the objects
        index_illumination  = (dz.reducDf.reduc_tag == 'illumFrame') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
        illum_address       = dz.reducDf.loc[index_illumination, 'file_location'].values[0] + dz.reducDf.loc[index_illumination, 'file_name'].values[0]
                   
        #Define cropping region
        cropping            = dz.observation_dict[arm_color + '_cropping']
        cropping_region     = '[{rawA}:{rawB},{columnA}:{columnB}]'.format(rawA=cropping[0], rawB=cropping[1],columnA=cropping[2], columnB=cropping[3])
           
        #Scaling region
        obj_scaling_key     = '{Color}_scale_region'.format(Color=arm_color)
        stats_section       = map(int, dz.observation_dict[obj_scaling_key])
 
        #Getting the crop region
        Cropping_key        = dz.observation_dict['{Color}_cropping'.format(Color=arm_color)]
        cropping_area       = map(int, Cropping_key) 
        object_reference    = '{CodeName}_refline_{Color}'.format(CodeName=target, Color=arm_color)
        Store_cords         = dz.observation_dict[object_reference]
        x_peak, y_peak      = int(Store_cords[0]), int(Store_cords[1])
 
        for i in range(len(File_Name)):
              
            File_Name_bg        = '{Folder_i}{CodeName_i}_Frame{frame_i}_{color_arm}_bg.fits'.format(Folder_i = File_Folder[i], CodeName_i = target.replace('[','').replace(']',''), frame_i = i+1, color_arm=arm_color)
              
            print
            print cropping_area
            print '--', object_reference
            print '--', target, 'reference line:', y_peak #- cropping_area[2] #No need to crop in this case
            print 
              
            #Remove background
            dz.reset_task_dict()
            dz.task_attributes['run folder']    = dz.reducFolders['objects']
            dz.task_attributes['color']         = arm_color
            dz.task_attributes['input']         = File_Folder[i] + File_Name[i]
            dz.task_attributes['output']        = File_Name_bg  
            dz.task_attributes['axis']          = 1
            dz.task_attributes['order']         = 1  
            dz.run_iraf_task('background', run_externally=True)
            dz.object_to_dataframe(File_Name_bg, {'reduc_tag': 'frame_bg'})
          
        #--Combine the objects
        indeces_bgRemoved   = (dz.reducDf.frame_tag == target) & (dz.reducDf.reduc_tag == 'frame_bg') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)   
        Files_Names         = dz.reducDf.loc[indeces_bgRemoved, 'file_name'].values
        File_Folder         = dz.reducDf.loc[indeces_bgRemoved, 'file_location'].values
        frame_number        = len(Files_Names) 
                 
        #Getting the effective air mass from each frame
        air_eff_array   = zeros(frame_number)
        median_values   = empty(frame_number)
        for i in range(len(Files_Names)):
            File_Address        = File_Folder[i] + Files_Names[i]
            frame_data          = pyfits.getdata(File_Address, 0)
            air_eff_array[i]    = pyfits.getval(File_Address, 'AIRMASS', 0)
            median_values[i]    = median(frame_data[stats_section[2]:stats_section[3],stats_section[0]:stats_section[1]])
                     
        #Calculate effective airmass
        if frame_number == 2:
            Airmass_combine = (air_eff_array[0] + air_eff_array[1]) / 2            
        if frame_number == 3:
            Airmass_combine = (air_eff_array[0] + 4 * air_eff_array[1] + air_eff_array[2]) / 6
                
        #Sort names according to max median
        orgFiles_Names  = Files_Names[median_values.argsort()[::-1]]
        Sorted_median   = median_values[median_values.argsort()[::-1]]
                
        #Ready task configuration
        dz.task_attributes['run folder']    = dz.reducFolders['objects']
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['input']         = ','.join(list(File_Folder + orgFiles_Names))
        dz.task_attributes['output']        = File_Name_comb   
        dz.task_attributes['combine']       = 'median'
        dz.task_attributes['scale']         = 'none'
        dz.task_attributes['statsec']       = '[{XA}:{XB},{YA}:{YB}]'.format(XA=stats_section[0],XB=stats_section[1],YA=stats_section[2],YB=stats_section[3])
        dz.task_attributes['reject']        = 'crreject'
        dz.task_attributes['weight']        = '""'             
        dz.task_attributes['gain']          = 'GAIN'
        dz.task_attributes['snoise']        = 'READNOIS'
        dz.run_iraf_task('imcombine', run_externally=False)       
          
        #Add objects to data frame with the new frame_tag
        dz.object_to_dataframe(dz.task_attributes['output'], {'reduc_tag' : 'obj_combine'})
        
#Generate pdf file
idx_print = ((dz.reducDf.frame_tag.isin(targets_with_issues)) & (dz.reducDf.reduc_tag == 'obj_combine')) | ((dz.reducDf.frame_tag.isin(targets_with_issues)) & (dz.reducDf.reduc_tag ==  'frame_bg'))
dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'combine_frames_nobg', ext = 0, plots_type='frame_combine', include_graph=True) 

print 'Data treated'




# import os
# import sys
# import pyfits
# sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
# os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
# os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
# from DZ_observation_reduction import spectra_reduction
# from numpy import zeros, median, mean, empty, argsort
# 
# '''
# Run externally
# python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/E0_Independent_Bg_Component.py
# '''
# 
# #Load iraf pypeline object
# dz = spectra_reduction()
#    
# #Load reduction data frame
# dz.declare_catalogue(dz.Catalogue_folder)
# 
# #Output tag
# data_dict = {'reduc_tag': 'background_removed_component'}
# 
# #Loop through the arms
# colors = ['Blue', 'Red']
# for arm_color in colors:
#         
#     for target in ['[71]', '[3]']:
#                      
#         #Get object and global indeces
#         indeces_objframes   = (dz.reducDf.frame_tag == target) & (dz.reducDf.reduc_tag == 'cosmic_ray_removal') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)   
#      
#         File_Folder         = dz.reducDf.loc[indeces_objframes, 'file_location'].values
#         File_Name           = dz.reducDf.loc[indeces_objframes, 'file_name'].values
#         frame_number        = len(File_Name)
#             
#         #Define flat
#         index_objflat       = (dz.reducDf.reduc_tag == target + '_flatobj_n') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) 
#         obj_flat_address    = dz.reducDf.loc[index_objflat, 'file_location'].values[0] + dz.reducDf.loc[index_objflat, 'file_name'].values[0]
#     
#         #Same illumination frame for all the objects
#         index_illumination  = (dz.reducDf.reduc_tag == 'illumFrame') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color))
#         illum_address       = dz.reducDf.loc[index_illumination, 'file_location'].values[0] + dz.reducDf.loc[index_illumination, 'file_name'].values[0]
#                   
#         #Define cropping region
#         cropping            = dz.observation_dict[arm_color + '_cropping']
#         cropping_region     = '[{rawA}:{rawB},{columnA}:{columnB}]'.format(rawA=cropping[0], rawB=cropping[1],columnA=cropping[2], columnB=cropping[3])
#           
#         #Scaling region
#         obj_scaling_key = '{Color}_scale_region'.format(Color=arm_color)
#         stats_section       = map(int, dz.observation_dict[obj_scaling_key])
#           
#         for i in range(len(File_Name)):
#             
#             File_Name_flatcor   = '{Folder_i}{CodeName_i}_Frame{frame_i}_{color_arm}_f.fits'.format(Folder_i = File_Folder[i], CodeName_i = target.replace('[','').replace(']',''), frame_i = i+1, color_arm=arm_color) 
#             File_Name_trim      = '{Folder_i}{CodeName_i}_Frame{frame_i}_{color_arm}_f_t.fits'.format(Folder_i = File_Folder[i], CodeName_i = target.replace('[','').replace(']',''), frame_i = i+1, color_arm=arm_color) 
#             File_Name_bg        = '{Folder_i}{CodeName_i}_Frame{frame_i}_{color_arm}_f_t_bg.fits'.format(Folder_i = File_Folder[i], CodeName_i = target.replace('[','').replace(']',''), frame_i = i+1, color_arm=arm_color)
#                           
#             #Flat the frame
#             dz.reset_task_dict()
#             dz.task_attributes['color']         = arm_color
#             dz.task_attributes['run folder']    = dz.reducFolders['arcs']
#             dz.task_attributes['input']         = File_Folder[i] + File_Name[i]
#             dz.task_attributes['output']        = File_Name_flatcor
#             dz.task_attributes['flatcor']       = 'yes'
#             dz.task_attributes['flat']          = obj_flat_address
#             dz.task_attributes['illumco']       = 'yes' 
#             dz.task_attributes['illum']         = illum_address
#             dz.run_iraf_task('ccdproc')        
#             dz.object_to_dataframe(File_Name_flatcor, {'reduc_tag': 'frame_flatcor'})    
#                  
#             #Crop the frame
#             dz.reset_task_dict()
#             dz.task_attributes['color']         = arm_color
#             dz.task_attributes['run folder']    = dz.reducFolders['objects']
#             dz.task_attributes['color']         = arm_color
#             dz.task_attributes['input']         = File_Name_flatcor + cropping_region
#             dz.task_attributes['output']        = File_Name_trim  
#             dz.run_iraf_task('imcopy')  
#             dz.object_to_dataframe(File_Name_trim, {'reduc_tag': 'frame_trim'})
#                  
#             #Bg the frame
#             object_reference    = '{CodeName}_refline_{Color}'.format(CodeName=target, Color=arm_color)
#             Store_cords         = dz.observation_dict[object_reference]
#             x_peak, y_peak      = int(Store_cords[0]), int(Store_cords[1])
#              
#             #Getting the crop region
#             Cropping_key    = dz.observation_dict['{Color}_cropping'.format(Color=arm_color)]
#             cropping_area   = map(int, Cropping_key) 
#                   
#             print
#             print cropping_area
#             print '--', object_reference
#             print '--', target, 'reference line:', y_peak - cropping_area[2] #No need to crop in this case
#             print 
# 
#             #Remove background
#             dz.reset_task_dict()
#             dz.task_attributes['run folder']    = dz.reducFolders['objects']
#             dz.task_attributes['color']         = arm_color
#             dz.task_attributes['input']         = File_Name_trim
#             dz.task_attributes['output']        = File_Name_bg  
#             dz.task_attributes['axis']          = 1            
#             dz.run_iraf_task('background', run_externally=True)
#             dz.object_to_dataframe(File_Name_bg, {'reduc_tag': 'frame_bg'})
#        
#         #Generate pdf file
#         idx_print = (dz.reducDf.frame_tag == target) & (dz.reducDf.reduc_tag == 'frame_bg') & (dz.reducDf.valid_file)
#         dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + target  + 'frame_bg', ext = 0, plots_type='flats', include_graph=True) 
#   
#         #--Combine the objects
#         indeces_bgRemoved   = (dz.reducDf.frame_tag == target) & (dz.reducDf.reduc_tag == 'frame_bg') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)   
#         Files_Names         = dz.reducDf.loc[indeces_bgRemoved, 'file_name'].values
#         File_Folder         = dz.reducDf.loc[indeces_bgRemoved, 'file_location'].values
#         File_Name_comb      = '{Folder_i}{CodeName_i}_f_t_comb.fits'.format(Folder_i = File_Folder[0], CodeName_i = target.replace('[','').replace(']',''))
#         frame_number        = len(Files_Names) 
#                 
#         #Getting the effective air mass from each frame
#         air_eff_array   = zeros(frame_number)
#         median_values   = empty(frame_number)
#         for i in range(len(Files_Names)):
#             File_Address        = File_Folder[i] + Files_Names[i]
#             frame_data          = pyfits.getdata(File_Address, 0)
#             air_eff_array[i]    = pyfits.getval(File_Address, 'AIRMASS', 0)
#             median_values[i]    = median(frame_data[stats_section[2]:stats_section[3],stats_section[0]:stats_section[1]])
#                     
#         #Calculate effective airmass
#         if frame_number == 2:
#             Airmass_combine = (air_eff_array[0] + air_eff_array[1]) / 2            
#         if frame_number == 3:
#             Airmass_combine = (air_eff_array[0] + 4 * air_eff_array[1] + air_eff_array[2]) / 6
#                
#         #Sort names according to max median
#         orgFiles_Names  = Files_Names[median_values.argsort()[::-1]]
#         Sorted_median   = median_values[median_values.argsort()[::-1]]
#                
#         #Ready task configuration
#         dz.task_attributes['run folder']    = dz.reducFolders['objects']
#         dz.task_attributes['color']         = arm_color
#         dz.task_attributes['input']         = ','.join(list(File_Folder + orgFiles_Names))
#         dz.task_attributes['output']        = File_Name_comb   
#         dz.task_attributes['combine']       = 'median'
#         dz.task_attributes['scale']         = 'none'
#         dz.task_attributes['statsec']       = '[{XA}:{XB},{YA}:{YB}]'.format(XA=stats_section[0],XB=stats_section[1],YA=stats_section[2],YB=stats_section[3])
#         dz.task_attributes['reject']        = 'crreject'
#         dz.task_attributes['weight']        = '""'             
#         dz.task_attributes['gain']          = 'GAIN'
#         dz.task_attributes['snoise']        = 'READNOIS'
#         dz.run_iraf_task('imcombine', run_externally=False)       
#          
#         #Add objects to data frame with the new frame_tag
#         dz.object_to_dataframe(dz.task_attributes['output'], {'reduc_tag' : 'frameComb_nobackground'})
#     
# #Generate pdf file
# idx_print = (dz.reducDf.reduc_tag == 'frameComb_nobackground') | (dz.reducDf.reduc_tag == 'frame_bg')
# dz.generate_step_pdf(idx_print, file_address = dz.reducFolders['reduc_data'] + 'frame_Combines_nobg', ext = 0, plots_type='frame_combine', include_graph=True) 
# 
# print 'Data treated'
