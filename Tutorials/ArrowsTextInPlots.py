'''
Created on Oct 7, 2012
  
@author: vital
'''
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.pyplot as plt
import pylab

Fig = plt.figure()
Fig.suptitle('Bold figuire suptitle', fontsize=14, fontweight='bold')

Ax = Fig.add_subplot(111)
Fig.subplots_adjust(top=0.85)
Ax.set_title('Axes title')

Ax.set_xlabel('xlabel',fontsize=30)
Ax.set_ylabel('ylabel')

pylab.yticks(fontsize=15)
pylab.xticks(fontsize=15)

Ax.text(3,8,'boxed italics text in data coords',style='italic',bbox={'facecolor':'red','alpha':0.5,'pad':10})

Ax.text(2, 6, r'an equation: $E=mc^2$', fontsize=15)

Ax.text(3,2,unicode('unicode: Institut f\374r Festk\366rperphysik','latin-1'))

Ax.text(0.95, 0.01, 'colored text in axes coords',verticalalignment='bottom',horizontalalignment='right',transform=Ax.transAxes,color='green',fontsize=15)

Ax.plot([2],[1],'o',color='r')

#Ax.annotate('annotate',xytext=(3,4))
Ax.annotate('annotate',xy=(2,1),xytext=(3,4),arrowprops=dict(facecolor='yellow',edgecolor='yellow'))

Ax.axis([0, 10, 0, 10])

plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# import matplotlib.cm as cmx
# 
# DATA = np.random.rand(5,5)
# 
# cmap = plt.cm.jet
# 
# cNorm  = colors.Normalize(vmin=np.min(DATA[:,4]), vmax=np.max(DATA[:,4]))
# 
# scalarMap = cmx.ScalarMappable(norm=cNorm,cmap=cmap)
# 
# for idx in range(0,len(DATA[:,1])):
#     colorVal = scalarMap.to_rgba(DATA[idx,4])
#     plt.arrow(DATA[idx,0],  #x1
#               DATA[idx,1],  # y1
#               DATA[idx,2]-DATA[idx,0], # x2 - x1
#               DATA[idx,3]-DATA[idx,1], # y2 - y1
#               color=colorVal)
# 
# plt.show()  