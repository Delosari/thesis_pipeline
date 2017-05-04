from pymc               import deterministic, stochastic, Normal, Uniform, MCMC, Bernoulli, stochastic_from_dist

from dazer_methods import Dazer

#Generate dazer object
dz = Dazer()
 
#Choose plots configuration
dz.FigConf()
 
#Import catalogue
Catalogue = dz.import_catalogue()
 
#Perform operations
x = [1,2,3,4,5,6]
y = [1,2,3,4,5,6]
 
#Plot the data
dz.data_plot(x, y, markerstyle = 'o')
 
#Generate the figure
dz.display_fig()