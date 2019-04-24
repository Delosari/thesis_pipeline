import numpy as np
import pandas as pd
import uncertainties as unnp
import uncertainties.umath as umath
from dazer_methods import Dazer
from collections import OrderedDict
from lib.inferenceModel import SpectraSynthesizer
from lmfit import Model, Parameters
from scipy import stats
from lib.Math_Libraries.bces_script import bces, bcesboot
from scipy.optimize import curve_fit
from lib.CodeTools.sigfig import round_sig

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


def convert_natural_scale(nom_values, er_values):
    un_array_log = unnp.unumpy.uarray(nom_values, er_values)
    un_array_nat = unnp.unumpy.pow(10, un_array_log - 12)
    return unnp.unumpy.nominal_values(un_array_nat), unnp.unumpy.std_devs(un_array_nat)


# Create class object
dz = Dazer()
specS = SpectraSynthesizer()

# Generate the indeces
Regresions_dict = OrderedDict()
Regresions_dict['Regressions']      = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
Regresions_dict['metal x axis']     = ['OI_HI', 'NI_HI', 'SI_HI']
Regresions_dict['helium y axis']    = ['Ymass_O', 'Ymass_O', 'Ymass_S']
Regresions_dict['color']          = ['tab:green', 'tab:blue', 'tab:orange']
Regresions_dict['factor'] = [1e5, 1e6, 1e6]
Regresions_dict['factor_labels'] = [1e-5, 1e-6, 1e-6]
Regresions_dict['title'] = ['Helium mass fraction versus oxygen abundance',
                            'Helium mass fraction versus nitrogen abundance',
                            'Helium mass fraction versus sulfur abundance']
Regresions_dict['x label'] = [r'$\frac{{O}}{{H}}$ $\left({}\right)$'.format(latex_float(Regresions_dict['factor_labels'][0])),
                              r'$\frac{{N}}{{H}}$ $\left({}\right)$'.format(latex_float(Regresions_dict['factor_labels'][1])),
                              r'$\frac{{S}}{{H}}$ $\left({}\right)$'.format(latex_float(Regresions_dict['factor_labels'][2]))]
Regresions_dict['excluded'] = [['FTDTR-2', 'MRK689', 'FTDTR-5', 'PHL293B'],
                              ['FTDTR-2', 'FTDTR-5', 'PHL293B'],
                              ['coso', 'PHL293B']]
Regresions_dict['y label'] = [r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{S}{H}}$']
Regresions_list = [['O', 'N'], ['O', 'S'], ['N', 'S'], ['O', 'N', 'S']]
label_regr = 'Linear fit'
method_dict = {'lm2': linear_model2, 'lm3': linear_model3, 'rlm2': residuals_lin2, 'rlm3': residuals_lin3}

# Past regression
inter_regr_dict = OrderedDict()
inter_regr_dict['$Y_{P,\,O}^{1}$'] = [0.246,0.005,'18'] #Peimbert
inter_regr_dict['$Y_{P,\,N}^{1}$'] = [0.251,0.005,'18'] #Aver
inter_regr_dict['$Y_{P,\,S}^{1}$'] = [0.244,0.006,'21'] #Izotov
inter_regr_dict['$Y_{P,\,O-N-S}^{1}$'] = [0.245,0.007,'17'] #Izotov

# Other users
exter_regr_dict = OrderedDict()
exter_regr_dict['$Y_{P,\,O}^{2}$'] = ['0.2446','0.0029','5'] #Peimbert
exter_regr_dict['$Y_{P,\,O}^{3}$'] = ['0.2449','0.0040','15'] #Aver
exter_regr_dict['$Y_{P,\,O}^{4}$'] = ['0.2551','0.0022','28'] #Izotov
exter_regr_dict['$Y_{P,\,Planck BBN}^{5}$'] = [0.24467,0.00020,'-']


# Define plot frame and colors
size_dict = {'figure.figsize': (18, 8), 'axes.labelsize': 38, 'legend.fontsize': 28,
             'font.family': 'Times New Roman', 'mathtext.default': 'regular', 'xtick.labelsize': 34, 'ytick.labelsize': 34}
dz.FigConf(plotSize=size_dict)

# Regressions properties
MC_iterations = 5000
WMAP_coordinates = np.array([unnp.ufloat(0.0, 0.0), unnp.ufloat(0.24709, 0.00025)])
YmassForElement = dict(O='Ymass_O', N='Ymass_O', S='Ymass_S')

