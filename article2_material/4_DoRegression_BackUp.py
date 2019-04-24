from dazer_methods import Dazer
from collections import OrderedDict
from numpy import empty, random, median, percentile, array, linspace, zeros, std
from scipy import stats
from uncertainties import ufloat
from uncertainties.unumpy import nominal_values, std_devs
from lib.CodeTools.sigfig import round_sig
from lib.Math_Libraries.bces_script import bces, bcesboot
import pandas as pd
from lmfit import Model, Parameters
from scipy.optimize import curve_fit
from kapteyn import kmpfit
import statsmodels.formula.api as smf


def linear_model(x, m, n):
    return m * x + n


def residuals_lin(p, c):
    x, y = c
    m, n = p
    return (y - linear_model(x, m, n))


def linear_model2(x, mA, mB, n):
    return mA * x[0] + mB * x[1] + n


def linear_model3(x, mA, mB, mC, n):
    return mA * x[0] + mB * x[1] + mC * x[2] + n


def residuals_lin2(p, c):
    x, y = c
    mA, mB, n = p
    return (y - linear_model2(x, mA, mB, n))


def residuals_lin3(p, c):
    x, y = c
    mA, mB, mC, n = p
    return (y - linear_model3(x, mA, mB, mC, n))
    return mA * x[0] + mB * x[1] + mC * x[2] + n


def latex_float(f):
    float_str = "{0:.2g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"10^{{{}}}".format(int(exponent))
    else:
        return float_str


# Create class object
dz = Dazer()
script_code = dz.get_script_code()

# Define plot frame and colors
size_dict = {'figure.figsize': (18, 8), 'axes.labelsize': 38, 'legend.fontsize': 28, 'font.family': 'Times New Roman',
             'mathtext.default': 'regular', 'xtick.labelsize': 34, 'ytick.labelsize': 34}
dz.FigConf(plotSize=size_dict)

# Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
bayes_catalogue_df_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
bayes_catalogue_df = pd.read_csv(bayes_catalogue_df_address, delim_whitespace=True, header=0, index_col=0)
dz.quick_indexing(catalogue_df)

# Regressions properties
MC_iterations = 5000
WMAP_coordinates = array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])

# Generate the indeces
Regresions_dict = OrderedDict()
Regresions_dict['Regressions'] = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
Regresions_dict['metal x axis'] = ['OI_HI', 'NI_HI', 'SI_HI']
Regresions_dict['helium y axis'] = ['Ymass_O', 'Ymass_O', 'Ymass_S']
Regresions_dict['element'] = ['O', 'N', 'S']
Regresions_dict['factor'] = [1e5, 1e6, 1e6]
Regresions_dict['title'] = ['Helium mass fraction versus oxygen abundance',
                            'Helium mass fraction versus nitrogen abundance',
                            'Helium mass fraction versus sulfur abundance']
