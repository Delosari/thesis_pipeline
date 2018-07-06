# import os
# import numpy as np
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as tt
# import pymc3 as pm
# import matplotlib.pyplot as plt
#
# # Constants
# R_air_true  = 286.986 # J / (kg * K)
#
# # True Values
# P_true      = 101325 # kg * m * s**-2
# T_true      = 15 + 273 # K
# V_true      = 0.01 # m**-3
# m_true      = P_true * V_true / (R_air_true * T_true) #Kg

# # Lab data
# n_obs       = 10
# T_obs       = np.sort(np.random.uniform(low=10, high=50, size=n_obs)) + 273
# P_obs       = (m_true * R_air_true * T_obs) / V_true
# T_sigma     = 1 # K

# image = np.arange(0, 9).reshape((3,3))
# b = np.array([0,1,0])
# c = np.array([0,0,1])
#
# image_colum = image.dot(b)
#
# print image
#
# print image_colum
#
# print image_colum.dot(c)


# density_range = np.linspace(0, 2, 100).reshape((10, 10))
# print density_range

# # Model with all the observational measurements
# with pm.Model() as lab_all_variables:
#
#     # Define priors
#     R_air = pm.Normal('R_air', mu=1000, sd=200)
#
#     # Simulated expectation value
#     T_synth = P_obs * V_true /(R_air * m_true)
#
#     # Declare the model likelihood:
#     Y_obs = pm.Normal('Y_obs', mu=T_synth, sd=T_sigma, observed=T_obs)
#
#     # Run NUTS sampler
#     trace = pm.sample(10000, tune=2000)

# # Model without pressure readings
# with pm.Model() as lab_no_pressure:
#
#     P_air = pm.Normal('P_air', mu=100000, sd=10000, shape=n_obs)
#     R_air = pm.Normal('R_air', mu=1000, sd=200)
#
#     #Simulated expectation value
#     T_synth = P_air * V_true /(R_air * m_true)
#
#     #Declare the model likelihood:
#     Y_obs = pm.Normal('Y_obs', mu=T_synth, sd=T_sigma, observed=T_obs)
#
#     #Run NUTS sampler
#     trace = pm.sample(10000, tune=2000)

# #Outside data
# n_obs       = 10
# T_obs       = np.sort(np.random.uniform(low=15, high=25, size=n_obs)) + 273
# P_obs       = (m_true * R_air_true * T_obs) / V_true
# T_sigma     = 1 # K
#
# print P_obs


# import os
# import numpy as np
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as tt
# import pymc3 as pm
# import matplotlib.pyplot as plt
#
# # Constants
# R_air_true  = 286.986 # J / (kg * K)
#
# #Street measurements
# P_true = 101325  # kg * m * s**-2
# n_obs = 10
# T_obs = np.random.uniform(low=10, high=12, size=n_obs) + 273
# T_sigma = 1 # K
#
# # Model ingredients data:
# axis_length = 10
# X_coords = np.linspace(5, 40, axis_length)
# Y_coords = np.linspace(10, 20, axis_length)
# density_grid = np.linspace(0.5, 2, 100).reshape((axis_length, axis_length))
#
# # Converting to theano variables
# X_coords_t = theano.shared(X_coords)
# Y_coords_t = theano.shared(Y_coords)
# density_grid_t = theano.shared(density_grid)
#
# # Control the sparsity?
# Dirprior = 1./axis_length
#
# # Model using street measurements
# with pm.Model() as outside_temperature:
#
#     # Priors for the air gas constant
#     R_air = pm.Normal('R_air', mu=300, sd=200)
#
#     # Priors for the grid indeces
#     beta1_x = pm.Gamma('beta1_x', alpha=Dirprior, beta=1., shape=axis_length)
#     beta2_y = pm.Gamma('beta2_y', alpha=Dirprior, beta=1., shape=axis_length)
#
#     # Variables for marginalized vectors
#     x_idx_vector = pm.Deterministic('x', beta1_x/tt.sum(beta1_x))
#     y_idx_vector = pm.Deterministic('y', beta2_y/tt.sum(beta2_y))
#
#     # Values for X and Y coordinates (not needed in this example)
#     x = x_idx_vector.dot(X_coords_t)
#     y = y_idx_vector.dot(Y_coords_t)
#
#     # Computing interpolated value from grid
#     grid_column = density_grid_t.dot(x_idx_vector)
#     rho_air = grid_column.dot(y_idx_vector)
#
#     # Simulated expectation value
#     T_synth = P_true / (R_air * rho_air)
#
#     # Declare the model likelihood:
#     Y_obs = pm.Normal('Y_obs', mu=T_synth, sd=T_sigma, observed=T_obs)
#
#     # Run NUTS sampler
#     trace = pm.sample(4000, tune=2000)
#
# # Display summary
# print pm.summary(trace)
#
# # Display trace
# pm.traceplot(trace)
# plt.show()



