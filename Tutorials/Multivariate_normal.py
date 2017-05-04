'''
Created on Aug 3, 2015

@author: vital
'''
import matplotlib.pyplot as plt
import numpy as np

mean    = [15,10]
cov     = [[4,0],[0,1]]     # diagonal covariance, points lie on x or y-axis

x,y = np.random.multivariate_normal(mean,cov,1000).T

plt.plot(x, y, 'ok')
plt.xlabel('x')
plt.ylabel('y');

plt.show()
