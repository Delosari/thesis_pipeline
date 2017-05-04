'''
Created on Mar 15, 2017

@author: vital
'''

import numpy as np
from dazer_methods import Dazer

dz = Dazer()

#Set figure format
sizing_dict = {'figure.figsize' : (8, 8)}
dz.FigConf(sizing_dict)

te_SIII = np.linspace(8000, 20000, 50)
te_SII = 0.88 * te_SIII + 1560
line_unity = te_SIII

dz.data_plot(te_SIII, te_SII, label = r'$T_e[SII]=0.88T_e[SIII]+1560$')
dz.data_plot(te_SIII, te_SIII, label = '', color='grey', linestyle='--')

dz.Axis.set_xlim(8000, 20000)
dz.Axis.set_ylim(8000, 20000)
dz.Axis.grid(True)


ticklines = dz.Axis.get_xticklines() + dz.Axis.get_yticklines()
gridlines = dz.Axis.get_xgridlines() + dz.Axis.get_ygridlines()
ticklabels = dz.Axis.get_xticklabels() + dz.Axis.get_yticklabels()

for line in ticklines:
    line.set_linewidth(3)

for line in gridlines:
    line.set_linestyle('-.')



dz.FigWording(xlabel = r'$T_e[SIII]$ $(K)$', ylabel = r'$T_e[SII]$ $(K)$', title = 'Relation between $S^{+1}$ and $S^{+2}$ temperatures')

dz.display_fig()