# Declare data location
root_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\'  # root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'
article_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\source files\\images\\'
tables_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\source files\\tables\\'
whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'  # whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'

# Load catalogue dataframe
catalogue_df = dz.load_excel_DF(whtSpreadSheet)
dz.quick_indexing(catalogue_df)

# Sample objects
abundList = ['O_abund', 'N_abund', 'S_abund', 'Ymass_O', 'Ymass_S']
excludeObjects = ['SHOC579', 'SHOC575_n2', '11', 'SHOC588', 'SDSS3', 'SDSS1', 'SHOC36', '52319-521']
sampleObjects = catalogue_df.loc[dz.idx_include & ~catalogue_df.index.isin(excludeObjects)].index.values
bayes_catalogue_df = pd.DataFrame(columns=['quick_reference', 'local_reference'] + abundList)


# Loop throught the objects and generate the dataframe
for i in range(sampleObjects.size):

    # Object references
    objName = sampleObjects[i]
    local_reference = objName.replace('_', '-')
    quick_reference = catalogue_df.loc[objName].quick_index

    # Declare configuration file
    objectFolder = '{}{}/'.format(root_folder, objName)  # '{}{}\\'.format(root_folder, objName)
    dataFileAddress = '{}{}_objParams.txt'.format(objectFolder, objName)
    obsData = specS.load_obsData(dataFileAddress, objName)

    # Object references
    bayes_catalogue_df.loc[objName, 'quick_reference'] = quick_reference
    bayes_catalogue_df.loc[objName, 'local_reference'] = local_reference

    # Get abundance values
    for abund in abundList:
        if abund in obsData:
            bayes_catalogue_df.loc[objName, abund + '_nom'] = obsData[abund][0]
            bayes_catalogue_df.loc[objName, abund + '_er'] = obsData[abund][1]

# Perform the individual regressions:
results_dict = OrderedDict()
regressions_list = ['O', 'N', 'S']
for i in range(len(regressions_list)):

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

    # Get fit mean values
    m_Median, m_std, m_16th, m_84th = np.median(m_vector), np.std(m_vector), np.percentile(m_vector, 16), np.percentile(m_vector, 84)
    n_Median, n_std, n_16th, n_84th = np.median(n_vector), np.std(n_vector), np.percentile(n_vector, 16), np.percentile(n_vector, 84)
    print '-- {} abundance Yp scipy: median {}, std {}; {} objects'.format(element_label, np.median(n_vector), np.std(n_vector), n_objects)

    # print '-- {} abundance Yp bces:  {} +/- {}'.format(element_label, n_bces[0], n_err_bces[0])

    # Saving the data
    entry_key = r'$Y_{{P,\,{elem}}}$'.format(elem=element)
    results_dict[element] = np.array([entry_key, n_Median, n_std, n_objects])

    # Linear data
    elemt_scale = Regresions_dict['factor'][i]
    x_regression_range = np.linspace(0.0, np.max(x_nat) * 1.10, 20)
    y_regression_range = m_Median * x_regression_range + n_Median

    # Plotting the data,
    label_regression = r'Plank prediction: $Y = 0.24709\pm0.00025$'
    dz.data_plot(x_regression_range * elemt_scale, y_regression_range, label=label_regr, linestyle='--', color=Regresions_dict['color'][i])
    dz.data_plot(x_nat * elemt_scale, y, label='HII galaxies included', markerstyle='o', x_error=x_er_nat * elemt_scale, y_error=y_er, color=Regresions_dict['color'][i])
    #dz.plot_text(x_nat, y, objRegress)

    # Plot WMAP prediction
    dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color=dz.colorVector['pink'],
    label='Planck prediction', markerstyle='o', x_error=WMAP_coordinates[0].std_dev, y_error=WMAP_coordinates[1].std_dev)

    dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], '', loc='lower center', ncols_leg=2)
    dz.Axis.set_ylim(0.1, 0.4)

    output_pickle = '{objFolder}{element}_BayesDataRegression'.format(objFolder=article_folder, element=element)
    dz.save_manager(output_pickle, save_pickle=False)

# Perform the triple regression
idcs_3Regres = bayes_catalogue_df['O_abund_nom'].notnull() &\
               bayes_catalogue_df['N_abund_nom'].notnull() &\
               bayes_catalogue_df['S_abund_nom'].notnull() &\
               bayes_catalogue_df['Ymass_S_nom'].notnull() &\
               ~bayes_catalogue_df.quick_reference.isin(Regresions_dict['excluded'][0] + Regresions_dict['excluded'][1] + Regresions_dict['excluded'][2])


