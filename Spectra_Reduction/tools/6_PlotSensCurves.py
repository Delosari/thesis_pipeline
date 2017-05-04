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
 
#-- Sky frames
ext = 0
indeces  = (dz.reducDf.reduc_tag == 'skycombine_f') & (dz.reducDf.valid_file)
indeces = (dz.reducDf.reduc_tag.str.contains('_flatobj_n'))

# #Figure for the plot            
# Pdf_Fig, GridAxis   = plt.subplots(2, 1, figsize=(6, 7))  
# GridAxis_list       = GridAxis.ravel()

# #Loop through the arms
# for color in ['Blue', 'Red']:
# 
#     for starcode in dz.observation_dict['Standard_stars']:
#         
#         CodeName = starcode.replace('[','').replace(']','')
#     
#         sensfunc_local = '{run_folder}sen_{starcode}_{color}_{slit_size}.fits'.format(run_folder = dz.reducFolders['objects'], starcode = CodeName, color = color, slit_size = 'wide')
#     
#         wavelength, Flux_array, Header_0 = dz.get_spectra_data(sensfunc_local, ext=0)
#             
#         line_Style = '-'
#         
#         if color == 'Blue':
#             GridAxis_list[0].plot(wavelength, Flux_array, label = CodeName, linestyle=line_Style)
#         else:
#             GridAxis_list[1].plot(wavelength, Flux_array, label = CodeName, linestyle=line_Style)        
# 
# 
# #Elena files
# list_curves = {'BD+17' : '/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/sensbd-5.0001.fits',
#             'G191' :    '/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/sensg191.0001.fits',
#             'F34' :     '/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/sensf34-4.0001.fits',
#             'wolf' :    '/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/senswoolf2.0001.fits'}
# 
# 
# for sens_code in list_curves:
#         
#     sensfunc_local = list_curves[sens_code]
# 
#     wavelength, Flux_array, Header_0 = dz.get_spectra_data(sensfunc_local, ext=0)
#     
#     GridAxis_list[0].plot(wavelength, Flux_array, label = sens_code, linestyle='--')

# #Plot layout
# plt.axis('tight')
# for idx, val in enumerate(['Blue arm spectra', 'Red arm spectra']):
#     GridAxis[idx].set_xlabel('Pixel value',          fontsize = 15)
#     GridAxis[idx].set_ylabel('Mean spatial count',   fontsize = 15)
#     GridAxis[idx].set_title(val, fontsize = 15) 
#     GridAxis[idx].tick_params(axis='both', labelsize=10)
#     GridAxis[idx].legend(loc='upper right', prop={'size':14}, ncol=2)  
#    
# #Pdf_Fig.canvas.mpl_connect('pick_event', onpick)
# plt.connect('button_press_event', on_plot_hover)
# plt.show()   



list_curves = ['/home/vital/Astrodata/WHT_2011_11/Night1/objects/sen_Blue_wide.fits',
'/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/reduction-2-blue/sens.fits',
'/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/reduction-2-blue/sens2.fits',
'/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/reduction-2-blue/sensx.fits',
'/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/reduction-2-blue/sensx2.fits',
'/home/vital/Astrodata/WHT_2011_11/Night1_Elena/raw_fits/flux-blue/reduction-2-blue/sens2-s101.fits']

#Figure for the plot            
Pdf_Fig, GridAxis   = plt.subplots(1, 1, figsize=(6, 7))  

for sens_code in list_curves:
          
    wavelength, Flux_array, Header_0 = dz.get_spectra_data(sens_code, ext=0)
    
    curve_name = sens_code[sens_code.rfind('/')+1:-1]
    
    GridAxis.plot(wavelength, Flux_array, label = curve_name)

#Plot layout
plt.axis('tight')
GridAxis.set_xlabel('wavelength $(\AA)$',          fontsize = 15)
GridAxis.set_ylabel('log(m)',   fontsize = 15)
GridAxis.set_title('Sensitivity curves', fontsize = 15) 
GridAxis.tick_params(axis='both', labelsize=10)
GridAxis.legend(loc='upper right', prop={'size':14}, ncol=2)  
   
#Pdf_Fig.canvas.mpl_connect('pick_event', onpick)
plt.connect('button_press_event', on_plot_hover)
plt.show()   


    