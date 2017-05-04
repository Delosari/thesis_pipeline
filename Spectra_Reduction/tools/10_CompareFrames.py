from astropy.io import fits
from matplotlib import pyplot as plt
from DZ_observation_reduction import spectra_reduction
from pyfits                     import getheader, getdata

from matplotlib import rcParams

rcParams.update({'font.size': 30})

font_size= 20

def plotter_4_grid(idx_list, dataframe_list):
    
    Fig, GridAxis       = plt.subplots(2, 2, figsize=(10, 12))
    
    for i in range(len(dataframe_list)):
        
        files_name      = dataframe_list[i].reducDf[idx_list[i]].file_name.values
        files_address   = dataframe_list[i].reducDf[idx_list[i]].file_location.values
                
        for j in range(len(files_name)):
            try:
                ext = 0
                with fits.open(files_address[j] + files_name[j]) as hdu_list:
                    image_data = hdu_list[ext].data
            except:
                ext = 1
                with fits.open(files_address[j] + files_name[j]) as hdu_list:
                    image_data = hdu_list[ext].data
            
            y_values_ver = image_data.mean(axis=1) 
            x_values_ver = range(len(y_values_ver))        
        
            y_values_hor = image_data.mean(axis=0) 
            x_values_hor = range(len(y_values_hor))
            
            GridAxis[0][i].plot(x_values_ver, y_values_ver, label = files_name[j])
            GridAxis[1][i].plot(x_values_hor, y_values_hor, label = files_name[j])
            GridAxis[j][i].legend()
            
        GridAxis[1][i].set_xlabel('Pixel', fontsize = font_size)
        GridAxis[1][i].set_xlabel('Pixel', fontsize = font_size)

        GridAxis[i][0].set_ylabel('Mean column value', fontsize = font_size)
        GridAxis[i][0].set_ylabel('Mean row value', fontsize = font_size)        

        GridAxis[0][i].set_title(files_name, fontsize = font_size)
        GridAxis[0][i].set_title(files_name, fontsize = font_size)        
    
    plt.show()
    
    return

def plotter_compare(idx_list, dataframe_list):

    Fig, GridAxis = plt.subplots(2, 1, figsize=(10, 12))

    line_dict = {}
    line_dict['0'] = '-'
    line_dict['1'] = '--'

    for i in range(len(dataframe_list)):

        files_name      = dataframe_list[i].reducDf[idx_list[i]].file_name.values
        files_address   = dataframe_list[i].reducDf[idx_list[i]].file_location.values

        for j in range(len(files_name)):
            try:
                ext = 0
                with fits.open(files_address[j] + files_name[j]) as hdu_list:
                    image_data = hdu_list[ext].data
            except:
                ext = 1
                with fits.open(files_address[j] + files_name[j]) as hdu_list:
                    image_data = hdu_list[ext].data

            y_values_ver = image_data.mean(axis=1) 
            x_values_ver = range(len(y_values_ver))        
        
            y_values_hor = image_data.mean(axis=0) 
            x_values_hor = range(len(y_values_hor))

            GridAxis[0].plot(x_values_ver, y_values_ver, label = files_name[j], linestyle = line_dict[str(i)], linewidth = 3)
            GridAxis[1].plot(x_values_hor, y_values_hor, label = files_name[j], linestyle = line_dict[str(i)], linewidth = 3)
            
        GridAxis[i].set_xlabel('Pixel', fontsize = font_size)

        GridAxis[i].set_ylabel('Mean pixel value', fontsize = font_size)
        
    GridAxis[0].set_title('Spectral direction', fontsize = font_size)
    GridAxis[1].set_title('Spatial direction', fontsize = font_size)
    GridAxis[0].legend(fontsize = font_size)
    GridAxis[1].legend(fontsize = font_size)
    
    plt.show()

def plotter_compare_spectra(idx_list, dataframe_list):

    Fig, GridAxis = plt.subplots(1, 1, figsize=(10, 12))

    line_dict = {}
    line_dict['0'] = '-'
    line_dict['1'] = '--'

    for i in range(len(dataframe_list)):

        files_name      = dataframe_list[i].reducDf[idx_list[i]].file_name.values
        files_address   = dataframe_list[i].reducDf[idx_list[i]].file_location.values

        for j in range(len(files_name)):
#             try:
            ext = 0
            Flux_array  = getdata(files_address[j] + files_name[j], ext=ext)
