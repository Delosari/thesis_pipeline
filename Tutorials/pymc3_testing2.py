from os import environ
from sys import exit
environ["MKL_THREADING_LAYER"] = "GNU"
import theano
import theano.tensor as tt
import pymc3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyneb_tests import EmissivitySurfaceFitter
from lib.inferenceModel import SpectraSynthesizer
from lib.Astro_Libraries.spectrum_fitting.gasEmission_functions import TOIII_TSIII_relation
from numpy import log10
from collections import OrderedDict

def genStatsDict(trace):

    param_dict, stats_dict = OrderedDict(), OrderedDict()
    for parameter in trace.varnames:
        if ('_log__' not in parameter) and ('interval' not in parameter):

            trace_norm = specS.normContants[parameter] if parameter in specS.normContants else 1.0
            trace_i = trace_norm * trace[parameter]

            stats_dict[parameter] = OrderedDict()
            param_dict[parameter] = np.array([trace[parameter].mean(), trace[parameter].std()])

            stats_dict[parameter]['mean'] = np.mean(trace_i)
            stats_dict[parameter]['median'] = np.median(trace_i)
            stats_dict[parameter]['standard deviation'] = np.std(trace_i)
            stats_dict[parameter]['n'] = trace_i.size
            stats_dict[parameter]['16th_p'] = np.percentile(trace_i, 16)
            stats_dict[parameter]['84th_p'] = np.percentile(trace_i, 84)
            stats_dict[parameter]['95% HPD interval'] = (
            stats_dict[parameter]['16th_p'], stats_dict[parameter]['84th_p'])
            stats_dict[parameter]['trace'] = trace_i

    return stats_dict


# Declare synthesizer object
specS = SpectraSynthesizer()

specS.synth_coefs = dict(He1_3889A = np.array([0.904, 1.5e-6, -0.173, -0.00054]),
                   He1_4026A = np.array([-8.12509670e-02, 1.78807195e-04, 4.31012092e+00, -1.95511656e-04]),
                   He1_4471A = np.array([-1.19176501e-01, 2.67353941e-04, 2.04665573e+00, -1.37697881e-04]),
                   He1_5876A = np.array([-2.07460883e-01, 6.03088917e-04, 7.37037512e-01, -1.13466418e-04]),
                   He1_6678A = np.array([-2.18639788e-01, 6.40026064e-04, 2.59194623e+00, -4.07583592e-04]),
                   He1_7065A = np.array([4.329, -0.0024, -0.368, -0.0017]),
                   H1_6563A = np.array([10.35,  -3.254, 0.3457]),
                   H1_4341A = np.array([0.0254, 0.1922, -0.0204]),
                   He2_4686A = np.array([12.309698048256134, -0.06407094]))

def H1_linesEmis(xy_space, a, b, c):
    temp_range, den_range = xy_space
    return a + b * np.log10(temp_range) + c * np.log10(temp_range) * np.log10(temp_range)

def He1_linesEmis(xy_space, a, b, c, d):
    temp_range, den_range = xy_space
    return np.power(temp_range/10000.0, a + b * den_range) / (c + d * den_range)

def He2_linesEmis(xy_space, a, b):
    temp_range, den_range = xy_space
    return a * np.power(temp_range / 10000, b)

def H1_linesFlux(emis_ratio, cHbeta, flambda, abund=None, ftau=None, continuum=None):
    return emis_ratio * np.power(10, -1 * flambda * cHbeta)

def He1_linesFlux(emis_ratio, cHbeta, flambda, abund, ftau=None, continuum=None):
    return abund * emis_ratio * ftau * np.power(10, -1 * flambda * cHbeta)

def He2_linesFlux(emis_ratio, cHbeta, flambda, abund, ftau=None, continuum=None):
    return abund * emis_ratio * np.power(10, -1 * flambda * cHbeta)

specS.ionEmisEq = {'H1_4102A': H1_linesEmis,
                  'H1_4341A': H1_linesEmis,
                  'H1_6563A': H1_linesEmis,
                  'He1_3889A': He1_linesEmis,
                  'He1_4026A': He1_linesEmis,
                  'He1_4471A': He1_linesEmis,
                  'He1_5876A': He1_linesEmis,
                  'He1_6678A': He1_linesEmis,
                  'He1_7065A': He1_linesEmis,
                  'He2_4686A': He2_linesEmis}

specS.ionFluxEq = {'H1_4102A': H1_linesFlux,
                  'H1_4341A': H1_linesFlux,
                  'H1_6563A': H1_linesFlux,
                  'He1_3889A': He1_linesFlux,
                  'He1_4026A': He1_linesFlux,
                  'He1_4471A': He1_linesFlux,
                  'He1_5876A': He1_linesFlux,
                  'He1_6678A': He1_linesFlux,
                  'He1_7065A': He1_linesFlux,
                  'He2_4686A': He2_linesFlux}

