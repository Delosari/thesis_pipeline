# '''
# Created on Sep 22, 2014
# 
# @author: INAOE_Vital
# '''
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import numpy as np
# 
# # The data
# x = np.linspace(0, 10, 1000)
# y = np.sin(2 * np.pi * x)
# 
# # The colormap
# cmap = cm.jet
# 
# # Create figure and axes
# fig = plt.figure(1)
# # fig.clf()
# ax = fig.add_subplot(1, 1, 1)
# 
# c2 = np.linspace(10, 40, 7)
# 
# c = np.linspace(0, 10, 1000)
# print len(c)
# print len(x),len(y)
# 
# ax.scatter(x, y, c=c, cmap=cmap)
# 
# plt.show()


import matplotlib as mpl 
import matplotlib.pyplot as plt
from numpy import arange,meshgrid,sqrt

u,v = arange(-50,51,10),arange(-50,51,10)
u,v = meshgrid(u,v)
x,y = u,v
C = sqrt(u**2 + v**2)
cmap=plt.cm.jet
bounds = [10, 20, 40, 60]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
img=plt.barbs(x,y,u,v,C,cmap=cmap,norm=norm)
# plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds)
plt.show()