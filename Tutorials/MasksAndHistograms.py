'''
Created on Jun 18, 2014

@author: INAOE_Vital
'''
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

x1 = x2 = np.arange(5)
y1 = np.array([1,5,20,2,4])
y2 = np.array([4,2,3,32,6])

NumberOfMasks = 2
Y_DataVector = [y1,y2]
X_DataVector = [x1,x2]
ColorVector = ['r','b']

PairingVector = []

for i in range(len(Y_DataVector)):
    for j in range(len(Y_DataVector)):
        if set(Y_DataVector[i]) != set(Y_DataVector[j]):
            PairingVector.append([Y_DataVector[i], Y_DataVector[j]])
            
MaskVector = []
for Pairing in PairingVector:
    Mask = ma.where(Pairing[0]<=Pairing[1])
    MaskVector.append(Mask)


for i in range(len(Y_DataVector)):
    p = plt.bar(X_DataVector[i], Y_DataVector[i], color=ColorVector[i], alpha=1, edgecolor='none', linewidth=0,width=0.5, log=False)

for i in range(len(MaskVector)):
    m = plt.bar(X_DataVector[i][MaskVector[i]], Y_DataVector[i][MaskVector[i]], color=ColorVector[i], alpha=1, edgecolor='none',linewidth=0,width=0.5, log=False)
    
plt.show()






# import matplotlib.pyplot as plt
# import numpy as np
# import numpy.ma as ma
# 
# x1 = x2 = np.arange(5)
# y1 = np.array([1,4,25,2,4])
# y2 = np.array([4,2,3,32,6])
# 
# mask1 = ma.where(y1>=y2)
# mask2 = ma.where(y2>=y1)
# 
# print mask1
# print mask2
# 
# p1 = plt.bar(x1[mask1], y1[mask1], color='r', alpha=1, edgecolor='none',linewidth=0,width=0.5, log=False)
# p2 = plt.bar(x2, y2, color='b', alpha=1, edgecolor='none', linewidth=0,width=0.5, log=False)
# p3 = plt.bar(x1[mask2], y1[mask2], color='r', alpha=1, edgecolor='none',linewidth=0,width=0.5, log=False)
# 
# plt.show()