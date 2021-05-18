import numpy as np
import pyneb as pn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from sys import exit
from kapteyn            import kmpfit

class EmissivitySurfaceFitter():

    def __init__(self):

        self.emis_eq_dict= {'S2_6717A'  : self.emisEquation_TeDe,
                            'S2_6731A'  : self.emisEquation_TeDe,
                            'S3_6312A'  : self.emisEquation_Te,
                            'S3_9069A'  : self.emisEquation_Te,
                            'S3_9531A'  : self.emisEquation_Te,
                            'Ar4_4740A' : self.emisEquation_Te,
                            'Ar3_7136A' : self.emisEquation_Te,
                            'Ar3_7751A' : self.emisEquation_Te,
                            'O3_4363A'  : self.emisEquation_Te,
                            'O3_4959A'  : self.emisEquation_Te,
                            'O3_5007A'  : self.emisEquation_Te,
                            'O2_3726A'  : self.emisEquation_TeDe,
                            'O2_3729A'  : self.emisEquation_TeDe,
                            'O2_7319A'  : self.emisEquation_TeDe,
                            'O2_7330A'  : self.emisEquation_TeDe,
                            'N2_6548A'  : self.emisEquation_Te,
                            'N2_6584A'  : self.emisEquation_Te,
                            'H1_4102A'  : self.emisEquation_HI,
                            'H1_4340A'  : self.emisEquation_HI,
                            'H1_6563A'  : self.emisEquation_HI,
                            'He1_4471A' : self.emisEquation_HeI,
                            'He1_5876A' : self.emisEquation_HeI,
                            'He1_6678A' : self.emisEquation_HeI,
                            'He1_7065A' : self.emisEquation_HeI,
                            'He2_4686A' : self.emisEquation_HeII}

        self.high_temp_ions = ['He1', 'He2', 'O3', 'Ar4'] # TODO this should be read from a file

        self.load_ftau_coeffs()

        return

    def load_ftau_coeffs(self):

        paths_dict = {'Helium_OpticalDepth':'/home/vital/PycharmProjects/dazer/bin/lib/Astro_Libraries/literature_data/Benjamin1999_OpticalDepthFunctionCoefficients.txt'}

        opticalDepthCoeffs_df = pd.read_csv(paths_dict['Helium_OpticalDepth'], delim_whitespace=True, header=0)

        self.opticalDepthCoeffs = {}
        for column in opticalDepthCoeffs_df.columns:
            self.opticalDepthCoeffs[column] = opticalDepthCoeffs_df[column].values

        return

    def optical_depth_function(self, tau, temp, den, a, b, c, d):
        return 1 + tau/2.0 * (a + (b + c * den + d * den * den)*temp/10000.0)

    def genEmisGrid(self, linesList, teRange, neRange):

        # Hbeta data
        H1 = pn.RecAtom('H', 1)
        HBeta = H1.getEmissivity(teRange, neRange, wave=4861, product=False)

        # Generate the emissivity grids for all the ions
        emis_dict = {'HBeta': HBeta}

        # Loop through the lines list:
        for i in range(len(linesList)):

            element, ionization, wave = linesList[i][0][:-1], linesList[i][0][-1], linesList[i][1]
            line_label = '{}{}_{}A'.format(element, ionization, wave)
            if element in ['H', 'He']:
                ion = pn.RecAtom(element, ionization)
                if element == 'H':
                    emis_dict[line_label] = ion.getEmissivity(teRange, neRange, wave=wave, product=False) / HBeta
                if element == 'He':
                    emis_dict[line_label] = ion.getEmissivity(teRange, neRange, wave=wave, product=False) / HBeta

            else:
                ion = pn.Atom(element, ionization)
                emis_dict[line_label] = np.log10(ion.getEmissivity(teRange, neRange, wave=wave, product=False) / HBeta)

        return emis_dict

    def emisEquation_Te(self, xy_space, a, b, c):
        temp_range, den_range = xy_space
        return a + b / temp_range + c * np.log10(temp_range)

    def emisEquation_TeDe(self, xy_space, a, b, c, d, e):
        temp_range, den_range = xy_space
        return a + b / temp_range + c * np.log10(temp_range) + np.log10(1 + e * den_range)

    def emisEquation_HI(self, xy_space, a, b, c):
        temp_range, den_range = xy_space
        return a + b * np.log(temp_range) + c * np.log10(temp_range) * np.log10(temp_range)

    def emisEquation_HeI(self, xy_space, a, b, c, d):
        temp_range, den_range = xy_space
        return (a + b * den_range) * np.log10(temp_range/10000.0) - np.log10(c + d*den_range)

    def residuals(self, d, p):
        temp_range, den_range, pyneb_grid = d
        a,b,c = p
        return self.emisEquation_HeI((temp_range, den_range), a,b,c) - pyneb_grid

    def emisEquation_HeI_log(self, xy_space, a, b, c):
        temp_range, den_range = xy_space
        return np.log10(a + b * den_range) + (c + b * den_range) * np.log10(temp_range/10000.0)

    def emisEquation_HeII(self, xy_space, a, b):
        temp_range, den_range = xy_space
        return a * np.power(temp_range, b)

    def fitEmis(self, func_emis, xy_space, line_emis, p0 = None):
        p1, p1_cov = curve_fit(func_emis, xy_space, line_emis, p0)
        return p1, p1_cov

    def emisTeNe_3DPlot(self, coeffs, func_emis, te_ne_grid, emis_grid, line_label):

        # Plot the grid points
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the grid points
        ax.scatter(te_ne_grid[0], te_ne_grid[1], emis_grid, color='r', alpha=0.5)

        # Generate fitted surface points
        matrix_edge = int(np.sqrt(te_ne_grid[0].shape[0]))
        surface_points = func_emis(te_ne_grid, *coeffs).reshape((matrix_edge, matrix_edge))

        surface_epm = (0.745-5.1e-5*te_ne_grid[1]) * np.power(te_ne_grid[0]/10000.0, 0.226-0.0011*te_ne_grid[1])
        surface_aver = (0.754) * np.power(te_ne_grid[0]/10000.0, 0.212-0.00051*te_ne_grid[1])
        ax.scatter(te_ne_grid[0], te_ne_grid[1], surface_epm, color='blue', alpha=0.5)
        ax.scatter(te_ne_grid[0], te_ne_grid[1], surface_aver, color='green', alpha=0.5)

        #Plot surface
        ax.plot_surface(te_ne_grid[0].reshape((matrix_edge, matrix_edge)), te_ne_grid[1].reshape((matrix_edge, matrix_edge)), surface_points, rstride=1, cstride=1, color='g', alpha=0.5)

        # Add labels
        ax.set_xlabel('Temperature $(K)$', fontsize=15)
        ax.set_ylabel('Density ($cm^{-3}$)', fontsize=15)
        title_label = line_label
        ax.set_title(title_label, fontsize=15)

        # Display graph
        plt.show()

        return

    def emisTeNe_2DPlot(self, coeffs, func_emis, te_ne_grid, emis_grid, line_label):

        print 'estos son', coeffs

        # Generate figure
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Generate fitted surface points
        matrix_edge = int(np.sqrt(te_ne_grid[0].shape[0]))
        surface_points = func_emis(te_ne_grid, *coeffs)

        # Plot plane
        plt.imshow(surface_points.reshape((matrix_edge, matrix_edge)), aspect=0.03,
                   extent=(te_ne_grid[1].min(), te_ne_grid[1].max(), te_ne_grid[0].min(), te_ne_grid[0].max()))

        # Compare pyneb values with values from fitting
        percentage_difference = (1 - surface_points/emis_grid) * 100

        # Points with error below 1.0 are transparent:
        idx_interest = percentage_difference < 1.0
        plt.scatter(te_ne_grid[1][idx_interest], te_ne_grid[0][idx_interest], c="None", edgecolors='black', linewidths=0.35, label='Error below 1%')

        if idx_interest.sum() < emis_grid.size:

            # Plot grid points
            plt.scatter(te_ne_grid[1][~idx_interest], te_ne_grid[0][~idx_interest], c=percentage_difference[~idx_interest],
                        edgecolors='black', linewidths=0.1, cmap=cm.OrRd , label='Error above 1%')

            # Color bar
            cbar = f.colorbar()
            cbar.ax.set_ylabel('% difference', rotation=270, fontsize=15)

        # Add labels
        ax.set_ylabel('Temperature $(K)$', fontsize=15)
        ax.set_xlabel('Density ($cm^{-3}$)', fontsize=15)
        title_label = line_label
        ax.set_title(title_label, fontsize=15)

        plt.ylim(te_ne_grid[0].min(), te_ne_grid[0].max())
        plt.xlim(te_ne_grid[1].min(), te_ne_grid[1].max())

        # Display the plot
        plt.legend()
        plt.show()
        plt.cla()

        # Save the plot
        # output_address = '{}{}'.format('/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/input_data/2Demis_',line_label)
        # fig.savefig(output_address, bbox_inches='tight', pad_inches=0.2)
        # plt.cla()

        return

