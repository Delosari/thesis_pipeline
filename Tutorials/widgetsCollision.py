"""
The SpanSelector is a mouse widget to select a xmin/xmax range and plot the
detail view of the selected region in the lower axes
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import matplotlib.widgets as widgets

Fig = plt.figure(figsize=(8,6))
Fig.set_facecolor('w')
Fig.set
Ax = Fig.add_subplot(211)


x = np.arange(0.0, 5.0, 0.01)
y = np.sin(2*np.pi*x) + 0.5*np.random.randn(len(x))

Ax.plot(x, y, '-')
Ax.set_ylim(-2,2)
Ax.set_title('Press left mouse button and drag to test')

RegionIndices = []

ax2 = Fig.add_subplot(212)
line2, = ax2.plot(x, y, '-')


def onselect(xmin, xmax):
    if len(RegionIndices) == 2:
        Ax.fill_between(x[:], 0.0, y[:],facecolor='White',alpha=1)
        del RegionIndices[:]


    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x)-1, indmax)

    Ax.fill_between(x[indmin:indmax], 0.0, y[indmin:indmax],facecolor='Blue',alpha=0.30)

    thisx = x[indmin:indmax]
    thisy = y[indmin:indmax]
    line2.set_data(thisx, thisy)
    ax2.set_xlim(thisx[0], thisx[-1])
    ax2.set_ylim(thisy.min(), thisy.max())
    Fig.canvas.draw()

    RegionIndices.append(xmin)
    RegionIndices.append(xmax)

# set useblit True on gtkagg for enhanced performance
span = SpanSelector(Ax, onselect, 'horizontal', useblit = False,rectprops=dict(alpha=0.5, facecolor='purple') )
cursor = widgets.Cursor(Ax, color="red", linewidth = 1, useblit = False)

plt.show()