def H1_linesEmis_tt(xy_space, a, b, c):
    temp_range, den_range = xy_space
    return a + b * tt.log10(temp_range) + c * tt.log10(temp_range) * tt.log10(temp_range)

def He1_linesEmis_tt(xy_space, a, b, c, d):
    temp_range, den_range = xy_space
    return tt.pow(temp_range/10000.0, a + b * den_range) / (c + d * den_range)

def He2_linesEmis_tt(xy_space, a, b):
    temp_range, den_range = xy_space
    return a * tt.power(temp_range / 10000, b)

def H1_linesFlux_tt(emis_ratio, cHbeta, flambda, abund=None, ftau=None, continuum=None):
    return emis_ratio * tt.power(10, -1 * flambda * cHbeta)

def He1_linesFlux_tt(emis_ratio, cHbeta, flambda, abund, ftau=None, continuum=None):
    return abund * emis_ratio * ftau * tt.power(10, -1 * flambda * cHbeta)

def He2_linesFlux_tt(emis_ratio, cHbeta, flambda, abund, ftau=None, continuum=None):
    return abund * emis_ratio * tt.power(10, -1 * flambda * cHbeta)


specS.ionEmisEq_tt = {'H1_4102A': H1_linesEmis_tt,
                  'H1_4341A': H1_linesEmis_tt,
                  'H1_6563A': H1_linesEmis_tt,
                  'He1_3889A': He1_linesEmis_tt,
                  'He1_4026A': He1_linesEmis_tt,
                  'He1_4471A': He1_linesEmis_tt,
                  'He1_5876A': He1_linesEmis_tt,
                  'He1_6678A': He1_linesEmis_tt,
                  'He1_7065A': He1_linesEmis_tt,
                  'He2_4686A': He2_linesEmis_tt}

specS.ionFluxEq_tt = {'H1_4102A': H1_linesFlux_tt,
                  'H1_4341A': H1_linesFlux_tt,
                  'H1_6563A': H1_linesFlux_tt,
                  'He1_3889A': He1_linesFlux_tt,
                  'He1_4026A': He1_linesFlux_tt,
                  'He1_4471A': He1_linesFlux_tt,
                  'He1_5876A': He1_linesFlux_tt,
                  'He1_6678A': He1_linesFlux_tt,
                  'He1_7065A': He1_linesFlux_tt,
                  'He2_4686A': He2_linesFlux_tt}

# Import observation
data_address = '/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/' + 'ObsHIIgalaxySynth' + '_objParams.txt'
specS.obj_data = specS.load_obsData(data_address, 'ObsHIIgalaxySynth')

#Declare lines for the analysis
inputLines = np.array(['H1_4341A', 'H1_6563A', 'He1_4026A', 'He1_4471A', 'He1_5876A', 'He1_6678A', 'He1_7065A','He2_4686A'])

# Read log with observational features and masks
obj_lines_df = pd.read_csv(specS.obj_data['obj_lines_file'], delim_whitespace=True, header=0, index_col=0)

# Prepare data from emission line file
specS.import_emission_line_data(obj_lines_df, input_lines=inputLines)

# Reddening parameters
specS.obj_data['lineFlambda'] = specS.gasExtincParams(specS.obj_data['lineWaves'], specS.Rv_model, specS.reddedning_curve_model)

#Calculate line fluxes
specS.rangeLines = np.arange(specS.obj_data['lineLabels'].size)
specS.lineLabels = specS.obj_data['lineLabels']
specS.lineIons = specS.obj_data['lineIons']
specS.lineFlambda = specS.obj_data['lineFlambda']

# Variables to make the iterations simpler
specS.gasSamplerVariables(specS.lineIons, specS.high_temp_ions)

# Generate line fluxes
def calcEmisFlux(T_low, n_e, cHbeta, tau, abund_dict):

    fluxArray = np.empty(specS.obj_data['lineLabels'].size)

    for i in specS.rangeLines:

        # Line data
        line_label = specS.lineLabels[i]
        line_ion = specS.lineIons[i]
        line_flambda = specS.lineFlambda[i]

        # Parameters to compute the emissivity
        emisCoeffs, emisFunc = specS.synth_coefs[line_label], specS.ionEmisEq[line_label]

        # High temperature
        T_high = TOIII_TSIII_relation(T_low)

        # Appropiate data for the ion
        Te_calc = T_high if specS.idx_highU[i] else T_low

        # Line Emissivitiy
        line_emis = emisFunc((Te_calc, n_e), *emisCoeffs)

        # Atom abundance
        line_abund = 1.0 if specS.H1_lineIdcs[i] else abund_dict[line_ion]

        # ftau correction for HeI lines
        line_ftau = specS.ftau_func(tau, Te_calc, n_e, *specS.ftau_coeffs[line_label]) if specS.He1_lineIdcs[i] else None

        # Line synthetic flux
        fluxArray[i] = specS.ionFluxEq[line_label](line_emis, cHbeta, line_flambda, line_abund, line_ftau, continuum=None)

    return fluxArray