if __name__ == "__main__":

    print 2**(3.2 - 1.5)

    print (2**3.2 / 2**1.5)

    # efitter = EmissivitySurfaceFitter()
    #
    # efitter.load_ftau_coeffs()
    #
    # tau_true = 0.234
    # Te_true = 12550.0
    # ne_true = 125.0
    #
    # for line_label in efitter.opticalDepthCoeffs:
    #     ftau_coefs = efitter.opticalDepthCoeffs[line_label]
    #
    #     print line_label, efitter.optical_depth_function(tau_true, Te_true, ne_true, *ftau_coefs), ftau_coefs


    #
    # Hbeta = H1.getEmissivity(tem=T_true, den=ne_true, wave=4861)
    # He1_4471A = He1.getEmissivity(tem=T_true, den=ne_true, wave=4471)
    #
    # #print Hbeta
    # print He1_4471A
    # print Hbeta
    #
    # print He1_4471A/Hbeta
    # print (2.0301+1.5e-5*ne_true) * ((T_true/10000.0)**(0.1463-0.0005*ne_true))
    #
    #
    #
    # print (0.745) * (T_true/10000.0)**(0.226-0.0011*ne_true)
    # print 0.754 * np.power(10000.0/10000.0, 0.212 - 0.0051 * ne_true)
    #
    #
    #
    # efitter = EmissivitySurfaceFitter()
    #
    # # Lines list
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
    # X,Y = np.meshgrid(Te_range, ne_array)
    # XX = X.flatten()
    # YY = Y.flatten()
    #
    # # Generate emissivity grid
    # emis_dict = efitter.genEmisGrid(lines_list, teRange=XX, neRange=YY)
    #
    # # Loop through the lines list:
    # coefs_dict ={}
    # for line_label in ['He1_5876A']: #efitter.emis_eq_dict.keys():
    #
    #     # Fit emissivity plane
    #     line_func = efitter.emis_eq_dict[line_label]
    #     p1, cov1 = efitter.fitEmis(line_func, (XX, YY), emis_dict[line_label], p0=(0.745, 0.226, 0.0011))
    #     coefs_dict[line_label] = p1
    #
    #     fitobj = kmpfit.Fitter(residuals=efitter.residuals, data=(XX, YY, emis_dict[line_label]))
    #     fitobj.fit(params0=(0.745, 0.226, 0.0011))
    #     print p1
    #     print fitobj.params
    #     print line_func((T_true, ne_true), *fitobj.params)
    #     exit()
    #
    #     # 3D plot
    #     #efitter.emisTeNe_3DPlot(p1, line_func, (XX, YY), emis_dict[line_label], line_label)
    #
    #     # 2D plot
    #     efitter.emisTeNe_2DPlot(p1, line_func, (XX, YY), emis_dict[line_label], line_label)
    #
    #



