import tkinter as tk


class lsys_gui:
    def __init__(self, parent):
        self.parent = parent
        self.state = 'css'
        self.init_form()
        self.init_commands()


    def init_form(self):
        self.parent.title('LTI analysis')

        def drawABCD():
            self.frame_entry_labels = tk.Frame(self.parent)
            self.frame_entry_labels.pack(side='left')
            self.labelA = tk.Label(self.frame_entry_labels, text='A = ').pack()
            self.labelB = tk.Label(self.frame_entry_labels, text='B = ').pack()
            self.labelC = tk.Label(self.frame_entry_labels, text='C = ').pack()
            self.labelD = tk.Label(self.frame_entry_labels, text='D = ').pack()

            self.frame_entry = tk.Frame(self.parent)
            self.frame_entry.pack(side='left')
            self.entryA = tk.Entry(self.frame_entry, width=30).pack(padx=2, pady=2)
            self.entryB = tk.Entry(self.frame_entry, width=30).pack(padx=2, pady=2)
            self.entryC = tk.Entry(self.frame_entry, width=30).pack(padx=2, pady=2)
            self.entryD = tk.Entry(self.frame_entry, width=30).pack(padx=2, pady=2)

        def drawTF():
            self.frame_entry_labels = tk.Frame(self.parent)
            self.frame_entry_labels.pack(side='left')
            self.labelNum = tk.Label(self.frame_entry_labels, text='Numerator ').pack(anchor='w')
            self.labelDen = tk.Label(self.frame_entry_labels, text='Denominator ').pack()

            self.frame_entry = tk.Frame(self.parent)
            self.frame_entry.pack(side='left')
            self.entryNum = tk.Entry(self.frame_entry, width=30).pack(padx=2, pady=2)
            self.entryDen = tk.Entry(self.frame_entry, width=30).pack(padx=2, pady=2)

        def draw_discrete():
            self.labelT = tk.Label(self.frame_entry_labels, text='T= ').pack(anchor='w')
            self.entryT = tk.Entry(self.frame_entry, width=5).pack(padx=2, pady=2)

        def select_mode():
            self.frame_entry_labels.destroy()
            self.frame_entry.destroy()
            if self.sstf.get() == 0:
                drawABCD()
            else:
                drawTF()
            if self.cd.get() == 1:
                    draw_discrete()

        frame_cd = tk.Frame()
        frame_cd.pack(side='left')
        self.cd = tk.BooleanVar()
        self.cd.set(0)
        self.radioc = tk.Radiobutton(frame_cd, text='Continuous', variable=self.cd, value=0,
                                     command=select_mode)
        self.radioc.pack(anchor='nw')
        self.radiod = tk.Radiobutton(frame_cd, text='Discrete', variable=self.cd, value=1,
                                     command=select_mode)
        self.radiod.pack(anchor='nw')

        frame_sstf = tk.Frame()
        frame_sstf.pack(side='left')
        self.sstf = tk.BooleanVar()
        self.sstf.set(0)
        self.radioss = tk.Radiobutton(frame_sstf, text='State space', variable=self.sstf, value=0,
                                     command=select_mode)
        self.radioss.pack(anchor='nw')
        self.radiotf = tk.Radiobutton(frame_sstf, text='Transfer function', variable=self.sstf, value=1,
                                     command=select_mode)
        self.radiotf.pack(anchor='nw')

        drawABCD()

    def init_commands(self):
        pass


root = tk.Tk()
my_gui = lsys_gui(root)
root.mainloop()
