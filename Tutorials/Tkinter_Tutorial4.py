'''
Created on May 2, 2015

@author: vital
'''

import matplotlib
matplotlib.use('TkAgg')
import ttk
import Tkinter as Tk
from matplotlib.backends.backend_tkagg  import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure                  import Figure
import  matplotlib.widgets  as widgets

from    DZ_ScreenManager    import Plots_Manager


def on_key_event(event):
    print('you pressed %s'%event.key)
#     key_press_handler(event, canvas, toolbar)

def Span_Manager(Wlow,Whig):
    
    print Wlow, Whig
    
    return


root = Tk.Tk()
root.wm_title("Dazer")

pv                         = Plots_Manager()

pv.FigFormat_One(ColorConf = 'Night', StoreParameters = False)

CodeName, FileName, FileFolder = pv.FileAnalyzer('/home/vital/Dropbox/Astrophysics/Data/WHT_HII_Galaxies/08/'+'obj08_WHT.fits')

Wave, Int, ExtraData = pv.File2Data(FileFolder, FileName)

pv.DataPloter_One(Wave, Int, 'Flux', pv.Color_Vector[2][1])

canvas = FigureCanvasTkAgg(pv.Fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg( canvas, root )
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

canvas.mpl_connect('key_press_event', on_key_event)
Span = widgets.SpanSelector(pv.Axis1, Span_Manager, 'horizontal', useblit=False, rectprops=dict(alpha=1, facecolor='Blue'))


Tk.mainloop()