# import numpy as np
# import pyneb as pn
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.optimize import curve_fit
#
# class EmissivitySurfaceFitter():
#
#     def __init__(self):
#
#         self.emis_eq_dict= {'S2_6717A'  : self.emisEquation_TeDe,
#                             'S2_6731A'  : self.emisEquation_TeDe,
#                             'S3_6312A'  : self.emisEquation_Te,
#                             'S3_9069A'  : self.emisEquation_Te,
#                             'S3_9531A'  : self.emisEquation_Te,
#                             'Ar4_4740A' : self.emisEquation_Te,
#                             'Ar3_7136A' : self.emisEquation_Te,
#                             'Ar3_7751A' : self.emisEquation_Te,
#                             'O3_4363A'  : self.emisEquation_Te,
#                             'O3_4959A'  : self.emisEquation_Te,
#                             'O3_5007A'  : self.emisEquation_Te,
#                             'O2_7319A'  : self.emisEquation_TeDe,
#                             'O2_7330A'  : self.emisEquation_TeDe,
#                             'N2_6548A'  : self.emisEquation_Te,
#                             'N2_6584A'  : self.emisEquation_Te}
#
#         return
#
#     def genEmisGrid(self, linesList, teRange, neRange):
#
#         # Hbeta data
#         H1 = pn.RecAtom('H', 1)
#         HBeta = H1.getEmissivity(teRange, neRange, wave=4861, product=False)
#
#         # Generate the emissivity grids for all the ions
#         emis_dict = {'HBeta': HBeta}
#
#         # Loop through the lines list:
#         for i in range(len(linesList)):
#
#             element, ionization, wave = linesList[i][0][:-1], linesList[i][0][-1], linesList[i][1]
#             line_label = '{}{}_{}A'.format(element, ionization, wave)
#
#             ion = pn.Atom(element, ionization)
#             emis_dict[line_label] = np.log10(ion.getEmissivity(teRange, neRange, wave=wave, product=False) / HBeta)
#
#         return emis_dict
#
#     def emisEquation_Te(self, xy_space, a, b, c):
#         temp_range, den_range = xy_space
#         return a + b / temp_range + c * np.log10(temp_range)
#
#     def emisEquation_TeDe(self, xy_space, a, b, c, d, e):
#         temp_range, den_range = xy_space
#         return a + b / temp_range + c * np.log10(temp_range) + np.log10(1 + e * den_range)
#
#     def emisEquation_TeDe_O2(self, xy_space, a, b, c, d, e, f):
#         temp_range, den_range = xy_space
#         return a + b / temp_range + c * np.log10(temp_range) + e * den_range * (1 - f * den_range)
#
#     def fitEmis(self, func_emis, xy_space, line_emis, p0 = None):
#         p1, p1_cov = curve_fit(func_emis, xy_space, line_emis, p0)
#         return p1, p1_cov
#
#     def emisTeNe_3DPlot(self, coeffs, func_emis, te_ne_grid, emis_grid, line_label):
#
#         # Plot the grid points
#         fig = plt.figure()
#         ax = fig.add_subplot(111, projection='3d')
#
#         # Plot the grid points
#         ax.scatter(te_ne_grid[0], te_ne_grid[1], emis_grid, color='r', alpha=0.5)
#
#         # Generate fitted surface points
#         matrix_edge = int(np.sqrt(te_ne_grid[0].shape[0]))
#         surface_points = func_emis(te_ne_grid, *coeffs).reshape((matrix_edge, matrix_edge))
#
#         #Plot surface
#         ax.plot_surface(te_ne_grid[0].reshape((matrix_edge, matrix_edge)), te_ne_grid[1].reshape((matrix_edge, matrix_edge)), surface_points, rstride=1, cstride=1, color='g', alpha=0.5)
#
#         # Add labels
#         ax.set_xlabel('Temperature $(K)$', fontsize=15)
#         ax.set_ylabel('Density ($cm^{-3}$)', fontsize=15)
#         title_label = line_label
#         ax.set_title(title_label, fontsize=15)
#
#         # Display graph
#         plt.show()
#
#         return
#
#     def emisTeNe_2DPlot(self, coeffs, func_emis, te_ne_grid, emis_grid, line_label):
#
#         # Generate figure
#         fig = plt.figure()
#         ax = fig.add_subplot(111)
#
#         # Generate fitted surface points
#         matrix_edge = int(np.sqrt(te_ne_grid[0].shape[0]))
#         surface_points = func_emis(te_ne_grid, *coeffs)
#
#         # Plot plane
#         plt.imshow(surface_points.reshape((matrix_edge, matrix_edge)), aspect=0.03,
#                    extent=(te_ne_grid[1].min(), te_ne_grid[1].max(), te_ne_grid[0].min(), te_ne_grid[0].max()))
#
#         # Compare pyneb values with values from fitting
#         percentage_difference = (1 - surface_points/emis_grid) * 100
#
#         # Points with error below 1.0 are transparent:
#         idx_interest = percentage_difference < 1.0
#         plt.scatter(te_ne_grid[1][idx_interest], te_ne_grid[0][idx_interest], c="None", edgecolors='black', linewidths=0.35, label='Error below 1%')
#
#         if idx_interest.sum() < emis_grid.size:
#
#             # Plot grid points
#             plt.scatter(te_ne_grid[1][~idx_interest], te_ne_grid[0][~idx_interest], c=percentage_difference[~idx_interest],
#                         edgecolors='black', linewidths=0.1, cmap=cm.OrRd , label='Error above 1%')
#
#             # Color bar
#             cbar = plt.colorbar()
#             cbar.ax.set_ylabel('% difference', rotation=270, fontsize=15)
#
#         # Add labels
#         ax.set_ylabel('Temperature $(K)$', fontsize=15)
#         ax.set_xlabel('Density ($cm^{-3}$)', fontsize=15)
#         title_label = line_label
#         ax.set_title(title_label, fontsize=15)
#
#         plt.ylim(te_ne_grid[0].min(), te_ne_grid[0].max())
#         plt.xlim(te_ne_grid[1].min(), te_ne_grid[1].max())
#         plt.legend()
#         plt.show()
#         # output_address = '{}{}'.format('/home/vital/PycharmProjects/thesis_pipeline/spectrum_fitting/testing_output/input_data/2Demis_',line_label)
#         # fig.savefig(output_address, bbox_inches='tight', pad_inches=0.2)
#         # plt.cla()
#
#         return
#
# if __name__ == "__main__":
#
#     efitter = EmissivitySurfaceFitter()
#
#     # Lines list
#     lines_list = [('S3', 9069),
#                   ('S3', 9531),
#                   ('S3', 6312),
#                   ('S2', 6717),
#                   ('S2', 6731),
#                   ('Ar4', 4740),
#                   ('Ar3', 7136),
#                   ('Ar3', 7751),
#                   ('O3', 4363),
#                   ('O3', 4959),
#                   ('O3', 5007),
#                   ('O2', 7319),
#                   ('O2', 7330),
#                   ('N2', 6548),
#                   ('N2', 6584)]
#
#     # Range of temperatures and densities
#     Te_range = np.linspace(5000, 25000, 20)
#     ne_array = np.linspace(1, 500, 20)
#     X,Y = np.meshgrid(Te_range, ne_array)
#     XX = X.flatten()
#     YY = Y.flatten()
#
#     # Generate emissivity grid
#     emis_dict = efitter.genEmisGrid(lines_list, teRange=XX, neRange=YY)
#
#     # Loop through the lines list:
#     coefs_dict ={}
#     for line_label in ['O2_7319A']:
#
#         # Fit emissivity plane
#         line_func = efitter.emis_eq_dict[line_label]
#         p1, cov1 = efitter.fitEmis(line_func, (XX, YY), emis_dict[line_label])
#         coefs_dict[line_label] = p1
#
#         # 3D plot
#         #efitter.emisTeNe_3DPlot(p1, line_func, (XX, YY), emis_dict[line_label], line_label)
#
#         # 2D plot
#         efitter.emisTeNe_2DPlot(p1, line_func, (XX, YY), emis_dict[line_label], line_label)



