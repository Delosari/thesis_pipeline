import pyfits
import numpy as np
from StringIO import StringIO 
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('legend', frameon=True)
# modulos propios

# Lectura del fichero del espectro con los valores del continuo
def lectura_espectro(input_file):
    entrada = open(input_file, "r")
    lines = entrada.readlines()
    entrada.close()
    spec_ldo = []
    spec_flux = []
    for line in lines:
        if not line.startswith("#"):
           p = line.split()
           spec_ldo.append(float(p[0]))
           spec_flux.append(float(p[1]))
    return(spec_ldo,spec_flux)


#Esta es la funcion que se ejecuta al hacer click
def coordinates_on_click(event, axis= None, mousebottom = 3):
    x, y = event.x, event.y
     
    #Este numero decide el boton del raton: 1 para izquierdo, 3 para derecho.
    if event.button == mousebottom:   
        if event.inaxes is not None:
            print '-Coordiantes  {} {}'.format(event.xdata, event.ydata)  
             
            #Estas lineas intentan encontrar a que curva (si esta tiene label) pertenecen los datos                      
            if axis != None: 
                for curve in axis.get_lines():
                    if curve.contains(event)[0]:
                        curve_label = curve.get_label()
                        if curve_label[0] != '_':
                            print '--Curve: {}'.format(curve_label)

c_speed = 299792.458   # km/s, speed of light

input_file = 'spec_select.spec'
spec_ldo,spec_flux = lectura_espectro(input_file)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(spec_ldo,spec_flux,label = input_file,color = 'red')
plt.xlabel(r'LDO, $\AA$')
leyenda = plt.legend(loc = 1)
marco = leyenda.get_frame()
marco.set_facecolor('white')
marco.set_edgecolor('red')
 
#Esta linea conecta tu plot a un proceso cando clickeas
mouse_button = {'left':1, 'right':3}
coordinates = plt.connect('button_press_event', lambda event: coordinates_on_click(event, ax, mouse_button['right']))
 
plt.show()