Regresions_dict['x label'] = [r'$\frac{{O}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][0])),
                              r'$\frac{{N}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][1])),
                              r'$\frac{{S}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][2]))]
Regresions_dict['y label'] = [r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{S}{H}}$']
Regresions_dict['Colors'] = [dz.colorVector['green'], dz.colorVector['dark blue'], dz.colorVector['orangish']]
Regresions_list = [['O', 'N'], ['O', 'S'], ['N', 'S'], ['O', 'N', 'S']]

# Additional regression label
regr_dict = {'0': ['y|x'], '3': ['Orthogonal']}
lmod = Model(linear_model)

# Dict with regression methods
method_dict = {'lm2': linear_model2, 'lm3': linear_model3, 'rlm2': residuals_lin2, 'rlm3': residuals_lin3}

p0 = array([0.005, 0.25])
p0_c = array([0.005, 0.005, 0.25])

# Folder to save the plots
output_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/'

# Dictionary to store the the data from the table (we are going to use kapteyn)
regr_dict = OrderedDict()
regr_dict['$Y_{P,\,O}$'] = [0, 0, 0]
regr_dict['$Y_{P,\,N}$'] = [0, 0, 0]
regr_dict['$Y_{P,\,S}$'] = [0, 0, 0]
regr_dict['$Y_{P,\,O-N}$'] = [0, 0, 0]
regr_dict['$Y_{P,\,O-S}$'] = [0, 0, 0]
regr_dict['$Y_{P,\,N-S}$'] = [0, 0, 0]
regr_dict['$Y_{P,\,O-N-S}$'] = [0, 0, 0]

regr_dict['$Y_{P,\,O-N-S}$'] = [0, 0, 0]

exter_regr_dict = OrderedDict()
exter_regr_dict['$Y_{P,\,O}^{1}$'] = [0.2446, 0.0029, '5']  # Peimbert
exter_regr_dict['$Y_{P,\,O}^{2}$'] = [0.2449, 0.0040, '15']  # Aver
exter_regr_dict['$Y_{P,\,O}^{3}$'] = [0.2551, 0.0022, '28']  # Izotov
exter_regr_dict['$Y_{P,\,Planck BBN}^{4}$'] = [0.24467, 0.00020, '-']

arguments_coords = {'xycoords': 'data', 'textcoords': 'data', 'arrowprops': dict(arrowstyle='->'),
                    'horizontalalignment': 'right', 'verticalalignment': 'top'}

# catalogueDf.loc['MRK36_A2', 'Ymass_S'] = 0.243
# catalogueDf.loc['MRK36_A2', 'Ymass_O'] = 0.243
# catalogueDf.loc['MAR1318', 'Ymass_S'] = 0.275
# catalogueDf.loc['MAR1318', 'Ymass_O'] = 0.274
# catalogueDf.loc['MAR1324', 'Ymass_S'] = 0.237
# catalogueDf.loc['MAR1324', 'Ymass_O'] = 0.236
# catalogueDf.loc['52703-612', 'Ymass_S'] = 0.232
# catalogueDf.loc['52703-612', 'Ymass_O'] = 0.231
# catalogueDf.loc['MAR868', 'Ymass_S'] = 0.234
# catalogueDf.loc['14', 'Ymass_O'] = 0.251
# catalogueDf.loc['14', 'Ymass_S'] = 0.251

(['14', 'MAR868', '52703-612', 'MAR1324', 'MAR1318', 'MRK36_A2'])
MRK627
FTDTR2
FTDTR8
MRK689
MRK36A2


# Perform linear regressions with plots
for i in range(len(Regresions_dict['Regressions'])):

    print 'Doing regression', Regresions_dict['Regressions'][i]

    # Get right regression values properties
    element = Regresions_dict['element'][i]
    regression = Regresions_dict['Regressions'][i]
    metal_x = Regresions_dict['metal x axis'][i]
    helium_y = Regresions_dict['helium y axis'][i]
    reject_idx = catalogue_df[element + '_valid'].isnull()
    reject_objs = catalogue_df[element + '_valid'][~reject_idx].index.values
    #print '--reject_objs', reject_objs

    # Get objects which meet regression conditions
    idces_metal = (bayes_catalogue_df[metal_x].notnull()) & (bayes_catalogue_df[helium_y].notnull()) & (~bayes_catalogue_df.index.isin(reject_objs)) & (~bayes_catalogue_df.index.isin(['14', 'MAR868', '52703-612', 'MAR1324', 'MAR1318', 'MRK36_A2']))
    objects = bayes_catalogue_df.loc[idces_metal].index.values
    x = bayes_catalogue_df.loc[idces_metal, metal_x].values * Regresions_dict['factor'][i]
    x_er = bayes_catalogue_df.loc[idces_metal, metal_x + '_err'].values * Regresions_dict['factor'][i]
    y = bayes_catalogue_df.loc[idces_metal, helium_y].values
    y_er = bayes_catalogue_df.loc[idces_metal, helium_y + '_err'].values
    quick_ref = bayes_catalogue_df.loc[idces_metal].quick_index
    print bayes_catalogue_df.loc[idces_metal].index

    for idx in range(len(x)):
        print objects[idx], x[idx], x_er[idx], y[idx], y_er[idx]

    print '--Doing regression', Regresions_dict['element'][i]
    print '--- Using these objs {}:'.format(len(objects)), ', '.join(list(objects))
    print '--- Estos no me gustan {}:'.format(len(reject_objs)), ', '.join(list(reject_objs))

    # Create containers
    metal_matrix = empty((len(objects), MC_iterations))
    Y_matrix = empty((len(objects), MC_iterations))
    m_vector, n_vector = empty(MC_iterations), empty(MC_iterations)
    m_vectorlmfit = empty(MC_iterations)
    n_vectorlmfit = empty(MC_iterations)
    lmfit_matrix = empty([2, MC_iterations])
    lmfit_error = empty([2, MC_iterations])
    curvefit_matrix = empty([2, MC_iterations])
    kapteyn_matrix = empty([2, MC_iterations])

    # Generate the distributions
    for j in range(len(objects)):
        metal_matrix[j, :] = random.normal(x[j], x_er[j], size=MC_iterations)
        Y_matrix[j, :] = random.normal(y[j], y_er[j], size=MC_iterations)

    # Run the fits
    for k in range(MC_iterations):
        x_i = metal_matrix[:, k]
        y_i = Y_matrix[:, k]

        m, n, r_value, p_value, std_err = stats.linregress(x_i, y_i)
        m_vector[k], n_vector[k] = m, n

        # Lmfit
        result_lmfit = lmod.fit(y_i, x=x_i, m=0.005, n=0.24709)
        lmfit_matrix[:, k] = array(result_lmfit.params.valuesdict().values())
        lmfit_error[:, k] = array([result_lmfit.params['m'].stderr, result_lmfit.params['n'].stderr])

        # Curvefit
        best_vals, covar = curve_fit(linear_model, x_i, y_i, p0=p0)
        curvefit_matrix[:, k] = best_vals

        # kapteyn
        fitobj = kmpfit.Fitter(residuals=residuals_lin, data=(x_i, y_i))
        fitobj.fit(params0=p0)
        kapteyn_matrix[:, k] = fitobj.params

    # Get fit mean values
    n_Median, n_16th, n_84th = median(n_vector), percentile(n_vector, 16), percentile(n_vector, 84)
    m_Median, m_16th, m_84th = median(m_vector), percentile(m_vector, 16), percentile(m_vector, 84)
    m_Median_lm, m_16th_lm, m_84th_lm = median(lmfit_matrix[0, :]), percentile(lmfit_matrix[0, :], 16), percentile(
        lmfit_matrix[0, :], 84)
    n_Median_lm, n_16th_lm, n_84th_lm = median(lmfit_matrix[1, :]), percentile(lmfit_matrix[1, :], 16), percentile(
        lmfit_matrix[1, :], 84)
    m_Median_lm_error, n_Median_lm_error = median(lmfit_error[0, :]), median(lmfit_error[1, :])
    m_Median_cf, m_16th_cf, m_84th_cf = median(curvefit_matrix[0, :]), percentile(curvefit_matrix[0, :],
                                                                                  16), percentile(curvefit_matrix[0, :],
                                                                                                  84)
    n_Median_cf, n_16th_cf, n_84th_cf = median(curvefit_matrix[1, :]), percentile(curvefit_matrix[1, :],
                                                                                  16), percentile(curvefit_matrix[1, :],
                                                                                                  84)
    m_Median_kp, m_16th_kp, m_84th_kp = median(kapteyn_matrix[0, :]), percentile(kapteyn_matrix[0, :], 16), percentile(
        kapteyn_matrix[0, :], 84)
    n_Median_kp, n_16th_kp, n_84th_kp = median(kapteyn_matrix[1, :]), percentile(kapteyn_matrix[1, :], 16), percentile(
        kapteyn_matrix[1, :], 84)

    # Bootstrap BCES
    m, n, m_err, n_err, cov = bcesboot(nominal_values(x), std_devs(x), nominal_values(y), std_devs(y), cerr=zeros(len(x)), nsim=10000)

    print 'BCES y dependent'
    print 'n', n[0], n_err[0]
    print 'm',m[0], m_err[0]
    print 'BCES Orthogonal'
    print 'n', n[3], n_err[3]
    print 'm',m[3], m_err[3]
    print 'Stats lingress'
    print 'n', n_Median, n_Median - n_16th, n_84th - n_Median
    print 'm', m_Median, m_Median-m_16th, m_84th-m_Median
    print 'Lmfit'
    print 'n', n_Median_lm, n_Median_lm - n_16th_lm, n_84th_lm - n_Median_lm
    print 'm', m_Median_lm, m_Median_lm-m_16th_lm, m_84th_lm-m_Median_lm
    print 'curvefit'
    print 'n', n_Median_cf, n_Median_cf - n_16th_cf, n_84th_cf - n_Median_cf
    print 'm', m_Median_cf, m_Median_cf-m_16th_cf, m_84th_cf-m_Median_cf
    print 'kapteyn'
    print 'n', n_Median_kp, n_Median_kp - n_16th_kp, n_84th_kp - n_Median_kp, '\n'
    print 'm', m_Median_kp, m_Median_kp-m_16th_kp, m_84th_kp-m_Median_kp

    # Saving the data
    entry_key = r'$Y_{{P,\,{elem}}}$'.format(elem=element)
    regr_dict[entry_key][0] = median(kapteyn_matrix[1, :])
    regr_dict[entry_key][1] = std(kapteyn_matrix[1, :])
    regr_dict[entry_key][2] = len(objects)

    # Linear data
    x_regression_range = linspace(0.0, max(nominal_values(x)) * 1.10, 20)
    y_regression_range = m_Median_cf * x_regression_range + n_Median_cf
    label_regr = 'Linear fit'
    # label_regr = 'SCIPY bootstrap: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))

    # Plotting the data,
    label_regression = r'Plank prediction: $Y = 0.24709\pm0.00025$'
    dz.data_plot(x, y, color=Regresions_dict['Colors'][i], label='HII galaxies included', markerstyle='o', x_error=x_er, y_error=y_er)
    dz.data_plot(x_regression_range, y_regression_range, label=label_regr, color=Regresions_dict['Colors'][i], linestyle='--')
    dz.plot_text(nominal_values(x), nominal_values(y), quick_ref)

    # Plot WMAP prediction
    dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color=dz.colorVector['pink'],
                 label='Planck prediction', markerstyle='o', x_error=WMAP_coordinates[0].std_dev,
                 y_error=WMAP_coordinates[1].std_dev)

    # plotTitle = r'{title}: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
    dz.Axis.set_ylim(0.1, 0.4)
    dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], '', loc='lower center', ncols_leg=2)

    output_pickle = '{objFolder}{element}_BayesDataRegression'.format(objFolder=output_folder, element=element)
    dz.save_manager(output_pickle, save_pickle=False)