# #Outside data
# n_obs       = 10
# T_obs       = np.sort(np.random.uniform(low=15, high=25, size=n_obs)) + 273
# P_obs       = (m_true * R_air_true * T_obs) / V_true
# T_sigma     = 1 # K
#
# print P_obs






import os
import numpy as np
os.environ["MKL_THREADING_LAYER"] = "GNU"
import theano
import theano.tensor as tt
import pymc3 as pm
import matplotlib.pyplot as plt

# Constants
R_air_true  = 286.986 # J / (kg * K)

#Street measurements
P_true = 101325  # kg * m * s**-2
n_obs = 10
T_obs = np.random.uniform(low=10, high=12, size=n_obs) + 273
T_sigma = 1 # K

# Model ingredients data:
axis_length = 10
X_coords = np.linspace(5, 40, axis_length)
Y_coords = np.linspace(10, 20, axis_length)
density_grid = np.linspace(0.5, 2, 100).reshape((axis_length, axis_length))

# Converting to theano variables
X_coords_t = theano.shared(X_coords)
Y_coords_t = theano.shared(Y_coords)
density_grid_t = theano.shared(density_grid)

# Model using street measurements
with pm.Model() as outside_temperature:

    # Priors for the air gas constant
    R_air = pm.Normal('R_air', mu=300, sd=100)

    # Priors for the grid indeces
    x_idx = pm.Uniform('x_idx0', lower=0, upper=axis_length)
    y_idx = pm.Uniform('y_idx0', lower=0, upper=axis_length)

    # Use floor operaton to get the closest points in the grid
    x_idx1, y_idx1 = tt.cast(pm.math.floor(x_idx), 'int64'), tt.cast(pm.math.floor(y_idx), 'int64')
    x_idx2, y_idx2 = x_idx1 + 1, y_idx1 + 1

    # Interpolate the values for X and Y coordinates
    x_in = X_coords_t[x_idx1] + (x_idx - x_idx1) * (X_coords_t[x_idx2] - X_coords_t[x_idx1])/(x_idx2 - x_idx1)
    y_in = Y_coords_t[y_idx1] + (y_idx - y_idx1) * (Y_coords_t[y_idx2] - Y_coords_t[y_idx1])/(y_idx2 - y_idx1)

    # Neighbouring points for the grid for X and Y coordinates:
    x1, x2 = X_coords_t[x_idx1], X_coords_t[x_idx2]
    y1, y2 = Y_coords_t[y_idx1], Y_coords_t[y_idx2]
    z11, z12 = density_grid_t[x_idx1, y_idx1], density_grid_t[x_idx1, y_idx2]
    z21, z22 = density_grid_t[x_idx2, y_idx1], density_grid_t[x_idx2, y_idx2]

    #Bilinear interpolation of the grid
    rho_air = (z11 * (x2 - x_in) * (y2 - y_in) +
            z21 * (x_in - x1) * (y2 - y_in) +
            z12 * (x2 - x_in) * (y_in - y1) +
            z22 * (x_in - x1) * (y_in - y1)) / ((x2 - x1) * (y2 - y1))

    # Simulated expectation value
    T_synth = P_true / (R_air * rho_air)

    # Declare the model likelihood:
    Y_obs = pm.Normal('Y_obs', mu=T_synth, sd=T_sigma, observed=T_obs)

    # Run NUTS sampler
    trace = pm.sample(4000, tune=2000)

# Display summary
print pm.summary(trace)

# Display trace
pm.traceplot(trace)
plt.show()










