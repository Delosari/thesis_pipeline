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
from matplotlib import container

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


# Load catalogue dataframe
catalogue_dict = dz.import_catalogue()
catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
dz.quick_indexing(catalogue_df)

# Regressions properties
MC_iterations = 500
WMAP_coordinates = array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])

# Define plot frame and colors
size_dict = {'figure.figsize': (18, 8), 'axes.labelsize': 38, 'legend.fontsize': 28, 'font.family': 'Times New Roman',
            'mathtext.default': 'regular', 'xtick.labelsize': 34, 'ytick.labelsize': 34}
dz.FigConf(plotSize=size_dict)

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
Regresions_dict['x label'] = [r'$\frac{O}{H}\times10^{5}$',
                              r'$\frac{N}{H}\times10^{6}$',
                              r'$\frac{S}{H}\times10^{6}$']
Regresions_dict['y label'] = [r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{S}{H}}$']
Regresions_dict['Colors'] = [dz.colorVector['green'], dz.colorVector['dark blue'], dz.colorVector['orangish']]
# Regresions_list = [['O', 'N'], ['O', 'S'], ['N', 'S'], ['O', 'N', 'S']]

markerDict = {}
markerDict['SHOC579'] = 's'
markerDict['SHOC575'] = '^'
markerDict['SHOC588'] = 'd'

# Additional regression label
regr_dict = {'0': ['y|x'], '3': ['Orthogonal']}
lmod = Model(linear_model)

# Dict with regression methods
method_dict = {'lm2': linear_model2, 'lm3': linear_model3, 'rlm2': residuals_lin2, 'rlm3': residuals_lin3}

p0 = array([0.005, 0.25])
p0_c = array([0.005, 0.005, 0.25])

# Folder to save the plots
output_folder = '/home/vital/Dropbox/Astrophysics/Telescope Time/MEGARA_NOexcess_Gradients/'

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

# Establish the axis
AxHor2 = dz.Axis.twiny()
AxHor3 = dz.Axis.twiny()
Regresions_dict['axis'] = [dz.Axis, AxHor2, AxHor3]

AxHor2.set_frame_on(True)
AxHor2.patch.set_visible(False)
AxHor2.xaxis.set_ticks_position('bottom')
AxHor2.xaxis.set_label_position('bottom')
AxHor2.spines['bottom'].set_position(('outward', 120))

# AxHor3.set_frame_on(True)
# AxHor3.patch.set_visible(False)
# AxHor3.xaxis.set_ticks_position('bottom')
# AxHor3.xaxis.set_label_position('bottom')
# AxHor3.spines['bottom'].set_position(('outward', 80))

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
    idces_metal = (catalogue_df[metal_x].notnull()) & (catalogue_df[helium_y].notnull()) & (~catalogue_df.index.isin(reject_objs))
    objects = catalogue_df.loc[idces_metal].index.values
    x = catalogue_df.loc[idces_metal, metal_x].values * Regresions_dict['factor'][i]
    y = catalogue_df.loc[idces_metal, helium_y].values
    quick_ref = catalogue_df.loc[idces_metal].quick_index

    # Get the data for the excees N/O objects
    NO_excess_idcs = ((catalogue_df[element + '_valid'] == 'NO_excess') | (catalogue_df[element + '_valid'] == 'ignored')) & (catalogue_df[metal_x].notnull()) & (catalogue_df[helium_y].notnull())
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
    m_Median_lm, m_16th_lm, m_84th_lm = median(lmfit_matrix[0, :]), percentile(lmfit_matrix[0, :], 16), percentile(lmfit_matrix[0, :], 84)
    n_Median_lm, n_16th_lm, n_84th_lm = median(lmfit_matrix[1, :]), percentile(lmfit_matrix[1, :], 16), percentile(lmfit_matrix[1, :], 84)
    m_Median_lm_error, n_Median_lm_error = median(lmfit_error[0, :]), median(lmfit_error[1, :])
    m_Median_cf, m_16th_cf, m_84th_cf = median(curvefit_matrix[0, :]), percentile(curvefit_matrix[0, :],16), percentile(curvefit_matrix[0, :], 84)
    n_Median_cf, n_16th_cf, n_84th_cf = median(curvefit_matrix[1, :]), percentile(curvefit_matrix[1, :], 16), percentile(curvefit_matrix[1, :], 84)
    m_Median_kp, m_16th_kp, m_84th_kp = median(kapteyn_matrix[0, :]), percentile(kapteyn_matrix[0, :], 16), percentile(kapteyn_matrix[0, :], 84)
    n_Median_kp, n_16th_kp, n_84th_kp = median(kapteyn_matrix[1, :]), percentile(kapteyn_matrix[1, :], 16), percentile(kapteyn_matrix[1, :], 84)

    # Bootstrap BCES
    m, n, m_err, n_err, cov = bcesboot(nominal_values(x), std_devs(x), nominal_values(y), std_devs(y), cerr=zeros(len(x)), nsim=10000)

    # Saving the data
    entry_key = r'$Y_{{P,\,{elem}}}$'.format(elem=element)
    regr_dict[entry_key][0] = median(kapteyn_matrix[1, :])
    regr_dict[entry_key][1] = std(kapteyn_matrix[1, :])
    regr_dict[entry_key][2] = len(objects)

    # Linear data
    x_regression_range = linspace(0.0, max(nominal_values(x)) * 1.10, 20)
    y_regression_range = m_Median_cf * x_regression_range + n_Median_cf
    label_regr = 'Metal linear fit'

    # Plotting the data,
    if element == 'O':
        dz.data_plot(nominal_values(x), nominal_values(y), color='black', label='O/H abundance for linear sample', markerstyle='o', x_error=std_devs(x), y_error=std_devs(y), graph_axis = Regresions_dict['axis'][i], markersize=5)

    # Plot regression
    dz.data_plot(x_regression_range, y_regression_range, label=label_regr, color=Regresions_dict['Colors'][i], linestyle='--', graph_axis = Regresions_dict['axis'][i])

    # Plotting NO objects
    for j in range(len(x_NO)):
        objectName = quickref_NO[j]
        x_value, x_std = x_NO[j].nominal_value, x_NO[j].std_dev
        y_value, y_std = y_NO[j].nominal_value, y_NO[j].std_dev
        if (objectName != 'MRK689') and (objectName in markerDict.keys()):
            dz.data_plot(x_value, y_value, color=Regresions_dict['Colors'][i],
            label=objectName, markerstyle=markerDict[objectName], x_error=x_std, y_error=y_std, graph_axis = Regresions_dict['axis'][i], markersize=10)

    # dz.plot_text(nominal_values(x_NO), nominal_values(y_NO), quickref_NO, y_pad=1.05)
    # for ii in range(len(y_NO)):
    #     x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]
    #     arguments_coords = {'xycoords': 'data', 'textcoords': 'data', 'arrowprops': dict(arrowstyle='->'), 'horizontalalignment': 'right', 'verticalalignment': 'top'}
    #     dz.Axis.annotate(s=quickref_NO[ii],xy=(x_coord, y_coord), xytext=(x_coord, y_coord*1.20), **arguments_coords)
    #
    # if element != 'S':
    #     for ii in range(len(y_NO)):
    #         x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]
    #         dz.Axis.text(x_coord, y_coord, quickref_NO[ii], {'ha': 'left', 'va': 'bottom'}, rotation=65, fontsize=18)
    # else:
    #     counter = 0
    #     coords_sulfur = [3, 3.5, 3.25]
    #     arrows_sulfur = [3.1, 3.60, 3.35]
    #     for ii in range(len(y_NO)):
    #         if quickref_NO[ii] in ['SHOC592', 'SHOC220', 'SHOC036']:
    #             x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]
    #             dz.Axis.text(x_coord, y_coord, quickref_NO[ii], {'ha': 'left', 'va': 'bottom'}, rotation=65, fontsize=18)
    #
    #         elif quickref_NO[ii] in ['SHOC588', 'SHOC575', 'SHOC579']:
    #
    #             x_coord, y_coord = nominal_values(x_NO)[ii], nominal_values(y_NO)[ii]
    #
    #             dz.Axis.annotate('', xy=(x_coord, y_coord), xycoords='data',
    #                              xytext=(arrows_sulfur[counter], 0.308), textcoords='data',
    #                              arrowprops=dict(arrowstyle="->", lw=1.5), fontsize=18)
    #
    #             dz.Axis.annotate(quickref_NO[ii], xy=(x_coord, y_coord), xycoords='data',
    #                              xytext=(coords_sulfur[counter], 0.35), textcoords='data',
    #                              rotation=65, fontsize=18)
    #
    #             counter += 1

