import Tkinter as tk
import tkFileDialog
import datetime

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.windows = []
        menubar = tk.Menu(self)
        self.configure(menu=menubar)
        fileMenu = tk.Menu(self)
        fileMenu.add_command(label="New...", command=self.new_window)
        fileMenu.add_command(label="Save All", command=self.save_all)
        menubar.add_cascade(label="Window", menu=fileMenu)
        label = tk.Label(self, text="Select 'New' from the window menu")
        label.pack(padx=20, pady=40)

    def save_all(self):
        # ask each window object, which is acting both as 
        # the view and controller, to save it's data
        for window in self.windows:
            window.save()

    def new_window(self):
        filename = tkFileDialog.askopenfilename()
        if filename is not None:
            self.windows.append(TileWindow(self, filename))

class TileWindow(tk.Toplevel):
    def __init__(self, master, filename):
        tk.Toplevel.__init__(self, master)
        self.title("%s - Tile Editor" % filename)
        self.filename = filename
        # create an instance of a TileSet; all other
        # methods in this class can reference this
        # tile set
        self.tileset = TileSet(filename)
        label = tk.Label(self, text="My filename is %s" % filename)
        label.pack(padx=20, pady=40)
        self.status = tk.Label(self, text="", anchor="w")
        self.status.pack(side="bottom", fill="x")

    def save(self):
        # this method acts as a controller for the data,
        # allowing other objects to request that the 
        # data be saved
        now = datetime.datetime.now()
        self.status.configure(text="saved %s" % str(now))

class TileSet(object):
    def __init__(self, filename):
        self.data = "..."

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()