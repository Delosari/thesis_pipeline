#Perform the linear regression---------------------------
from dazer_methods import Dazer
from numpy import nanmean, nanstd, min as np_min, linspace,  max as np_max, size, empty, random, array, mean
from uncertainties import ufloat
from uncertainties import unumpy
from libraries.Math_Libraries.FittingTools import bces_regression
import statsmodels.formula.api as smf
from mpl_toolkits.mplot3d import Axes3D
import pymc as pm
import pymc3 as pm3
from lmfit import Model

def linear_model(x, m, n):
    return m*x+n

def multlinear_model(x, y, m1, m2, n):
    return m1 * x + m2 * y + n
    
def bayes_model(x, x_error, y, y_error):
    m = pm.Uniform('m', 0, 3, value=1)
    n = pm.Uniform('n', -50000, 50000, value=0)
    
    x_pred = pm.Normal('x_pred', mu=x, tau=1/(x_error**-2))
    
    @pm.deterministic(plot=False)
    def linear_one(x=x_pred, m=m, n=n):
        return n + x * m
    
    #The likelihood
    y = pm.Normal('f', mu=linear_one, tau=1.0/(y_error**2), value=y, observed=True)
    
    return locals()

def bayes_model_pymc3(x, x_error, y, y_error):
    
    with pm3.Model() as model3:
    
        m = pm3.Uniform('m', 0, 3, testval=1)
        n = pm3.Uniform('n', -50000, 50000, testval=0)
            
        x_pred = pm3.Normal('x_pred', mu=x, tau=1.0/(x_error**-2), shape=size(x)).random()
        
        linear_model = pm3.Deterministic('linear_model', m * x_pred + n)
        
        f = pm3.Normal('f', mu=linear_model, tau=1.0/y_error, observed=y)
    
        start=pm3.find_MAP()
        step=pm3.NUTS()
        tracex=pm3.sample(50000,start=start)
    
    return tracex

#Generate dazer object

dz = Dazer()

#Define plot frame and colors
size_dict = {'axes.labelsize':20, 'legend.fontsize':17, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)

#Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
MC_iterations   = 5000

#Declare data for the analisis
AbundancesFileExtension = '_' + catalogue_dict['Datatype'] + '_linesLog_reduc.txt'
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)
idcs = (~catalogue_df.TeOIII_emis2nd.isnull() & ~catalogue_df.TeSIII_emis2nd.isnull() & catalogue_df.quick_index.notnull())

x_data = catalogue_df.loc[idcs].TeOIII_emis2nd.values
y_data = catalogue_df.loc[idcs].TeSIII_emis2nd.values

m_TNII          = 1.0 / ufloat(1.312, 0.075) 
n_TNII          = ufloat(0.313,0.058) / ufloat(1.312, 0.075)       
m_TNII_matrix   = random.normal(m_TNII.nominal_value, m_TNII.std_dev, size = len(x_data))
n_TNII_matrix   = random.normal(n_TNII.nominal_value, n_TNII.std_dev, size = len(x_data))

z_axis = y_data
y_axis = m_TNII_matrix * y_data + n_TNII_matrix
x_axis = x_data

print 'New relation', m_TNII, n_TNII

#PYMC2
# MDL = pm.MCMC(bayes_model(unumpy.nominal_values(x_data), unumpy.std_devs(x_data), unumpy.nominal_values(y_data), unumpy.std_devs(y_data)))
# MDL.use_step_method(pm.AdaptiveMetropolis, MDL.x_pred) # use AdaptiveMetropolis to "learn" how to step
# MDL.sample(500000, 100000, 10) 
# print MDL.stats()['n']['mean'], MDL.stats()['n']['quantiles'][2.5], MDL.stats()['n']['quantiles'][97.5]
# pm.Matplot.plot(MDL)
# dz.display_fig()

#PYMC3
# MDL = bayes_model_pymc3(unumpy.nominal_values(x_data), unumpy.std_devs(x_data), unumpy.nominal_values(y_data), unumpy.std_devs(y_data))
# print pm3.summary(MDL)
# print 'm, pymc3', MDL.get_values('m').mean()
# print 'n, pym3', MDL.get_values('n').mean()
# y_fit = MDL.get_values('linear_model').mean()
# x_fit = MDL.get_values('x_pred').mean()
# dz.data_plot(x_fit, y_fit, 'Bayesian fit3', linestyle = '--')


#Generate matrix with random values
x_matrix        = empty((len(x_data), MC_iterations))
y_matrix        = empty((len(x_data), MC_iterations))
m_vector, m_vector = empty(MC_iterations), empty(MC_iterations)
for i in range(len(x_data)): 
    x_matrix[i,:]  = random.normal(x_data[i].nominal_value, x_data[i].std_dev, size = MC_iterations)
    y_matrix[i,:]  = random.normal(y_data[i].nominal_value, y_data[i].std_dev, size = MC_iterations)

#LMFIT
initial_values  = 0
lmfit_matrix    = empty([2, MC_iterations])
lmod            = Model(linear_model)
for i in range(MC_iterations):
    x_i = x_matrix[:,i]
    y_i = y_matrix[:,i]
    result = lmod.fit(y_i, x=x_i, m=1, n=0)
    lmfit_matrix[:,i] = array(result.params.valuesdict().values())

print 'Shape1', x_matrix[:,0].shape
print 'Shape2', x_matrix[0,:].shape

    
m_lmfit, n_lmfit =  lmfit_matrix.mean(1)
print m_lmfit, n_lmfit 
print mean(lmfit_matrix[0,:]), mean(lmfit_matrix[1,:])

#Plot data points
dz.data_plot(unumpy.nominal_values(x_data), unumpy.nominal_values(y_data), 'HII galaxies', markerstyle='o',  x_error=unumpy.std_devs(x_data),  y_error=unumpy.std_devs(y_data))

#Regression with bces
reg_code        = 0
x_regression    = linspace(0.8 * np_min(unumpy.nominal_values(x_data)), 1.20 * np_max(unumpy.nominal_values(x_data)), 10)
regr_dict       = bces_regression(unumpy.nominal_values(x_data), unumpy.nominal_values(y_data), unumpy.std_devs(x_data), unumpy.std_devs(y_data))
y_fit           = regr_dict['m'][reg_code] * x_regression + regr_dict['n'][reg_code]
dz.data_plot(x_regression, y_fit, 'BCES linear fit from data', linestyle = '-')
dz.data_plot(x_regression, m_lmfit*x_regression+n_lmfit, 'lmfit Montecarlo', linestyle = ':')

print regr_dict['m'][reg_code]
print regr_dict['n'][reg_code]

Title       = r'Sulfur versus Oxygen temperature comparison'
y_Title     = r'$T_{e}[SIII]\,(K)$'
x_Title     = r'$T_{e}[OIII]\,(K)$'
dz.FigWording(x_Title, y_Title, Title)
dz.display_fig()
#dz.savefig('/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/Images/temperatures_comparison')



# #Run MCMC with MAP
# MAP_Model               = pm.MAP(bayes_model(unumpy.nominal_values(x_data), unumpy.std_devs(x_data), unumpy.nominal_values(y_data), unumpy.std_devs(y_data)))
# MAP_Model.fit(method    = 'fmin_powell') 
# MAP_Model.revert_to_max()
# 
# print MAP_Model.variables
# 
# MDL = pm.MCMC(MAP_Model.variables)
# MDL.sample(iter=20000, burn=1000, thin=2) #Optimun test
