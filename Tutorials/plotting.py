'''
Created on Aug 19, 2015

@author: vital
'''
import numpy as np
from CodeTools.PlottingManager      import myPickle
import matplotlib.pyplot as plot
#Generate dazer object
pv = myPickle()

#Define plot frame and colors
pv.FigFormat_One(ColorConf='Night1')

x = 25 * (np.random.random(50) - 0.5)
y = np.exp(- x**2 / 2)

pv.Axis1.plot(x,y,'o')

pv.DisplayFigure()