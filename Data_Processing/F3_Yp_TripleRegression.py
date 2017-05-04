from dazer_methods                      import Dazer
from collections                        import OrderedDict
from numpy                              import empty, random, median, percentile, array, linspace
from scipy                              import stats
from uncertainties                      import ufloat
from uncertainties.unumpy               import nominal_values, std_devs
from libraries.Math_Libraries.sigfig    import round_sig
from pandas import DataFrame
import statsmodels.formula.api as smf
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def latex_float(f):
    float_str = "{0:.2g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
#         return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
        return r"10^{{{}}}".format(int(exponent))
    else:
        return float_str
    
#Create class object
dz = Dazer()
script_code = dz.get_script_code()

#Plot configuration
# dz.FigConf()

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')

#Regressions properties
MC_iterations   = 1000
WMAP_coordinates = array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])

#Generate the indeces
Regresions_dict = OrderedDict()
Regresions_dict['Regressions']      = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
Regresions_dict['metal x axis']     = ['OI_HI_emis', 'NI_HI_emis', 'SI_HI_emis']
Regresions_dict['helium y axis']    = ['Ymass_O_emis',  'Ymass_O_emis', 'Ymass_S_emis']
Regresions_dict['element']          = ['O', 'N', 'S']
# Regresions_dict['factor']           = [1e5, 1e6, 1e6]
Regresions_dict['title']            = ['Helium mass fraction versus oxygen abundance', 'Helium mass fraction versus nitrogen abundance', 'Helium mass fraction versus sulfur abundance']
    
#Get right regression values properties
idxA, idxB          = 0, 2
elementA, elementB  = Regresions_dict['element'][idxA], Regresions_dict['element'][idxB]
acepted_elemA       = catalogue_df.loc[catalogue_df[elementA + '_valid'].isnull()].index.values
acepted_elemB       = catalogue_df.loc[catalogue_df[elementB + '_valid'].isnull()].index.values
acepted_objs        = array(list(set(list(acepted_elemA) + list(acepted_elemB))))

idx_notrejection    = (catalogue_df.index.isin(acepted_objs))

#Get objects which meet regression conditions
idces_metal         = (catalogue_df[elementA + 'I_HI_emis'].notnull()) & (catalogue_df[elementB + 'I_HI_emis'].notnull()) & idx_notrejection
objects             = catalogue_df.loc[idces_metal].index.values
metalA              = catalogue_df.loc[idces_metal, elementA + 'I_HI_emis'].values #* Regresions_dict['factor'][idxA]
metalB              = catalogue_df.loc[idces_metal, elementB + 'I_HI_emis'].values #* Regresions_dict['factor'][idxB]
y                   = catalogue_df.loc[idces_metal, 'Ymass_O_emis'].values

print '--- Using these objs {}:'.format(len(objects)), ', '.join(list(objects))
#print '--- Estos no me gustan {}:'.format(len(reject_objs)), ', '.join(list(reject_objs))
 
#Create containers
metalA_matrix   = empty((len(objects), MC_iterations))
metalB_matrix   = empty((len(objects), MC_iterations))
Y_matrix        = empty((len(objects), MC_iterations))
mA_vector, mB_vector, n_vector = empty(MC_iterations), empty(MC_iterations), empty(MC_iterations)
  
#Generate the distributions
for j in range(len(objects)): 
    metalA_matrix[j,:]  = random.normal(metalA[j].nominal_value, metalA[j].std_dev, size = MC_iterations)
    metalB_matrix[j,:]  = random.normal(metalB[j].nominal_value, metalB[j].std_dev, size = MC_iterations)
    Y_matrix[j,:]       = random.normal(y[j].nominal_value, y[j].std_dev, size = MC_iterations)
  
for k in range(MC_iterations):
    grid_j  = DataFrame({elementA: metalA_matrix[:,k], elementB:metalB_matrix[:,k], 'Y':Y_matrix[:,k]})
    lm      = smf.ols(formula='Y ~ {} + {}'.format(elementA, elementB), data=grid_j).fit()
    mA_vector[k] = lm.params[elementA]
    mB_vector[k] = lm.params[elementB]
    n_vector[k]  = lm.params['Intercept']
      
n_Median, n_16th, n_84th = median(n_vector), percentile(n_vector,16), percentile(n_vector,84) 
m_MedianA, m_16thA, m_84thA = median(mA_vector), percentile(mA_vector,16), percentile(mA_vector,84)
m_MedianB, m_16thB, m_84thB = median(mB_vector), percentile(mB_vector,16), percentile(mB_vector,84)
  
print n_Median, n_16th, n_84th
print m_MedianA, m_16thA, m_84thA
print m_MedianB, m_16thB, m_84thB  

fig     = plt.figure()
ax      = fig.add_subplot(111, projection = '3d')

A_range             = linspace(0.0, max(nominal_values(metalA)) * 1.10, 20)
B_range             = linspace(0.0, max(nominal_values(metalB)) * 1.10, 20)
linear_regresion    = n_Median + m_MedianA * A_range + m_MedianB * B_range

print A_range
print B_range
print linear_regresion

ax.plot(A_range, B_range, linear_regresion, label='{} - {} regression'.format(elementA, elementB))
ax.scatter(nominal_values(metalA), nominal_values(metalB), nominal_values(y), marker='o', label='Sample: {}I_HI, {}I_HI abundances'.format(elementA, elementB))
ax.legend(loc='lower left')

plt.show()
