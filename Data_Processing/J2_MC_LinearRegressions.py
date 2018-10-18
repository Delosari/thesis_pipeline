from dazer_methods import Dazer
from collections import OrderedDict
from numpy import empty, random, median, percentile, array, linspace, zeros, std
from scipy import stats
from uncertainties import ufloat
from uncertainties.unumpy import nominal_values, std_devs
from lib.CodeTools.sigfig import round_sig
from lib.Math_Libraries.bces_script import bces, bcesboot
from pandas import DataFrame
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
dz.quick_indexing(catalogue_df)

# Regressions properties
MC_iterations = 10000
WMAP_coordinates = array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])

# Generate the indeces
Regresions_dict = OrderedDict()
Regresions_dict['Regressions'] = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
Regresions_dict['metal x axis'] = ['OI_HI_emis2nd', 'NI_HI_emis2nd', 'SI_HI_emis2nd']
Regresions_dict['helium y axis'] = ['Ymass_O_emis2nd', 'Ymass_O_emis2nd', 'Ymass_S_emis2nd']
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
output_folder = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/images/'

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

# Perform linear regressions with plots
for i in range(len(Regresions_dict['Regressions'])):

    # Get right regression values properties
    element = Regresions_dict['element'][i]
    regression = Regresions_dict['Regressions'][i]
    metal_x = Regresions_dict['metal x axis'][i]
    helium_y = Regresions_dict['helium y axis'][i]
    reject_idx = catalogue_df[element + '_valid'].isnull()
    reject_objs = catalogue_df[element + '_valid'][~reject_idx].index.values

    # Get objects which meet regression conditions
    idces_metal = (catalogue_df[metal_x].notnull()) & (catalogue_df[helium_y].notnull()) & (
        ~catalogue_df.index.isin(reject_objs))
    objects = catalogue_df.loc[idces_metal].index.values
    x = catalogue_df.loc[idces_metal, metal_x].values * Regresions_dict['factor'][i]
    y = catalogue_df.loc[idces_metal, helium_y].values
    quick_ref = catalogue_df.loc[idces_metal].quick_index

    # Get the data for the excees N/O objects
    NO_excess_idcs = ((catalogue_df[element + '_valid'] == 'NO_excess') | (
                catalogue_df[element + '_valid'] == 'ignored')) & (catalogue_df[metal_x].notnull()) & (
                         catalogue_df[helium_y].notnull())
    x_NO = catalogue_df.loc[NO_excess_idcs, metal_x].values * Regresions_dict['factor'][i]
    y_NO = catalogue_df.loc[NO_excess_idcs, helium_y].values
    quickref_NO = catalogue_df.loc[NO_excess_idcs].quick_index

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
        metal_matrix[j, :] = random.normal(x[j].nominal_value, x[j].std_dev, size=MC_iterations)
        Y_matrix[j, :] = random.normal(y[j].nominal_value, y[j].std_dev, size=MC_iterations)

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
    m, n, m_err, n_err, cov = bcesboot(nominal_values(x), std_devs(x), nominal_values(y), std_devs(y),
                                       cerr=zeros(len(x)), nsim=10000)

    print '\nBCES y dependent'
    print 'n', n[0], n_err[0]
    print 'm',m[0], m_err[0]
    print '\nBCES Orthogonal'
    print 'n', n[3], n_err[3]
    print 'm',m[3], m_err[3]
    print '\nStats lingress'
    print 'n', n_Median, n_Median - n_16th, n_84th - n_Median
    print 'm', m_Median, m_Median-m_16th, m_84th-m_Median
    print '\nLmfit'
    print 'n', n_Median_lm, n_Median_lm - n_16th_lm, n_84th_lm - n_Median_lm
    print 'm', m_Median_lm, m_Median_lm-m_16th_lm, m_84th_lm-m_Median_lm
    print '\ncurvefit'
    print 'n', n_Median_cf, n_Median_cf - n_16th_cf, n_84th_cf - n_Median_cf
    print 'm', m_Median_cf, m_Median_cf-m_16th_cf, m_84th_cf-m_Median_cf
    print '\nkapteyn'
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
    dz.data_plot(nominal_values(x), nominal_values(y), color=Regresions_dict['Colors'][i],
                 label='HII galaxies included', markerstyle='o', x_error=std_devs(x), y_error=std_devs(y))
    dz.data_plot(x_regression_range, y_regression_range, label=label_regr, color=Regresions_dict['Colors'][i],
                 linestyle='--')
    # dz.plot_text(nominal_values(x), nominal_values(y), quick_ref)

    # Plotting NO objects
    dz.data_plot(nominal_values(x_NO), nominal_values(y_NO), color=Regresions_dict['Colors'][i],
                 label='HII galaxies excluded', markerstyle='x', x_error=std_devs(x_NO), y_error=std_devs(y_NO),
                 e_style=':')
    # dz.plot_text(nominal_values(x_NO), nominal_values(y_NO), quickref_NO, y_pad=1.05)

    # for ii in range(len(y_NO)):
    #     x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]
    #     dz.Axis.annotate(s=quickref_NO[ii],xy=(x_coord, y_coord), xytext=(x_coord, y_coord*1.20), **arguments_coords)

    if element != 'S':
        for ii in range(len(y_NO)):
            x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]
            dz.Axis.text(x_coord, y_coord, quickref_NO[ii], {'ha': 'left', 'va': 'bottom'}, rotation=65, fontsize=18)
    else:
        counter = 0
        coords_sulfur = [3, 3.5, 3.25]
        arrows_sulfur = [3.1, 3.60, 3.35]
        for ii in range(len(y_NO)):
            if quickref_NO[ii] in ['SHOC592', 'SHOC220', 'SHOC036']:
                x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]
                dz.Axis.text(x_coord, y_coord, quickref_NO[ii], {'ha': 'left', 'va': 'bottom'}, rotation=65,
                             fontsize=18)

            elif quickref_NO[ii] in ['SHOC588', 'SHOC575', 'SHOC579']:

                x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]

                # dz.Axis.annotate(quickref_NO[ii], xy=(x_coord, y_coord), xycoords='data',
                #                  xytext=(coords_sulfur[counter], 0.35), textcoords='data',
                #                  arrowprops=dict(arrowstyle="->", lw=1.5), rotation=65, fontsize=18)

                dz.Axis.annotate('', xy=(x_coord, y_coord), xycoords='data',
                                 xytext=(arrows_sulfur[counter], 0.308), textcoords='data',
                                 arrowprops=dict(arrowstyle="->", lw=1.5), fontsize=18)

                dz.Axis.annotate(quickref_NO[ii], xy=(x_coord, y_coord), xycoords='data',
                                 xytext=(coords_sulfur[counter], 0.35), textcoords='data',
                                 rotation=65, fontsize=18)

                counter += 1

    # Plot WMAP prediction
    dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color=dz.colorVector['pink'],
                 label='Planck prediction', markerstyle='o', x_error=WMAP_coordinates[0].std_dev,
                 y_error=WMAP_coordinates[1].std_dev)

    # plotTitle = r'{title}: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
    dz.Axis.set_ylim(0.1, 0.4)
    dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], '', loc='lower center', ncols_leg=2)

    output_pickle = '{objFolder}{element}_regression_2nd'.format(objFolder=output_folder, element=element)
    dz.save_manager(output_pickle, save_pickle=False)

