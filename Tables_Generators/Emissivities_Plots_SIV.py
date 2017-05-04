from CodeTools.PlottingManager              import myPickle
from Plotting_Libraries.dazer_plotter       import Plot_Conf
from numpy                                  import linspace
import seaborn as sns
import pyneb as pn

# pn.atomicData.setDataFile('h_i_rec_SH95.hdf5', 'H1', 'rec')
# pn.atomicData.setDataFile('he_ii_rec_SH95.hdf5', 'He2', 'rec')

#Declare Classes
pv      = myPickle()
dz      = Plot_Conf() 

#Define figure format
dz.FigConf()

# Atom creation and definition of physical conditions
S4     = pn.Atom('S', 4)

#Define physical conditions
tem = 10000
tem_range = linspace(10000, 25000, 100)
 
den = 100
den_range = linspace(10, 300, 100)

# Comment the second if you want all the lines to be plotted
# S_Lines=[105100, 1404.81, 1423.84, 1398.04, 1416.89, 290100.0, 1387.46, 1406.02, 112300, 183200]
# S_Lines=[1404.81, 1423.84, 1416.89, 1406.02, 112300]
S_Lines=[105000]


#--------------------------Density case----------------------------------
#Plot the lines
for line in S_Lines:
    y           = S4.getEmissivity(tem, den_range, wave = line)
    y_1000_100  = S4.getEmissivity(tem, den, wave = line)
    dz.data_plot(den_range, y/y_1000_100, label=str(line) + r' $\AA$ line')
    
# dz.Axis.set_xscale('log')
dz.Axis.tick_params(axis='both', labelsize=20.0)
dz.Axis.set_ylim(0.0,2.5)
# dz.Axis.patch.set_facecolor('white')
# dz.Fig.set_facecolor('black')
# dz.Fig.set_edgecolor('black')

#Plot wording
xtitle  = r'$n_{e}$ $(cm^{-3})$'
# ytitle  = r'j(T) [erg cm$^{-3}$ s${-1}$]'
ytitle  = 'Relative emissivity'
title   = 'HeI emissivities @ $T_e$={:.0f}'.format(tem)
dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)

#Display figure
# dz.display_fig()
dz.savefig('/home/vital/Dropbox/Astrophysics/Lore/PopStar_SEDs/SIV_Emissivity_den', extension = '.png', reset_fig=True)

#--------------------------Temperature case----------------------------------
#Plot the lines
for line in S_Lines:
    y           = S4.getEmissivity(tem_range, den, wave=line)
    y_1000_100  = S4.getEmissivity(tem, den, wave=line)
    dz.data_plot(tem_range, y/y_1000_100, label=str(line) + r' $\AA$ line', linestyle='--', linewidth=2)
    
# dz.Axis.set_xscale('log')
dz.Axis.tick_params(axis='both', labelsize=20.0)
# dz.Axis.set_ylim(0.0,2.5)
# dz.Axis.patch.set_facecolor('white')
# dz.Fig.set_facecolor('black')
# dz.Fig.set_edgecolor('black')

#Plot wording
xtitle  = r'$T_{e}$ $(K)$'
# ytitle  = r'j(T) [erg cm$^{-3}$ s${-1}$]'
ytitle  = 'Relative emissivity'
title   = 'HeI emissivities @ $n_e$={:.0f}'.format(den)
dz.FigWording(xtitle, ytitle, title, axis_Size = 20.0, title_Size = 20.0, legend_size=20.0)

#Display figure
dz.display_fig()
# dz.savefig('/home/vital/Dropbox/Astrophysics/Lore/PopStar_SEDs/SIV_Emissivity_tem', extension = '.png', reset_fig=True)

print 'Data treated'