specS.obj_data['tau_true'] = 1.3
abund_dict = {'He1r':0.0869, 'He2r':0.00057}
Te_true, ne_true = specS.obj_data['T_low_true'],specS.obj_data['n_e_true']
cHbeta_true, tau_true = specS.obj_data['cHbeta_true'], specS.obj_data['tau_true']
specS.obj_data['He1r_true'], specS.obj_data['He2r_true'] = abund_dict['He1r'], abund_dict['He2r']

lineFluxes = calcEmisFlux(Te_true, ne_true, cHbeta_true, tau_true, abund_dict)
lineFluxes_err = lineFluxes * 0.01

for j in range(specS.lineLabels.size):
    print specS.lineLabels[j], specS.obj_data['lineFluxes'][j], lineFluxes[j]

# Pymc3 model
# Container to store the synthetic line fluxes
lineFlux_tt = tt.zeros(specS.lineLabels.size)
specS.normContants = {'n_e':100, 'He1r': 0.1, 'He2r':0.001}
with pymc3.Model() as model:

    # Gas Physical conditions priors
    T_low   = pymc3.Normal('T_low', mu=12000.0, sd=1000.0)
    cHbeta  = pymc3.Lognormal('cHbeta', mu=0, sd=1) #self.obj_data['cHbeta_true']
    n_e     = specS.normContants['n_e'] * pymc3.Lognormal('n_e', mu=0, sd=1) #pymc3.Normal('n_e', mu=100.0, sd=50.0)
    tau     = pymc3.Lognormal('tau', mu=1, sd=0.75)

    #cHbeta_true
    # High temperature
    T_high  = TOIII_TSIII_relation(T_low)

    # Composition priors
    abund_dict = {'H1r': 1.0}
    for j in specS.rangeObsAtoms:
        if specS.obsAtoms[j] == 'He1r':
            abund_dict[specS.obsAtoms[j]] = specS.normContants['He1r'] * pymc3.Lognormal(specS.obsAtoms[j], mu=0, sd=1)  # pymc3.Uniform(self.obsAtoms[j], lower=0, upper=1)
        elif specS.obsAtoms[j] == 'He2r':
            abund_dict[specS.obsAtoms[j]] = specS.normContants['He2r'] * pymc3.Lognormal(specS.obsAtoms[j], mu=0, sd=1)  # pymc3.Uniform(self.obsAtoms[j], lower=0, upper=1)

    for i in specS.rangeLines:

        # Line data
        line_label = specS.lineLabels[i]
        line_ion = specS.lineIons[i]
        line_flambda = specS.lineFlambda[i]

        # Parameters to compute the emissivity
        emisCoeffs, emisFunc = specS.synth_coefs[line_label], specS.ionEmisEq_tt[line_label]

        # High temperature
        T_high = TOIII_TSIII_relation(T_low)

        # Appropiate data for the ion
        Te_calc = T_high if specS.idx_highU[i] else T_low

        # Line Emissivitiy
        line_emis = emisFunc((Te_calc, n_e), *emisCoeffs)

        # Atom abundance
        line_abund = 1.0 if specS.H1_lineIdcs[i] else abund_dict[line_ion]

        # ftau correction for HeI lines
        line_ftau = specS.ftau_func(tau, Te_calc, n_e, *specS.ftau_coeffs[line_label]) if specS.He1_lineIdcs[i] else None

        # Line synthetic flux
        flux_i = specS.ionFluxEq_tt[line_label](line_emis, cHbeta, line_flambda, line_abund, line_ftau, continuum=None)

        # Store in container
        lineFlux_tt = tt.inc_subtensor(lineFlux_tt[i], flux_i)

    Y = pymc3.Normal('Y', mu=lineFlux_tt, sd=lineFluxes_err, observed=lineFluxes)

    for RV in model.basic_RVs:
        print(RV.name, RV.logp(model.test_point))

    # Provide starting points
    start= pymc3.find_MAP()
    # print start
    step=pymc3.NUTS()

    # Launch model
    trace = pymc3.sample(4000, tune=2000, nchains=2, njobs=2, step=step)

    print trace.varnames, type(trace.varnames)
    print pymc3.summary(trace)
    #pymc3.traceplot(trace)

    stats_dict = genStatsDict(trace)
    specS.tracesPosteriorPlot(np.array(trace.varnames), stats_dic=stats_dict)
    plt.show()
