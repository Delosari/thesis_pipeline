'''
Created on Oct 8, 2015

@author: vital
'''

import pymc
from CodeTools.PlottingManager import myPickle

Databases_Folder    = '/home/vital/Workspace/X_ModelData/MCMC_databases/' 
Db_name             = 'he_Abundance_10000_Hope2'   

#Generate dazer object
pv = myPickle()

#Define plot frame and colors
pv.FigFormat_One(ColorConf = 'Night1')