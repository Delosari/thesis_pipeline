'''
Created on Sep 1, 2016

@author: vital
'''

import numpy as np
from astropy import units as u
from astropy.coordinates import Angle
  
StarA = ['14:29:42.95', '-62:40:46.1']
StarB = ['14:39:36.50', '-60:50:2.3']
  
cord_A = [Angle(StarA[0], unit = u.hourangle), Angle(StarA[1], unit = u.degree)]
cord_B = [Angle(StarB[0], unit = u.hourangle), Angle(StarB[1], unit = u.degree)]
 
print cord_A, cord_B
 
print np.array([cord_A[0], cord_B[0]])
print cord_A[0].degree, cord_A[1].degree
print cord_B[0].degree, cord_B[1].degree
  
Delta_RA    = cord_B[0].degree - cord_A[0].degree
Delta_Dec   = cord_B[1].degree - cord_A[1].degree
  
print Delta_RA
print Delta_Dec
print np.cos(cord_A[1].radian)
  
Delta_Theta = np.sqrt((Delta_RA * np.cos(cord_A[1].radian))**2 + (Delta_Dec)**2)
  
print Delta_Theta
    print dz.reducDf.iloc[i].RA, Angle(dz.reducDf.iloc[i].RA, unit = u.hourangle)
    print dz.reducDf.iloc[i].DEC, Angle(dz.reducDf.iloc[i].DEC, unit = u.degree)