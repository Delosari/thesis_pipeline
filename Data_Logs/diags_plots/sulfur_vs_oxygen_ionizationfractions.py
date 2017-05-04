#Ionization fractions---------------------------
from dazer_methods import Dazer
from numpy import nanmean, nanstd, min as np_min, linspace,  max as np_max
from uncertainties import ufloat, umath
from uncertainties import unumpy
from libraries.Math_Libraries.FittingTools import bces_regression
  
#Generate dazer object
dz = Dazer()

#Define plot frame and colors
size_dict = {'axes.labelsize':20, 'legend.framealpha':None, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)

#Load catalogue dataframe
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)

idcs    = ~catalogue_df.OII_HII_emis2nd.isnull() & ~catalogue_df.OIII_HII_emis2nd.isnull() & ~catalogue_df.SII_HII_emis2nd.isnull() & ~catalogue_df.SIII_HII_emis2nd.isnull() & (catalogue_df.quick_index.notnull()) 
   
TeOIII_array = catalogue_df.loc[idcs].TeOIII_emis.values
TeSIII_array = catalogue_df.loc[idcs].TeSIII_emis.values
   
#Axis values
objects             = catalogue_df.loc[idcs].index.values
OII_HII_abundances  = catalogue_df.loc[idcs].OII_HII_emis2nd.values
OIII_HII_abundances = catalogue_df.loc[idcs].OIII_HII_emis2nd.values
SII_HII_abundances  = catalogue_df.loc[idcs].SII_HII_emis2nd.values
SIII_HII_abundances = catalogue_df.loc[idcs].SIII_HII_emis2nd.values
quick_reference     =  catalogue_df.loc[idcs].quick_index.values

oxygen_ratio = OII_HII_abundances / OIII_HII_abundances
sulfur_ratio = SII_HII_abundances / SIII_HII_abundances
  
dz.data_plot(unumpy.nominal_values(sulfur_ratio), unumpy.nominal_values(oxygen_ratio), 'HII galaxies', markerstyle='o',  x_error=unumpy.std_devs(sulfur_ratio),  y_error=unumpy.std_devs(oxygen_ratio))
dz.plot_text(unumpy.nominal_values(sulfur_ratio), unumpy.nominal_values(oxygen_ratio),  quick_reference)

Title       = r'Oxygen versus Sulfur ionization fractions'
y_Title     = r'$\frac{O^{+}}{O^{2+}}$'
x_Title     = r'$\frac{S^{+}}{S^{2+}}$'
dz.FigWording(x_Title, y_Title, Title)  #, XLabelPad = 20
dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/Images/ionizationFraction')