objRegress = bayes_catalogue_df[idcs_3Regres].quick_reference.values
O, O_er = bayes_catalogue_df.loc[idcs_3Regres, 'O_abund_nom'].values, bayes_catalogue_df.loc[idcs_3Regres, 'O_abund_er'].values
N, N_er = bayes_catalogue_df.loc[idcs_3Regres, 'N_abund_nom'].values, bayes_catalogue_df.loc[idcs_3Regres, 'N_abund_er'].values
S, S_er = bayes_catalogue_df.loc[idcs_3Regres, 'S_abund_nom'].values, bayes_catalogue_df.loc[idcs_3Regres, 'S_abund_er'].values
y, y_er = bayes_catalogue_df.loc[idcs_3Regres,'Ymass_S_nom'].values, bayes_catalogue_df.loc[idcs_3Regres, 'Ymass_S_er'].values

print 'Included objects: {}'.format(objRegress)

# Convert to natural scale
O_nat, O_er_nat = convert_natural_scale(O, O_er)
N_nat, N_er_nat = convert_natural_scale(N, N_er)
S_nat, S_er_nat = convert_natural_scale(S, S_er)

# Create containers
n_objects = len(objRegress)
p0 = np.array([0.005] * 3 + [0.25])
O_matrix, N_matrix, S_matrix = np.empty((n_objects, MC_iterations)), np.empty((n_objects, MC_iterations)), np.empty((n_objects, MC_iterations))
metal_matrix    = np.empty((3, n_objects, MC_iterations))
curvefit_matrix = np.empty([3 + 1, MC_iterations])

Y_matrix = np.empty((n_objects, MC_iterations))

mO_vector, mN_vector, mS_vector = np.empty(MC_iterations), np.empty(MC_iterations), np.empty(MC_iterations)
n_vector = np.empty(MC_iterations)

# Generate the distributions
for j in range(n_objects):
    Y_matrix[j, :] = np.random.normal(y[j], y_er[j], size=MC_iterations)
    metal_matrix[0, j, :] = np.random.normal(O_nat[j], O_er_nat[j], size=MC_iterations)
    metal_matrix[1, j, :] = np.random.normal(N_nat[j], N_er_nat[j], size=MC_iterations)
    metal_matrix[2, j, :] = np.random.normal(S_nat[j], S_er_nat[j], size=MC_iterations)

#Perform the regressions in a loop
for k in range(MC_iterations):

    # Dictionary to store the current iteration
    x_ith = metal_matrix[:, :, k]
    y_ith = Y_matrix[:, k]

    # Curvefit
    best_vals, covar = curve_fit(method_dict['lm3'], x_ith, y_ith, p0=p0)
    curvefit_matrix[:, k] = best_vals

# Generat mean value
n_Median_cf, n_std_df, n_16th_cf, n_84th_cf = np.median(curvefit_matrix[3, :]), np.std(curvefit_matrix[3, :]), np.percentile(curvefit_matrix[3, :],16), np.percentile(curvefit_matrix[3, :], 84)
entry_key = r'$Y_{{P,\,{elemA}-{elemB}-{elemC}}}$'.format(elemA='O', elemB='N', elemC='S')

# Save the results
results_dict['ONS'] = np.array([entry_key, n_Median_cf, n_std_df, n_objects])

# Make the table
pdf_address = tables_folder + 'yp_determinations'
# dz.create_pdfDoc(pdf_address, pdf_type='table')

headers = ['Element regression', 'Value', 'Number of objects']
dz.pdf_insert_table(headers)

last_key = results_dict.keys()[-1]
for key in results_dict:
    magnitude_entry = r'${}\pm{}$'.format(round_sig(results_dict[key][1], 3, scien_notation=False), round_sig(results_dict[key][2], 1, scien_notation=False))
    row = [results_dict[key][0], magnitude_entry, str(int(results_dict[key][3]))]
    dz.addTableRow(row, last_row = False if last_key != last_key else True)
dz.table.add_hline()

for key in inter_regr_dict:
    magnitude_entry = r'${}\pm{}$'.format(inter_regr_dict[key][0], inter_regr_dict[key][1])
    row = [key, magnitude_entry, inter_regr_dict[key][2]]
    dz.addTableRow(row, last_row = False if last_key != last_key else True)
dz.table.add_hline()