# Combined regressions
for i in range(len(Regresions_list)):

    regr_group = Regresions_list[i]
    dim_group = len(regr_group)
    ext_method = str(dim_group)
    p0 = array([0.005] * dim_group + [0.25])

    # Define lmfit model
    params = Parameters()
    for idx in range(dim_group):
        params.add('m' + str(idx), value=0.005)
    params.add('n', value=0.25)

    # Loop through the elements valid objects
    idcs = (catalogue_df['Ymass_O_emis2nd'].notnull())
    for element in regr_group:
        abunCode = '{}I_HI_emis2nd'.format(element)
        valCode = '{}_valid'.format(element)
        idcs = idcs & (catalogue_df[abunCode].notnull()) & (catalogue_df[valCode].isnull())

    # Get data
    data_dict = OrderedDict()
    objects = catalogue_df.loc[idcs].index.values
    data_dict['Y'] = catalogue_df.loc[idcs, 'Ymass_O_emis2nd'].values
    for element in regr_group:
        abunCode = '{}I_HI_emis2nd'.format(element)
        data_dict[element] = catalogue_df.loc[idcs, abunCode].values

    # Generate containers for the data
    metal_matrix = empty((dim_group, len(objects), MC_iterations))
    Y_matrix = empty((len(objects), MC_iterations))
    lmfit_matrix = empty([dim_group + 1, MC_iterations])
    lmfit_error = empty([dim_group + 1, MC_iterations])
    curvefit_matrix = empty([dim_group + 1, MC_iterations])
    kapteyn_matrix = empty([dim_group + 1, MC_iterations])
    stats_matrix = empty([dim_group + 1, MC_iterations])

    # Generate the distributions
    for j in range(len(objects)):
        Y_matrix[j, :] = random.normal(data_dict['Y'][j].nominal_value, data_dict['Y'][j].std_dev, size=MC_iterations)
        for i_dim in range(dim_group):
            element = regr_group[i_dim]
            metal_matrix[i_dim, j, :] = random.normal(data_dict[element][j].nominal_value,
                                                      data_dict[element][j].std_dev,
                                                      size=MC_iterations)
    # Run the curvefit and kapteyn fit
    formula_label = 'Y ~ ' + ' + '.join(regr_group)
    for k in range(MC_iterations):
        # Dictionary to store the current iteration
        x_ith = metal_matrix[:, :, k]
        y_ith = Y_matrix[:, k]

        # Curvefit
        best_vals, covar = curve_fit(method_dict['lm' + ext_method], x_ith, y_ith, p0=p0)
        curvefit_matrix[:, k] = best_vals

        # kapteyn
        fitobj = kmpfit.Fitter(residuals=method_dict['rlm' + ext_method], data=(x_ith, y_ith))
        fitobj.fit(params0=p0)
        kapteyn_matrix[:, k] = fitobj.params

    # Get fit mean values
    idx_n = dim_group
    n_median_lmerror = median(lmfit_matrix[idx_n, :])
    n_Median_cf, n_16th_cf, n_84th_cf = median(curvefit_matrix[idx_n, :]), percentile(curvefit_matrix[idx_n, :],
                                                                                      16), percentile(
        curvefit_matrix[idx_n, :], 84)
    n_Median_kp, n_16th_kp, n_84th_kp = median(kapteyn_matrix[idx_n, :]), percentile(kapteyn_matrix[idx_n, :],
                                                                                     16), percentile(
        kapteyn_matrix[idx_n, :], 84)

    # Saving the data
    if dim_group == 2:
        entry_key = r'$Y_{{P,\,{elemA}-{elemB}}}$'.format(elemA=regr_group[0], elemB=regr_group[1])
        regr_dict[entry_key][0] = median(kapteyn_matrix[idx_n, :])
        regr_dict[entry_key][1] = std(kapteyn_matrix[idx_n, :])
        regr_dict[entry_key][2] = int(len(objects))
    elif dim_group == 3:
        entry_key = r'$Y_{{P,\,{elemA}-{elemB}-{elemC}}}$'.format(elemA=regr_group[0], elemB=regr_group[1],
                                                                  elemC=regr_group[2])
        regr_dict[entry_key][0] = median(kapteyn_matrix[idx_n, :])
        regr_dict[entry_key][1] = std(kapteyn_matrix[idx_n, :])
        regr_dict[entry_key][2] = int(len(objects))

        # Display results
    print '\n---Regression', Regresions_list[i], 'using {} objects'.format(len(objects))
    print 'curvefit'
    print n_Median_cf, n_84th_cf - n_Median_cf, n_Median_cf - n_16th_cf
    print 'kapteyn'
    print n_Median_kp, n_84th_kp - n_Median_kp, n_Median_kp - n_16th_kp

# # Make the table
# pdf_address = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/yp_determinations'
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
# dz.table.add_hline()
# for key in exter_regr_dict:
#     magnitude_entry = r'${}\pm{}$'.format(exter_regr_dict[key][0], exter_regr_dict[key][1])
#     row = [key, magnitude_entry, exter_regr_dict[key][2]]
#     dz.addTableRow(row, last_row=False if last_key != last_key else True)
#
# dz.generate_pdf(output_address=pdf_address)
# # dz.generate_pdf()
