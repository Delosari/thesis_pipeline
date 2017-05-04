from    numpy import copy
from    astropy.io import fits
from    DZ_observation_reduction import spectra_reduction

#Load iraf pypeline object
dz = spectra_reduction()
  
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)   

#Loop through the arms
extension   = 0
colors      = ['Blue','Red']
ordenes     = ['High', 'Low']

#Combine the low and high orders
for arm_color in colors:

    list_targets = dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']

    for i in range(len(list_targets)):
        
        #Store the data and header
        frames_dit  = {}
        obj_target  = list_targets[i]

        for orden_type in ordenes:
                     
            tag             = '{flat_code}_{orden_type}order'.format(flat_code = obj_target + '_nflatobj', orden_type=orden_type)
            idx_ObjFlat     = (dz.reducDf.reduc_tag == tag) & (dz.reducDf.valid_file) & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color))    
      
            file_name       = dz.reducDf.loc[idx_ObjFlat].file_name.values[0]
            file_address    = dz.reducDf.loc[idx_ObjFlat].file_location.values[0]
        
            with fits.open(file_address + file_name) as hdu_list:
                frames_dit[orden_type + '_data']   = hdu_list[extension].data
                frames_dit[orden_type + '_header'] = hdu_list[extension].header    

        #Create frame
        New_frame   = copy(frames_dit['Low_data'])
                                
        #Set edges with high order fit
        limits_flat = map(int, dz.observation_dict['Flat_limits'])   
        if arm_color == 'Blue':
            New_frame[0:limits_flat[0],:]  =  frames_dit['High_data'][0:limits_flat[0],:]
            New_frame[limits_flat[1]:-1,:] =  frames_dit['High_data'][limits_flat[1]:-1,:]
        else:
            New_frame[0:limits_flat[2],:]   =  frames_dit['High_data'][0:limits_flat[2],:]
            New_frame[limits_flat[3]:-1,:]  =  frames_dit['High_data'][limits_flat[3]:-1,:]            

        #Create the fits file
        fits_address = '{folder_output}{object}_nflatobj{color}.fits'.format(folder_output = dz.reducFolders['flat lamp'], object = obj_target, color=arm_color).replace('[','').replace(']','')
        fits.writeto(fits_address, data = New_frame, header = frames_dit['Low_header'], clobber = True)

        #Add objects to data frame with the new reduc_tag
        data_dict = {'reduc_tag': obj_target + '_flatobj_n'}
        dz.object_to_dataframe(fits_address, data_dict)            
                      
#Generate pdf file
indeces_to_pdf = (dz.reducDf.reduc_tag.str.contains('_flatobj_n'))
dz.generate_step_pdf(indeces_to_pdf, file_address = dz.reducFolders['reduc_data'] + 'CombineOrder_nObjectsflat', plots_type = 'flats', ext = 0, include_graph=True)

print 'Data treated'


# from    numpy import copy
# from    astropy.io import fits
# import  matplotlib.pyplot as plt
# from    DZ_observation_reduction import spectra_reduction
# 
# #Load iraf pypeline object
# dz = spectra_reduction()
#   
# #Load reduction data frame
# dz.declare_catalogue(dz.Catalogue_folder)   
# 
# #Loop through the arms
# extension   = 0
# colors      = ['Blue','Red']
# ordenes     = ['High', 'Low']
# Blue_lim    = map(int, dz.observation_dict['Flat_Blue_limits'])
# Red_lim     = map(int, dz.observation_dict['Flat_Red_limits'])
# 
# #Define image
# Fig     = plt.figure(figsize = (16,10))
# Axis    = Fig.add_subplot(111)
# 
# #Combine the low and high orders
# for arm_color in colors:
# 
#     list_targets = dz.observation_dict['objects'] + dz.observation_dict['Standard_stars']
# 
#     for i in range(len(list_targets)):
#         
#         #Store the data and header
#         frames_order_dict  = {}
#         obj_target  = list_targets[i]
# 
#         for orden_type in ordenes:
#                      
#             tag             = '{flat_code}_{orden_type}order'.format(flat_code = obj_target + '_nflatobj', orden_type=orden_type)
#             idx_ObjFlat     = (dz.reducDf.reduc_tag == tag) & (dz.reducDf.valid_file) & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color))    
#       
#             file_name       = dz.reducDf.loc[idx_ObjFlat].file_name.values[0]
#             file_address    = dz.reducDf.loc[idx_ObjFlat].file_location.values[0]
#         
#             with fits.open(file_address + file_name) as hdu_list:
#                 frames_order_dict[orden_type + '_data']   = hdu_list[extension].data
#                 frames_order_dict[orden_type + '_header'] = hdu_list[extension].header    
# 
#         #Create frame
#         New_frame = copy(frames_order_dict['Low_data'])
#             
#         #Set edges with high order fit 
#         if arm_color == 'Blue':
#             New_frame[0:Blue_lim[0],:]  =  frames_order_dict['High_data'][0:Blue_lim[0],:]
#             New_frame[Blue_lim[1]:-1,:] =  frames_order_dict['High_data'][Blue_lim[1]:-1,:]
#         else:
#             New_frame[0:Red_lim[0],:]   =  frames_order_dict['High_data'][0:Red_lim[0],:]
#             New_frame[Red_lim[1]:-1,:]  =  frames_order_dict['High_data'][Red_lim[1]:-1,:]            
#             
#         #Create the fits file
#         fits_address = '{folder_output}{object}_nflatobj{color}.fits'.format(folder_output = dz.reducFolders['flat lamp'], object = obj_target, color=arm_color).replace('[','').replace(']','')
#         fits.writeto(fits_address, data = New_frame, header = frames_order_dict['Low_header'], clobber = True)
#             
#         #Add objects to data frame with the new reduc_tag
#         data_dict = {'reduc_tag': obj_target + '_flatobj_n'}
#         dz.object_to_dataframe(fits_address, data_dict)            
#                       
# #Generate pdf file
# indeces_to_pdf = (dz.reducDf.reduc_tag.str.contains('_flatobj_n'))
# dz.generate_step_pdf(indeces_to_pdf, file_address = dz.reducFolders['reduc_data'] + 'object_flats_Highlow_orders', plots_type = 'fits_compare', ext = 0, include_graph=True) 
#      
# print 'Data treated'
