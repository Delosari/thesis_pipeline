import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
from article3_material.line_measuring import LineMesurer, line_regions
from scipy.integrate import simps

lm = LineMesurer()

# Generate fake data
np.random.seed(0)
x = np.linspace(-5., 5., 200)
m, n = 0.05, 0.5
yLine = m * x + n
A, mu, sig = 3.0, -0.8, 0.5
y = A * np.exp(-0.5 * (x - mu)**2 / sig**2)
y += np.random.normal(0., 0.2, x.shape)
# y += yLine

waves_lim = np.array([-4.4, -3.0, -2, 0.5, 2.0, 3.0])
idcs_line, idcs_cont = line_regions(x, waves_lim)

results_dict = lm.lineFit(x, y, idcs_line, idcs_cont, plot_data=True)

print results_dict['p1_Mean'],results_dict['intgInt'],results_dict['gaussInt']
print simps(results_dict['resampleCurve'], results_dict['resampleRegion']), np.trapz(results_dict['resampleCurve'], results_dict['resampleRegion']), '//n'

results_dict2 = lm.lineFit(x, y + yLine, idcs_line, idcs_cont, plot_data=True)

print results_dict2['p1_Mean'],results_dict2['intgInt'],results_dict2['gaussInt']
print simps(results_dict2['resampleCurve'], results_dict2['resampleRegion']), np.trapz(results_dict2['resampleCurve'], results_dict2['resampleRegion']), '//n'

# Fit the data using a Gaussian
g_init = models.Gaussian1D(amplitude=1., mean=0, stddev=1.)
fit_g = fitting.LevMarLSQFitter()
g = fit_g(g_init, x, y)

# Plot the data with the best-fit model
plt.figure(figsize=(8,5))
plt.plot(x, y, 'ko')
plt.plot(x, yLine, label='Linear')
plt.plot(x, g(x), label='Gaussian')
plt.plot(results_dict['resampleRegion'], results_dict['resampleCurve'], label='my Gaussian')
plt.plot(results_dict2['resampleRegion'], results_dict2['resampleCurve'], label='my Gaussian + cont')

plt.xlabel('Position')
plt.ylabel('Flux')
plt.legend(loc=2)
plt.show()