# #Street measurements
# n_obs = 10
# T_obs = np.random.uniform(low=10, high=12, size=n_obs) + 273
# T_sigma = 1 # K
#
# # Model ingredients data:
# X_coords = np.linspace(5, 40, 10)
# Y_coords = np.linspace(10, 20, 10)
# density_grid = np.linspace(0.5, 2, 100).reshape((10, 10))
#
# # # Declare the theano operation for the interpolation:
# # x1, x2, y1, y2, z11, z12, z21, z22, x_in, y_in = tt.dscalars(10)
# #
# # out_bInterp = (z11 * (x2 - x_in) * (y2 - y_in) +
# #                z21 * (x_in - x1) * (y2 - y_in) +
# #                z12 * (x2 - x_in) * (y_in - y1) +
# #                z22 * (x_in - x1) * (y_in - y1)) / ((x2 - x1) * (y2 - y1))
# #
# # bInterp = theano.function(inputs=[x1, x2, y1, y2, z11, z12, z21, z22, x_in, y_in], outputs=out_bInterp)
#
# # Model using street measurements
# with pm.Model() as outside_temperature:
#
#     # Priors for the air gas constant
#     R_air = pm.Normal('R_air', mu=1000, sd=200)
#
#     # Priors for the density grid
#     x = pm.Uniform('x', lower=X_coords[0], upper=X_coords[-1])
#     y = pm.Uniform('y', lower=Y_coords[0], upper=Y_coords[-1])
#
#     # Indexing closest point coordinates
#     x_idx0 = tt.argmin(pm.math.abs_(X_coords - x))
#     y_idx0 = tt.argmin(pm.math.abs_(Y_coords - y))
#
#     # Gettig neightbouring points
#     x1, x2 = X_coords[x_idx0], X_coords[x_idx0 + 1]
#     y1, y2 = Y_coords[y_idx0], Y_coords[y_idx0 + 1]
#     z11, z12 = density_grid[x_idx0, y_idx0], density_grid[x_idx0, y_idx0 + 1]
#     z21, z22 = density_grid[x_idx0 + 1, y_idx0], density_grid[x_idx0 + 1, y_idx0 + 1]
#
#     # Calculating the density from the bilinear interpolation in the grid
#     # rho_air = bInterp(x1, x2, y1, y2, z11, z12, z21, z22, x_in, y_in)
#     rho_air = (z11 * (x2 - x) * (y2 - y) +
#             z21 * (x - x1) * (y2 - y) +
#             z12 * (x2 - x) * (y - y1) +
#             z22 * (x - x1) * (y - y1)) / ((x2 - x1) * (y2 - y1))
#
#     # Simulated expectation value
#     T_synth = P_true / (R_air * rho_air)
#
#     # Declare the model likelihood:
#     Y_obs = pm.Normal('Y_obs', mu=T_synth, sd=T_sigma, observed=T_obs)
#
#     # Run NUTS sampler
#     trace = pm.sample(10000, tune=2000)
#
# # Display summary
# print pm.summary(trace)
#
# # Display trace
# pm.traceplot(trace)
# plt.show()





# temp_array  = np.arange(10, 40, 1) + 273 # K
#
#
# PV = nRT
# PV = (m/M) * R * T
# P = n * (R/M) * T
# m =  PVM/RT
# PV = m * Rgas * T
# m = PV/(Rgas * T)
# P = (m * Rgas * T) / V
# T = (P * V) / (m * Rgas)

# T = P * V/M * Rgas

# print temp_array






