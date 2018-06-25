import pyneb as pn
import numpy as np

# Declarar pyneb ions
H1 = pn.RecAtom('H', 1)
He1 = pn.RecAtom('He', 1)

Te, ne = 12000.0, 100.0

He1.printSources()

# Calcular emisividades de pyneb
Hbeta = H1.getEmissivity(tem=Te, den=ne, wave=4861)
He1_5876A = He1.getEmissivity(tem=Te, den=ne, wave=5876)

# Calcular emisividades de Perez Montero 2017
He1_5876A_epm = (0.745 - 5.1e-5 * ne) * np.power(Te / 10000.0, 0.226 - 0.0011 * ne)

print 'Emisividades para la linea de helio 5876'
print (1 - (He1_5876A / Hbeta)/(1/He1_5876A_epm)) * 100



# from os import environ
# environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as tt
# import pymc3 as pm
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from pyneb_tests import EmissivitySurfaceFitter
#
# # Line to avoid the compute_test_value error
# theano.config.compute_test_value = "ignore"
#
# def TOIII_TSIII_relation(TSIII):
#     return (1.0807 * TSIII / 10000.0 - 0.0846) * 10000.0
#
# def emisEquation_Te_pm(temp_range, den_range, a, b, c):
#     return a + b / temp_range + c * tt.log10(temp_range)
#
# def emisEquation_TeDe_pm(temp_range, den_range, a, b, c, d, e):
#     return a + b / temp_range + c * tt.log10(temp_range) + tt.log10(1 + e * den_range)
#
# def emisEquation_HI_pm(temp_range, den_range, a, b, c):
#     return a + b * np.log(temp_range) + c * tt.log10(temp_range) * tt.log10(temp_range)
#
# def emisEquation_HeI_pm(temp_range, den_range, a, b, c, d):
#     return (a + b * den_range) * tt.power(temp_range/10000.0, c + d * den_range)
#
# def emisEquation_HeII_pm(temp_range, den_range, a, b):
#     return a * tt.power(temp_range, b)
#
# # Chemical surface fitting function
# efitter = EmissivitySurfaceFitter()
#
# lines_list = [('H1', 4102),
#             ('H1', 4340),
#             ('H1', 6563),
#             ('He1', 4471),
#             ('He1', 5876),
#             ('He1', 6678),
#             ('He1', 7065),
#             ('He2', 4686),
#             ('S3', 9069),
#             ('S3', 9531),
#             ('S3', 6312),
#             ('S2', 6717),
#             ('S2', 6731),
#             ('Ar4', 4740),
#             ('Ar3', 7136),
#             ('Ar3', 7751),
#             ('O3', 4363),
#             ('O3', 4959),
#             ('O3', 5007),
#             ('O2', 7319),
#             ('O2', 7330),
#             ('N2', 6548),
#             ('N2', 6584)]
#
# # Range of temperatures and densities
# Te_range = np.linspace(5000, 25000, 20)
# ne_array = np.linspace(1, 500, 20)
# X, Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
# Te_true, ne_true = 12500.0, 125.0
# Te_err, ne_err = 500, 25.0
# tau_true = 0.225
# cHbeta_true = 0.125
# cHbeta_err = 0.02
#
# # Generate emissivity grid
# emis_dict = efitter.genEmisGrid(lines_list, teRange=XX, neRange=YY)
#
# total_labels_array = np.array(['S2_6717A', 'S2_6731A', 'S3_6312A', 'S3_9069A', 'S3_9531A',
#                         'O2_7319A', 'O2_7330A', 'O3_4363A','O3_4959A', 'O3_5007A',
#                         'N2_6548A', 'N2_6584A',
#                         'Ar4_4740A', 'Ar3_7136A', 'Ar3_7751A',
#                          'H1_4102A', 'H1_4340A', 'H1_6563A',
#                          'He1_4471A', 'He1_5876A', 'He1_6678A', 'He1_7065A',
#                         'He2_4686A'])
#
# lines_df = pd.DataFrame(index = total_labels_array, columns = ['Flux'])
# lines_df['ion'] = lines_df.index
# lines_df['wavelength'] = lines_df.index
# lines_df['ion'] = lines_df['ion'].apply(lambda x: x[0:x.find('_')])
# lines_df['wavelength'] = lines_df['wavelength'].apply(lambda x: x[x.find('_') + 1:-1])
# lines_df['wavelength'] = lines_df['wavelength'].apply(pd.to_numeric)
# lines_df.sort_values(by=['wavelength'], ascending=True, inplace=True)
#
# lines_df['HI_lines'] = lines_df.index.str.contains('H1')
# lines_df['HeI_lines'] = lines_df.index.str.contains('He1')
# lines_df['HeII_lines'] = lines_df.index.str.contains('He2')
# lines_df['temp_low_array'] = ~lines_df.ion.isin(efitter.high_temp_ions).values
#
#
# synth_coefs = dict(He1_4471A = np.array([2.0301, 1.5e-5, 0.1463, -0.0005]), He1_5876A = np.array([0.745, -5.1e-5, 0.226, -0.0011]),
#                    He1_6678A = np.array([2.612, -0.000146, 0.2355, -0.0016]), He1_7065A = np.array([4.329, -0.0024, -0.368, -0.0017]))
#
# abund_dict = {'He1':0.0869, 'He2':0.00088, 'Ar3':5.72, 'Ar4':5.06, 'O2':7.80, 'O3':8.0, 'N2':5.48, 'S2':5.48, 'S3':6.36}
# f_lambda_dict = dict(S2_6717A=-0.318, S2_6731A=-0.320, S3_6312A=-0.264, S3_9069A=-0.594, S3_9531A=-0.605,
#                      O2_7319A=-0.398, O2_7330A=-0.400, O3_4363A=0.149, O3_4959A=-0.026, O3_5007A=-0.038,
#                      N2_6548A=-0.295, N2_6584A=-0.304, Ar4_4740A=0.038, Ar3_7136A=-0.378, Ar3_7751A=-0.450,
#                      H1_4102A=0.229, H1_4340A=0.157, H1_6563A=-0.298,
#                      He1_4471A = 0.115, He1_5876A = -0.203, He1_6678A = -0.313, He1_7065A = -0.364,
#                      He2_4686A = 0.050)
#
# # Define lines to treat
# #idx = lines_df.ion.isin(['H1', 'He1'])
# idx = ~lines_df.ion.isin(['H1', 'O3', 'O2', 'S2', 'S3'])
# #idx = lines_df.ion.isin(lines_df.ion.values)
# obs_lines = lines_df.loc[idx].index.values
#
# coeffs_dict, emis_pmEq = {}, {}
# flux_array = np.empty(obs_lines.size)
#
# obs_ions = lines_df.loc[idx].ion.unique() #EXCLUDE H1
# obs_abund = lines_df.loc[idx & ~lines_df.ion.isin(['H1'])].ion.unique()
# ions_array = lines_df.loc[idx].ion.values
# wave_array = lines_df.loc[idx].wavelength.values
# HI_lines = lines_df.loc[idx, 'HI_lines'].values
# HeI_lines = lines_df.loc[idx, 'HeI_lines'].values
# HeII_lines = lines_df.loc[idx, 'HeII_lines'].values
# temp_low_array = lines_df.loc[idx, 'temp_low_array'].values
#
# range_lines = np.arange(obs_lines.size)
# range_abund = np.arange(obs_abund.size)
# He1_check = np.any(lines_df.loc[idx].ion.isin(['He1']))
# # 'Treating lines'
# print obs_lines
# print ions_array
# print obs_ions
# print obs_abund
#
# # Generate synthetic data
# for i in range(len(obs_lines)):
#
#     #Get line label
#     line_label = obs_lines[i]
#
#     # Lines data
#     line_func       = efitter.emis_eq_dict[line_label]
#     f_lambda        = f_lambda_dict[line_label]
#
#     # Compute emissivity functions coefficients
#     p1, cov1 = efitter.fitEmis(line_func, (XX, YY), emis_dict[line_label])
#     coeffs_dict[line_label] = p1
#
#     if line_label in ['He1_4471A', 'He1_5876A', 'He1_6678A', 'He1_7065A']:
#         coeffs_dict[line_label] = synth_coefs[line_label]
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
#     elif emisfunc.__name__ == 'emisEquation_HI':
#         emis_pmEq[line_label] = emisEquation_HI_pm
#
#     elif emisfunc.__name__ == 'emisEquation_HeI':
#         emis_pmEq[line_label] = emisEquation_HeI_pm
#
#     elif emisfunc.__name__ == 'emisEquation_HeII':
#         emis_pmEq[line_label] = emisEquation_HeII_pm
#
#     #Temperature for the ion
#     T_high = TOIII_TSIII_relation(Te_true)
#     T_calc = Te_true if temp_low_array[i] else T_high
#
#     # Emissivity calculation data
#     line_emis = emisfunc((T_calc, ne_true), *coeffs_dict[line_label])
#
#     # Flux calculation
#     if HI_lines[i]:
#         flux_array[i] = line_emis * np.power(10, f_lambda * cHbeta_true)
#     elif HeI_lines[i]:
#         f_tau_coeffs = efitter.opticalDepthCoeffs[line_label]
#         f_tau = efitter.optical_depth_function(tau_true, T_calc, ne_true, *f_tau_coeffs)
#         flux_array[i] = abund_dict[ions_array[i]] * line_emis * f_tau * np.power(10, f_lambda * cHbeta_true)
#     elif HeII_lines[i]:
#         flux_array[i] = abund_dict[ions_array[i]] * line_emis * np.power(10, f_lambda * cHbeta_true)
#     else:
#         flux_array[i] = abund_dict[ions_array[i]] + line_emis - f_lambda * cHbeta_true - 12
#         print '{}_{}_{}'.format(obs_lines[i], ions_array[i], wave_array[i]), line_emis, flux_array[i]
#
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
#     cHbeta = pm.Uniform('cHbeta', lower=0.0, upper=1.0)
#
#     if He1_check:
#         tau = pm.Uniform('tau', lower=0, upper=5)
#
#     T_high = TOIII_TSIII_relation(T_low)
#
#     # Composition priors
#     abund_dict = {'H1':1.0}
#     for j in range_abund:
#         abund_dict[obs_abund[j]] = pm.Uniform(obs_abund[j], lower=0, upper=10)
#
#     # abund_dict = {'S2': pm.Uniform('S2_abund', lower=0, upper=10),
#     #               'S3': pm.Uniform('S3_abund', lower=0, upper=10),
#     #               'O2': pm.Uniform('O2_abund', lower=0, upper=10),
#     #               'O3': pm.Uniform('O3_abund', lower=0, upper=10),
#     #               'N2': pm.Uniform('N2_abund', lower=0, upper=10),
#     #               'Ar3': pm.Uniform('Ar3_abund', lower=0, upper=10),
#     #               'Ar4': pm.Uniform('Ar4_abund', lower=0, upper=10)}
#
#     for i in range_lines:
#
#         # Line data
#         line_label = obs_lines[i]
#         line_ion = ions_array[i]
#         line_coeffs = coeffs_dict[line_label]
#         line_func = emis_pmEq[line_label]
#         line_flambda = f_lambda_dict[line_label]
#
#         Te_calc = T_low if temp_low_array[i] else T_high
#
#         line_emis = line_func(Te_calc, n_e, *line_coeffs)
#
#         # H1 flux
#         if HI_lines[i]:
#             line_flux_i = line_emis * tt.power(10, line_flambda * cHbeta)
#
#         # He1 flux
#         elif HeI_lines[i]:
#             line_abund = abund_dict[line_ion]
#             f_tau_coeffs = efitter.opticalDepthCoeffs[line_label]
#             f_tau = efitter.optical_depth_function(tau, T_calc, n_e, *f_tau_coeffs)
#             line_flux_i = line_abund * line_emis * f_tau * tt.power(10, line_flambda * cHbeta)
#
#         # He2 flux
#         elif HeII_lines[i]:
#             line_abund = abund_dict[line_ion]
#             line_flux_i = line_abund * line_emis * tt.power(10, line_flambda * cHbeta)
#
#         # Metals flux
#         else:
#             line_abund = abund_dict[line_ion]
#             line_flux_i = line_abund + line_emis - line_flambda * cHbeta - 12.0
#
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
#
#
#
# # from os import environ
# # environ["MKL_THREADING_LAYER"] = "GNU"
# # import theano
# # import theano.tensor as tt
# # import pymc3 as pm
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from pyneb_tests import EmissivitySurfaceFitter
# #
# # # Line to avoid the compute_test_value error
# # theano.config.compute_test_value = "ignore"
# #
# # def TOIII_TSIII_relation(TSIII):
# #     # TODO we should make a class with these physical relations
# #     return (1.0807 * TSIII / 10000.0 - 0.0846) * 10000.0
# #
# # def emisEquation_Te_pm(temp_range, den_range, a, b, c):
# #     return a + b / temp_range + c * tt.log10(temp_range)
# #
# #
# # def emisEquation_TeDe_pm(temp_range, den_range, a, b, c, d, e):
# #     return a + b / temp_range + c * tt.log10(temp_range) + tt.log10(1 + e * den_range)
# #
# #
# # # Chemical surface fitting function
# # efitter = EmissivitySurfaceFitter()
# #
# # # Lines list
# # lines_list = [('S3', 9069),
# #               ('S3', 9531),
# #               ('S3', 6312),
# #               ('S2', 6717),
# #               ('S2', 6731),
# #               ('Ar4', 4740),
# #               ('Ar3', 7136),
# #               ('Ar3', 7751),
# #               ('O3', 4363),
# #               ('O3', 4959),
# #               ('O3', 5007),
# #               ('O2', 7319),
# #               ('O2', 7330),
# #               ('N2', 6548),
# #               ('N2', 6584)]
# #
# # # Range of temperatures and densities
# # Te_range = np.linspace(5000, 25000, 20)
# # ne_array = np.linspace(1, 500, 20)
# # X, Y = np.meshgrid(Te_range, ne_array)
# # XX = X.flatten()
# # YY = Y.flatten()
# # Te_true, ne_true = 12500.0, 125.0
# # Te_err, ne_err = 500, 25.0
# # cHbeta_true = 0.125
# # cHbeta_err = 0.02
# #
# # # Generate emissivity grid
# # emis_dict = efitter.genEmisGrid(lines_list, teRange=XX, neRange=YY)
# #
# # labels_array = np.array(['S2_6717A', 'S2_6731A', 'S3_6312A', 'S3_9069A', 'S3_9531A',
# #                         'O2_7319A', 'O2_7330A', 'O3_4363A','O3_4959A', 'O3_5007A',
# #                         'N2_6548A', 'N2_6584A',
# #                         'Ar4_4740A', 'Ar3_7136A', 'Ar3_7751A'])
# #
# # temp_low_array = np.array([True, True, True, True, True,
# #                            True, True, False, False, False,
# #                            True, True,
# #                            False, True, True])
# #
# # range_lines = np.arange(labels_array.size)
# # abund_dict = {'He1':0.0869, 'He2':0.00088, 'Ar3':5.72, 'Ar4':5.06, 'O2':7.80, 'O3':8.0, 'N2':5.48, 'S2':5.48, 'S3':6.36}
# # f_lambda_dict = dict(S2_6717A=-0.318, S2_6731A=-0.320, S3_6312A=-0.264, S3_9069A=-0.594, S3_9531A=-0.605,
# #                      O2_7319A=-0.398, O2_7330A=-0.400, O3_4363A=0.149, O3_4959A=-0.026, O3_5007A=-0.038,
# #                      N2_6548A=-0.295, N2_6584A=-0.304, Ar4_4740A=0.038, Ar3_7136A=-0.378, Ar3_7751A=-0.450)
# #
# # # Loop through the lines list:
# # coeffs_dict, emis_pmEq = {}, {}
# # flux_array,waves_array = np.empty(labels_array.size), np.empty(labels_array.size)
# # ions_array = np.empty(labels_array.size, dtype='S10')
# #
# # for i in range(len(labels_array)):
# #
# #     #Get line label
# #     line_label = labels_array[i]
# #
# #     # Lines data
# #     ions_array[i] = line_label[0:line_label.find('_')]
# #     waves_array[i] = float(line_label[line_label.find('_') + 1:-1])
# #     line_func = efitter.emis_eq_dict[line_label]
# #
# #     # Compute emissivity functions coefficients
# #     p1, cov1 = efitter.fitEmis(line_func, (XX, YY), emis_dict[line_label])
# #     coeffs_dict[line_label] = p1
# #     f_lambda = f_lambda_dict[line_label]
# #
# #     # Operation data
# #     emisfunc = efitter.emis_eq_dict[line_label]
# #
# #     # Assign equation to model
# #     if emisfunc.__name__ == 'emisEquation_Te':
# #         emis_pmEq[line_label] = emisEquation_Te_pm
# #
# #     elif emisfunc.__name__ == 'emisEquation_TeDe':
# #         emis_pmEq[line_label] = emisEquation_TeDe_pm
# #
# #     T_high = TOIII_TSIII_relation(Te_true)
# #
# #     if temp_low_array[i]:
# #         Te_calc = Te_true
# #     else:
# #         Te_calc = T_high
# #
# #     # Flux data
# #     line_emis = emisfunc((Te_calc, ne_true), *coeffs_dict[line_label])
# #     flux_array[i] = abund_dict[ions_array[i]] + line_emis - f_lambda * cHbeta_true - 12
# #     print '{}_{}_{}'.format(labels_array[i], ions_array[i], waves_array[i]), flux_array[i], 'antes', abund_dict[ions_array[i]] + emisfunc((Te_true, ne_true), *coeffs_dict[line_label])  - f_lambda * cHbeta_true - 12
# #
# # # Synthetic error for the data
# # err_array = np.abs(flux_array * 0.05)
# #
# # # Run pymc3 model
# # line_flux_tt = tt.zeros(flux_array.size)
# # print '-Starting the model'
# # with pm.Model() as model:
# #
# #     # Physical conditions priors
# #     T_low = pm.Normal('T_low', mu=10000.0, sd=1000.0)
# #     n_e = pm.Normal('n_e', mu=80, sd=50)
# #     cHbeta = cHbeta_true#pm.Uniform('cHbeta', lower=0.0, upper=1.0)
# #
# #     T_high = TOIII_TSIII_relation(T_low)
# #
# #     # Composition priors
# #     abund_dict = {'S2': pm.Uniform('S2_abund', lower=0, upper=10),
# #                   'S3': pm.Uniform('S3_abund', lower=0, upper=10),
# #                   'O2': pm.Uniform('O2_abund', lower=0, upper=10),
# #                   'O3': pm.Uniform('O3_abund', lower=0, upper=10),
# #                   'N2': pm.Uniform('N2_abund', lower=0, upper=10),
# #                   'Ar3': pm.Uniform('Ar3_abund', lower=0, upper=10),
# #                   'Ar4': pm.Uniform('Ar4_abund', lower=0, upper=10)}
# #
# #     for i in range_lines:
# #
# #         # Line data
# #         line_label = labels_array[i]
# #         line_ion = ions_array[i]
# #         line_abund = abund_dict[line_ion]
# #         line_coeffs = coeffs_dict[line_label]
# #         line_func = emis_pmEq[line_label]
# #         line_flambda = f_lambda_dict[line_label]
# #
# #         if temp_low_array[i]:
# #             Te_calc = T_low
# #         else:
# #             Te_calc = T_high
# #
# #         # Line parameters
# #         line_flux_i = line_abund + line_func(Te_calc, n_e, *line_coeffs) - line_flambda * cHbeta - 12.0
# #         line_flux_tt = tt.inc_subtensor(line_flux_tt[i], line_flux_i)
# #
# #         #Likelihood individual line
# #         #chiSq = pm.Normal(line_label + '_Y', mu=line_flux, sd=err_list[i], observed=fluxes_list[i])
# #
# #     # Global normal Likelihood for all lines
# #     Y = pm.Normal('Y', mu=line_flux_tt, sd=err_array, observed=flux_array)
# #
# #     # Global multivariable likelihood for all lines
# #     #Y = pm.MvNormal('Y', mu=line_flux_tt, cov=cov_array, observed=flux_array)
# #
# #     for RV in model.basic_RVs:
# #         print(RV.name, RV.logp(model.test_point))#
# #
# #     # Launch model
# #     trace = pm.sample(8000, tune=2000)
# #
# # print pm.summary(trace)
# # pm.traceplot(trace)
# # plt.show()