# import numpy as np
# import matplotlib.pylab as plt
#
# x = np.arange(10)
# y = np.arange(10)
#
# alphas = np.linspace(0.1, 1, 10)
# rgba_colors = np.zeros((10,4))
# print rgba_colors
# # for red the first column needs to be one
# rgba_colors[:,0] = 1.0
# print
# print rgba_colors
# # the fourth column needs to be your alphas
# rgba_colors[:, 3] = alphas
# print
# print rgba_colors
# plt.scatter(x, y, color=rgba_colors)
# plt.show()


# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
# import numpy as np
#
#
# fig = plt.figure()
# ax = fig.gca(projection='3d')
#
# # Make data.
# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# print X.shape, Y.shape
# X, Y = np.meshgrid(X, Y)
# print X.shape, Y.shape
# R = np.sqrt(X**2 + Y**2)
# print R.shape
# Z = np.sin(R)
# print Z.shape
#
# # Plot the surface.
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
#
# # Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#
# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)
#
# plt.show()



# import numpy as np
#
# def addf(a,b,c,d,e):
#     return a + b + c + d + e
#
# mylist = np.array([1,2,3,4])
#
# print mylist
#
#
# print np.matrix(mylist)

# import numpy as np
# from collections import OrderedDict
# from scipy.optimize import minimize, curve_fit, leastsq
# from dazer_methods import Dazer
# import pyneb as pn
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# def emisEquation_tempDen(grid_space, a, b, c, d, e):
#     temp_range, den_range = grid_space
#     return a + b / temp_range + c * np.log10(temp_range) + d * den_range * (1 - e * den_range)
#
# def emisEquation_temp(temp_range, p0):
#     return p0[0] + p0[1] / temp_range + p0[2] * np.log10(temp_range)
#
# def fit_emis(temp_range, line_emis, p0 = None):
#     p1, p1_cov = curve_fit(emisEquation_temp, temp_range, line_emis, p0)
#     return p1, p1_cov
#
# def fit_emis_TeNe(grid_space, line_emis, a=1.0, b=1.0, c=1.0, d=1.0, e=1.0):
#     p1, p1_cov = curve_fit(emisEquation_tempDen, grid_space, line_emis, (a, b, c, d, e))
#     return p1, p1_cov
#
# def func(X, a, b, c):
#     x,y = X
#     return np.log(a) + b*np.log(x) + c*np.log(y)
#
#
# # Set atomic data we want to use
# pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
#
# # Atom creation and definition of physical conditions
# H1 = pn.RecAtom('H', 1)
# S2 = pn.Atom('S', 2)
#
# print 'Using atomic data from {}'.format(S2.printSources())
#
# # Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = 4861
# Wave_dict['S3_9069A']   = 9069
# Wave_dict['S3_9531A']   = 9531
#
# # Define physical conditions
# tem_range   = np.linspace(5000, 25000, 20)
# t4_range    = tem_range/10000
# den         = 100
#
# # Flatten the Te and ne arrays
# Te_range = np.linspace(5000, 25000, 20)
# ne_array = np.linspace(1, 500, 20)
# X,Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
# emis_grid_flatten = np.log10(S2.getEmissivity(XX, YY, wave=6717, product=False)/H1.getEmissivity(XX, YY, wave=4861, product=False))
#
# # Emissivities ranges
# Hbeta_emis = H1.getEmissivity(tem=tem_range, den=den, wave=4861)
# S3_9531A_emis = S2.getEmissivity(tem=tem_range, den=den, wave=6717)
# S2_emis_vector_pyneb = np.log10(S3_9531A_emis/Hbeta_emis)
#
# # Fitting characteristics
# p2, cov2 = fit_emis(t4_range, S2_emis_vector_pyneb)
# print p2
# print type(p2)