for key in exter_regr_dict:
    magnitude_entry = r'${}\pm{}$'.format(exter_regr_dict[key][0], exter_regr_dict[key][1])
    row = [key, magnitude_entry, exter_regr_dict[key][2]]
    dz.addTableRow(row, last_row = False if last_key != last_key else True)

dz.generate_pdf(output_address=pdf_address)
# dz.generate_pdf(clean_tex=True)




# import numpy as np
# import pandas as pd
# from dazer_methods import Dazer
# from collections import OrderedDict
# from uncertainties import ufloat
# from lib.inferenceModel import SpectraSynthesizer
# from lmfit import Model, Parameters
# from scipy import stats
#
#
# def linear_model(x, m, n):
#     return m * x + n
#
#
# def residuals_lin(p, c):
#     x, y = c
#     m, n = p
#     return (y - linear_model(x, m, n))
#
#
# def linear_model2(x, mA, mB, n):
#     return mA * x[0] + mB * x[1] + n
#
#
# def linear_model3(x, mA, mB, mC, n):
#     return mA * x[0] + mB * x[1] + mC * x[2] + n
#
#
# def residuals_lin2(p, c):
#     x, y = c
#     mA, mB, n = p
#     return (y - linear_model2(x, mA, mB, n))
#
#
# def residuals_lin3(p, c):
#     x, y = c
#     mA, mB, mC, n = p
#     return (y - linear_model3(x, mA, mB, mC, n))
#     return mA * x[0] + mB * x[1] + mC * x[2] + n
#
#
# def latex_float(f):
#     float_str = "{0:.2g}".format(f)
#     if "e" in float_str:
#         base, exponent = float_str.split("e")
#         return r"10^{{{}}}".format(int(exponent))
#     else:
#         return float_str
#
#
# # Create class object
# dz = Dazer()
# specS = SpectraSynthesizer()
#
# # Generate the indeces
# Regresions_dict = OrderedDict()
# Regresions_dict['Regressions'] = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
# Regresions_dict['metal x axis'] = ['OI_HI', 'NI_HI', 'SI_HI']
# Regresions_dict['helium y axis'] = ['Ymass_O', 'Ymass_O', 'Ymass_S']
# Regresions_dict['element'] = ['O', 'N', 'S']
# Regresions_dict['factor'] = [1e5, 1e6, 1e6]
# Regresions_dict['title'] = ['Helium mass fraction versus oxygen abundance',
#                             'Helium mass fraction versus nitrogen abundance',
#                             'Helium mass fraction versus sulfur abundance']
# Regresions_dict['x label'] = [r'$\frac{{O}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][0])),
#                               r'$\frac{{N}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][1])),
#                               r'$\frac{{S}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][2]))]
# Regresions_dict['y label'] = [r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{S}{H}}$']
# Regresions_list = [['O', 'N'], ['O', 'S'], ['N', 'S'], ['O', 'N', 'S']]
#
# # Define plot frame and colors
# size_dict = {'figure.figsize': (18, 8), 'axes.labelsize': 38, 'legend.fontsize': 28,
#              'font.family': 'Times New Roman', 'mathtext.default': 'regular', 'xtick.labelsize': 34, 'ytick.labelsize': 34}
# dz.FigConf(plotSize=size_dict)
#
# # Regressions properties
# MC_iterations = 5000
# WMAP_coordinates = np.array([ufloat(0.0, 0.0), ufloat(0.24709, 0.00025)])
# YmassForElement = dict(O='Ymass_O', N='Ymass_O', S='Ymass_O')
#
# # Declare data location
# root_folder = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\bayesianModel\\'  # root_folder = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/bayesianModel/'
# article_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\source files\\images\\'
# whtSpreadSheet = 'E:\\Dropbox\\Astrophysics\\Data\\WHT_observations\\WHT_Galaxies_properties.xlsx'  # whtSpreadSheet = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx'
#
# # Load catalogue dataframe
# catalogue_df = dz.load_excel_DF(whtSpreadSheet)
# dz.quick_indexing(catalogue_df)
#
# # Sample objects
# abundList = ['O_abund', 'N_abund', 'S_abund', 'Ymass_O', 'Ymass_S']
# excludeObjects = ['SHOC579', 'SHOC575_n2', '11', 'SHOC588', 'SDSS3', 'SDSS1', 'SHOC36']
# sampleObjects = catalogue_df.loc[dz.idx_include & ~catalogue_df.index.isin(excludeObjects)].index.values
# bayes_catalogue_df = pd.DataFrame(columns=['quick_reference', 'local_reference'] + abundList)
#
# # Loop throught the objects and generate the dataframe
# for i in range(sampleObjects.size):
#
#     # Object references
#     objName = sampleObjects[i]
#     local_reference = objName.replace('_', '-')
#     quick_reference = catalogue_df.loc[objName].quick_index
#
#     # Declare configuration file
#     objectFolder = '{}{}/'.format(root_folder, objName)  # '{}{}\\'.format(root_folder, objName)
#     dataFileAddress = '{}{}_objParams.txt'.format(objectFolder, objName)
#     obsData = specS.load_obsData(dataFileAddress, objName)
#
#     # Object references
#     bayes_catalogue_df.loc[objName, 'quick_reference'] = quick_reference
#     bayes_catalogue_df.loc[objName, 'local_reference'] = local_reference
#
#     for abund in abundList:
#         if abund in obsData:
#             bayes_catalogue_df.loc[objName, abund] = obsData[abund]
#
# # Perform the three regressions:
# regressions_list = ['O', 'N', 'S']
# for i in range(len(regressions_list)):
#
#     # Data labels
#     element = regressions_list[i]
#     element_label = element + '_abund'
#     YmassFraction_label = YmassForElement[element]
#
#     # Get plot data
#     idcs_regresions = bayes_catalogue_df[element_label].notnull() & bayes_catalogue_df[YmassFraction_label].notnull()
#     objRegress = bayes_catalogue_df[idcs_regresions].index.values
#     xAbundRegress = bayes_catalogue_df.loc[idcs_regresions, element_label].values
#     yMassRegress = bayes_catalogue_df.loc[idcs_regresions, YmassFraction_label].values
#
#     # Create containers
#     n_objects = len(objRegress)
#     metal_matrix, Y_matrix = np.empty((n_objects, MC_iterations)), np.empty((n_objects, MC_iterations))
#     m_vector, n_vector = np.empty(MC_iterations), np.empty(MC_iterations)
#
#     # Generate the abundance distributions
#     for j in range(n_objects):
#
#         # Metals treatment
#         x_elementLog = np.random.normal(xAbundRegress[j][0], xAbundRegress[j][1], size=MC_iterations)
#         metal_matrix[j, :] = np.power(10, x_elementLog - 12)
#
#         # Helium treatment
#         y, y_er = yMassRegress[j][0], yMassRegress[j][1]
#         Y_matrix[j, :] = np.random.normal(y, y_er, size=MC_iterations)
#
#     # Perform the regressions in a loop
#     for k in range(MC_iterations):
#         x_i = metal_matrix[:, k]
#         y_i = Y_matrix[:, k]
#
#         m, n, r_value, p_value, std_err = stats.linregress(x_i, y_i)
#         m_vector[k], n_vector[k] = m, n
#
#     # Get fit mean values
#     m_Median, m_16th, m_84th = np.median(m_vector), np.percentile(m_vector, 16), np.percentile(m_vector, 84)
#     n_Median, n_16th, n_84th = np.median(n_vector), np.percentile(n_vector, 16), np.percentile(n_vector, 84)
#
#     # Saving the data
#     entry_key = r'$Y_{{P,\,{elem}}}$'.format(elem=element)
#
#     print '{}: median {}, std {}'.format(element_label, np.median(n_vector), np.std(n_vector))
#
#     # Linear data
#     x_regression_range = np.linspace(0.0, np.max(metal_matrix[0, :]) * 1.10, 20)
#     y_regression_range = m_Median * x_regression_range + n_Median
#     label_regr = 'Linear fit'
#
#     # Plotting the data,
#     label_regression = r'Plank prediction: $Y = 0.24709\pm0.00025$'
#     dz.data_plot(x_regression_range, y_regression_range, label=label_regr, linestyle='--')
#     # dz.data_plot(x, y, color=Regresions_dict['Colors'][i], label='HII galaxies included', markerstyle='o', x_error=x_er, y_error=y_er)
#     # dz.plot_text(nominal_values(x), nominal_values(y), quick_ref)
#
#     # Plot WMAP prediction
#     dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color=dz.colorVector['pink'],
#                  label='Planck prediction', markerstyle='o', x_error=WMAP_coordinates[0].std_dev,
#                  y_error=WMAP_coordinates[1].std_dev)
#
#     # plotTitle = r'{title}: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
#     dz.Axis.set_ylim(0.1, 0.4)
#     dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], '', loc='lower center', ncols_leg=2)
#
#     output_pickle = '{objFolder}{element}_BayesDataRegression'.format(objFolder=article_folder, element=element)
#     dz.save_manager(output_pickle, save_pickle=False)





