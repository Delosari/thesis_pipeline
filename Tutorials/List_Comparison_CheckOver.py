'''
Created on Oct 16, 2015

@author: vital
'''
import numpy as np
from collections import OrderedDict

Abunances_dict    = OrderedDict()

Sulfur_abundances = OrderedDict()  
Helium_Abundances = OrderedDict()

Sulfur_abundances['A'] = 2
Sulfur_abundances['B'] = 3
Sulfur_abundances['C'] = 4
Sulfur_abundances['D'] = 5
Sulfur_abundances['E'] = 6
Sulfur_abundances['F'] = 7
Sulfur_abundances['G'] = 8
Sulfur_abundances['H'] = 9
Sulfur_abundances['I'] = 10

Helium_Abundances['A'] = 2
Helium_Abundances['C'] = 4
Helium_Abundances['D'] = 5
Helium_Abundances['F'] = 7
Helium_Abundances['G'] = 8
Helium_Abundances['I'] = 10
Helium_Abundances['J'] = 2
Helium_Abundances['K'] = 2
Helium_Abundances['M'] = 2

Y_keys, X_keys = Helium_Abundances.keys(), Sulfur_abundances.keys()

Obj_vector  = np.intersect1d(ar1=Y_keys, ar2=X_keys, assume_unique=True)
Y_vector    = np.zeros(len(Obj_vector))
X_vector    = np.zeros(len(Obj_vector))

for i in range(len(Obj_vector)):
    X_vector[i] = Sulfur_abundances[Obj_vector[i]]
    Y_vector[i] = Helium_Abundances[Obj_vector[i]]
    print Obj_vector[i], X_vector[i], Y_vector[i]
    
    
Abunances_dict['O_Vectors'] = [Obj_vector[i], X_vector[i], Y_vector[i]]