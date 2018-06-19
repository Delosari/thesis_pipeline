from os import environ
environ["MKL_THREADING_LAYER"] = "GNU"
import theano
import theano.tensor as tt
import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
from pyneb_tests import EmissivitySurfaceFitter

# Line to avoid the compute_test_value error
theano.config.compute_test_value = "ignore"

def TOIII_TSIII_relation(TSIII):
    # TODO we should make a class with these physical relations
    return (1.0807 * TSIII / 10000.0 - 0.0846) * 10000.0

def emisEquation_Te_pm(temp_range, den_range, a, b, c):
    return a + b / temp_range + c * tt.log10(temp_range)


def emisEquation_TeDe_pm(temp_range, den_range, a, b, c, d, e):
    return a + b / temp_range + c * tt.log10(temp_range) + tt.log10(1 + e * den_range)


# Chemical surface fitting function
efitter = EmissivitySurfaceFitter()

# Lines list
lines_list = [('S3', 9069),
              ('S3', 9531),
              ('S3', 6312),
              ('S2', 6717),
              ('S2', 6731),
              ('Ar4', 4740),
              ('Ar3', 7136),
              ('Ar3', 7751),
              ('O3', 4363),
              ('O3', 4959),
              ('O3', 5007),
              ('O2', 7319),
              ('O2', 7330),
              ('N2', 6548),
              ('N2', 6584)]

# Range of temperatures and densities
Te_range = np.linspace(5000, 25000, 20)
ne_array = np.linspace(1, 500, 20)
X, Y = np.meshgrid(Te_range, ne_array)
XX = X.flatten()
YY = Y.flatten()
Te_true, ne_true = 12500.0, 125.0
Te_err, ne_err = 500, 25.0
cHbeta_true = 0.125
cHbeta_err = 0.02

# Generate emissivity grid
emis_dict = efitter.genEmisGrid(lines_list, teRange=XX, neRange=YY)

labels_array = np.array(['S2_6717A', 'S2_6731A', 'S3_6312A', 'S3_9069A', 'S3_9531A',
                        'O2_7319A', 'O2_7330A', 'O3_4363A','O3_4959A', 'O3_5007A',
                        'N2_6548A', 'N2_6584A',
                        'Ar4_4740A', 'Ar3_7136A', 'Ar3_7751A'])

temp_low_array = np.array([True, True, True, True, True,
                           True, True, False, False, False,
                           True, True,
                           False, True, True])

range_lines = np.arange(labels_array.size)
abund_dict = {'He1':0.0869, 'He2':0.00088, 'Ar3':5.72, 'Ar4':5.06, 'O2':7.80, 'O3':8.0, 'N2':5.48, 'S2':5.48, 'S3':6.36}
f_lambda_dict = dict(S2_6717A=-0.318, S2_6731A=-0.320, S3_6312A=-0.264, S3_9069A=-0.594, S3_9531A=-0.605,
                     O2_7319A=-0.398, O2_7330A=-0.400, O3_4363A=0.149, O3_4959A=-0.026, O3_5007A=-0.038,
                     N2_6548A=-0.295, N2_6584A=-0.304, Ar4_4740A=0.038, Ar3_7136A=-0.378, Ar3_7751A=-0.450)

# Loop through the lines list:
coeffs_dict, emis_pmEq = {}, {}
flux_array,waves_array = np.empty(labels_array.size), np.empty(labels_array.size)
ions_array = np.empty(labels_array.size, dtype='S10')