# # # Combined regressions
# # for i in range(len(Regresions_list)):
# #
# #     regr_group = Regresions_list[i]
# #     dim_group = len(regr_group)
# #     ext_method = str(dim_group)
# #     p0 = array([0.005] * dim_group + [0.25])
# #
# #     # Define lmfit model
# #     params = Parameters()
# #     for idx in range(dim_group):
# #         params.add('m' + str(idx), value=0.005)
# #     params.add('n', value=0.25)
# #
# #     # Loop through the elements valid objects
# #     idcs = (catalogue_df['Ymass_O'].notnull())
# #     for element in regr_group:
# #         abunCode = '{}I_HI'.format(element)
# #         valCode = '{}_valid'.format(element)
# #         idcs = idcs & (bayes_catalogue_df[abunCode].notnull()) & (bayes_catalogue_df[valCode].isnull()) & (~bayes_catalogue_df.index.isin(['14', 'MAR868', '52703-612', 'MAR1324', 'MAR1318', 'MRK36_A2']))
# #
# #     # Get data
# #     data_dict = OrderedDict()
# #     objects = bayes_catalogue_df.loc[idcs].index.values
# #     data_dict['Y'] = bayes_catalogue_df.loc[idcs, 'Ymass_O'].values
# #     for element in regr_group:
# #         abunCode = '{}I_HI'.format(element)
# #         data_dict[element] = bayes_catalogue_df.loc[idcs, abunCode].values
# #
# #     # Generate containers for the data
# #     metal_matrix = empty((dim_group, len(objects), MC_iterations))
# #     Y_matrix = empty((len(objects), MC_iterations))
# #     lmfit_matrix = empty([dim_group + 1, MC_iterations])
# #     lmfit_error = empty([dim_group + 1, MC_iterations])
# #     curvefit_matrix = empty([dim_group + 1, MC_iterations])
# #     kapteyn_matrix = empty([dim_group + 1, MC_iterations])
# #     stats_matrix = empty([dim_group + 1, MC_iterations])
# #
# #     # Generate the distributions
# #     for j in range(len(objects)):
# #         Y_matrix[j, :] = random.normal(data_dict['Y'][j].nominal_value, data_dict['Y'][j].std_dev, size=MC_iterations)
# #         for i_dim in range(dim_group):
# #             element = regr_group[i_dim]
# #             metal_matrix[i_dim, j, :] = random.normal(data_dict[element][j].nominal_value,
# #                                                       data_dict[element][j].std_dev,
# #                                                       size=MC_iterations)
# #     # Run the curvefit and kapteyn fit
# #     formula_label = 'Y ~ ' + ' + '.join(regr_group)
# #     for k in range(MC_iterations):
# #         # Dictionary to store the current iteration
# #         x_ith = metal_matrix[:, :, k]
# #         y_ith = Y_matrix[:, k]
# #
# #         # Curvefit
# #         best_vals, covar = curve_fit(method_dict['lm' + ext_method], x_ith, y_ith, p0=p0)
# #         curvefit_matrix[:, k] = best_vals
# #
# #         # kapteyn
# #         fitobj = kmpfit.Fitter(residuals=method_dict['rlm' + ext_method], data=(x_ith, y_ith))
# #         fitobj.fit(params0=p0)
# #         kapteyn_matrix[:, k] = fitobj.params
# #
# #     # Get fit mean values
# #     idx_n = dim_group
# #     n_median_lmerror = median(lmfit_matrix[idx_n, :])
# #     n_Median_cf, n_16th_cf, n_84th_cf = median(curvefit_matrix[idx_n, :]), percentile(curvefit_matrix[idx_n, :],
# #                                                                                       16), percentile(
# #         curvefit_matrix[idx_n, :], 84)
# #     n_Median_kp, n_16th_kp, n_84th_kp = median(kapteyn_matrix[idx_n, :]), percentile(kapteyn_matrix[idx_n, :],
# #                                                                                      16), percentile(
# #         kapteyn_matrix[idx_n, :], 84)
# #
# #     # Saving the data
# #     if dim_group == 2:
# #         entry_key = r'$Y_{{P,\,{elemA}-{elemB}}}$'.format(elemA=regr_group[0], elemB=regr_group[1])
# #         regr_dict[entry_key][0] = median(kapteyn_matrix[idx_n, :])
# #         regr_dict[entry_key][1] = std(kapteyn_matrix[idx_n, :])
# #         regr_dict[entry_key][2] = int(len(objects))
# #     elif dim_group == 3:
# #         entry_key = r'$Y_{{P,\,{elemA}-{elemB}-{elemC}}}$'.format(elemA=regr_group[0], elemB=regr_group[1],
# #                                                                   elemC=regr_group[2])
# #         regr_dict[entry_key][0] = median(kapteyn_matrix[idx_n, :])
# #         regr_dict[entry_key][1] = std(kapteyn_matrix[idx_n, :])
# #         regr_dict[entry_key][2] = int(len(objects))
# #
# #         # Display results
# #     print '\n---Regression', Regresions_list[i], 'using {} objects'.format(len(objects))
# #     print 'curvefit'
# #     print n_Median_cf, n_84th_cf - n_Median_cf, n_Median_cf - n_16th_cf
# #     print 'kapteyn'
# #     print n_Median_kp, n_84th_kp - n_Median_kp, n_Median_kp - n_16th_kp
#
# # Make the table
# pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/bayes_Regressions.tex'
# headers = ['Elemental regression', 'Magnitude', 'Number of objects']
# dz.pdf_insert_table(headers)
# # pdf_address = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/yp_determinations.pdf'
# # dz.create_pdfDoc(pdf_address, pdf_type='table')
# #
# # headers = ['Elemental regression', 'Magnitude', 'Number of objects']
# # dz.pdf_insert_table(headers)
#
# last_key = regr_dict.keys()[-1]
# for key in regr_dict:
#     magnitude_entry = r'${}\pm{}$'.format(round_sig(regr_dict[key][0], 3, scien_notation=False),
#                                           round_sig(regr_dict[key][1], 1, scien_notation=False))
#     row = [key, magnitude_entry, str(int(regr_dict[key][2]))]
#     dz.addTableRow(row, last_row=False if last_key != last_key else True)
#
# dz.generate_pdf(output_address=pdf_address)
# # dz.generate_pdf()


    # Data labels
    element = regressions_list[i]
    element_label = element + '_abund'
    Ymass_label = YmassForElement[element]

    # Get plot data
    idcs_regresions = bayes_catalogue_df[element_label + '_nom'].notnull() & bayes_catalogue_df[Ymass_label + '_nom'].notnull() & ~bayes_catalogue_df.quick_reference.isin(Regresions_dict['excluded'][i])
    objRegress = bayes_catalogue_df[idcs_regresions].quick_reference.values
    print '{} included objects ({}): {}'.format(element_label, Ymass_label, '')
    x, x_er = bayes_catalogue_df.loc[idcs_regresions, element_label + '_nom'].values, bayes_catalogue_df.loc[idcs_regresions, element_label + '_er'].values
    y, y_er = bayes_catalogue_df.loc[idcs_regresions, Ymass_label + '_nom'].values, bayes_catalogue_df.loc[idcs_regresions, Ymass_label + '_er'].values

    # Convert to natural scale
    x_nat, x_er_nat = convert_natural_scale(x, x_er)

    # Create containers
    n_objects = len(objRegress)
    metal_matrix, Y_matrix = np.empty((n_objects, MC_iterations)), np.empty((n_objects, MC_iterations))
    m_vector, n_vector = np.empty(MC_iterations), np.empty(MC_iterations)

    # Generate abundance distributions
    for j in range(n_objects):
        metal_matrix[j, :] = np.random.normal(x_nat[j], x_er_nat[j], size=MC_iterations)
        Y_matrix[j, :] = np.random.normal(y[j], y_er[j], size=MC_iterations)

    # Perform the regressions in a loop
    for k in range(MC_iterations):
        x_i, y_i = metal_matrix[:, k], Y_matrix[:, k]
        m_vector[k], n_vector[k], r_value, p_value, std_err = stats.linregress(x_i, y_i)

    # BCES method
    m_bces, n_bces, m_err_bces, n_err_bces, cov_bces = bcesboot(x_nat,  x_er_nat, y, y_er, cerr=np.zeros(n_objects), nsim=5000)
