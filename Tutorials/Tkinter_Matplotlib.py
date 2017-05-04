#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Embedding in TK")


f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0,3.0,0.01)
s = sin(2*pi*t)

a.plot(t,s)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg( canvas, root )
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def on_key_event(event):
    print('you pressed %s'%event.key)
#     key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()



















# #!/usr/bin/env python
# 
# #!/usr/bin/env python
# """
# show how to add a matplotlib FigureCanvasGTK or FigureCanvasGTKAgg widget and
# a toolbar to a gtk.Window
# """
# import gtk
# 
# from matplotlib.figure import Figure
# from numpy import arange, sin, pi
# 
# # uncomment to select /GTK/GTKAgg/GTKCairo
# #from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
# from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
# #from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas
# 
# # or NavigationToolbar for classic
# #from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
# from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
# 
# # implement the default mpl key bindings
# from matplotlib.backend_bases import key_press_handler
# 
# win = gtk.Window()
# win.connect("destroy", lambda x: gtk.main_quit())
# win.set_default_size(400,300)
# win.set_title("Embedding in GTK")
# 
# vbox = gtk.VBox()
# win.add(vbox)
# 
# fig = Figure(figsize=(5,4), dpi=100)
# ax = fig.add_subplot(111)
# t = arange(0.0,3.0,0.01)
# s = sin(2*pi*t)
# 
# ax.plot(t,s)
# 
# 
# canvas = FigureCanvas(fig)  # a gtk.DrawingArea
# vbox.pack_start(canvas)
# toolbar = NavigationToolbar(canvas, win)
# vbox.pack_start(toolbar, False, False)
# 
# 
# def on_key_event(event):
#     print('you pressed %s'%event.key)
#     key_press_handler(event, canvas, toolbar)
# 
# canvas.mpl_connect('key_press_event', on_key_event)
# 
# win.show_all()
# gtk.main()
#  
# # Tk.mainloop()
# # If you put root.destroy() here, it will cause an error if
# # the window is closed with the window manager.e
# 
# 
# # !/usr/bin/env python
# #  """
# #  demonstrate NavigationToolbar with GTK3 accessed via pygobject
# #  """
#  
# # from gi.repository import Gtk
# # 
# # from matplotlib.figure import Figure
# # from numpy import arange, sin, pi
# # from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
# # from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
# # 
# # win = Gtk.Window()
# # win.connect("delete-event", Gtk.main_quit )
# # win.set_default_size(400,300)
# # win.set_title("Embedding in GTK")
# # 
# # f = Figure(figsize=(5,4), dpi=100)
# # a = f.add_subplot(1,1,1)
# # t = arange(0.0,3.0,0.01)
# # s = sin(2*pi*t)
# # a.plot(t,s)
# # 
# # vbox = Gtk.VBox()
# # win.add(vbox)
# # 
# # # Add canvas to vbox
# # canvas = FigureCanvas(f)  # a Gtk.DrawingArea
# # vbox.pack_start(canvas, True, True, 0)
# # 
# # # Create toolbar
# # toolbar = NavigationToolbar(canvas, win)
# # vbox.pack_start(toolbar, False, False, 0)
# # 
# # win.show_all()
# # Gtk.main()
# 
# #!/usr/bin/env python
# 
# # """
# # Example of embedding matplotlib in an application and interacting with
# # a treeview to store data.  Double click on an entry to update plot
# # data
# # 
# # """
# # import pygtk
# # pygtk.require('2.0')
# # import gtk
# # from gtk import gdk
# # 
# # import matplotlib
# # matplotlib.use('GTKAgg')  # or 'GTK'
# # from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
# # 
# # from numpy.random import random
# # from matplotlib.figure import Figure
# # 
# # 
# # class DataManager(gtk.Window):
# #     numRows, numCols = 20,10
# # 
# #     data = random((numRows, numCols))
# # 
# #     def __init__(self):
# #         gtk.Window.__init__(self)
# #         self.set_default_size(600, 600)
# #         self.connect('destroy', lambda win: gtk.main_quit())
# # 
# #         self.set_title('GtkListStore demo')
# #         self.set_border_width(8)
# # 
# #         vbox = gtk.VBox(False, 8)
# #         self.add(vbox)
# # 
# #         label = gtk.Label('Double click a row to plot the data')
# # 
# #         vbox.pack_start(label, False, False)
# # 
# #         sw = gtk.ScrolledWindow()
# #         sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
# #         sw.set_policy(gtk.POLICY_NEVER,
# #                       gtk.POLICY_AUTOMATIC)
# #         vbox.pack_start(sw, True, True)
# # 
# #         model = self.create_model()
# # 
# #         self.treeview = gtk.TreeView(model)
# #         self.treeview.set_rules_hint(True)
# # 
# # 
# #         # matplotlib stuff
# #         fig = Figure(figsize=(6,4))
# # 
# #         self.canvas = FigureCanvas(fig)  # a gtk.DrawingArea
# #         vbox.pack_start(self.canvas, True, True)
# #         ax = fig.add_subplot(111)
# #         self.line, = ax.plot(self.data[0,:], 'go')  # plot the first row
# # 
# #         self.treeview.connect('row-activated', self.plot_row)
# #         sw.add(self.treeview)
# # 
# #         self.add_columns()
# # 
# #         self.add_events(gdk.BUTTON_PRESS_MASK |
# #                         gdk.KEY_PRESS_MASK|
# #                         gdk.KEY_RELEASE_MASK)
# # 
# # 
# #     def plot_row(self, treeview, path, view_column):
# #         ind, = path  # get the index into data
# #         points = self.data[ind,:]
# #         self.line.set_ydata(points)
# #         self.canvas.draw()
# # 
# # 
# #     def add_columns(self):
# #         for i in range(self.numCols):
# #             column = gtk.TreeViewColumn('%d'%i, gtk.CellRendererText(), text=i)
# #             self.treeview.append_column(column)
# # 
# # 
# #     def create_model(self):
# #         types = [float]*self.numCols
# #         store = gtk.ListStore(*types)
# # 
# #         for row in self.data:
# #             store.append(row)
# #         return store
# # 
# # 
# # manager = DataManager()
# # manager.show_all()
# # gtk.main()