# import os
# import warnings
# warnings.filterwarnings("ignore")
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import numpy as np
# import scipy
# import theano.tensor as tt
# from theano import function
# from lib.Astro_Libraries.spectrum_fitting.multi_comp_v2 import bilinear_interpolator_axis
# from bisect import bisect_left
# import pymc3 as pm
# 
# class Bilinear_interp_theano():
# 
#     def __init__(self):
# 
#         self.indexing_bilinear()
# 
#         self.operation_bilinear()
# 
#         return
# 
#     def neighbour_points(self, x0_idx, y0_idx, x_range, y_range, image_matrix):
# 
#         x1, x2 = x_range[x0_idx:x0_idx + 2]
#         y1, y2 = y_range[y0_idx:y0_idx + 2]
# 
#         z11, z12 = image_matrix[y0_idx][x0_idx:x0_idx + 2]
#         z21, z22 = image_matrix[y0_idx + 1][x0_idx:x0_idx + 2]
# 
#         # x1, x2 = x_steps[x0_idx], x_steps[x0_idx+1]
#         # y1, y2 = y_steps[y0_idx], y_steps[y0_idx+1]
#         # z11, z12 = image[x0_idx,y0_idx], image[x0_idx,y0_idx+1]
#         # z21, z22 = image[x0_idx+1,y0_idx], image[x0_idx+1,y0_idx+1]
# 
#         return x1, x2, y1, y2, z11, z12, z21, z22
# 
#     def indexing_bilinear(self):
# 
#         a = tt.dvector()  # declare variable
#         b = tt.dscalar()
#         out = tt.argmin(tt.abs_(a - b))  # build symbolic expression
#         self.tt_index_array = theano.function([a, b], out)  # compile function
# 
#     def operation_bilinear(self):
# 
#         te_1, te_2, ne_1, ne_2, emis_11, emis_12, emis_21, emis_22, x_in, y_in = tt.dscalars(10)
#         out_bInterp = (emis_11 * (te_2 - x_in) * (ne_2 - y_in) +
#                        emis_21 * (x_in - te_1) * (ne_2 - y_in) +
#                        emis_12 * (te_2 - x_in) * (y_in - ne_1) +
#                        emis_22 * (x_in - te_1) * (y_in - ne_1)) / ((te_2 - te_1) * (ne_2 - ne_1))
#         self.tt_interp_array = theano.function(inputs=[te_1, te_2, ne_1, ne_2, emis_11, emis_12, emis_21, emis_22, x_in, y_in], outputs=out_bInterp)
# 
# 
# # Input data
# x_steps = np.array([10.0,10.5,11.0,11.5,12.0])
# y_steps = np.array([4.2,4.4,4.6,4.8,5.0])
# 
# image   = np.array([[1.0,2.0,3.0,4.0,5.0],
#                     [5.0,6.0,7.0,8.0,9.0],
#                     [10.0, 11.0, 12.0, 13.0, 14.0],
#                     [15.0, 16.0, 17.0, 18.0, 19.0],
#                     [20.0, 21.0, 22.0, 23.0, 24.0]])
# 
# image2 = np.arange(1.0, 26.0, 1.0).reshape(5, 5)
# 
# print image2
# 
# x_cord, y_cord = 10.25, 4.3
# 
# #Scipy interpolation
# scipy_interpol = scipy.interpolate.interp2d(x_steps, y_steps, image, kind='linear')
# print 'Scipy interpolate', scipy_interpol(x_cord, y_cord)
# 
# # Declare theano variables
# x_steps_t   = theano.shared(x_steps,'x_steps')
# y_steps_t   = theano.shared(y_steps,'y_steps')
# image_t     = theano.shared(image,'image')
# x_cord_t    = theano.shared(x_cord,'x_cord')
# y_cord_t    = theano.shared(y_cord,'y_cord')
# 
# # Get idx0 coordinates
# a       = tt.dvector()                           # declare variable
# b       = tt.dscalar()
# out     = tt.argmin(tt.abs_(a - b))               # build symbolic expression
# f       = theano.function([a, b], out)          # compile function
# x0_idx  = f(x_steps, x_cord)
# y0_idx  = f(y_steps, y_cord)
# print 'x', x0_idx, x_steps[x0_idx], type(x0_idx)
# print 'y', y0_idx, y_steps[y0_idx], type(y0_idx)
# print 'image[x0, y0]', image[x0_idx, y0_idx]
# print 'interpolate', image_t[tt.cast(tt.floor(x0_idx), 'uint16'), tt.cast(tt.floor(y0_idx), 'uint16')]
# 
# 
# 
# # Nearest neighbour
# x1, x2 = x_steps[x0_idx:x0_idx + 2]
# y1, y2 = y_steps[y0_idx:y0_idx + 2]
# 
# z11, z12 = image[y0_idx][x0_idx:x0_idx + 2]
# z21, z22 = image[y0_idx + 1][x0_idx:x0_idx + 2]
# 
# # x1, x2 = x_steps[x0_idx], x_steps[x0_idx+1]
# # y1, y2 = y_steps[y0_idx], y_steps[y0_idx+1]
# # z11, z12 = image[x0_idx,y0_idx], image[x0_idx,y0_idx+1]
# # z21, z22 = image[x0_idx+1,y0_idx], image[x0_idx+1,y0_idx+1]
# 
# inter_value = (z11 * (x2 - x_cord) * (y2 - y_cord) +
#                z21 * (x_cord - x1) * (y2 - y_cord) +
#                z12 * (x2 - x_cord) * (y_cord - y1) +
#                z22 * (x_cord - x1) * (y_cord - y1)) / ((x2 - x1) * (y2 - y1))
# 
# print 'Numpy interpolate', inter_value
# 
# # Theano interpolation
# te_1, te_2, ne_1, ne_2, emis_11, emis_12, emis_21, emis_22, x_in, y_in = tt.dscalars(10)
# out_bInterp = (emis_11 * (te_2 - x_in) * (ne_2 - y_in) +
#                emis_21 * (x_in - te_1) * (ne_2 - y_in) +
#                emis_12 * (te_2 - x_in) * (y_in - ne_1) +
#                emis_22 * (x_in - te_1) * (y_in - ne_1)) / ((te_2 - te_1) * (ne_2 - ne_1))
# f_bInterp = theano.function(inputs=[te_1, te_2, ne_1, ne_2, emis_11, emis_12, emis_21, emis_22, x_in, y_in], outputs=out_bInterp)
# 
# inter_value_theano = f_bInterp(x1, x2, y1, y2, z11, z12, z21, z22, x_cord, y_cord)
# 
# print 'Theano interpolate', inter_value_theano
# 
# myTheanoOps = Bilinear_interp_theano()
# 
# te_0_idx = myTheanoOps.tt_index_array(x_steps, x_cord)
# ne_0_idx = myTheanoOps.tt_index_array(y_steps, y_cord)
# print 'te_0_idx', te_0_idx, x_steps[te_0_idx], type(te_0_idx)
# print 'ne_0_idx', ne_0_idx, y_steps[ne_0_idx], type(ne_0_idx)
# x1, x2, y1, y2, z11, z12, z21, z22 = myTheanoOps.neighbour_points(te_0_idx, ne_0_idx, x_steps, y_steps, image)
# inter_emis = myTheanoOps.tt_interp_array(x1, x2, y1, y2, z11, z12, z21, z22, x_cord, y_cord)
# print 'Theano interpolate 2', inter_emis


