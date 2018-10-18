import numpy as np
from dazer_methods import Dazer
from lib.Astro_Libraries.spectrum_fitting.inferenceModel import SpectraSynthesizer

#Generate dazer object
dz = Dazer()
specS = SpectraSynthesizer()

#Define plot frame and colors
size_dict = {'axes.labelsize':28, 'legend.fontsize':24, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':24, 'ytick.labelsize':24}
dz.FigConf(plotSize = size_dict)

Te = 10000.0
wave = np.arange(600, 10000, 1)
HeII_HII = 0.1
HeIII_HII = 0.001

H_He_frac = 1 + HeII_HII * 4 + HeIII_HII * 4

# Bound bound continuum
gamma_2q = specS.twoPhotonGammaCont(wave, Te)

# Free-Free continuum
gamma_ff = H_He_frac * specS.freefreeGammaCont(wave, Te, Z_ion=1.0)

# Get the wavelength range in ryddbergs for the Ercolano grids
wave_ryd = (specS.nebConst['h'] * specS.nebConst['c_Angs']) / (specS.nebConst['Ryd2erg'] * wave)

# Free-Bound continuum
gamma_fb_HI = specS.freeboundGammaCont(wave_ryd, Te, specS.HI_fb_dict)
gamma_fb_HeI = specS.freeboundGammaCont(wave_ryd, Te, specS.HeI_fb_dict)
gamma_fb_HeII = specS.freeboundGammaCont(wave_ryd, Te, specS.HeII_fb_dict)
gamma_fb = gamma_fb_HI + HeII_HII * gamma_fb_HeI + HeIII_HII * gamma_fb_HeII

# dz.data_plot(wave, gamma_ff, r'Bremsstrahlung')
# dz.data_plot(wave, gamma_fb, r'Free-Bound')
# dz.data_plot(wave, gamma_2q, r'Two photon continuum')

nebular_components = ['Bremsstrahlung', 'Free-Bound', 'Two photon continuum']
gamma_nu = [gamma_ff, gamma_fb, gamma_2q]
saving_folder = '/home/vital/Dropbox/Astrophysics/Thesis/images/'

for i in range(len(nebular_components)):

    dz.data_plot(wave, gamma_nu[i], r'Two photon continuum')
    dz.Axis.set_yscale('log')
    Title = ''
    y_Title = r'$\gamma_{nu}\left(erg\ cm^{}\ s^{-1}\ Hz^{-1}\right)$'
    x_Title = r'$Wavelength (\AA)$'
    dz.FigWording(x_Title, y_Title, Title)
    # dz.display_fig()
    dz.savefig(saving_folder + nebular_components[i])