for i in range(len(labels_array)):

    #Get line label
    line_label = labels_array[i]

    # Lines data
    ions_array[i] = line_label[0:line_label.find('_')]
    waves_array[i] = float(line_label[line_label.find('_') + 1:-1])
    line_func = efitter.emis_eq_dict[line_label]

    # Compute emissivity functions coefficients
    p1, cov1 = efitter.fitEmis(line_func, (XX, YY), emis_dict[line_label])
    coeffs_dict[line_label] = p1
    f_lambda = f_lambda_dict[line_label]

    # Operation data
    emisfunc = efitter.emis_eq_dict[line_label]

    # Assign equation to model
    if emisfunc.__name__ == 'emisEquation_Te':
        emis_pmEq[line_label] = emisEquation_Te_pm

    elif emisfunc.__name__ == 'emisEquation_TeDe':
        emis_pmEq[line_label] = emisEquation_TeDe_pm

    T_high = TOIII_TSIII_relation(Te_true)

    if temp_low_array[i]:
        Te_calc = Te_true
    else:
        Te_calc = T_high

    # Flux data
    line_emis = emisfunc((Te_calc, ne_true), *coeffs_dict[line_label])
    flux_array[i] = abund_dict[ions_array[i]] + line_emis - f_lambda * cHbeta_true - 12
    print '{}_{}_{}'.format(labels_array[i], ions_array[i], waves_array[i]), flux_array[i], 'antes', abund_dict[ions_array[i]] + emisfunc((Te_true, ne_true), *coeffs_dict[line_label])  - f_lambda * cHbeta_true - 12

# Synthetic error for the data
err_array = np.abs(flux_array * 0.05)

# Run pymc3 model
line_flux_tt = tt.zeros(flux_array.size)
print '-Starting the model'
with pm.Model() as model:

    # Physical conditions priors
    T_low = pm.Normal('T_low', mu=10000.0, sd=1000.0)
    n_e = pm.Normal('n_e', mu=80, sd=50)
    cHbeta = cHbeta_true#pm.Uniform('cHbeta', lower=0.0, upper=1.0)

    T_high = TOIII_TSIII_relation(T_low)

    # Composition priors
    abund_dict = {'S2': pm.Uniform('S2_abund', lower=0, upper=10),
                  'S3': pm.Uniform('S3_abund', lower=0, upper=10),
                  'O2': pm.Uniform('O2_abund', lower=0, upper=10),
                  'O3': pm.Uniform('O3_abund', lower=0, upper=10),
                  'N2': pm.Uniform('N2_abund', lower=0, upper=10),
                  'Ar3': pm.Uniform('Ar3_abund', lower=0, upper=10),
                  'Ar4': pm.Uniform('Ar4_abund', lower=0, upper=10)}

    for i in range_lines:

        # Line data
        line_label = labels_array[i]
        line_ion = ions_array[i]
        line_abund = abund_dict[line_ion]
        line_coeffs = coeffs_dict[line_label]
        line_func = emis_pmEq[line_label]
        line_flambda = f_lambda_dict[line_label]

        if temp_low_array[i]:
            Te_calc = T_low
        else:
            Te_calc = T_high

        # Line parameters
        line_flux_i = line_abund + line_func(Te_calc, n_e, *line_coeffs) - line_flambda * cHbeta - 12.0
        line_flux_tt = tt.inc_subtensor(line_flux_tt[i], line_flux_i)

        #Likelihood individual line
        #chiSq = pm.Normal(line_label + '_Y', mu=line_flux, sd=err_list[i], observed=fluxes_list[i])

    # Global normal Likelihood for all lines
    Y = pm.Normal('Y', mu=line_flux_tt, sd=err_array, observed=flux_array)

    # Global multivariable likelihood for all lines
    #Y = pm.MvNormal('Y', mu=line_flux_tt, cov=cov_array, observed=flux_array)

    for RV in model.basic_RVs:
        print(RV.name, RV.logp(model.test_point))#

    # Launch model
    trace = pm.sample(8000, tune=2000)