# >>> x = T.dscalar('x')
# >>> y = T.dscalar('y')
# >>> z = x + y
# >>> f = function([x, y], z)
#
# import os
# import warnings
# warnings.filterwarnings("ignore")
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor as T
# a1 = T.dscalar('a1')
# a2 = T.dscalar('a2')
# a3 = T.dscalar('a3')
# out_bInterp = a1 + a2 + a3
# f_bInterp = theano.function([a1, a2, a3], out_bInterp)
# print f_bInterp


# def cosas_raras(x1, x2, y1, y2, z11, z12, z21, z22, x_in, y_in):
#     print x1, x2, y1, y2, z11, z12, z21, z22, x_in, y_in
#     return
#
# cosas_raras(x_steps[x0_idx:x0_idx + 2], y_steps[y0_idx:y0_idx + 2], image[y0_idx][x0_idx:x0_idx + 2], image[y0_idx + 1][x0_idx:x0_idx + 2], x_cord, y_cord)


# with pm.Model():
#     x_pm = pm.Normal('x_pm', mu=2, sd=1, shape=1, testval=2)
#     print type(x_pm)

# a  = T.vector('a')
# b  = T.vector('b')
# sum_op = a + b
# f_sum_op = theano.function(name='get_sum', inputs=[a, b], outputs=sum_op)
# f_sum_op[np.asarray(x_steps), np.asarray(y_steps)]