# p1, cov1 = fit_emis_TeNe((t4_range, ne_array), S2_emis_vector_pyneb)
# print 'coefficients 1', p1 #[ 5.8163162  -0.63361905  0.64329123]
# print 'coefficients 2', p2 #[ 5.8163162  -0.63361905  0.64329123]
#
# # New fitting valuesx
# Vit_Emis = p1[0] + p1[1]/t4_range + p1[2] * np.log10(t4_range)
# Vit_plane = p1[0] + p1[1]/(XX/10000.0) + p1[2] * np.log10(XX/10000.0)
# difference = 1 - (Vit_plane/emis_grid_flatten)
#
# print difference
# print p1[0] + p1[1]/(XX[0]/10000.0) + p1[2] * np.log10(XX[0]/10000.0)
# print p1[0] + p1[1]/t4_range[0] + p1[2] * np.log10(t4_range[0])
# print np.log10(S2.getEmissivity(XX[0], YY[0], wave=6717, product=False)/H1.getEmissivity(XX[0], YY[0], wave=4861, product=False))
#
# # # Surface plot
# fig = plt.figure()
# ax = fig.add_subplot(111)
# plt.imshow(Vit_plane.reshape((20,20)), aspect=0.05, extent=(ne_array.min(), ne_array.max(), Te_range.min(), Te_range.max()))
# plt.scatter(YY, XX, c=difference)
# plt.colorbar()
# plt.show()

