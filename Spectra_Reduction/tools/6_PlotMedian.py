from astropy.io import fits
from matplotlib import pyplot as plt
from DZ_observation_reduction import spectra_reduction
 
def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    print 'onpick points:', zip(xdata[ind], ydata[ind])
 
def on_plot_hover(event):
    for axis in GridAxis_list:
        for curve in axis.get_lines():
            if curve.contains(event)[0]:
                print curve.get_gid()
  
#Objects and file
dz = spectra_reduction()
   
#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

print dz.reducDf.OBJECT.unique()

#-- Sky frames
ext = 1 
indeces = (dz.reducDf.frame_tag == 'arc') & (dz.reducDf.file_location.str.contains('/raw_fits/'))
# ext = 0
# indeces  = (dz.reducDf.frame_tag == 'SHOC579') & ((dz.reducDf.reduc_tag == 'frame_bg') | (dz.reducDf.reduc_tag == 'obj_combine'))
# ext = 1 
# indeces  = (dz.reducDf.OBJECT == 'SP0031-124')  & (dz.reducDf.file_location.str.contains('/raw_fits/'))


files_name          = dz.reducDf[indeces].sort_values(['RUN']).file_name.values
files_address       = dz.reducDf[indeces].sort_values(['RUN']).file_location.values
frames_color        = dz.reducDf[indeces].sort_values(['RUN']).ISIARM.values
frames_object       = dz.reducDf[indeces].sort_values(['RUN']).OBJECT.values
valid_array         = dz.reducDf[indeces].sort_values(['RUN']).OBJECT.values
validity_check      = dz.reducDf[indeces].sort_values(['RUN']).valid_file.values

#Figure for the plot            
Pdf_Fig, GridAxis   = plt.subplots(2, 1, figsize=(6, 7))  
GridAxis_list       = GridAxis.ravel()
 
count = {}
count['blue']   = 0
count['red']    = 0 
 
#Loop through the arms
for i in range(len(files_name)):
      
    CodeName = files_name[i][0:files_name[i].find('.')]
      
    with fits.open(files_address[i] + files_name[i]) as hdu_list:
        image_data = hdu_list[ext].data
      
    y_values = image_data.mean(axis=1) 
    x_values = range(len(y_values))
     
    line_Style = '-' if validity_check[i] else ':' 
     
    if frames_color[i] == 'Blue arm':
        GridAxis_list[0].plot(x_values, y_values, label = CodeName, linestyle=line_Style, gid=files_name[i])
        count['blue'] += 1
    else:
        GridAxis_list[1].plot(x_values, y_values, label = CodeName, linestyle=line_Style, gid=files_name[i])        
        count['red'] += 1
 
for coso in count:
    print coso, 'count: ', count[coso]
      
#Plot layout
plt.axis('tight')
for idx, val in enumerate(['Blue arm spectra', 'Red arm spectra']):
    GridAxis[idx].set_xlabel('Pixel value',          fontsize = 15)
    GridAxis[idx].set_ylabel('Mean spatial count',   fontsize = 15)
    GridAxis[idx].set_title(val, fontsize = 15) 
    GridAxis[idx].tick_params(axis='both', labelsize=10)
    GridAxis[idx].legend(loc='upper right', prop={'size':14}, ncol=2)  
    
#Pdf_Fig.canvas.mpl_connect('pick_event', onpick)
plt.connect('button_press_event', on_plot_hover)
plt.show()   

#Figure for the plot            
# Pdf_Fig, GridAxis   = plt.subplots(1, 1, figsize=(6, 7))  
#  
# count = {}
# count['blue']   = 0
# count['red']    = 0 
#  
# #Loop through the arms
# for i in range(len(files_name)):
#       
#     CodeName = files_name[i][0:files_name[i].find('.')]
#       
#     with fits.open(files_address[i] + files_name[i]) as hdu_list:
#         image_data = hdu_list[ext].data
#       
#     y_values = image_data.mean(axis=1) 
#     x_values = range(len(y_values))
#      
#     line_Style = '-' if validity_check[i] else ':' 
#      
#     GridAxis.plot(x_values, y_values, label = CodeName, linestyle=line_Style)        
#     count['red'] += 1
#       
# #Plot layout
# plt.axis('tight')
# for idx, val in enumerate(['Blue arm spectra', 'Red arm spectra']):
#     GridAxis.set_xlabel('Pixel value',          fontsize = 15)
#     GridAxis.set_ylabel('Mean spatial count',   fontsize = 15)
#     GridAxis.set_title(val, fontsize = 15) 
#     GridAxis.tick_params(axis='both', labelsize=10)
#     GridAxis.legend(loc='upper right', prop={'size':14}, ncol=2)  
#     
# plt.show()   

    