# print pm.summary(trace)
# pm.traceplot(trace)
# plt.show()
#
# from os import environ
# environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as tt
# import pymc3 as pm
# import numpy as np
# import matplotlib.pyplot as plt
# from pyneb_tests import EmissivitySurfaceFitter
#
# # Line to avoid the compute_test_value error
# theano.config.compute_test_value = "ignore"
#
# def TOIII_TSIII_relation(TSIII):
#     # TODO we should make a class with these physical relations
#     return (1.0807 * TSIII / 10000.0 - 0.0846) * 10000.0
#
# def emisEquation_Te_pm(temp_range, den_range, a, b, c):
#     return a + b / temp_range + c * tt.log10(temp_range)
#
#
# def emisEquation_TeDe_pm(temp_range, den_range, a, b, c, d, e):
#     return a + b / temp_range + c * tt.log10(temp_range) + tt.log10(1 + e * den_range)
#
#
# # Chemical surface fitting function
# efitter = EmissivitySurfaceFitter()
#
# # Lines list
# lines_list = [('S3', 9069),
#               ('S3', 9531),
#               ('S3', 6312),
#               ('S2', 6717),
#               ('S2', 6731),
#               ('Ar4', 4740),
#               ('Ar3', 7136),
#               ('Ar3', 7751),
#               ('O3', 4363),
#               ('O3', 4959),
#               ('O3', 5007),
#               ('O2', 7319),
#               ('O2', 7330),
#               ('N2', 6548),
#               ('N2', 6584)]
#
# # Range of temperatures and densities
# Te_range = np.linspace(5000, 25000, 20)
# ne_array = np.linspace(1, 500, 20)
# X, Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
# Te_true, ne_true = 12500.0, 125.0
# Te_err, ne_err = 500, 25.0
# cHbeta_true = 0.125
# cHbeta_err = 0.02
#
# # Generate emissivity grid
# emis_dict = efitter.genEmisGrid(lines_list, teRange=XX, neRange=YY)
#
# labels_array = np.array(['S2_6717A', 'S2_6731A', 'S3_6312A', 'S3_9069A', 'S3_9531A',
#                         'O2_7319A', 'O2_7330A', 'O3_4363A','O3_4959A', 'O3_5007A',
#                         'N2_6548A', 'N2_6584A',
#                         'Ar4_4740A', 'Ar3_7136A', 'Ar3_7751A'])
#
# temp_low_array = np.array([True, True, True, True, True,
#                            True, True, False, False, False,
#                            True, True,
#                            False, True, True])
#
# range_lines = np.arange(labels_array.size)
# abund_dict = {'He1':0.0869, 'He2':0.00088, 'Ar3':5.72, 'Ar4':5.06, 'O2':7.80, 'O3':8.0, 'N2':5.48, 'S2':5.48, 'S3':6.36}
# f_lambda_dict = dict(S2_6717A=-0.318, S2_6731A=-0.320, S3_6312A=-0.264, S3_9069A=-0.594, S3_9531A=-0.605,
#                      O2_7319A=-0.398, O2_7330A=-0.400, O3_4363A=0.149, O3_4959A=-0.026, O3_5007A=-0.038,
#                      N2_6548A=-0.295, N2_6584A=-0.304, Ar4_4740A=0.038, Ar3_7136A=-0.378, Ar3_7751A=-0.450)
#
# # Loop through the lines list:
# coeffs_dict, emis_pmEq = {}, {}
# flux_array,waves_array = np.empty(labels_array.size), np.empty(labels_array.size)
# ions_array = np.empty(labels_array.size, dtype='S10')
#
# for i in range(len(labels_array)):
#
#     #Get line label
#     line_label = labels_array[i]
#
#     # Lines data
#     ions_array[i] = line_label[0:line_label.find('_')]
#     waves_array[i] = float(line_label[line_label.find('_') + 1:-1])
#     line_func = efitter.emis_eq_dict[line_label]
#
#     # Compute emissivity functions coefficients
#     p1, cov1 = efitter.fitEmis(line_func, (XX, YY), emis_dict[line_label])
#     coeffs_dict[line_label] = p1
#     f_lambda = f_lambda_dict[line_label]
#
#     # Operation data
#     emisfunc = efitter.emis_eq_dict[line_label]
#
#     # Assign equation to model
#     if emisfunc.__name__ == 'emisEquation_Te':
#         emis_pmEq[line_label] = emisEquation_Te_pm
#
#     elif emisfunc.__name__ == 'emisEquation_TeDe':
#         emis_pmEq[line_label] = emisEquation_TeDe_pm
#
#     T_high = TOIII_TSIII_relation(Te_true)
#
#     if temp_low_array[i]:
#         Te_calc = Te_true
#     else:
#         Te_calc = T_high
#
#     # Flux data
#     line_emis = emisfunc((Te_calc, ne_true), *coeffs_dict[line_label])
#     flux_array[i] = abund_dict[ions_array[i]] + line_emis - f_lambda * cHbeta_true - 12
#     print '{}_{}_{}'.format(labels_array[i], ions_array[i], waves_array[i]), flux_array[i], 'antes', abund_dict[ions_array[i]] + emisfunc((Te_true, ne_true), *coeffs_dict[line_label])  - f_lambda * cHbeta_true - 12
#
# # Synthetic error for the data
# err_array = np.abs(flux_array * 0.05)
#
# # Run pymc3 model
# line_flux_tt = tt.zeros(flux_array.size)
# print '-Starting the model'
# with pm.Model() as model:
#
#     # Physical conditions priors
#     T_low = pm.Normal('T_low', mu=10000.0, sd=1000.0)
#     n_e = pm.Normal('n_e', mu=80, sd=50)
#     cHbeta = cHbeta_true#pm.Uniform('cHbeta', lower=0.0, upper=1.0)
#
#     T_high = TOIII_TSIII_relation(T_low)
#
#     # Composition priors
#     abund_dict = {'S2': pm.Uniform('S2_abund', lower=0, upper=10),
#                   'S3': pm.Uniform('S3_abund', lower=0, upper=10),
#                   'O2': pm.Uniform('O2_abund', lower=0, upper=10),
#                   'O3': pm.Uniform('O3_abund', lower=0, upper=10),
#                   'N2': pm.Uniform('N2_abund', lower=0, upper=10),
#                   'Ar3': pm.Uniform('Ar3_abund', lower=0, upper=10),
#                   'Ar4': pm.Uniform('Ar4_abund', lower=0, upper=10)}
#
#     for i in range_lines:
#
#         # Line data
#         line_label = labels_array[i]
#         line_ion = ions_array[i]
#         line_abund = abund_dict[line_ion]
#         line_coeffs = coeffs_dict[line_label]
#         line_func = emis_pmEq[line_label]
#         line_flambda = f_lambda_dict[line_label]
#
#         if temp_low_array[i]:
#             Te_calc = T_low
#         else:
#             Te_calc = T_high
#
#         # Line parameters
#         line_flux_i = line_abund + line_func(Te_calc, n_e, *line_coeffs) - line_flambda * cHbeta - 12.0
#         line_flux_tt = tt.inc_subtensor(line_flux_tt[i], line_flux_i)
#
#         #Likelihood individual line
#         #chiSq = pm.Normal(line_label + '_Y', mu=line_flux, sd=err_list[i], observed=fluxes_list[i])
#
#     # Global normal Likelihood for all lines
#     Y = pm.Normal('Y', mu=line_flux_tt, sd=err_array, observed=flux_array)
#
#     # Global multivariable likelihood for all lines
#     #Y = pm.MvNormal('Y', mu=line_flux_tt, cov=cov_array, observed=flux_array)
#
#     for RV in model.basic_RVs:
#         print(RV.name, RV.logp(model.test_point))#
#
#     # Launch model
#     trace = pm.sample(8000, tune=2000)
#
# print pm.summary(trace)
# pm.traceplot(trace)
# plt.show()