# # Plot the grid points
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# # Plot the grid points
# ax.scatter(XX, YY, emis_grid_flatten, color='r', alpha=0.5)
#
# # Plot fit surface
# ax.plot_surface(X, Y, Vit_plane.reshape((20,20)), rstride=1, cstride=1, color='g', alpha=0.5)
#
# # Add labels
# ax.set_xlabel('Temperature $(K)$', fontsize=15)
# ax.set_ylabel('Density ($cm^{-3}$)', fontsize=15)
# ax.set_zlabel(r'Emissivity $\left(log\left(\frac{\epsilon\left(\left[SIII\right]\lambda9531\right)}{\epsilon\left(H\beta\right)}\right)\right)$', fontsize=15)
#
# # Display graph
# plt.show()



# import numpy as np
# from collections import OrderedDict
# from scipy.optimize import minimize, curve_fit, leastsq
# from dazer_methods import Dazer
# import pyneb as pn
#
# def emis_equation(temp_range, a, b, c):
#     return a + b / temp_range + c * np.log10(temp_range)
#
#
# def fit_emis(temp_Range, line_emis, a=1.0, b=1.0, c=1.0):
#     p1, p1_cov = curve_fit(emis_equation, temp_Range, line_emis, (a, b, c))
#     return p1, p1_cov
#
#
# # Set atomic data we want to use
# pn.atomicData.setDataFile('s_iii_coll_HRS12.dat')
#
# # Atom creation and definition of physical conditions
# H1 = pn.RecAtom('H', 1)
# S3 = pn.Atom('S', 3)
#
# print 'Using atomic data from {}'.format(S3.printSources())
#
# # Define lines:
# Wave_dict               = OrderedDict()
# Wave_dict['Hbeta']      = '4_2'
# Wave_dict['S3_9069A']   = 9069
# Wave_dict['S3_9531A']   = 9531
#
# # Define physical conditions
# tem_range   = np.linspace(5000, 25000, 20)
# t4_range    = tem_range/10000
# den         = 100
#
# # Flatten the Te and ne arrays
# Te_range = np.linspace(5000, 25000, 20)
# ne_array = np.linspace(1, 500, 20)
# X,Y = np.meshgrid(Te_range, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
# emis_grid_flatten = np.log10(S3.getEmissivity(XX, YY, wave=9531, product=False)/H1.getEmissivity(XX, YY, wave=4861, product=False))
#
# # Emissivities ranges
# Hbeta_emis = H1.getEmissivity(tem=tem_range, den=den, wave=4861)
# S3_9531A_emis = S3.getEmissivity(tem=tem_range, den=den, wave=9531)
# S3_emis_vector_pyneb  = np.log10(S3_9531A_emis/Hbeta_emis)
#
# # Fitting characteristics
# p1, cov = fit_emis(t4_range, S3_emis_vector_pyneb)
# print p1
# # New fitting values
# Vit_Emis = p1[0] + p1[1]/t4_range + p1[2] * np.log10(t4_range)
#
# # Generate the plot
#
# # Generate dazer object
# dz = Dazer()
#
# # Define figure format
# dz.FigConf()
#
# dz.data_plot(tem_range, Vit_Emis, label='Fit surface')
# dz.data_plot(tem_range, S3_emis_vector_pyneb, label='PyNeb values')
#
# xtitle, ytitle = r'$T_{e}$ $(K)$', r'$log\left(\frac{E_{[SIII]9531}}{E_{H\beta}}\right)$'
# title   = r'Sulfur emissivity comparison: 9531$\AA$ line, $ n_e = $' + str(den)
# dz.FigWording(xtitle, ytitle, title)
#
# # Display figure
# dz.display_fig()





