from dazer_methods                      import Dazer
from collections                        import OrderedDict
from numpy                              import empty, random, median, percentile, array, linspace, zeros
from scipy                              import stats
from uncertainties                      import ufloat
from uncertainties.unumpy               import nominal_values, std_devs
from lib.Math_Libraries.sigfig          import round_sig
from lib.Math_Libraries.bces_script     import bces, bcesboot
from lmfit import Model
from scipy.optimize import curve_fit
from kapteyn import kmpfit

def linear_model(x, m, n):
    return m*x+n

def residuals_lin(p, c):
    x, y = c
    m, n = p
    return (y - linear_model(x, m, n))

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

#Define plot frame and colors
size_dict = {'axes.labelsize':20, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':18, 'ytick.labelsize':18}
dz.FigConf(plotSize = size_dict)

#Load catalogue dataframe
catalogue_dict  = dz.import_catalogue()
catalogue_df    = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)

#Regressions properties
MC_iterations   = 500
WMAP_coordinates = array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])

#Generate the indeces
Regresions_dict = OrderedDict()
Regresions_dict['Regressions']      = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
Regresions_dict['metal x axis']     = ['OI_HI_emis2nd', 'NI_HI_emis2nd', 'SI_HI_emis2nd']
Regresions_dict['helium y axis']    = ['Ymass_O_emis2nd',  'Ymass_O_emis2nd', 'Ymass_S_emis2nd']
Regresions_dict['element']          = ['O', 'N', 'S']
Regresions_dict['factor']           = [1e5, 1e6, 1e6]
Regresions_dict['title']            = ['Helium mass fraction versus oxygen abundance', 'Helium mass fraction versus nitrogen abundance', 'Helium mass fraction versus sulfur abundance']

Regresions_dict['x label']          = [r'$\frac{{O}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][0])),  r'$\frac{{N}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][1])), r'$\frac{{S}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][2]))]
Regresions_dict['y label']          = [r'$Y_{\frac{O}{H}}$',  r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{S}{H}}$']
Regresions_dict['Colors']           = [dz.colorVector['green'], dz.colorVector['dark blue'], dz.colorVector['orangish']]

#Additional regression label
regr_dict       = {}
regr_dict['0']  = ['y|x']
regr_dict['3']  = ['Orthogonal']
lmod            = Model(linear_model)

p0 = array([0.005, 0.25])

#Get the objects which contain both abundances
for i in range(len(Regresions_dict['Regressions'])):
    
    print '--Doing regression',  Regresions_dict['element'][i]
    
    #Get right regression values properties
    element     = Regresions_dict['element'][i]
    regression  = Regresions_dict['Regressions'][i]
    metal_x     = Regresions_dict['metal x axis'][i]
    helium_y    = Regresions_dict['helium y axis'][i]
    reject_idx  = catalogue_df[element + '_valid'].isnull()
    reject_objs = catalogue_df[element + '_valid'][~reject_idx].index.values
    
    #Get objects which meet regression conditions
    idces_metal = (catalogue_df[metal_x].notnull()) & (catalogue_df[helium_y].notnull()) & (~catalogue_df.index.isin(reject_objs))
    objects     = catalogue_df.loc[idces_metal].index.values
    x           = catalogue_df.loc[idces_metal, metal_x].values * Regresions_dict['factor'][i]
    y           = catalogue_df.loc[idces_metal, helium_y].values
    quick_ref   = catalogue_df.loc[idces_metal].quick_index
    
    #Get the data for the excees N/O objects
    NO_excess_idcs = ((catalogue_df[element + '_valid'] == 'NO_excess') | (catalogue_df[element + '_valid'] == 'ignored')) & (catalogue_df[metal_x].notnull()) & (catalogue_df[helium_y].notnull())
    x_NO           = catalogue_df.loc[NO_excess_idcs, metal_x].values * Regresions_dict['factor'][i]
    y_NO           = catalogue_df.loc[NO_excess_idcs, helium_y].values
    quickref_NO    = catalogue_df.loc[NO_excess_idcs].quick_index
   
    print '--- Using these objs {}:'.format(len(objects)), ', '.join(list(objects))
    print '--- Estos no me gustan {}:'.format(len(reject_objs)), ', '.join(list(reject_objs))
    
    #Create containers
    metal_matrix    = empty((len(objects), MC_iterations))
    Y_matrix        = empty((len(objects), MC_iterations))
    m_vector, n_vector = empty(MC_iterations), empty(MC_iterations)
    m_vectorlmfit, n_vectorlmfit = empty(MC_iterations), empty(MC_iterations)
    lmfit_matrix    = empty([2, MC_iterations])
    lmfit_error     = empty([2, MC_iterations])
    curvefit_matrix = empty([2, MC_iterations])
    kapteyn_matrix  = empty([2, MC_iterations])
    
    #Generate the distributions
    for j in range(len(objects)): 
        metal_matrix[j,:]   = random.normal(x[j].nominal_value, x[j].std_dev, size = MC_iterations)
        Y_matrix[j,:]       = random.normal(y[j].nominal_value, y[j].std_dev, size = MC_iterations)
    
