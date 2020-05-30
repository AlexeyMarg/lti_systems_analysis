import tkinter as tk

class lsys_gui:
    def __init__(self, parent):
        self.parent = parent
        self.init_form()
        self.init_commands()

    def init_form(self):
        self.parent.title('LTI analysis')

    def init_commands(self):
        pass

root = tk.Tk()
my_gui = lsys_gui(root)
root.mainloop()