# #------Fitting quadratic plane
#
# import pyneb as pn
# import numpy as np
# from numpy.polynomial import polynomial
# import scipy as sp
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# def polyfit2d(x, y, f, deg):
#     x = np.asarray(x)
#     y = np.asarray(y)
#     f = np.asarray(f)
#     deg = np.asarray(deg)
#     vander = polynomial.polyvander2d(x, y, deg)
#     vander = vander.reshape((-1,vander.shape[-1]))
#     f = f.reshape((vander.shape[0],))
#     c = np.linalg.lstsq(vander, f)[0]
#     return c.reshape(deg+1)
#
# # Declare ions
# H1 = pn.RecAtom('H',1)
# S3 = pn.Atom('S',3)
#
# # Define Te and ne grid
# Te_array = np.linspace(8000, 20000, 20)
# ne_array = np.linspace(1, 500, 20)
#
# # Flatten the Te and ne arrays
# X,Y = np.meshgrid(Te_array, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
#
# # Use PyNeb to compute the emissivity grid
# emis_grid_flatten = np.log10(S3.getEmissivity(XX, YY, wave=9531, product=False)/H1.getEmissivity(XX, YY, wave=4861, product=False))
#
# # Array with Te, ne, and Emissivity values
# data = np.c_[XX, YY, emis_grid_flatten]
#
# # best-fit quadratic curve (2nd-order)
# A = np.c_[np.ones(data.shape[0]), data[:, :2], np.prod(data[:, :2], axis=1), data[:, :2] ** 2]
# C, _, _, _ = sp.linalg.lstsq(A, data[:, 2])
#
# # evaluate it on the Te-ne grid (2nd-order)
# Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape)
#
# # Treat the abundance
# C_poly = polyfit2d(XX, YY, emis_grid_flatten, deg=[2,2])
#
# Z_poly = polynomial.polyval2d(XX, YY, C_poly)
#
# print C.shape, Z.shape
# print C_poly.shape, Z_poly.shape
#
# # Plot the grid points
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# # Plot the grid points
# ax.scatter(XX, YY, emis_grid_flatten, color='r', alpha=0.5)
#
# # Plot fit surface
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='g', alpha=0.5)
# ax.plot_surface(X, Y, Z_poly.reshape((20,20)), rstride=1, cstride=1, alpha=0.5)
#
# # Add labels
# ax.set_xlabel('Temperature $(K)$', fontsize=15)
# ax.set_ylabel('Density ($cm^{-3}$)', fontsize=15)
# ax.set_zlabel(r'Emissivity $\left(log\left(\frac{\epsilon\left(\left[SIII\right]\lambda9531\right)}{\epsilon\left(H\beta\right)}\right)\right)$', fontsize=15)
#
# # Display graph
# plt.show()


# import numpy as np
# import scipy.linalg
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
#
# np.random.seed(12345)
# x = 2 * (np.random.random(500) - 0.5)
# y = 2 * (np.random.random(500) - 0.5)
#
# def f(x, y):
#     return np.exp(-(x + y ** 2))
#
# z = f(x, y)
#
# data = np.c_[x, y, z]
#
# print x.shape, y.shape
# print z.shape
# print data.shape
#
# print 'esti', data[:, :2]
# print 'es', data[:, :2].shape
#
# # regular grid covering the domain of the data
# mn = np.min(data, axis=0)
# mx = np.max(data, axis=0)
# X, Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))
# XX = X.flatten()
# YY = Y.flatten()
#
# # best-fit quadratic curve (2nd-order)
# A = np.c_[np.ones(data.shape[0]), data[:, :2], np.prod(data[:, :2], axis=1), data[:, :2] ** 2]
# C, _, _, _ = scipy.linalg.lstsq(A, z)
#
# # evaluate it on a grid
# Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape)
#
# fig1 =  plt.figure(figsize=(10, 10))
# ax = fig1.gca(projection='3d')
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
# ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
# ax.scatter(data[:,0], data[:,1], z, c='b', s=60)
#
# plt.xlabel('X')
# plt.ylabel('Y')
# ax.set_zlabel('Z')
# ax.axis('equal')
# ax.axis('tight')
#
# plt.show()

# import pyneb as pn
# import numpy as np
# import scipy as sp
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# from itertools import combinations
#
# H1 = pn.RecAtom('H',1)
# S3 = pn.Atom('S',3)
#
# Te_array = np.linspace(8000, 20000, 40)
# ne_array = np.linspace(1, 500, 40)
#
# X,Y = np.meshgrid(Te_array, ne_array)
# XX = X.flatten()
# YY = Y.flatten()
#
# Emis_S3 = S3.getEmissivity(Te_array, ne_array, wave=9531)
# Emis_H1 = H1.getEmissivity(Te_array, ne_array, wave=4861)
# emis_r  = np.log10(Emis_S3/Emis_H1)
# EMIS_R  = np.log10(S3.getEmissivity(XX, YY, wave=9531, product=False)/H1.getEmissivity(XX, YY, wave=4861, product=False))
#
# # EMIS_R  = emis_r.flatten()
# # print 'seguro', XX.shape[0]
# # for i in range(XX.shape[0]):
# #     print XX[i], YY[i], EMIS_R[i], np.log10(S3.getEmissivity(XX, YY, wave=9531, product=False)/H1.getEmissivity(XX, YY, wave=4861, product=False))
#
# data = np.c_[XX, YY, EMIS_R]
#
#
# dim = data.shape[1]
# A = np.concatenate((data**2, np.array([np.prod(data[:, k], axis=1) for k in combinations(range(dim), dim-1)]).transpose(), data, np.ones((data.shape[0], 1))), axis=1)
# C, _, _, _ = sp.linalg.lstsq(A, data[:, 2])
# print C
# Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape)

