from Tkinter import Tk, StringVar
import ttk

class Application:

    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, 
                                state='readonly')
        self.box['values'] = ('A', 'B', 'C')
        self.box.current(0)
        self.box.grid(column=0, row=0)

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
    
root = Tk()

value = StringVar()
box = ttk.Combobox(root, textvariable=value, state='readonly')
box['values'] = ('A', 'B', 'C')
box.current(1)
box.grid(column=0, row=0)

root.mainloop()