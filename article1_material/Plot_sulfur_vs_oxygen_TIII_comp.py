#Perform the linear regression---------------------------
from dazer_methods import Dazer
from numpy import nanmean, nanstd, min as np_min, linspace,  max as np_max, arange
from uncertainties import ufloat
from uncertainties import unumpy
from lib.Math_Libraries.FittingTools import bces_regression

#Generate dazer object
dz = Dazer()

#Define plot frame and colors
size_dict = {'axes.labelsize':35, 'legend.fontsize':24, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':30, 'ytick.labelsize':30}
dz.FigConf(plotSize = size_dict)

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
 
#Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Quick indexing
dz.quick_indexing(catalogue_df)

idcs = (~catalogue_df.TeOIII_emis2nd.isnull() & ~catalogue_df.TeSIII_emis2nd.isnull() & catalogue_df.quick_index.notnull())
  
TeOIII_array = catalogue_df.loc[idcs].TeOIII_emis2nd.values
TeSIII_array = catalogue_df.loc[idcs].TeSIII_emis2nd.values
objects = catalogue_df.loc[idcs].quick_index.values
 
#Make the plot
x_regression            = linspace(0.8 * np_min(unumpy.nominal_values(TeOIII_array)), 1.20 * np_max(unumpy.nominal_values(TeOIII_array)), 10)
y_regression_Garnet92   = (0.83 * x_regression/10000 + 0.17) * 10000
y_regression_EpmDiaz05  = (1.05 * x_regression/10000 - 0.08) * 10000
y_regression_Epm2014    = (0.92 * x_regression/10000 + 0.078) * 10000

#Perform the fit
regr_dict = bces_regression(unumpy.nominal_values(TeOIII_array), unumpy.nominal_values(TeSIII_array), unumpy.std_devs(TeOIII_array), unumpy.std_devs(TeSIII_array))
 
# for i in range(len(regr_dict['m'])):
reg_code = 3
y_fit = regr_dict['m'][reg_code] * x_regression + regr_dict['n'][reg_code]
dz.data_plot(x_regression, y_fit, 'Linear fit', linestyle = '-')
 
dz.data_plot(unumpy.nominal_values(TeOIII_array), unumpy.nominal_values(TeSIII_array), 'HII galaxies', markerstyle='o',  x_error=unumpy.std_devs(TeOIII_array),  y_error=unumpy.std_devs(TeSIII_array), color='tab:blue')
dz.plot_text(unumpy.nominal_values(TeOIII_array), unumpy.nominal_values(TeSIII_array),  objects, fontsize = 17)
  
dz.data_plot(x_regression, y_regression_Garnet92,   'Garnett (1992)', linestyle = ':')
dz.data_plot(x_regression, y_regression_EpmDiaz05,  r'$P\'erez$-Montero et al (2005)', linestyle = '--')
dz.data_plot(x_regression, y_regression_Epm2014,    r'$P\'erez$-Montero (2014)', linestyle = '-.')

dz.Axis.yaxis.set_ticks(arange(8000, 26000, 4000))

Title       = ''#r'Sulfur versus Oxygen temperature comparison'
y_Title     = r'$T_{e}[SIII]\,(K)$'
x_Title     = r'$T_{e}[OIII]\,(K)$'
dz.FigWording(x_Title, y_Title, Title)
#dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/temperatures_comparison')