#             except:
#                 ext = 1
#                 Flux_array  = getdata(files_address[j] + files_name[j], ext=ext)

            y_values_ver = Flux_array[0][0]
            x_values_ver = range(len(y_values_ver))
            print y_values_ver
            print x_values_ver       
        
            GridAxis.plot(x_values_ver, y_values_ver, label = files_name[j], linestyle = line_dict[str(i)], linewidth = 4)
            
        GridAxis.set_xlabel('Pixel', fontsize = font_size)

        GridAxis.set_ylabel('Mean pixel value', fontsize = font_size)
        
    GridAxis.set_title('Extracted spectrum', fontsize = font_size)
    GridAxis.legend(fontsize = font_size)
    
    plt.show()


#Load the catalogues

dz_vit = spectra_reduction()
dz_vit.declare_catalogue(catalogue_address = '/home/vital/Astrodata/WHT_2011_11/Night1/')
dz_ele = spectra_reduction()
dz_ele.declare_catalogue(catalogue_address = '/home/vital/Astrodata/WHT_2011_11/Night1_Elena/')


# #Plot 
# list_files1, list_files2 = ['master_bias_Blue.fits'], ['Zero-blue.fits']
# idx1 = dz_vit.reducDf.file_name.isin(list_files1) & (dz_vit.reducDf.ISIARM == 'Blue arm')
# idx2 = dz_ele.reducDf.file_name.isin(list_files2) & (dz_ele.reducDf.ISIARM == 'Blue arm')
# plotter_4_grid([idx1, idx2], [dz_vit, dz_ele])

#Loop through the files
list_files1, list_files2 = ['r01725595_b.fits', 'flat_combine_Blue.fits' ], ['ccdblue1725595.fits', 'Flat.fits']
list_files1, list_files2 = ['master_bias_Blue_b.fits'], ['Zero-blue.fits']
list_files1, list_files2 = ['flat_combine_Blue.fits'], ['Flat.fits']
# list_files1, list_files2 = ['r01725769_b.fits', 'r01725771_b.fits', 'r01725772_b.fits', 'r01725775_b.fits', 'r01725777_b.fits'], ['ccdblue1725769.fits', 'ccdblue1725771.fits', 'ccdblue1725772.fits', 'ccdblue1725775.fits', 'ccdblue1725777.fits']
# list_files1, list_files2 = ['r01725769_b_cr.fits', 'r01725771_b_cr.fits', 'r01725772_b_cr.fits', 'r01725775_b_cr.fits', 'r01725777_b_cr.fits'], ['ccdblue1725769.fits', 'ccdblue1725771.fits', 'ccdblue1725772.fits', 'ccdblue1725775.fits', 'ccdblue1725777.fits']
list_files1, list_files2 = ['sky_combine_Blue.fits'], ['flatskyblue.fits']
# list_files1, list_files2 = ['nMasterFlatBlue.fits'], ['nFlat.fits']
# list_files1, list_files2 = ['70_Blue.fits'], ['PHL70blue.fits'] #Combined images
# list_files1, list_files2 = ['r01725671_b.fits'], ['ccdblue1725671.fits'] #Standard star bias corrected
# 
# list_files1, list_files2 = ['sky_combine_Blue_f.fits'], ['ffflatskyblue.fits'] #skys flat corrected
# list_files1, list_files2 = ['illumflat_Blue.fits'], ['nskyblue.fits'] #illumination frame
# list_files1, list_files2 = ['BD+17_Blue_Wide_f.fits', 'BD+17_Blue_Narrow_f.fits', 'wolf_Blue_Wide_f.fits'], ['ffblue1725671.fits', 'ffblue1725673.fits', 'ffblue1725682.fits']  #illumination frame
# 
# list_files1, list_files2 = ['BD+17_Blue_Wide_f_e.fits', 'BD+17_Blue_Narrow_f_e.fits', 'wolf_Blue_Wide_f_e.fits'], ['1dblue1725671.0001.fits', '1dblue1725673.0001.fits', '1dblue1725682.0001.fits']  #illumination frame

idx1 = dz_vit.reducDf.file_name.isin(list_files1) & (dz_vit.reducDf.ISIARM == 'Blue arm')
idx2 = dz_ele.reducDf.file_name.isin(list_files2) & (dz_ele.reducDf.ISIARM == 'Blue arm')
plotter_compare([idx1, idx2], [dz_vit, dz_ele])
#plotter_compare_spectra([idx1, idx2], [dz_vit, dz_ele])

#plt.tight_layout()
