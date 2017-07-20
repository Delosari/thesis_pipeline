
from dazer_methods import Dazer
import os
import numpy as np

dz = Dazer()
dz.FigConf()

file_address    = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/code5varyZ.lin'

#Cont  nu    incident    trans    DiffOut    net trans    reflc    total    reflin    outlin    lineID    cont    nLine

OIII = np.loadtxt(file_address, usecols = (09, unpack = True)    


dz.data_plot(nu, incident, label = 'Incident spectrum')
dz.data_plot(nu, trans, label = 'Transmitted spectrum')
dz.data_plot(nu, total, label = 'Total spectrum')

dz.Axis.set_xlim(0.01,10000)
dz.Axis.set_ylim(1e-37,1e-22)
# 
# # dz.Axis.set_ylim(1e-9,1)
dz.Axis.set_yscale('log')    
dz.Axis.set_xscale('log')    

dz.FigWording(r'Wavelength (microns)', r'Radiation spectrum', 'Coronal')

dz.display_fig()






# from dazer_methods import Dazer
# import os
# import numpy as np
# 
# dz = Dazer()
# dz.FigConf()
# 
# file_address = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/code4_vcoronalv.grd'
# file_address2 = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/code4_vcoronalv.col'
# 
# #Cont  nu    incident    trans    DiffOut    net trans    reflc    total    reflin    outlin    lineID    cont    nLine
# 
# nu, incident, trans, total  = np.loadtxt(file_address, usecols = (0, 1, 2, 6), unpack = True)    
# nu, incident, trans, total  = np.loadtxt(file_address, usecols = (0, 1, 2, 6), unpack = True)    
# 
# 
# dz.data_plot(nu, incident, label = 'Incident spectrum')
# dz.data_plot(nu, trans, label = 'Transmitted spectrum')
# dz.data_plot(nu, total, label = 'Total spectrum')
# 
# dz.Axis.set_xlim(0.01,10000)
# dz.Axis.set_ylim(1e-37,1e-22)
# # 
# # # dz.Axis.set_ylim(1e-9,1)
# dz.Axis.set_yscale('log')    
# dz.Axis.set_xscale('log')    
# 
# dz.FigWording(r'Wavelength (microns)', r'Radiation spectrum', 'Coronal')
# 
# dz.display_fig()

# from dazer_methods import Dazer
# import os
# import numpy as np
#  
# dz = Dazer()
# dz.FigConf()
#  
# file_address = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/code4corontal.con'
#  
# #Cont  nu    incident    trans    DiffOut    net trans    reflc    total    reflin    outlin    lineID    cont    nLine
#  
# nu, incident, trans, total  = np.loadtxt(file_address, usecols = (0, 1, 2, 6), unpack = True)    
#  
#  
# dz.data_plot(nu, incident, label = 'Incident spectrum')
# dz.data_plot(nu, trans, label = 'Transmitted spectrum')
# dz.data_plot(nu, total, label = 'Total spectrum')
#  
# dz.Axis.set_xlim(0.01,10000)
# dz.Axis.set_ylim(1e-37,1e-22)
# # 
# # # dz.Axis.set_ylim(1e-9,1)
# dz.Axis.set_yscale('log')    
# dz.Axis.set_xscale('log')    
#  
# dz.FigWording(r'Wavelength (microns)', r'Radiation spectrum', 'Coronal')
#  
# dz.display_fig()

# from dazer_methods import Dazer
# import os
# import numpy as np
# 
# dz = Dazer()
# dz.FigConf()
# 
# file_address = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/hii_Um3_mod.con'
# file_address = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/hii_Um3_mod.ovr'
# #Cont  nu    incident    trans    DiffOut    net trans    reflc    total    reflin    outlin    lineID    cont    nLine
# 
# nu, incident, trans, DiffOut  = np.loadtxt(file_address, usecols = (0, 1, 2,  3), unpack = True)    
# nu, incident, trans, DiffOut  = np.loadtxt(file_address, usecols = (0, 1, 2,  3), unpack = True)    
# 
# 
# dz.data_plot(nu, incident, label = 'incident')
# dz.data_plot(nu, trans, label = 'trans')
# 
# dz.Axis.set_xlim(0.001,0.1)
# # dz.Axis.set_ylim(1e5,1e25)
# # 
# # # dz.Axis.set_ylim(1e-9,1)
# dz.Axis.set_yscale('log')    
# #dz.Axis.set_xscale('log')    
# 
# dz.FigWording(r'Wavelength', r'flux', 'Continuum file components')
# 
# dz.display_fig()


# from dazer_methods import Dazer
# import os
# import numpy as np
# 
# dz = Dazer()
# dz.FigConf()
# 
# file_address = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/varyR.grd'
# file_address2 = '/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/varyR.hyd'
# 
# H_molecular = np.loadtxt(file_address2, usecols = (3), unpack = True)    
# radius = np.loadtxt(file_address, usecols = (6), unpack = True)
# 
# age = 'One'
# 
# dz.data_plot(radius, H_molecular, label = age)
# 
# # dz.Axis.set_xlim(0.01,1000)
# # dz.Axis.set_ylim(1e5,1e25)
# # 
# # # dz.Axis.set_ylim(1e-9,1)
# # dz.Axis.set_yscale('log')    
# # dz.Axis.set_xscale('log')    
# 
# dz.FigWording(r'Wavelength', r'flux', 'Cloudy Example')
# 
# dz.display_fig()