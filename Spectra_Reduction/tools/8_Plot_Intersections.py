from numpy                      import argwhere, isclose, arange as np_range, zeros
from astropy.io                 import fits
from matplotlib                 import pyplot as plt
from DZ_observation_reduction   import spectra_reduction
 
def onpick(event):
    if event.button == 3:
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            x_cords, y_cords = int(x + 0), int(y + 0)
            print 'X coords', x_cords
              
#Objects and file
dz = spectra_reduction()
    
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)
 
#extension for the flats
ext = 0
  
#Figure for the plot            
Pdf_Fig, GridAxis   = plt.subplots(2, 1, figsize=(12, 9))  
  
#Loop through the arms
colors = ['Blue', 'Red']
for arm_color in colors:
     
    #Locate frames of interest
    indeces             = ((dz.reducDf.reduc_tag == 'nflatcombine_Highorder') | (dz.reducDf.reduc_tag == 'nflatcombine_Loworder')) & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color))
    index_combine       = (dz.reducDf.reduc_tag == 'flatcombine') & (dz.reducDf.ISIARM == '{color} arm'.format(color=arm_color))
     
    files_name          = dz.reducDf[indeces].sort_values(['reduc_tag']).file_name.values
    files_address       = dz.reducDf[indeces].sort_values(['reduc_tag']).file_location.values
    file_comb_name      = dz.reducDf[index_combine].file_name.values[0]
    file_comb_address   = dz.reducDf[index_combine].file_location.values[0]
     
    #Dict to store the fits data 
    values_dict         = {} 
     
    #Blue spectra on top, red down
    axis_index          = dz.plots_dict[arm_color]
     
    #Loop through the files (assumes two)
    for i in range(len(files_name)):
         
        CodeName = files_name[i][0:files_name[i].find('.')]
         
        #Open the frames
        with fits.open(files_address[i] + files_name[i]) as hdu_list:
            image_data = hdu_list[ext].data
          
        y_values = image_data.mean(axis=1) 
        x_values = np_range(len(y_values))
         
        #Plot the response curves
        GridAxis[axis_index].plot(x_values, y_values, label = CodeName, gid=files_name[i])
         
        #Store the data for later
        values_dict[i]      = y_values
        values_dict['x']    = x_values
         
    #Plot the intersections between the frames
    idx_match = argwhere(isclose(values_dict[0], values_dict[1], atol=0.0005)).reshape(-1)
    GridAxis[axis_index].scatter(values_dict['x'][idx_match], values_dict[0][idx_match], label='Curves intersections', color='brown')
     
    #Plot edges limits
    if 'Flat_limits' in dz.observation_dict:
        limits_flat = map(int, dz.observation_dict['Flat_limits'])
        GridAxis[axis_index].axvline(limits_flat[2*axis_index + 0], color = 'red', linestyle = '--', label = 'Flat limits')
        GridAxis[axis_index].axvline(limits_flat[2*axis_index + 1], color = 'red', linestyle = '--', label = '')
 
    #Plot crop limits
    entry_dict = '{color}_cropping'.format(color = arm_color)
    if entry_dict in dz.observation_dict:
        limits_crop = map(float, dz.observation_dict[entry_dict])
        GridAxis[axis_index].axvline(limits_crop[2], color = 'black', linestyle = '--', label = 'Cropping limits')
        GridAxis[axis_index].axvline(limits_crop[3], color = 'black', linestyle = '--', label = '')
 
    #Plot combine flat
    with fits.open(file_comb_address + file_comb_name) as hdu_list:
        image_comb_data = hdu_list[ext].data
  
    y_values = image_comb_data.mean(axis=1) 
    x_values = values_dict['x']
     
    Axis2 = GridAxis[axis_index].twinx()
    line = Axis2.plot(x_values, y_values, label = 'Master flat ' + arm_color.lower(), color='purple')
    for tl in Axis2.get_yticklabels():
        tl.set_color(line[0].get_color())


    #Plot the fit regions
    entry_dict = 'flat_{order}Order_{color}_fitting_regions'.format(order='Low', color=arm_color)
    if entry_dict in dz.observation_dict:
        ranges_fit = dz.observation_dict[entry_dict]
        for j in range(len(ranges_fit)):
            limits_interval = map(int, ranges_fit[j].split(':'))
            x_interval      = x_values[limits_interval[0]:limits_interval[1]]
            y_interval      = y_values[limits_interval[0]:limits_interval[1]]
            label_region    = 'Fitting region' if j == 0 else ''
            Axis2.fill_between(x_interval, 0, y_interval, facecolor='purple', alpha=0.2, label= label_region)    
    Axis2.legend(loc='upper right', prop={'size':14})
    
#Plot layout
for idx, val in enumerate(['Blue arm spectra', 'Red arm spectra']):
    GridAxis[idx].set_xlabel('Pixel value',          fontsize = 15)
    GridAxis[idx].set_ylabel('Mean spatial count',   fontsize = 15)
    GridAxis[idx].set_title(val, fontsize = 20) 
    GridAxis[idx].tick_params(axis='both', labelsize=14)
    GridAxis[idx].legend(loc='upper left', prop={'size':14}, ncol=1)  
    GridAxis[idx].set_xlim(0, len(values_dict['x']))
    GridAxis[idx].set_ylim(0.6, 1.3)
 
# plt.axis('tight')
 
plt.connect('button_press_event', onpick)
plt.show()   
 
 
     