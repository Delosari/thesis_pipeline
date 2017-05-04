from numpy import copy
from astropy.io import fits
from DZ_observation_reduction import spectra_reduction
 
#Load iraf pypeline object
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
 
ordenes         = ['High', 'Low']
orden_mag       = {'High' : 200, 'Low' : 10}
extension       = 0
plotting_limits = [0,30]
limits_flat     = map(int, dz.observation_dict['Flat_limits'])    
  
#Combine the low and high orders
colors = ['Blue', 'Red']
for arm_color in colors:
       
    frames_dit = {}
    for orden_type in ordenes:
   
        #Get files
        tag             = 'nflatcombine_{orden_type}order'.format(orden_type=orden_type)
        index_ObjFlat   = (dz.reducDf.reduc_tag == tag) & (dz.reducDf.valid_file) & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color))    
       
        file_name       = dz.reducDf.loc[index_ObjFlat].file_name.values[0]
        file_address    = dz.reducDf.loc[index_ObjFlat].file_location.values[0]
         
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
    fits_address = '{folder_output}nMasterFlat{color}.fits'.format(folder_output = dz.reducFolders['flat lamp'], color = arm_color)
    fits.writeto(fits_address, data = New_frame, header = frames_dit['Low_header'], clobber = True)
 
    #Add objects to data frame with the new reduc_tag
    data_dict = {'reduc_tag': 'nflatcombine'}
    dz.object_to_dataframe(fits_address, data_dict)
 
#Generate pdf file
indeces_print = (dz.reducDf.reduc_tag == 'nflatcombine')
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'CombineOrder_nMasterflat', plots_type = 'flats', ext = 0, include_graph=True)
 
dz.beep_alarmn()

# #-------replacing only the wiggles section
# 
# from numpy import copy, zeros, arange, std
# from astropy.io import fits
# from DZ_observation_reduction import spectra_reduction
# from scipy import ndimage
# import matplotlib.pyplot as plt
# import numpy.random as rnd
# 
#  
# #Load iraf pypeline object
# dz = spectra_reduction()
#   
# #Load reduction data frame
# dz.declare_catalogue(dz.Catalogue_folder)
# 
# ordenes         = ['High', 'Low']
# orden_mag       = {'High' : 200, 'Low' : 10}
# extension       = 0
# plotting_limits = [0,30]
# limits_flat     = map(int, dz.observation_dict['Flat_limits'])    
# 
# #Combine the low and high orders
# colors = ['Blue', 'Red']
# for arm_color in colors:
#      
#     sections_flat_key   = 'flat_LowOrder_{color_arm}_fitting_regions'.format(color_arm = arm_color)
#     sections_flat       = dz.observation_dict[sections_flat_key]
#       
#     frames_dit = {}
#     for orden_type in ordenes:
#    
#         #Get files
#         tag             = 'nflatcombine_{orden_type}order'.format(orden_type=orden_type)
#         index_ObjFlat   = (dz.reducDf.reduc_tag == tag) & (dz.reducDf.valid_file) & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color))    
#        
#         file_name       = dz.reducDf.loc[index_ObjFlat].file_name.values[0]
#         file_address    = dz.reducDf.loc[index_ObjFlat].file_location.values[0]
#          
#         with fits.open(file_address + file_name) as hdu_list:
#             frames_dit[orden_type + '_data']   = hdu_list[extension].data
#             frames_dit[orden_type + '_header'] = hdu_list[extension].header
#       
#     #Create frame
#     New_frame     = copy(frames_dit['High_data'])
#     average_noise = std(New_frame)
#        
#     #Generate empty indices matrix
#     matrix_good_regions = zeros(New_frame.shape, bool)
#      
#     low_idx, high_idx = New_frame.shape[0], 0 
#     for j in range(len(sections_flat)):
#         limits_interval = map(int, sections_flat[j].split(':'))
#         limits_interval.sort()
#         matrix_good_regions[limits_interval[0]:limits_interval[1],:] = True
#         print limits_interval
#         if limits_interval[0] < low_idx:
#             low_idx = limits_interval[0]
#         if limits_interval[1] > high_idx:
#             high_idx = limits_interval[1]
#      
#     #Include the edges
#     matrix_good_regions[0:low_idx,:]                    = True
#     matrix_good_regions[high_idx:New_frame.shape[0],:]  = True
#      
#     matrix_wiggles = ~matrix_good_regions
#     New_frame[matrix_wiggles] = frames_dit['Low_data'][matrix_wiggles]
#      
#      
#     #Create the fits file
#     fits_address = '{folder_output}nMasterFlat{color}.fits'.format(folder_output = dz.reducFolders['flat lamp'], color = arm_color)
#     fits.writeto(fits_address, data = New_frame, header = frames_dit['Low_header'], clobber = True)
#  
#     #Add objects to data frame with the new reduc_tag
#     data_dict = {'reduc_tag': 'nflatcombine'}
#     dz.object_to_dataframe(fits_address, data_dict)
#  
# #Generate pdf file
# indeces_print = (dz.reducDf.reduc_tag == 'nflatcombine')
# #dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'CombineOrder_nMasterflat', plots_type = 'fits_compare', ext = 0, include_graph=True, limits=plotting_limits)
# dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'CombineOrder_nMasterflat', plots_type = 'flats', ext = 0, include_graph=True)
#  
# dz.beep_alarmn()

  
# print 'Data treated'
# 
#     gauss       = ndimage.gaussian_filter1d(frames_dit['High_data'], 100, axis=1)
#     
#     #Replace the wiggles region with the low order fit
#     
#     if arm_color == 'Red':
#         y = New_frame[1147-smooth_lenght:1147+smooth_lenght,:].mean(axis=1)        
#         x = arange(1147-smooth_lenght, 1147+smooth_lenght)
#         axis.plot(arange(New_frame.shape[0]), New_frame.mean(axis=1), label = 'complete')
#         axis.plot(x, y, label = 'before')
# 
#     #Smoothing the edges
#     #New_frame[1147-smooth_lenght:1147+smooth_lenght,:] = ndimage.gaussian_filter(New_frame[1147-smooth_lenght:1147+smooth_lenght,:],sigma=5)
#     New_frame[1147-smooth_lenght:1147+smooth_lenght,:] = rnd.normal(1, scale=average_noise, size=New_frame[1147-smooth_lenght:1147+smooth_lenght,:].shape) 
# 
#     if arm_color == 'Red':
#         y = New_frame[1147-smooth_lenght:1147+smooth_lenght,:].mean(axis=1)
#         x = arange(1147-smooth_lenght, 1147+smooth_lenght)
#         axis.plot(x, y, label = 'after')
#         axis.legend()
#         plt.show()    



  
print 'Data treated'

# fig, axis = plt.subplots(1, 1, figsize=(8, 6))  
# smooth_lenght = 5
# 
# files_list =['/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/ffblue1725671.fits',
# '/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/ccdblue1725671.fits',
# '/home/vital/Astrodata/WHT_2011_11/Night1/objects/r01725671_b.fits',
# '/home/vital/Astrodata/WHT_2011_11/Night1/objects/BD+17_Blue_Wide_f.fits']
# 
# for coso in files_list:
#     x, counts_array, header = dz.get_spectra_data(coso, ext=0)
#     y = counts_array.mean(axis=1)
#     axis.plot(arange(len(y)),y,label = coso[coso.rfind('/')+1:-1])
# axis.legend()
# plt.show()