# # Generate the indeces
# Regresions_dict = OrderedDict()
# Regresions_dict['Regressions'] = ['Oxygen object abundance', 'Nitrogen object abundance', 'Sulfur object abundance']
# Regresions_dict['metal x axis'] = ['OI_HI', 'NI_HI', 'SI_HI']
# Regresions_dict['helium y axis'] = ['Ymass_O', 'Ymass_O', 'Ymass_S']
# Regresions_dict['element'] = ['O', 'N', 'S']
# Regresions_dict['factor'] = [1e5, 1e6, 1e6]
# Regresions_dict['title'] = ['Helium mass fraction versus oxygen abundance', 'Helium mass fraction versus nitrogen abundance', 'Helium mass fraction versus sulfur abundance']
# Regresions_dict['x label'] = [r'$\frac{{O}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][0])),
#                               r'$\frac{{N}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][1])),
#                               r'$\frac{{S}}{{H}}$ $({})$'.format(latex_float(Regresions_dict['factor'][2]))]
# Regresions_dict['y label'] = [r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{O}{H}}$', r'$Y_{\frac{S}{H}}$']
# Regresions_dict['Colors'] = [dz.colorVector['green'], dz.colorVector['dark blue'], dz.colorVector['orangish']]
# Regresions_list = [['O', 'N'], ['O', 'S'], ['N', 'S'], ['O', 'N', 'S']]
#
# # Additional regression label
# regr_dict = {'0': ['y|x'], '3': ['Orthogonal']}
# lmod = Model(linear_model)
#
# # Dict with regression methods
# method_dict = {'lm2': linear_model2, 'lm3': linear_model3, 'rlm2': residuals_lin2, 'rlm3': residuals_lin3}
#
# p0 = np.array([0.005, 0.25])
# p0_c = np.array([0.005, 0.005, 0.25])
#
# # Folder to save the plots
# output_folder = 'E:\\Dropbox\\Astrophysics\\Papers\\Yp_BayesianMethodology\\source files\\images\\'
#
# # Dictionary to store the the data from the table (we are going to use kapteyn)
# regr_dict = OrderedDict()
# regr_dict['$Y_{P,\,O}$'] = [0, 0, 0]
# regr_dict['$Y_{P,\,N}$'] = [0, 0, 0]
# regr_dict['$Y_{P,\,S}$'] = [0, 0, 0]
# regr_dict['$Y_{P,\,O-N}$'] = [0, 0, 0]
# regr_dict['$Y_{P,\,O-S}$'] = [0, 0, 0]
# regr_dict['$Y_{P,\,N-S}$'] = [0, 0, 0]
# regr_dict['$Y_{P,\,O-N-S}$'] = [0, 0, 0]
#
# regr_dict['$Y_{P,\,O-N-S}$'] = [0, 0, 0]
#
# exter_regr_dict = OrderedDict()
# exter_regr_dict['$Y_{P,\,O}^{1}$'] = [0.2446, 0.0029, '5']  # Peimbert
# exter_regr_dict['$Y_{P,\,O}^{2}$'] = [0.2449, 0.0040, '15']  # Aver
# exter_regr_dict['$Y_{P,\,O}^{3}$'] = [0.2551, 0.0022, '28']  # Izotov
# exter_regr_dict['$Y_{P,\,Planck BBN}^{4}$'] = [0.24467, 0.00020, '-']
#
# arguments_coords = {'xycoords': 'data', 'textcoords': 'data', 'arrowprops': dict(arrowstyle='->'),
#                     'horizontalalignment': 'right', 'verticalalignment': 'top'}
#
# # Perform linear regressions with plots
# for i in range(len(Regresions_dict['Regressions'])):
#
#     print 'Doing regression', Regresions_dict['Regressions'][i]
#
#     # Get right regression values properties
#     element = Regresions_dict['element'][i]
#     regression = Regresions_dict['Regressions'][i]
#     metal_x = Regresions_dict['metal x axis'][i]
#     helium_y = Regresions_dict['helium y axis'][i]
#     reject_idx = catalogue_df[element + '_valid'].isnull()
#     reject_objs = catalogue_df[element + '_valid'][~reject_idx].index.values
#     #print '--reject_objs', reject_objs
#
#     # Get objects which meet regression conditions
#     idces_metal = (bayes_catalogue_df[metal_x].notnull()) & (bayes_catalogue_df[helium_y].notnull()) & (~bayes_catalogue_df.index.isin(reject_objs)) & (~bayes_catalogue_df.index.isin(['14', 'MAR868', '52703-612', 'MAR1324', 'MAR1318', 'MRK36_A2']))
#     objects = bayes_catalogue_df.loc[idces_metal].index.values
#     x = bayes_catalogue_df.loc[idces_metal, metal_x].values * Regresions_dict['factor'][i]
#     x_er = bayes_catalogue_df.loc[idces_metal, metal_x + '_err'].values * Regresions_dict['factor'][i]
#     y = bayes_catalogue_df.loc[idces_metal, helium_y].values
#     y_er = bayes_catalogue_df.loc[idces_metal, helium_y + '_err'].values
#     quick_ref = bayes_catalogue_df.loc[idces_metal].quick_index
#     print bayes_catalogue_df.loc[idces_metal].index
#
#     for idx in range(len(x)):
#         print objects[idx], x[idx], x_er[idx], y[idx], y_er[idx]
#
#     print '--Doing regression', Regresions_dict['element'][i]
#     print '--- Using these objs {}:'.format(len(objects)), ', '.join(list(objects))
#     print '--- Estos no me gustan {}:'.format(len(reject_objs)), ', '.join(list(reject_objs))
#
#     # Create containers
#     metal_matrix = empty((len(objects), MC_iterations))
#     Y_matrix = empty((len(objects), MC_iterations))
#     m_vector, n_vector = empty(MC_iterations), empty(MC_iterations)
#     m_vectorlmfit = empty(MC_iterations)
#     n_vectorlmfit = empty(MC_iterations)
#     lmfit_matrix = empty([2, MC_iterations])
#     lmfit_error = empty([2, MC_iterations])
#     curvefit_matrix = empty([2, MC_iterations])
#     kapteyn_matrix = empty([2, MC_iterations])
#
#     # Generate the distributions
#     for j in range(len(objects)):
#         metal_matrix[j, :] = random.normal(x[j], x_er[j], size=MC_iterations)
#         Y_matrix[j, :] = random.normal(y[j], y_er[j], size=MC_iterations)
#
#     # Run the fits
#     for k in range(MC_iterations):
#         x_i = metal_matrix[:, k]
#         y_i = Y_matrix[:, k]
#
#         m, n, r_value, p_value, std_err = stats.linregress(x_i, y_i)
#         m_vector[k], n_vector[k] = m, n
#
#         # Lmfit
#         result_lmfit = lmod.fit(y_i, x=x_i, m=0.005, n=0.24709)
#         lmfit_matrix[:, k] = array(result_lmfit.params.valuesdict().values())
#         lmfit_error[:, k] = array([result_lmfit.params['m'].stderr, result_lmfit.params['n'].stderr])
#
#         # Curvefit
#         best_vals, covar = curve_fit(linear_model, x_i, y_i, p0=p0)
#         curvefit_matrix[:, k] = best_vals
#
#         # kapteyn
#         fitobj = kmpfit.Fitter(residuals=residuals_lin, data=(x_i, y_i))
#         fitobj.fit(params0=p0)
#         kapteyn_matrix[:, k] = fitobj.params
#
#     # Get fit mean values
#     n_Median, n_16th, n_84th = median(n_vector), percentile(n_vector, 16), percentile(n_vector, 84)
#     m_Median, m_16th, m_84th = median(m_vector), percentile(m_vector, 16), percentile(m_vector, 84)
#     m_Median_lm, m_16th_lm, m_84th_lm = median(lmfit_matrix[0, :]), percentile(lmfit_matrix[0, :], 16), percentile(
#         lmfit_matrix[0, :], 84)
#     n_Median_lm, n_16th_lm, n_84th_lm = median(lmfit_matrix[1, :]), percentile(lmfit_matrix[1, :], 16), percentile(
#         lmfit_matrix[1, :], 84)
#     m_Median_lm_error, n_Median_lm_error = median(lmfit_error[0, :]), median(lmfit_error[1, :])
#     m_Median_cf, m_16th_cf, m_84th_cf = median(curvefit_matrix[0, :]), percentile(curvefit_matrix[0, :],
#                                                                                   16), percentile(curvefit_matrix[0, :],
#                                                                                                   84)
#     n_Median_cf, n_16th_cf, n_84th_cf = median(curvefit_matrix[1, :]), percentile(curvefit_matrix[1, :],
#                                                                                   16), percentile(curvefit_matrix[1, :],
#                                                                                                   84)
#     m_Median_kp, m_16th_kp, m_84th_kp = median(kapteyn_matrix[0, :]), percentile(kapteyn_matrix[0, :], 16), percentile(
#         kapteyn_matrix[0, :], 84)
#     n_Median_kp, n_16th_kp, n_84th_kp = median(kapteyn_matrix[1, :]), percentile(kapteyn_matrix[1, :], 16), percentile(
#         kapteyn_matrix[1, :], 84)
#
#     # Bootstrap BCES
#     m, n, m_err, n_err, cov = bcesboot(nominal_values(x), std_devs(x), nominal_values(y), std_devs(y), cerr=zeros(len(x)), nsim=10000)
#
#     print 'BCES y dependent'
#     print 'n', n[0], n_err[0]
#     print 'm',m[0], m_err[0]
#     print 'BCES Orthogonal'
#     print 'n', n[3], n_err[3]
#     print 'm',m[3], m_err[3]
#     print 'Stats lingress'
#     print 'n', n_Median, n_Median - n_16th, n_84th - n_Median
#     print 'm', m_Median, m_Median-m_16th, m_84th-m_Median
#     print 'Lmfit'
#     print 'n', n_Median_lm, n_Median_lm - n_16th_lm, n_84th_lm - n_Median_lm
#     print 'm', m_Median_lm, m_Median_lm-m_16th_lm, m_84th_lm-m_Median_lm
#     print 'curvefit'
#     print 'n', n_Median_cf, n_Median_cf - n_16th_cf, n_84th_cf - n_Median_cf
#     print 'm', m_Median_cf, m_Median_cf-m_16th_cf, m_84th_cf-m_Median_cf
#     print 'kapteyn'
#     print 'n', n_Median_kp, n_Median_kp - n_16th_kp, n_84th_kp - n_Median_kp, '\n'
#     print 'm', m_Median_kp, m_Median_kp-m_16th_kp, m_84th_kp-m_Median_kp
#
#     # Saving the data
#     entry_key = r'$Y_{{P,\,{elem}}}$'.format(elem=element)
#     regr_dict[entry_key][0] = median(kapteyn_matrix[1, :])
#     regr_dict[entry_key][1] = std(kapteyn_matrix[1, :])
#     regr_dict[entry_key][2] = len(objects)
#
#     # Linear data
#     x_regression_range = linspace(0.0, max(nominal_values(x)) * 1.10, 20)
#     y_regression_range = m_Median_cf * x_regression_range + n_Median_cf
#     label_regr = 'Linear fit'
#     # label_regr = 'SCIPY bootstrap: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
#
#     # Plotting the data,
#     label_regression = r'Plank prediction: $Y = 0.24709\pm0.00025$'
#     dz.data_plot(x, y, color=Regresions_dict['Colors'][i], label='HII galaxies included', markerstyle='o', x_error=x_er, y_error=y_er)
#     dz.data_plot(x_regression_range, y_regression_range, label=label_regr, color=Regresions_dict['Colors'][i], linestyle='--')
#     dz.plot_text(nominal_values(x), nominal_values(y), quick_ref)
#
#     # Plot WMAP prediction
#     dz.data_plot(WMAP_coordinates[0].nominal_value, WMAP_coordinates[1].nominal_value, color=dz.colorVector['pink'],
#                  label='Planck prediction', markerstyle='o', x_error=WMAP_coordinates[0].std_dev,
#                  y_error=WMAP_coordinates[1].std_dev)
#
#     # plotTitle = r'{title}: $Y_{{P}} = {n}_{{-{lowerlimit}}}^{{+{upperlimit}}}$'.format(title = Regresions_dict['title'][i], n = round_sig(n_Median,4, scien_notation=False), lowerlimit = round_sig(n_Median-n_16th,2, scien_notation=False), upperlimit = round_sig(n_84th-n_Median,2, scien_notation=False))
#     dz.Axis.set_ylim(0.1, 0.4)
#     dz.FigWording(Regresions_dict['x label'][i], Regresions_dict['y label'][i], '', loc='lower center', ncols_leg=2)
#
#     output_pickle = '{objFolder}{element}_BayesDataRegression'.format(objFolder=output_folder, element=element)
#     dz.save_manager(output_pickle, save_pickle=False)
#
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