# cord_range  = T.vector('coordinates_range')
# cord_input  = T.scalar('input_cordinate')
# idx0        = T.argmin(T.abs_(cord_range - cord_input))
# f_idx0      = theano.function(name='get_idx0', inputs=[cord_range, cord_input], outputs=idx0)
# x0_idx      = f_idx0([x_steps_t, x_cord_t])
#
# print x_steps.shape, y_steps.shape, image.shape
# T.abs_
# #Nearest neighbour
# x_t = T.clip(x_cord_t,0,T.shape(image_t)[0]-2)
# y_t = T.clip(y_cord_t,0,T.shape(image_t)[1]-2)
#
# nearestNeighbour = image_t[T.cast(T.floor(x_t),'uint16'), T.cast(T.floor(y_t),'uint16')]
# nearestNeighbour.name = 'cord-nearestNeighbourSampler'
#
# argmin_Te = T.argmin(x_steps_t)  # symbolic expr for argmax
# find_min = theano.function([x_steps_t], argmin_Te)  # function computing argmax_a given a
# find_min(x_steps_t)
#
# print nearestNeighbour
# print type(nearestNeighbour)
#
# #Trilinear
# x0 = T.cast(T.floor(x_t),'uint16')
# y0 = T.cast(T.floor(y_t),'uint16')
#
# x1 = x0+1
# y1 = y0+1
#
# xd = (x_t-x0)
# yd = (y_t-y0)
#
# c00 = image_t[x0,y0]*(1-xd) + image_t[x1,y0]*xd
# c10 = image_t[x0,y1]*(1-xd) + image_t[x1,y1]*xd
# c01 = image_t[x0,y0]*(1-xd) + image_t[x1,y0]*xd
# c11 = image_t[x0,y1]*(1-xd) + image_t[x1,y1]*xd
#
# c0  = c00*(1-yd) + c10*yd
# c1  = c01*(1-yd) + c11*yd
#
# #trilinear = c0*(1-zd) + c1*zd
#
# #Scipy interpolation
# scipy_interpol = scipy.interpolate.interp2d(x_steps, y_steps, image, kind='linear')
#
# print scipy_interpol(10.0, 4.2), scipy_interpol(10.0, 4.3), scipy_interpol(10.25, 4.2)
# print scipy_interpol(x_cord, y_cord)
#
#
# import numpy as np
# from scipy import interpolate
# import matplotlib.pyplot as plt
# x = np.arange(-5.01, 5.01, 0.25)
# y = np.arange(-5.01, 5.01, 0.25)
# xx, yy = np.meshgrid(x, y)
# z = np.sin(xx**2+yy**2)
# f = interpolate.interp2d(x, y, z, kind='cubic')
# xnew = np.arange(-5.01, 5.01, 1e-2)
# ynew = np.arange(-5.01, 5.01, 1e-2)
# znew = f(xnew, ynew)
# plt.plot(x, z[0, :], 'ro-', xnew, znew[0, :], 'b-')
# plt.show()
#
#
#
# print 'myBilinear', bilinear_interpolator_axis(10.5, 4.4, x_steps, y_steps, image)
#
#
# import os
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import numpy as np
# from theano import function
#
# x = theano.tensor.dscalar('x')
# y = theano.tensor.dscalar('y')
# z = x + y
# f = function([x, y], z)
# d = f(16.3, 12.1)
# e = z.eval({x : 16.3, y : 12.1})
# print d, type(d)
# print e, type(e)

# import theano
# a = theano.tensor.vector() # declare variable
# out = a + a ** 10               # build symbolic expression
# f = theano.function([a], out)   # compile function
# print(f([0, 1, 2]))
#
# import theano
# a = theano.tensor.vector() # declare variable
# b = theano.tensor.dscalar()
# out = a ** 2 + 2 * a * b              # build symbolic expression
# f = theano.function([a, b], out)   # compile function
# print(f([0, 1, 2],3))

# import theano
# import theano.tensor as T
# a, b = T.dmatrices('a', 'b')
# diff = a - b
# abs_diff = abs(diff)
# diff_squared = diff**2
# f = theano.function([a, b], [diff, abs_diff, diff_squared])
# print f([[1, 1], [1, 1]], [[0, 1], [2, 3]])


# from theano import function
#
# a = np.array([[1.1,2.2,3.3],[4.4,5.5,6.6],[7.7,8.8,9.9]])
#
# print a
# print a.shape
#
# b = theano.shared(a)
#
# c = theano.tensor.as_tensor_variable(a)
# print 'c'
# print c
# print type(c)
# print c.get_value()


# print 'b'
# print b
# print type(b)
# print b.get_value()
# print
# print 'b[0]'
# print b[0]
# print type(b[0])
# print b[0].get_value()
# print
# print 'b[0,0]'
# print b[0,0]
# print type(b[0,0])
# print b[0,0].get_value()
# print
#
# my_range_max = theano.tensor.iscalar('my_range_max')
# my_range = b[0]
#
# f = function([my_range_max], my_range)
# print('f(10): {0}'.format(f(3)))

