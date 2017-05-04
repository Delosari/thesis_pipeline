# import numpy as np
# 
# def hunt_check(my_array, target_value):
#     
#     #Case the exact value is in array
#     if target_value in my_array:
#         idx = np.where(my_array==target_value)[0][0]
#         print 'index1', idx
#     else:
#         if (target_value < my_array[0]):
#             idx = 0
#             print 'index2', idx
#         elif (my_array[-1] < target_value):
#             idx = -1
#             print 'index3', idx            
#         else:
#             idx = np.searchsorted(my_array, target_value) - 1
#             print 'index4', idx
#             
#     return idx
# 
# target = 3.9
# a   =  np.array([1, 3, 4, 6, 9, 10, 54])
# idx =  hunt_check(a, target)
# 
# print 'jlo', a[idx]

import numpy as np

def import_levelspopulation_file(filename):
    with open(filename) as f_input:
        lines = f_input.readlines()
        for i in range(3, len(lines)):
            line = lines[i].split(',')
            del line[-1]
            for val in line:
                yield float(val)

TableAddress = '/home/vital/Dropbox/Astrophysics/Papers/Radiation_Correction/OriginalCodes/Distribution/He5B.optB'                

arr = np.array(list(import_levelspopulation_file(TableAddress)))

nsiz = 29
ndg = 5 
ntg = 5 
ntaug = 20 

# Account for python's Row-major ordering.
arr = arr.reshape((nsiz, ndg, ntg, ntaug), order='F')

print 'Empezamos'

for i in range(nsiz):
    for j in range(ndg):
        for k in range(ntg):
            for m in range(ntaug):
                print arr[i,j,k,m]
