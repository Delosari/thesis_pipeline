import numpy as np
from uncertainties import ufloat, unumpy
from dazer_methods import Dazer
 
#Generate dazer object
dz = Dazer()
  
#Set figure format
dz.FigConf()
  
file_tradional_reduc    = '/home/vital/Dropbox/Astrophysics/Data/Fabian_Catalogue/data/Traditional_Abundances.xlsx'
file_starlight          = '/home/vital/Dropbox/Astrophysics/Data/Fabian_Catalogue/data/Starlight_Abundances.xlsx'
  
df_dict = {}
df_dict['traditional']  = dz.load_excel_DF(file_tradional_reduc)
df_dict['starlight']    = dz.load_excel_DF(file_starlight)
      
type    = 'traditional'
element = 'Oxygen'
  
conf_dict = {}
conf_dict['Oxygen_xlabel']      = r'y'
conf_dict['Nitrogen_xlabel']    = r'N/H $(10^{-6})$'
conf_dict['ylabel']             = r'$Y$'
conf_dict['title']              = 'Helium mass fraction versus {} abundance'.format(element)
conf_dict['legend_label']       = 'Data generated from {} treatment'.format(type)
conf_dict['Oxygen_color']       = 'green'
conf_dict['Nitrogen_color']     = 'blue'
  
x       = df_dict[type][element]
y       = df_dict[type].y
x_err   = df_dict[type][element + '_error']
y_err   = df_dict[type].y_error
objCodes = np.arange(1, len(df_dict[type].index) + 1).astype(str)
 
NO = (unumpy.uarray(df_dict[type]['Nitrogen'].values, df_dict[type]['Nitrogen_error'].values) * 1e-6) / (unumpy.uarray(df_dict[type]['Oxygen'].values, df_dict[type]['Oxygen_error'].values) * 1e-5)
 
dz.data_plot(y, unumpy.nominal_values(NO), label = conf_dict['legend_label'], color=conf_dict[element + '_color'], markerstyle = 'o', x_error = y_err, y_error=unumpy.std_devs(NO))
dz.plot_text(y, unumpy.nominal_values(NO), objCodes)
dz.FigWording(conf_dict[element + '_xlabel'], 'N/O', conf_dict['title'])
 
dz.display_fig()


# import numpy as np
# from uncertainties import ufloat, unumpy
# from dazer_methods import Dazer
#  
# #Generate dazer object
# dz = Dazer()
#   
# #Set figure format
# dz.FigConf()
#   
# file_tradional_reduc    = '/home/vital/Dropbox/Astrophysics/Data/Fabian_Catalogue/data/Traditional_Abundances.xlsx'
# file_starlight          = '/home/vital/Dropbox/Astrophysics/Data/Fabian_Catalogue/data/Starlight_Abundances.xlsx'
#   
# df_dict = {}
# df_dict['traditional']  = dz.load_excel_DF(file_tradional_reduc)
# df_dict['starlight']    = dz.load_excel_DF(file_starlight)
#       
# type = 'starlight'
# element = 'Oxygen'
#   
# conf_dict = {}
# conf_dict['Oxygen_xlabel']      = r'O/H $(10^{-5})$'
# conf_dict['Nitrogen_xlabel']    = r'N/H $(10^{-6})$'
# conf_dict['ylabel']             = r'$Y$'
# conf_dict['title']              = 'Helium mass fraction versus {} abundance'.format(element)
# conf_dict['legend_label']       = 'Data generated from {} treatment'.format(type)
# conf_dict['Oxygen_color']       = 'green'
# conf_dict['Nitrogen_color']     = 'blue'
#   
# x       = df_dict[type][element]
# y       = df_dict[type].Y
# x_err   = df_dict[type][element + '_error']
# y_err   = df_dict[type].Y_error
# objCodes = np.arange(1, len(df_dict[type].index) + 1).astype(str)
#  
# NO = (unumpy.uarray(df_dict[type]['Nitrogen'].values, df_dict[type]['Nitrogen_error'].values) * 1e-6) / (unumpy.uarray(df_dict[type]['Oxygen'].values, df_dict[type]['Oxygen_error'].values) * 1e-5)
#  
# dz.data_plot(x, unumpy.nominal_values(NO), label = conf_dict['legend_label'], color=conf_dict[element + '_color'], markerstyle = 'o', x_error = x_err, y_error=unumpy.std_devs(NO))
# dz.plot_text(x, unumpy.nominal_values(NO), objCodes)
# dz.FigWording(conf_dict[element + '_xlabel'], 'N/O', conf_dict['title'])
#  
# dz.display_fig()
# dz.data_plot(x, y, label = conf_dict['legend_label'], color=conf_dict[element + '_color'], markerstyle = 'o', x_error = x_err, y_error=y_err)
# dz.plot_text(x, y, objCodes)
#   
# dz.FigWording(conf_dict[element + '_xlabel'], conf_dict['ylabel'], conf_dict['title'])
#   
# dz.display_fig()



# import numpy as np
# from uncertainties import ufloat
# from dazer_methods import Dazer
# from astropy.io import fits
#  
# #Generate dazer object
# dz = Dazer()
#  
# #Set figure format
# dz.FigConf()
#  
# #Load the data
# fits_address = '/home/vital/Dropbox/Astrophysics/Data/Fabian_Catalogue/10/spec10_dr10.fits'
#  
# data_array = fits.getdata(fits_address, ext=0)   
# header0 = fits.getheader(fits_address, ext=0)
# header1 = fits.getheader(fits_address, ext=1)
# header2 = fits.getheader(fits_address, ext=2)
#  
# flux = data_array['flux']
# WavelenRange = 10.0**data_array['loglam']
# # SDSS_z = float(header2["Z"] + 1)
# # Wavelength_z = WavelenRange / SDSS_z
#  
# dz.data_plot(WavelenRange, flux, label='')
# dz.insert_image('/home/vital/Dropbox/Astrophysics/Seminars/Angeles_Seminar/SDSS10.png', Image_Coordinates = [0.82,0.78], Zoom=0.25, Image_xyCoords = 'axes fraction')
# dz.FigWording(r'Wavelength $(\AA)$', r'Flux $(10^{-17}\,erg\,cm^{-2} s^{-1} \AA^{-1})$', 'SDSSJ082334.84+031315.6 spectrum')
# dz.display_fig()
# dz.savefig('/home/vital/Dropbox/Astrophysics/Seminars/Angeles_Seminar/' + 'SDSSJ082334', extension='.png')




