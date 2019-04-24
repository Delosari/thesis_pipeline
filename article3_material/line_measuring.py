import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, optimize


# Function to get spectrum regions from the input wavelengths
def line_regions(wave_range, wave_limits):
    idcsLines = (wave_limits[2] <= wave_range) & (wave_range <= wave_limits[3])
    idcsContinua = ((wave_limits[0] <= wave_range) & (wave_range <= wave_limits[1])) | (
                (wave_limits[4] <= wave_range) & (wave_range <= wave_limits[5]))
    return idcsLines, idcsContinua


# Function to get spectrum regions from a matrix of wavelengths
def line_regions_matrix(wave_range, waveLimitsMatrix):
    waveIndcs_matrix = np.searchsorted(wave_range, waveLimitsMatrix)

    idcsLines = (wave_range[waveIndcs_matrix[:, 2]] <= wave_range[:, None]) & (
                wave_range[:, None] <= wave_range[waveIndcs_matrix[:, 3]])
    idcsContinua = ((wave_range[waveIndcs_matrix[:, 0]] <= wave_range[:, None]) & (
                wave_range[:, None] <= wave_range[waveIndcs_matrix[:, 1]])) | (
                           (wave_range[waveIndcs_matrix[:, 4]] <= wave_range[:, None]) & (
                               wave_range[:, None] <= wave_range[waveIndcs_matrix[:, 5]]))

    return idcsLines, idcsContinua


# Gaussian curve with linear continuum
def gauss_curve(ind_params, a, mu, sigma):
    x, z = ind_params
    return a * np.exp(-((x - mu) * (x - mu)) / (2 * (sigma * sigma))) + z