# import os
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# import theano
# import theano.tensor
# import numpy as np
#
# def compute(minibatch):
#     xflat       = minibatch.reshape((minibatch.shape[0], -1))
#     partition   = np.array([1, 2, 3])
#     xsub1       = xflat[:, partition]
#     partition   = np.array([1])
#     xsub2       = xflat[:, partition]
#     return xsub1, xsub2
#
#
# def compile_theano_version():
#     minibatch       = theano.tensor.tensor3(name='minibatch', dtype=theano.config.floatX)
#     xsub1, xsub2    = compute(minibatch)
#     print xsub1.type, xsub2.type
#     return theano.function([minibatch], [xsub1, xsub2])
#
#
# def numpy_version(minibatch):
#     return compute(minibatch)
#
#
# def main():
#     batch_shape = (50, 40, 30, 30)
#     minibatch = np.random.standard_normal(size=batch_shape).astype(theano.config.floatX)
#
#     xsub1, xsub2 = numpy_version(minibatch)
#     print xsub1.shape, xsub2.shape
#
#     theano_version = compile_theano_version()
#     xsub1, xsub2 = theano_version(minibatch)
#     print xsub1.shape, xsub2.shape
#
#
# main()


# import os
# os.environ["MKL_THREADING_LAYER"] = "GNU"
# from bisect import bisect_left
# import theano
# import pymc3 as pm
# import numpy as np
# a = np.array([1,2,3,4,7])
#
# from scipy import interpolate
# from theano.tensor.nnet.abstract_conv
#
# x = np.arange(-5.01, 5.01, 0.25)
# y = np.arange(-5.01, 5.01, 0.25)
# xx, yy = np.meshgrid(x, y)
# z = np.sin(xx**2+yy**2)
# f = interpolate.interp2d(x, y, z, kind='cubic')
# znew = f(0, 0)
#
# with pm.Model():
#     x = pm.Normal('x', mu=2, sd=1, shape=5, testval=a)
#     y = pm.Uniform('y', lower=2, upper=6, shape=5, testval=a)
#     z = pm.Normal('zi', mu=2, sd=1)
#     n = a - z
#     # np.searchsorted(a, z)
#     z_p = z
#
#     f(x.tag.test_value, y.tag.test_value)
#
#     print 'high', np.searchsorted(a, z_p.tag.test_value)
#     print 'high', np.searchsorted(a, z.tag.test_value)
#     print 'high', np.searchsorted(a, z.tag.test_value)
#     print 'hola', z.astype(theano.config.floatX)
#
#     i = bisect_left(a, z.tag.test_value) - 1
#
# print '1', x
# print '2', y
# print '3', z.tag.test_value
# print '4', x.tag.test_value[0]
# print '5', y.tag.test_value[0]
# print '6', z_p.tag.test_value
# print '7', z_p, type(z_p)
# #print '8', np.astype(z_p, float), type(np.astype(z_p, float))

# import os
# os.environ["MKL_THREADING_LAYER"] = "GNU"
#
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
#
# from pymc3 import HalfCauchy, Model, Normal, get_data, sample
# from pymc3.distributions.timeseries import GaussianRandomWalk
#
# data = pd.read_csv(get_data('pancreatitis.csv'))
# countries = ['CYP', 'DNK', 'ESP', 'FIN', 'GBR', 'ISL']
# data = data[data.area.isin(countries)]
#
# age = data['age'] = np.array(data.age_start + data.age_end) / 2
# rate = data.value = data.value * 1000
# group, countries = pd.factorize(data.area, order=countries)
#
# ncountries = len(countries)
#
# for i, country in enumerate(countries):
#     plt.subplot(2, 3, i + 1)
# plt.title(country)
# d = data[data.area == country]
# plt.plot(d.age, d.value, '.')
#
# plt.ylim(0, rate.max())
#
# nknots = 10
# knots = np.linspace(data.age_start.min(), data.age_end.max(), nknots)
#
#
# def interpolate(x0, y0, x, group):
#     x = np.array(x)
#     group = np.array(group)
#
#     idx = np.searchsorted(x0, x)
#     dl = np.array(x - x0[idx - 1])
#     dr = np.array(x0[idx] - x)
#     d = dl + dr
#     wl = dr / d
#
#     return wl * y0[idx - 1, group] + (1 - wl) * y0[idx, group]
#
#
# with Model() as model:
#     coeff_sd = HalfCauchy('coeff_sd', 5)
#
#     y = GaussianRandomWalk('y', sd=coeff_sd, shape=(nknots, ncountries))
#
#     p = interpolate(knots, y, age, group)
#
#     sd = HalfCauchy('sd', 5)
#
#     vals = Normal('vals', p, sd=sd, observed=rate)
#
#
# def run(n=3000):
#     if n == "short":
#         n = 150
#     with model:
#         trace = sample(n, tune=int(n / 2), init='advi+adapt_diag')
#
#     for i, country in enumerate(countries):
#         plt.subplot(2, 3, i + 1)
#         plt.title(country)
#
#         d = data[data.area == country]
#         plt.plot(d.age, d.value, '.')
#         plt.plot(knots, trace[y][::5, :, i].T, color='r', alpha=.01)
#
#         plt.ylim(0, rate.max())
#
#
# if __name__ == '__main__':
#     run()



