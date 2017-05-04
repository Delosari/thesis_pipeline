import numpy as np



x = np.array([np.inf, 100, np.nan, 128, 128, 100, 100, 120])
y = np.array([1, 2, 3, 4, 5, 6, 7, 8])

print 'Antes', x

ind_below   = np.where(x < 75)
x[ind_below] = y[ind_below]

print 'below', len(ind_below), ind_below[0], len(ind_below[0])

inds_nan    = np.where(np.isnan(x))
x[inds_nan] = y[inds_nan]

print 'Despues', x

# '''
# Created on Sep 26, 2014
# 
# @author: INAOE_Vital
# '''
# import os
# basedir = '/Users/INAOE_Vital/Dropbox/Astrophysics/Data/SDSS_Galaxies/'
# for fn in os.listdir(basedir):
#     print fn
#     if not os.path.isdir(os.path.join(basedir, fn)):
#         continue # Not a directory
#     if ('spSpec' in fn) and ('dr10.fits' not in fn):
#         continue # Already in the correct form
# 
#     OldName = fn
#     NewName = OldName[0:OldName.find('_')]
#     SDSS_Code = OldName[6:OldName.find('_')]
#     if int(SDSS_Code) < 10 :
#         NewName = 'spSpec'+'0'+ SDSS_Code
#     
#     print 'Change ', os.path.join(basedir, OldName), 'to' ,os.path.join(basedir, NewName)
#     os.rename(os.path.join(basedir, OldName), os.path.join(basedir, NewName))