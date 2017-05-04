'''
Created on Apr 2, 2014

@author: vital
'''
#!/usr/bin/env python

import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes

# fig, (ax) = plt.subplots(1, 1, figsize=[5.5, 3])

Fig1=plt.figure(figsize=(16,10))
ax = Fig1.add_subplot(111)



# first subplot
ax.set_aspect(1.)

axins = inset_axes(ax,
                   width="30%", # width = 30% of parent_bbox
                   height="30%", # height : 1 inch
                   loc=1)

plt.xticks(visible=False)
plt.yticks(visible=False)

axins = inset_axes(ax,
                   width="20%", # width = 30% of parent_bbox
                   height="20%", # height : 1 inch
                   loc=2)

plt.xticks(visible=False)
plt.yticks(visible=False)


# second subplot
# ax2.set_aspect(1.)
# 
# axins = zoomed_inset_axes(ax2, 0.5, loc=1) # zoom = 0.5
# 
# plt.xticks(visible=False)
# plt.yticks(visible=False)
# 
plt.draw()
plt.show()

# 
# from pylab import *
# 
# # create some data to use for the plot
# dt = 0.001
# t = arange(0.0, 10.0, dt)
# r = exp(-t[:1000]/0.05)               # impulse response
# x = randn(len(t))
# s = convolve(x,r)[:len(x)]*dt  # colored noise
# 
# # the main axes is subplot(111) by default
# plot(t, s)
# axis([0, 1, 1.1*amin(s), 2*amax(s) ])
# xlabel('time (s)')
# ylabel('current (nA)')
# title('Gaussian colored noise')
# 
# # this is an inset axes over the main axes
# a = axes([.65, .6, .2, .2], axisbg='y')
# n, bins, patches = hist(s, 400, normed=1)
# title('Probability')
# setp(a, xticks=[], yticks=[])
# 
# # this is another inset axes over the main axes
# a = axes([0.2, 0.6, .2, .2], axisbg='y')
# plot(t[:len(r)], r)
# title('Impulse response')
# setp(a, xlim=(0,.2), xticks=[], yticks=[])
# 
# 
# show()