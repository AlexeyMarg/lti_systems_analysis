import tkinter as tk


class lsys_gui:
    def __init__(self, parent):
        self.parent = parent
        self.init_form()
        self.init_commands()


    def init_form(self):
        self.parent.title('LTI analysis')

        def drawABCD():
            self.frame_entry_labels = tk.Frame(self.parent)
            self.frame_entry_labels.pack(side='left', anchor='n')
            self.labelA = tk.Label(self.frame_entry_labels,
                                   text='A = ').pack()
            self.labelB = tk.Label(self.frame_entry_labels,
                                   text='B = ').pack()
            self.labelC = tk.Label(self.frame_entry_labels,
                                   text='C = ').pack()
            self.labelD = tk.Label(self.frame_entry_labels,
                                   text='D = ').pack()

            self.frame_entry = tk.Frame(self.parent)
            self.frame_entry.pack(side='left', anchor='n')
            self.entryA = tk.Entry(self.frame_entry,
                                   width=30).pack(padx=2, pady=2)
            self.entryB = tk.Entry(self.frame_entry,
                                   width=30).pack(padx=2, pady=2)
            self.entryC = tk.Entry(self.frame_entry,
                                   width=30).pack(padx=2, pady=2)
            self.entryD = tk.Entry(self.frame_entry,
                                   width=30).pack(padx=2, pady=2)

        def drawTF():
            self.frame_entry_labels = tk.Frame(self.parent)
            self.frame_entry_labels.pack(side='left', anchor='n')
            self.labelNum = tk.Label(self.frame_entry_labels,
                                     text='Numerator ').pack(anchor='w')
            self.labelDen = tk.Label(self.frame_entry_labels,
                                     text='Denominator ').pack()

            self.frame_entry = tk.Frame(self.parent)
            self.frame_entry.pack(side='left', anchor='n')
            self.entryNum = tk.Entry(self.frame_entry,
                                     width=30).pack(padx=2, pady=2)
            self.entryDen = tk.Entry(self.frame_entry,
                                     width=30).pack(padx=2, pady=2)

        def draw_discrete():
            self.labelT = tk.Label(self.frame_entry_labels,
                                   text='T= ').pack(anchor='w')
            self.entryT = tk.Entry(self.frame_entry,
                                   width=5).pack(padx=2, pady=2)

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
        frame_cd.pack(side='left', anchor='n')
        self.cd = tk.BooleanVar()
        self.cd.set(0)
        self.radioc = tk.Radiobutton(frame_cd,
                                     text='Continuous',
                                     variable=self.cd,
                                     value=0,
                                     command=select_mode).pack(anchor='nw')

        self.radiod = tk.Radiobutton(frame_cd,
                                     text='Discrete',
                                     variable=self.cd,
                                     value=1,
                                     command=select_mode).pack(anchor='nw')

        frame_sstf = tk.Frame()
        frame_sstf.pack(side='left', anchor='n')
        self.sstf = tk.BooleanVar()
        self.sstf.set(0)
        self.radioss = tk.Radiobutton(frame_sstf,
                                      text='State space',
                                      variable=self.sstf,
                                      value=0,
                                      command=select_mode).pack(anchor='nw')
        self.radiotf = tk.Radiobutton(frame_sstf,
                                      text='Transfer function',
                                      variable=self.sstf,
                                      value=1,
                                      command=select_mode).pack(anchor='nw')
        drawABCD()

        self.label_result = tk.Label(justify='left', font=('Arial', '10'),
                                     text='Stability: \n'
                                     'Observability: \n'
                                     'Controllability: \n'
                                     'Overshoot: \n'
                                     'Poles: \n'
                                     'Transient time: \n'
                                     'Oscillation coefficient: \n'
                                     'Damping coefficient: ')
        self.label_result.place(x=10, y=120)

        self.bcalc = tk.Button(text='Calculate')
        self.bcalc.place(x=10, y=60)

        self.bplot = tk.Button(text='Plot', width=9)
        self.bplot.place(x=100, y=60)

    def init_commands(self):
        def bcalc_pressed(event):
            pass

        self.bcalc.bind(bcalc_pressed)


root = tk.Tk()
root.geometry('500x300')
my_gui = lsys_gui(root)
root.mainloop()
