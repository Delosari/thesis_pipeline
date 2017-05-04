'''
Created on Apr 30, 2015

@author: vital
# '''
import operator
from collections import OrderedDict
import numpy as np

Father_dict = OrderedDict()

ListKeys    = ['A', 'B', 'C', 'D', 'E']
ListValues  = [[1,1],[2,2],[3,3],[4,4],[5,5]]
ListWanted  = ['B', 'D', 'E']



for i in range(len(ListKeys)):
    Father_dict[ListKeys[i]] = ListValues[i]
    
print 'my dictionaries'
print Father_dict

f = operator.itemgetter(*ListWanted)

print f(Father_dict), type(f(Father_dict))

Matrix = np.array(f(Father_dict))

print 'Output matrix', type(Matrix)
print Matrix

print 'A column'
print Matrix[:,0]

print 'A row'
print Matrix[1,:]

# from collections import OrderedDict
# 
# Father_dict = OrderedDict()
# 
# List_subDicts = ['A', 'B']
# 
# for i in range(len(List_subDicts)):
#     Father_dict[List_subDicts[i]] = OrderedDict()
#     
# print 'my dictionaries'
# 
# print Father_dict
# import numpy as np
# 
# TrueData_dict = {'y_plus':1, 
#                  'a':2, 
#                  'c':3}
 
# 
# dict1 = {}
# 
# dict1["a"] = 1
# dict1["b"] = 2
# dict1["c"] = 3
# 
# dict2 = {}
# 
# dict2["d"] = 1
# dict2["e"] = None
# dict2["f"] = 3
# 
# dict3 = None
# 
# print 'dict1'
# if (None not in dict1.values()):
#     print 'Does not contain None'
# 
# print 'dict2'
# if (None not in dict2.values()):
#     print 'values', dict2.values()
#     print 'Does not contain None'    
# 
# 
# print 'dict3'
# if (None not in dict3.values()):
#     print 'Does not contain None'  
# 
# 
# Flux_dict = {}
# 
# Flux_dict["O3_4959A"] = 1
# Flux_dict["O3_5007A"] = 2
# Flux_dict["H1_4861A"] = 3
# 
# print 'Diccionario completo', Flux_dict
# 
# for i in range(len(Flux_dict.keys())):
#     print Flux_dict.keys()[i], Flux_dict.values()[i]
# 
# 
# 
# myKeys      = Flux_dict.keys() 
# myValues    = np.array(Flux_dict.values()) * 10
#  
# Flux_dict = dict(zip(Flux_dict.keys() , myValues))
#  
# print 'After', Flux_dict
# 
# Kid =   {
#          'Name': 'Zara',
#          'Age': 7, 'Class': 'First'}
# 
# print "dict['Name']: ", Kid['Name'];
# print "dict['Age']: ", Kid['Age'];
# 
# 
# Kid['Age'] = 8; # update existing entry
# Kid['School'] = "DPS School"; # Add new entry
# 
# print "dict['Name']: ", Kid['Age'];
# print Kid
# 
# print 'Items',  Kid.items(),    type(Kid.items())
# print 'keys',   Kid.keys(),     type(Kid.keys())
# print 'Values', Kid.values(),   type(Kid.values())
# 
# 
# del Kid['Name']; # remove entry with key 'Name'
# 
# print Kid
# 
# Kid.clear();     # remove all entries in dict
# 
# Kid = {'Name': 'Zara', 'Age': 7, 'Class': 'First'};
# print 'Kid', Kid
# 
# orderdKid = OrderedDict()
# orderdKid['Name'] = 'Zara'
# orderdKid['Age'] = 7
# orderdKid['Class'] = 'First'
# 
# 
# for k, v in orderdKid.items():
#     print k, v
# 
# 
# orderdKid2 = OrderedDict(Kid)
# for k, v in orderdKid2.items():
#     print 'item', k, v
# Kid.upd
# 
# print 'flux y kid combinado'
# print dict(Flux_dict.items() | Kid.items())


# def test(a, b, c, d):
#     print 'a', a
#     print 'b', b
#     print 'c', c
#     print 'd', d
# 
# coso = {'c': 3, 
#         'd': 4}
# coso['d'] = 5
# test(a = 1, b = 2, **coso)