# import os
# os.environ["MKL_THREADING_LAYER"] = "GNU"
#
# import theano
# import numpy as np
# import pymc3 as pm
#
# v = np.arange(10)
# var = theano.tensor.vector()
# out = theano.tensor.eq(var, 2).nonzero()[0]
#
# with pm.Model():
#     x = pm.Norml('x', mu=0, sd=1, shape=5)
#     bicho = out.eval({var: v})[0]
#
# print bicho, type(bicho)
# print var, type(var)
# print out, type(out)
# print pm.math.sin(var)








# import pymc3 as pm
# from pymc3.distributions import transforms
# import theano
# import theano.tensor as tt
# import numpy as np
# from scipy.interpolate import InterpolatedUnivariateSpline
# pm.Interpolated
#
# pm.math.
#
# class SplineLikelihood(theano.Op):
#
#     def __init__(self, pmf, lower, upper):
#         self.itypes, self.otypes = [tt.dscalar], [tt.dscalar]
#         self.density = InterpolatedUnivariateSpline(np.linspace(lower, upper, len(pmf)), pmf, k=1, ext='zeros')
#         self.density_grad = self.density.derivative()
#         self.Z = self.density.integral(lower, upper)
#
#         @theano.as_op(itypes=[tt.dscalar], otypes=[tt.dscalar])
#         def grad_op(x):
#             return np.asarray(self.density_grad(x))
#
#         self.grad_op = grad_op
#
#     def perform(self, node, inputs, output_storage):
#         x, = inputs
#         output_storage[0][0] = np.asarray(self.density(x) / self.Z)
#
#     def grad(self, inputs, grads):
#         x, = inputs
#         x_grad, = grads  # added later, thanks to @aseyboldt
#         return [x_grad * self.grad_op(x) / self.Z]
#
# class SplineDist(pm.Continuous):
#
#     def __init__(self, pmf, lower=0, upper=1, transform='interval', *args, **kwargs):
#         if transform == 'interval':
#             transform = transforms.interval(lower, upper)
#         super(SplineDist, self).__init__(transform=transform, testval=(upper - lower) / 2, *args, **kwargs)
#         self.likelihood = SplineLikelihood(pmf, lower, upper)
#
#     def logp(self, value):
#         return tt.log(self.likelihood(value))
#
#
# with pm.Model() as m:
#     spline_p = SplineDist('spline_p', np.linspace(1.0, 10.0, 100), 0, 1)
#     trace = pm.sample(100000, random_seed=1, njobs=1)
#
#     pm.traceplot(trace)



# import numpy as np
# import pymc3 as pm
# print('Running on PyMC3 v{}'.format(pm.__version__))
#
# # Initialize random number generator
# np.random.seed(123)
#
# # True parameter values
# alpha, sigma = 1, 1
# beta = [1, 2.5]
#
# # Size of dataset
# size = 100
#
# # Predictor variable
# X1 = np.random.randn(size)
# X2 = np.random.randn(size) * 0.2
#
# # Simulate outcome variable
# Y = alpha + beta[0]*X1 + beta[1]*X2 + np.random.randn(size)*sigma
#
# basic_model = pm.Model()
#
# with basic_model:
#
#     # Priors for unknown model parameters
#     alpha = pm.Normal('alpha', mu=0, sd=10)
#     beta = pm.Normal('beta', mu=0, sd=10, shape=2)
#     sigma = pm.HalfNormal('sigma', sd=1)
#
#     # Expected value of outcome
#     mu = alpha + beta[0]*X1 + beta[1]*X2
#
#     # Likelihood (sampling distribution) of observations
#     Y_obs = pm.Normal('Y_obs', mu=mu, sd=sigma, observed=Y)
#
#     map_estimate = pm.find_MAP(model=basic_model)