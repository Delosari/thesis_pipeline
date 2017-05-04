import Tkinter as tk
import ttk
import  matplotlib.widgets  as widgets

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg  import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure                  import Figure
from matplotlib                         import pyplot as plt


LARGE_FONT= ("Verdana", 12)

Fig = Figure(figsize=(5,5), dpi=100)
Axis = Fig.add_subplot(111)
Axis.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])




        
def Span_Manager(Wlow,Whig):
    
    print Wlow, Whig
    
    return

def Key_Manager(event): 

    print event.key      

class ScreenSwitcher(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Dazer")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Screen in [PageInitial]:

            frame = Screen(container, self)

            self.frames[Screen] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageInitial)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class PageInitial(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
            command=lambda: controller.show_frame(PageInitial))
        button1.pack()

        canvas = FigureCanvasTkAgg(Fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
GUI             = ScreenSwitcher()
Span            = widgets.SpanSelector(Axis, Span_Manager, 'horizontal', useblit=False, rectprops=dict(alpha=1, facecolor='Blue'))

GUI.mainloop()