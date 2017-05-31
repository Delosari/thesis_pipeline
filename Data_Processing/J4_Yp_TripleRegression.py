from dazer_methods                      import Dazer
from collections                        import OrderedDict
from numpy                              import empty, random, median, percentile, array, linspace, zeros
from scipy                              import stats
from uncertainties                      import ufloat
from uncertainties.unumpy               import nominal_values, std_devs
from scipy.optimize                     import curve_fit
from lmfit                              import Model, Parameters, minimize as lmfit_minimize, fit_report, Minimizer
from kapteyn                            import kmpfit
from lib.CodeTools.sigfig               import round_sig
from lib.Math_Libraries.bces_script     import bces, bcesboot
from pandas                             import DataFrame
import statsmodels.formula.api as smf

def linear_model2(x, mA, mB, n):
    return mA*x[0] + mB*x[1] + n

def linear_model3(x, mA, mB, mC, n):
    return mA*x[0] + mB*x[1] + mC*x[2] + n

def residuals_lin2(p, c):
    x, y = c
    mA, mB, n = p
    return (y - linear_model2(x, mA, mB, n))

def residuals_lin3(p, c):
    x, y = c
    mA, mB, mC, n = p
    return (y - linear_model3(x, mA, mB, mC, n))

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
MC_iterations   = 5000
WMAP_coordinates = array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])

#Regression properties
Regresions_list = [['O', 'N'], ['O', 'S'], ['N', 'S'], ['O', 'N', 'S']]
p0      = array([0.005, 0.005, 0.25])

method_dict = {}
method_dict['lm2'] = linear_model2
method_dict['lm3'] = linear_model3
method_dict['rlm2'] = residuals_lin2
method_dict['rlm3'] = residuals_lin3

#Get the objects which contain both abundances
for i in range(len(Regresions_list)):
    
    print '\n---Regression', Regresions_list[i]
    Regression_group    = Regresions_list[i]
    dimensions_num      = len(Regression_group)
    ext_method          = str(dimensions_num) 
    p0                  = array([0.005] * dimensions_num + [0.25])
    
    #Define lmfit model
    params = Parameters()
    for i in range(dimensions_num):
        params.add('m' + str(i), value = 0.005)
    params.add('n', value = 0.25)

    #Loop through the elements valid objects
    idcs = (catalogue_df['Ymass_O_emis2nd'].notnull())
    for element in Regression_group:
        abunCode    = '{}I_HI_emis2nd'.format(element)
        valCode     = '{}_valid'.format(element)
        idcs        = idcs & (catalogue_df[abunCode].notnull()) & (catalogue_df[valCode].isnull())
    
    #Get data
    data_dict   = OrderedDict()
    objects     = catalogue_df.loc[idcs].index.values
    data_dict['Y'] = catalogue_df.loc[idcs, 'Ymass_O_emis2nd'].values
    for element in Regression_group:
        abunCode = '{}I_HI_emis2nd'.format(element)
        data_dict[element] = catalogue_df.loc[idcs, abunCode].values
    
    #Generate containers for the data     
    metal_matrix    = empty((dimensions_num, len(objects), MC_iterations))
    Y_matrix        = empty((len(objects), MC_iterations))
    lmfit_matrix    = empty([dimensions_num + 1, MC_iterations])
    lmfit_error     = empty([dimensions_num + 1, MC_iterations])
    curvefit_matrix = empty([dimensions_num + 1, MC_iterations])
    kapteyn_matrix  = empty([dimensions_num + 1, MC_iterations])
    stats_matrix    = empty([dimensions_num + 1, MC_iterations])
    
    #Generate the distributions
    for j in range(len(objects)):
        Y_matrix[j,:] = random.normal(data_dict['Y'][j].nominal_value, data_dict['Y'][j].std_dev, size = MC_iterations)
        for i in range(dimensions_num):
            element = Regression_group[i] 
            metal_matrix[i,j,:] = random.normal(data_dict[element][j].nominal_value, data_dict[element][j].std_dev, size = MC_iterations)
            
    #Run the fits
    for k in range(MC_iterations):
        
        #Dictionary to store the current iteration
        x_ith = metal_matrix[:,:,k]
        y_ith = Y_matrix[:,k]
        
        #Lmfit
        #result_lmfit        = lm_2.fit(y_ith, x_ith, p0[0], p0[1], p0[2])
        #lmfit_matrix[:,k]   = array(result_lmfit.params.valuesdict().values())
        #lmfit_error[:,k]    = array([result_lmfit.params['mA'].stderr, result_lmfit.params['mB'].stderr, result_lmfit.params['n'].stderr])
        #fit_Output      = lmfit_minimize(residual_gaussMix, fitting_parameters, args=(x, y_new, zero_lev, err_continuum, idcs_components))
        #output_params   = fit_Output.params
        
        #Curvefit
        best_vals, covar = curve_fit(method_dict['lm' + ext_method], x_ith, y_ith, p0=p0)
        curvefit_matrix[:,k] = best_vals
        
        #kapteyn
        fitobj = kmpfit.Fitter(residuals=method_dict['rlm' + ext_method], data= (x_ith, y_ith))
        fitobj.fit(params0  = p0)
        kapteyn_matrix[:,k] = fitobj.params
        