class LineMesurer():

    def __init__(self):

        # Mathematical terms
        self.sqrt2pi = np.sqrt(2 * np.pi)

        # Table with data for the labels
        default_address = 'C:\\Users\\Vital\\PycharmProjects\\dazer\\bin\\lib\\Astro_Libraries\\literature_data\\lines_data.xlsx'
        self.linesDb = pd.read_excel(default_address, sheet_name=0, header=0, index_col=0)

        # Default headers for the dictionary
        self.lineLogHeaders = ['Ion',
                               'lambda_theo',
                               'obs_wavelength',
                               'emis_type',
                               'pynebCode',
                               'flux_intg',
                               'flux_intg_er',
                               'flux_gauss',
                               'flux_gauss_er',
                               'eqw',
                               'eqw_er',
                               'A',
                               'A_er',
                               'mu',
                               'mu_er',
                               'sigma',
                               'sigma_er',
                               'zerolev_mean',
                               'zerolev_std',
                               'zerolev_width',
                               'm_zerolev',
                               'n_zerolev',
                               'w1',
                               'w2',
                               'w3',
                               'w4',
                               'w5',
                               'w6',
                               'blended_check',
                               'line_number',
                               'group_label',
                               'add_wide_component',
                               'fit_routine']

        return

    def gaussEm_linCont_curvefit(self, lineWave, lineFlux, synthLineFluxMatrix, contFit, mc_len):

        # Initial values for fit
        p0 = (lineFlux.max(), lineWave.mean(), 1.0)

        # Perform fitting batch
        p1_matrix = np.empty((mc_len, 3))
        for j in np.arange(mc_len):  # This one is not powerfull enought... add more points
            p1_matrix[j], pcov = optimize.curve_fit(gauss_curve, (lineWave, contFit), synthLineFluxMatrix[j], p0=p0)

        return p1_matrix

    def lineFit(self, wave, flux, idcs_lines, idcs_cont, mc_len=1000, plot_data=False):

        # Define line and continua regions
        lineWave, lineFlux = wave[idcs_lines], flux[idcs_lines]
        contWave, contFlux = wave[idcs_cont], flux[idcs_cont]
        n_pixels = lineWave.size
        lineWidth = lineWave[-1] - lineWave[0]
        pixel_width = lineWidth / (n_pixels - 1)

        # Linear continuum fit
        m_cont, n_cont, r_value, p_value, std_err = stats.linregress(contWave, contFlux)
        contFit = m_cont * contWave + n_cont
        lineCont = m_cont * lineWave + n_cont
        contInt = lineCont.sum() * pixel_width
        contStd = np.std(contFlux - contFit)

        # # Plot the spectrum
        # fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        # ax.plot(wave, flux, color='black', label='Object spectrum')
        # ax.plot(lineWave, lineFlux, label='lineFlux')
        # ax.plot(lineWave, lineCont, label='lineFlux')
        # ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux (normalised)'})
        # ax.legend()
        # plt.show()

        # Compute matrix with random noise from the continua standard deviation
        lineNoise = np.random.normal(0.0, contStd, (mc_len, n_pixels))
        lineSynthFluxMatrix = lineFlux + lineNoise

        # Compute integrated flux
        areasArray = lineSynthFluxMatrix.sum(axis=1) * pixel_width - contInt
        intgInt, intgStd = areasArray.mean(), areasArray.std()

        # Perform fit in loop
        p1_matrix = self.gaussEm_linCont_curvefit(lineWave, lineFlux, lineSynthFluxMatrix, lineCont, mc_len)

        # Compute results from gaussian fit
        gIntArray = p1_matrix[:, 0] * p1_matrix[:, 2] * self.sqrt2pi
        gaussInt, gaussStd = gIntArray.mean(), gIntArray.std()
        p1_Mean, p1_Std = p1_matrix.mean(axis=0), p1_matrix.std(axis=0)

        # Dictionary to store the results
        results_dict = dict(intgInt=intgInt, intgStd=intgStd, gaussInt=gaussInt, gaussStd=gaussStd,
                            p1_Mean=p1_Mean, p1_Std=p1_Std)

        # Add arrays to plot the fitting
        if plot_data:
            resampleRegion = np.linspace(lineWave[0], lineWave[-1], 100)
            resampleContinuum = m_cont * resampleRegion + n_cont
            resampleCurve = gauss_curve((resampleRegion, resampleContinuum), *p1_Mean)

            results_dict.update(
                dict(resampleRegion=resampleRegion, resampleCurve=resampleCurve, resampleContinuum=resampleContinuum,
                     lineWave=lineWave, lineFlux=lineFlux,
                     lineCont=lineCont))

        return results_dict

    def gui_line_fit(self, wave, flux, lines_df):

        return

    def batch_line_fit(self, wave, flux, lines_df):

        # Get lines data and regions
        lineLabels = lines_df.index.values
        waveLimitsMatrix = lines_df.loc[:, 'Wave1':'Wave6'].values

        # Treat the data
        idcsLines, idcsCont = line_regions_matrix(wave, waveLimitsMatrix)

        # Loop through the lines and perform the fits
        outputlinesLog = pd.DataFrame(columns=self.lineLogHeaders)
        for i in np.arange(lineLabels.size):

            line_i = lineLabels[i]
            print('-- Measuring line: {}'.format(lineLabels[i]))

            # Perform the fit
            lineFit_i = self.lineFit(wave, flux, idcsLines[:, i], idcsCont[:, i], plot_data=True)

            # Check if line is included in database
            if line_i in self.linesDb.index:
                outputlinesLog.loc[line_i, 'Ion'] = self.linesDb.loc[line_i, 'ion']
                outputlinesLog.loc[line_i, 'lambda_theo'] = self.linesDb.loc[line_i, 'wavelength']
                outputlinesLog.loc[line_i, 'emis_type'] = self.linesDb.loc[line_i, 'emis_type']
                outputlinesLog.loc[line_i, 'pynebCode'] = self.linesDb.loc[line_i, 'pyneb_code']

            # # Plot the spectrum
            # fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            # ax.plot(wave, flux, color='black', label='Object spectrum')
            # ax.plot(lineFit_i['resampleRegion'], lineFit_i['resampleCurve'], label='Gaussian')
            # ax.plot(lineFit_i['lineWave'], lineFit_i['lineCont'], label='Line continuum')
            # ax.update({'xlabel': r'Wavelength $(\AA)$', 'ylabel': 'Flux (normalised)'})
            # ax.legend()
            # plt.show()

            # Saving the data to the data frame
            outputlinesLog.loc[line_i, 'obs_wavelength'] = lineFit_i['p1_Mean'][1]
            outputlinesLog.loc[:, 'w1':'w6'] = waveLimitsMatrix[i]
            outputlinesLog.loc[line_i, 'obs_flux'], outputlinesLog.loc[line_i, 'obs_fluxErr'] = lineFit_i['intgInt'], lineFit_i['intgStd']
            outputlinesLog.loc[line_i, 'flux_gauss'], outputlinesLog.loc[line_i, 'flux_gauss_er'] = lineFit_i['gaussInt'], lineFit_i['gaussStd']
            outputlinesLog.loc[line_i, 'A'], outputlinesLog.loc[line_i, 'mu'], outputlinesLog.loc[line_i, 'sigma'] = lineFit_i['p1_Mean']
            outputlinesLog.loc[line_i, 'A_std'], outputlinesLog.loc[line_i, 'mu_std'], outputlinesLog.loc[line_i, 'sigma_std'] = lineFit_i['p1_Std']

        return outputlinesLog