#     x_i = metal_matrix[:,0]
#     y_i = Y_matrix[:,0]    
#     fitobj = kmpfit.Fitter(residuals=residuals_lin, data= (x_i, y_i))
    
    #Run the fits
    for k in range(MC_iterations):
        x_i = metal_matrix[:,k]
        y_i = Y_matrix[:,k]
        
        m, n, r_value, p_value, std_err = stats.linregress(x_i, y_i)
        m_vector[k], n_vector[k] = m, n
        
        #Lmfit
        result_lmfit = lmod.fit(y_i, x=x_i, m=0.005, n=0.24709)
        lmfit_matrix[:,k] = array(result_lmfit.params.valuesdict().values())
        lmfit_error[:,k] = array([result_lmfit.params['m'].stderr, result_lmfit.params['n'].stderr])
        
        #Curvefit
        best_vals, covar = curve_fit(linear_model, x_i, y_i, p0=p0)
        curvefit_matrix[:,k] = best_vals
        
        #kapteyn
        fitobj = kmpfit.Fitter(residuals=residuals_lin, data= (x_i, y_i))
        fitobj.fit(params0  = p0)
        kapteyn_matrix[:,k] = fitobj.params
        
    #Get fit mean values
    n_Median, n_16th, n_84th            = median(n_vector), percentile(n_vector,16), percentile(n_vector,84)
    m_Median, m_16th, m_84th            = median(m_vector), percentile(m_vector,16), percentile(m_vector,84)
    m_Median_lm, m_16th_lm, m_84th_lm   = median(lmfit_matrix[0,:]), percentile(lmfit_matrix[0,:],16), percentile(lmfit_matrix[0,:],84)
    n_Median_lm, n_16th_lm, n_84th_lm   = median(lmfit_matrix[1,:]), percentile(lmfit_matrix[1,:],16), percentile(lmfit_matrix[1,:],84)
    m_Median_lm_error, n_Median_lm_error = median(lmfit_error[0,:]), median(lmfit_error[1,:])
    m_Median_cf, m_16th_cf, m_84th_cf   = median(curvefit_matrix[0,:]), percentile(curvefit_matrix[0,:],16), percentile(curvefit_matrix[0,:],84)
    n_Median_cf, n_16th_cf, n_84th_cf   = median(curvefit_matrix[1,:]), percentile(curvefit_matrix[1,:],16), percentile(curvefit_matrix[1,:],84)    
    m_Median_kp, m_16th_kp, m_84th_kp   = median(kapteyn_matrix[0,:]), percentile(kapteyn_matrix[0,:],16), percentile(kapteyn_matrix[0,:],84)
    n_Median_kp, n_16th_kp, n_84th_kp   = median(kapteyn_matrix[1,:]), percentile(kapteyn_matrix[1,:],16), percentile(kapteyn_matrix[1,:],84)   

    #Bootstrap BCES
    m, n, m_err, n_err, cov = bcesboot(nominal_values(x), std_devs(x), nominal_values(y), std_devs(y), cerr=zeros(len(x)), nsim=10000)
    
    print element
    print 'New methods'
    print m[0], m[1], m[2], m[3]
    print m_err[0], m_err[1], m_err[2], m_err[3]
    print n[0], n[1], n[2], n[3]
    print n_err[0], n_err[1], n_err[2], n_err[3]

    print 'Classical'
    print n_Median, round_sig(n_Median-n_16th,2, scien_notation=False), round_sig(n_84th-n_Median,2, scien_notation=False)
    
    print 'Lmfit'
    print n_Median_lm, n_Median_lm_error
    
    print 'curvefit'
    print n_Median_cf, n_84th_cf - n_Median_cf ,n_Median_cf - n_16th_cf

    print 'kapteyn'
    print n_Median_kp, n_84th_kp - n_Median_kp ,n_Median_kp - n_16th_kp
  
    #Linear data
    x_regression_range  = linspace(0.0, max(nominal_values(x)) * 1.10, 20)
    y_regression_range  = m_Median * x_regression_range + n_Median
    label_regr = 'Linear fit'  
    #label_regr          = 'SCIPY bootstrap: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
    
    #Plotting the data, 
    label_regression = r'WMAP prediction: $Y = 0.24709\pm0.00025$'
    dz.data_plot(nominal_values(x), nominal_values(y), color = Regresions_dict['Colors'][i], label='HII galaxies included in regression', markerstyle='o', x_error=std_devs(x), y_error=std_devs(y))
    dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color = dz.colorVector['pink'], label='WMAP prediction', markerstyle='o', x_error=WMAP_coordinates[0].std_dev, y_error=WMAP_coordinates[1].std_dev)    
    dz.data_plot(x_regression_range, y_regression_range, label = label_regr, color = Regresions_dict['Colors'][i], linestyle = '--')
    dz.plot_text(nominal_values(x), nominal_values(y), quick_ref)
    
    #Plotting NO objects
    dz.data_plot(nominal_values(x_NO), nominal_values(y_NO), color = Regresions_dict['Colors'][i], label='HII galaxies excluded in regression', markerstyle='x', x_error=std_devs(x_NO), y_error=std_devs(y_NO))
    dz.plot_text(nominal_values(x_NO), nominal_values(y_NO), quickref_NO)

    #Lmfit regression
    label       =  r'{title}: $Y_{{P}} = {n}\pm_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = 'Lmfit', n = round_sig(n_Median_lm,4, scien_notation=False), lowerlimit = round_sig(n_Median_lm-n_16th_lm,2, scien_notation=False), upperlimit = round_sig(n_84th_lm-n_Median_lm,2, scien_notation=False))
    label       =  r'{title}: $Y_{{P}} = {n}\pm_{lmfit_err}$'.format(title = 'Lmfit', n = round_sig(n_Median_lm,4, scien_notation=False), lmfit_err = round_sig(n_Median_lm_error,2, scien_notation=False))
    y_regression_range_lmfit = m_Median_lm * x_regression_range + n_Median_lm
    dz.data_plot(x_regression_range, y_regression_range_lmfit, label = label, linestyle = '--')
    
#     for z in [0,3]:
#         n_z, n_err_z  = n[z], n_err[z]
#         m_z           = m[z]
#         label       = r'Method {title}: $Y_{{P}} = {n}\pm{n_err}$'.format(title = regr_dict[str(z)], n = round_sig(n_z, 4, scien_notation=False), n_err = round_sig(n_err_z, 2, scien_notation=False))
#         regre_z     = m_z * x_regression_range + n_z
#         dz.data_plot(x_regression_range, regre_z, label = label, linestyle = '--')
        
    plotTitle = r'{title}: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
    dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], plotTitle, loc='best')

    output_pickle = '{objFolder}{element}_regression_2nd'.format(objFolder='/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/Images/', element = element)
    dz.save_manager(output_pickle, save_pickle = False)