# Plot WMAP prediction
dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color=dz.colorVector['pink'], label=r'Planck $Y_{P}$ prediction', markerstyle='*', graph_axis = Regresions_dict['axis'][0], markersize=300)

dz.Axis.set_ylim(0.1, 0.4)
#dz.FigWording(Regresions_dict['x label'][0], 'Y', '', loc='lower center', ncols_leg=2, XLabelPad=0.40)



handles, labels = dz.Axis.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
leg = dz.Axis.legend(handles, labels, loc='lower center', ncol=2)

LH = leg.legendHandles
for idx in range(len(LH)):
    LH[idx].set_color('black')


# # Security checks to avoid empty legends
# if Axis.get_legend_handles_labels()[1] != None:
#
#     if len(Axis.get_legend_handles_labels()[1]) != 0:
#         Old_Handles, Old_Labels = Axis.get_legend_handles_labels()
#
#         if sort_legend:
#             labels, handles = zip(*sorted(zip(Old_Labels, Old_Handles), key=lambda t: t[0]))
#             Handles_by_Label = OrderedDict(zip(labels, handles))
#             Axis.legend(Handles_by_Label.values(), Handles_by_Label.keys(), loc=loc, ncol=ncols)
#         else:
#             Handles_by_Label = OrderedDict(zip(Old_Labels, Old_Handles))
#             Axis.legend(Handles_by_Label.values(), Handles_by_Label.keys(), loc=loc, ncol=ncols)






dz.Axis.set_ylabel('Y')
dz.Axis.set_xlabel(Regresions_dict['x label'][0], color = Regresions_dict['Colors'][0])
AxHor2.set_xlabel(Regresions_dict['x label'][1], y = 0.01, color = Regresions_dict['Colors'][1])
AxHor3.set_xlabel(Regresions_dict['x label'][2], color = Regresions_dict['Colors'][2])

dz.Axis.tick_params('x', colors=Regresions_dict['Colors'][0])
AxHor2.tick_params('x', colors=Regresions_dict['Colors'][1])
AxHor3.tick_params('x', colors=Regresions_dict['Colors'][2])

dz.Axis.spines['bottom'].set_color(Regresions_dict['Colors'][0])
AxHor2.spines['bottom'].set_color(Regresions_dict['Colors'][1])
AxHor3.spines['top'].set_color(Regresions_dict['Colors'][2])
AxHor3.spines['bottom'].set_color(Regresions_dict['Colors'][0])

output_pickle = '{objFolder}_triple_regression'.format(objFolder=output_folder, element=element)
dz.save_manager(output_pickle, save_pickle=False)
#dz.display_fig()