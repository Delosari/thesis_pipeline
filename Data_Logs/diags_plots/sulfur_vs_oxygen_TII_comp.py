#Perform the linear regression---------------------------
from dazer_methods import Dazer
from numpy import nanmean, nanstd, min as np_min, linspace,  max as np_max
from uncertainties import ufloat
from uncertainties import unumpy
 
#Generate dazer object
dz = Dazer()
dz.FigConf()
dz.load_elements()
 
#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
 
#Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

idcs = (~catalogue_df.TeOII_from_TeOIII_emis.isnull()) & (~catalogue_df.TeSIII_emis.isnull())
  
TeOII_array = catalogue_df.loc[idcs].TeOII_from_TeOIII_emis.values
TeSIII_array = catalogue_df.loc[idcs].TeSIII_emis.values
objects = catalogue_df.loc[idcs].index.values
 
#Make the plot
x_regression = linspace(0.8 * np_min(unumpy.nominal_values(TeOII_array)), 1.20 * np_max(unumpy.nominal_values(TeOII_array)), 10)
# y_regression_Epm2014    = (0.92 * x_regression/10000 + 0.078) * 10000
y_regression_One = 1.0 * x_regression + 0.0
 
 
#Perform the fit
regr_dict = bces_regression(unumpy.nominal_values(TeOII_array), unumpy.nominal_values(TeSIII_array), unumpy.std_devs(TeOII_array), unumpy.std_devs(TeSIII_array))
 
# for i in range(len(regr_dict['m'])):
reg_code = 0
y_fit = regr_dict['m'][reg_code] * x_regression + regr_dict['n'][reg_code]
dz.data_plot(x_regression, y_fit, 'Sample fit ({})'.format(regr_dict['methodology'][reg_code]), linestyle = '--')
 
dz.data_plot(unumpy.nominal_values(TeOII_array), unumpy.nominal_values(TeSIII_array), 'HII galaxies', markerstyle='o',  x_error=unumpy.std_devs(TeOII_array),  y_error=unumpy.std_devs(TeSIII_array))
dz.plot_text(unumpy.nominal_values(TeOII_array), unumpy.nominal_values(TeSIII_array),  objects)
dz.data_plot(x_regression, y_regression_One, '', color = 'black', linestyle = '--') 
 
#dz.data_plot(x_regression, y_regression_Epm2014, r'[$P\'erez$ montero 2014] models', linestyle = '--')
  
Title       = r'Sulfur TSIII versus Oxygen TOII temperature comparison'
y_Title     = r'$T_{e}[SIII]\,(K)$'
x_Title     = r'$T_{e}[OII]\,(K)$'
dz.FigWording(x_Title, y_Title, Title)

dz.display_fig()