# # best-fit quadratic curve (2nd-order)
# A = np.c_[np.ones(data.shape[0]), data[:, :2], np.prod(data[:, :2], axis=1), data[:, :2] ** 2]
# C, _, _, _ = sp.linalg.lstsq(A, data[:, 2])
#
# # evaluate it on a grid (2nd-order)
# Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape)




# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for i in range(len(Te_array)):
#     Te_vector = Te_array[i] * np.ones(Te_array.shape[0])
#     Emis_S3_i = emis_r[i,:]
#     ax.scatter(Te_vector, ne_array, Emis_S3_i)
#
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
# ax.set_xlabel('Temp')
# ax.set_ylabel('Den')
# ax.set_zlabel('Emis')
# plt.show()




# print X.shape
# print XX.shape
# A = np.c_[np.ones(emis_r.shape[0]), emis_r[:,:2], np.prod(emis_r[:,:2], axis=1), emis_r[:,:2]**2]
# print A.shape
# C,_,_,_ = sp.linalg.lstsq(A, emis_r[:,2])
# Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)


# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# import numpy as np
#
# # Fixing random state for reproducibility
# np.random.seed(19680801)
#
#
# def randrange(n, vmin, vmax):
#     '''
#     Helper function to make an array of random numbers having shape (n, )
#     with each number distributed Uniform(vmin, vmax).
#     '''
#     return (vmax - vmin)*np.random.rand(n) + vmin
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# n = 100
#
# # For each set of style and range settings, plot n random points in the box
# # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#     xs = randrange(n, 23, 32)
#     ys = randrange(n, 0, 100)
#     zs = randrange(n, zlow, zhigh)
#     print 'xs', xs.shape, 'ys', ys.shape,  'zs', zs.shape
#     ax.scatter(xs, ys, zs, c=c, marker=m)
#
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
#
# plt.show()



# Te, ne      = 13000, 50
# cHbeta      = 0.1
# f_lambda    = - 0.625
# Hbeta_emis  = H1.getEmissivity(Te, ne, wave=4861)
# ion_emis    = S3.getEmissivity(Te,ne ,wave=9531)
#
# print S3.getEmissivity(Te,ne,wave=9531)/S3.getEmissivity(Te,ne,wave=9069)
#
# S3_abund_12log = 6.36
#
# S3_abund = 10**(S3_abund_12log-12)
#
# F_S3_r      = S3_abund * (ion_emis/Hbeta_emis) * (10**(-1*cHbeta*f_lambda))
# F_S3_log    = np.log10(S3_abund) + np.log10((ion_emis/Hbeta_emis)) - cHbeta * f_lambda
# F_S3_log12  = S3_abund_12log + np.log10((ion_emis/Hbeta_emis)) - cHbeta * f_lambda - 12
#
# print F_S3_r
# print 10**F_S3_log
# print 10**F_S3_log12
#
#
# F_S3_obs = 0.591


# import seaborn as sns
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
#
#
# Te = np.linspace(8000, 20000, 250)
# ne = np.linspace(1, 500, 250)
#
# Emis_9531 = H1.getEmissivity(Te, ne, wave=4861)
#
# print Te.shape
# print ne.shape
# print Emis_9531.shape
#
# print Emis_9531
#
# # Make the plot
# # fig = plt.figure()
# # ax = fig.gca(projection='3d')
# # ax.plot_trisurf(ne, Te, Emis_9531, cmap=plt.cm.viridis, linewidth=0.2)
# # plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_wireframe(Te, ne, np.log10(Emis_9531), rstride=10, cstride=10)
# plt.show()
#
# print Emis_9531.shape

# library & dataset
#
# Te = np.linspace(8000, 20000, 250)
# ne = np.linspace(1, 500, 250)
#
# Emis_9531 = S3.getEmissivity(Te, ne, wave=9531)
#
# import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1 import make_axes_locatable
#
# ax = plt.subplot(111)
# im = ax.imshow(Emis_9531)
#
# # create an axes on the right side of ax. The width of cax will be 5%
# # of ax and the padding between cax and ax will be fixed at 0.05 inch.
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.05)
#
# plt.colorbar(im, cax=cax)
#
# plt.show()