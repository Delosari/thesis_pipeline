import numpy as np
import pyneb as pn
import matplotlib.pyplot as plt
from lib.Astro_Libraries.spectrum_fitting.plot_tools import MCMC_printer
from lib.Astro_Libraries.spectrum_fitting.gasEmission_functions import EmissivitySurfaceFitter
from lib.Astro_Libraries.spectrum_fitting.extinction_tools import ReddeningLaws
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams

def emissivitySurfaceFit_3D(line_label, emisGrid, te_ne_grid):
    # Plot format
    size_dict = {'figure.figsize': (20, 14), 'axes.titlesize': 16, 'axes.labelsize': 16, 'legend.fontsize': 18}
    rcParams.update(size_dict)

    # Plot the grid points
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Generate fitted surface points
    matrix_edge = int(np.sqrt(te_ne_grid[0].shape[0]))

    # Plotting pyneb emissivities
    x_values, y_values = te_ne_grid[0].reshape((matrix_edge, matrix_edge)), te_ne_grid[1].reshape((matrix_edge, matrix_edge))
    ax.plot_surface(x_values, y_values, emisGrid.reshape((matrix_edge, matrix_edge)), color='g', alpha=0.5)

    # Add labels
    ax.update({'ylabel': 'Density ($cm^{-3}$)', 'xlabel': 'Temperature $(K)$', 'title': line_label})

    return


#Functions to fit surfaces
emisPlanes = EmissivitySurfaceFitter()
ptPrinter = MCMC_printer()

# Pyneb atoms
S2 = pn.Atom('S',2)
S3 = pn.Atom('S',3)
O3 = pn.Atom('O',3)

#Temperature and density grid
Te_range = np.linspace(7500, 25000, 20)
ne_array = np.linspace(0, 500, 20)
ne_array[0] = 1.0
X, Y = np.meshgrid(Te_range, ne_array)
XX = X.flatten()
YY = Y.flatten()

# Ratio grids
RSII_grid = S2.getEmissivity(XX, YY, wave=6717, product=False) / S2.getEmissivity(XX, YY, wave=6731, product=False)
RSIII_grid = S3.getEmissivity(XX, YY, wave=6312, product=False) / (S3.getEmissivity(XX, YY, wave=9069, product=False) + S3.getEmissivity(XX, YY, wave=9531, product=False))
ROIII_grid = O3.getEmissivity(XX, YY, wave=4363, product=False) / (O3.getEmissivity(XX, YY, wave=4959, product=False) + O3.getEmissivity(XX, YY, wave=5007, product=False))

grid_dict = {'ROIII':ROIII_grid, 'RSII':RSII_grid, 'RSIII':RSIII_grid, 'ROIII':ROIII_grid}
funcDict = {'RSIII':emisPlanes.emisEquation_Te, 'ROIII':emisPlanes.emisEquation_Te, 'RSII':emisPlanes.emisEquation_HeI_fit}
ratios_lists = ['ROIII', 'RSIII']

emisCoeffs = {}
for i in range(len(ratios_lists)):

    # Get components
    ratio = ratios_lists[i]
    emisGrid = np.log10(grid_dict[ratios_lists[i]])
    emisFunc = emisPlanes.emisEquation_Te

    # Perform fit
    p1, cov1 = emisPlanes.fitEmis(emisFunc, (XX, YY), emisGrid)
    emisCoeffs[ratio] = p1

    print ratio, p1

    #Generate plot
    ptPrinter.emissivitySurfaceFit_3D(ratio, p1, emisGrid, emisFunc, (XX, YY))
    plt.show()


#Plot surface
# emissivitySurfaceFit_3D('ROIII', ROIII_grid, (XX, YY))
# plt.show()

# coeffsHeI5876_epmArranged = np.array([-0.226, 0.0011, 0.745, -5.1e-5])
# coeffsHeI5876_epmArranged = np.array([-0.226, 0.0011, 0.745, -5.1e-5])
#
# pt.emissivitySurfaceFit_2D(line_label, coeffsHeI5876_epmArranged, emisGrid_i, emisHeI5876_invNew, (XX, YY))
# pt.emissivitySurfaceFit_3D(line_label, coeffsHeI5876_epmArranged, emisGrid_i, emisHeI5876_invNew, (XX, YY))
#
# plt.show()