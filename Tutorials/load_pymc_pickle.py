'''
Created on Oct 7, 2015

@author: vital
'''

import pymc

db_address = '/home/vital/Workspace/X_ModelData/MCMC_databases/he_Abundance_20000_NewMCMC'

db = pymc.database.pickle.load(db_address)

db.close()