#         #Stats dataframe
#         grid_j  = DataFrame()
#         grid_j['Y'] = y_ith
#         formula_label = 'Y ~ ' + ' + '.join(Regression_group)
#         print formula_label
#         for i in range(dimensions_num):
#             grid_j[Regression_group[i]] = x_ith[i]
#         lm = smf.ols(formula=formula_label, data=grid_j).fit()
#         for i in range(dimensions_num):
#             stats_matrix[i,k] = lm.params[Regression_group[i]]
        
    #Get fit mean values
    idx_n = dimensions_num
    n_median_lmerror = median(lmfit_matrix[idx_n,:])
    #n_Median_lm, n_16th_lm, n_84th_lm   = median(lmfit_matrix[idx_n,:]),    percentile(lmfit_matrix[idx_n,:],16),       percentile(lmfit_matrix[idx_n,:],84)
    n_Median_cf, n_16th_cf, n_84th_cf   = median(curvefit_matrix[idx_n,:]), percentile(curvefit_matrix[idx_n,:],16),    percentile(curvefit_matrix[idx_n,:],84)    
    n_Median_kp, n_16th_kp, n_84th_kp   = median(kapteyn_matrix[idx_n,:]),  percentile(kapteyn_matrix[idx_n,:],16),     percentile(kapteyn_matrix[idx_n,:],84)   
    #n_Median_st, n_16th_st, n_84th_st   = median(stats_matrix[idx_n,:]),  percentile(stats_matrix[idx_n,:],16),     percentile(stats_matrix[idx_n,:],84)   

    
    #Display results      
    #print 'Lmfit'
    #print n_Median_lm, n_84th_lm - n_Median_lm, n_Median_lm - n_16th_lm
    #print n_median_lmerror
    
    print 'curvefit'
    print n_Median_cf, n_84th_cf - n_Median_cf ,n_Median_cf - n_16th_cf

    print 'kapteyn'
    print n_Median_kp, n_84th_kp - n_Median_kp ,n_Median_kp - n_16th_kp

    print 'stats'
#     print n_Median_st, n_84th_st - n_Median_st ,n_Median_st - n_16th_st

 
#     #Linear data
#     x_regression_range  = linspace(0.0, max(nominal_values(x)) * 1.10, 20)
#     y_regression_range  = m_Median * x_regression_range + n_Median
#     label_regr = 'Linear fit'  
#     #label_regr          = 'SCIPY bootstrap: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
#     
#     #Plotting the data, 
#     label_regression = r'WMAP prediction: $Y = 0.24709\pm0.00025$'
#     dz.data_plot(nominal_values(x), nominal_values(y), color = Regresions_dict['Colors'][i], label='HII galaxies included in regression', markerstyle='o', x_error=std_devs(x), y_error=std_devs(y))
#     dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color = dz.colorVector['pink'], label='WMAP prediction', markerstyle='o', x_error=WMAP_coordinates[0].std_dev, y_error=WMAP_coordinates[1].std_dev)    
#     dz.data_plot(x_regression_range, y_regression_range, label = label_regr, color = Regresions_dict['Colors'][i], linestyle = '--')
#     dz.plot_text(nominal_values(x), nominal_values(y), quick_ref)
#     
#     #Plotting NO objects
#     dz.data_plot(nominal_values(x_NO), nominal_values(y_NO), color = Regresions_dict['Colors'][i], label='HII galaxies excluded in regression', markerstyle='x', x_error=std_devs(x_NO), y_error=std_devs(y_NO))
#     dz.plot_text(nominal_values(x_NO), nominal_values(y_NO), quickref_NO)
# 
#     #Lmfit regression
#     label       =  r'{title}: $Y_{{P}} = {n}\pm_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = 'Lmfit', n = round_sig(n_Median_lm,4, scien_notation=False), lowerlimit = round_sig(n_Median_lm-n_16th_lm,2, scien_notation=False), upperlimit = round_sig(n_84th_lm-n_Median_lm,2, scien_notation=False))
#     label       =  r'{title}: $Y_{{P}} = {n}\pm_{lmfit_err}$'.format(title = 'Lmfit', n = round_sig(n_Median_lm,4, scien_notation=False), lmfit_err = round_sig(n_Median_lm_error,2, scien_notation=False))
#     y_regression_range_lmfit = m_Median_lm * x_regression_range + n_Median_lm
#     dz.data_plot(x_regression_range, y_regression_range_lmfit, label = label, linestyle = '--')
#     
# #     for z in [0,3]:
# #         n_z, n_err_z  = n[z], n_err[z]
# #         m_z           = m[z]
# #         label       = r'Method {title}: $Y_{{P}} = {n}\pm{n_err}$'.format(title = regr_dict[str(z)], n = round_sig(n_z, 4, scien_notation=False), n_err = round_sig(n_err_z, 2, scien_notation=False))
# #         regre_z     = m_z * x_regression_range + n_z
# #         dz.data_plot(x_regression_range, regre_z, label = label, linestyle = '--')
#         
#     plotTitle = r'{title}: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
#     dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], plotTitle, loc='best')
# 
#     output_pickle = '{objFolder}{element}_regression_2nd'.format(objFolder='/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/Images/', element = element)
#     dz.save_manager(output_pickle, save_pickle = False)


