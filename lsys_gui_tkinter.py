import tkinter as tk
from tkinter import messagebox as mb
import numpy as np
import lsys
import ast


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
                                   width=30)
            self.entryA.insert(0, '[[0,1],[-1, -2]]')
            self.entryA.pack(padx=2, pady=2)
            self.entryB = tk.Entry(self.frame_entry,
                                   width=30)
            self.entryB.insert(0, '[[0],[1]]')
            self.entryB.pack(padx=2, pady=2)
            self.entryC = tk.Entry(self.frame_entry,
                                   width=30)
            self.entryC.insert(0, '[[1, 0]]')
            self.entryC.pack(padx=2, pady=2)
            self.entryD = tk.Entry(self.frame_entry,
                                   width=30)
            self.entryD.insert(0, '[[0]]')
            self.entryD.pack(padx=2, pady=2)

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
                                     width=30)
            self.entryNum.insert(0, '[1]')
            self.entryNum.pack(padx=2, pady=2)
            self.entryDen = tk.Entry(self.frame_entry,
                                     width=30)
            self.entryDen.insert(0, '[1, 1]')
            self.entryDen.pack(padx=2, pady=2)

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

    def make_sys(self):
        if self.sstf.get() == 0:
            s = self.entryA.get()
            A = np.array(ast.literal_eval(s))
            s = self.entryB.get()
            B = np.array(ast.literal_eval(s))
            s = self.entryC.get()
            C = np.array(ast.literal_eval(s))
            s = self.entryD.get()
            D = np.array(ast.literal_eval(s))
            if self.cd.get() == 0:
                plant = lsys.SSC(A, B, C, D)
            else:
                T = float(self.entryT.get())
                plant = lsys.SSD(A, B, C, D, T)
        else:
            s = self.entryNum.get()
            num = np.array(ast.literal_eval(s))
            s = self.entryDen.get()
            den = np.array(ast.literal_eval(s))
            if self.cd.get() == 0:
                plant = lsys.TFC(num, den)
            else:
                T = float(self.entryT.get())
                plant = lsys.TFD(num, den, T)
        return plant

    def init_commands(self):

        def bcalc_pressed(event):
            try:
                plant = self.make_sys()
            except:
                mb.showerror("Error!", "Wrong input data")
            else:
                s = ''
                if lsys.stable(plant):
                    s = 'Stability: ' + 'true\n'
                else:
                    s = 'Stability: ' + 'false\n'
                if lsys.observable(plant):
                    s = s + 'Observability: ' + 'true\n'
                else:
                    s = s + 'Observability: ' + 'false\n'
                if lsys.controlable(plant):
                    s = s + 'Controlability: ' + 'true\n'
                else:
                    s = s + 'Controlability: ' + 'false\n'
                if lsys.stable(plant):
                    s = s + 'Overshoot: ' + str(lsys.overshoot(plant)) + '\n'
                else:
                    s = s + 'Overshoot: -'
                if lsys.stable(plant):
                    s = s + 'Transient time: ' + str(lsys.transient_time(plant)) + '\n'
                else:
                    s = s + 'Transient time: -'
                if lsys.stable(plant):
                    s = s + 'Oscillation coefficient: ' + str(lsys.oscillation_coef(plant)) + '\n'
                else:
                    s = s + 'Oscillation coefficient: -'
                if lsys.stable(plant):
                    s = s + 'Damping coefficient: ' + str(lsys.damping_coef(plant)) + '\n'
                else:
                    s = s + 'Damping coefficient: -'
                s = s + 'Poles: ' + str(lsys.poles(plant)) + '\n'
                self.label_result['text'] = s

        self.bcalc.bind('<Button-1>', bcalc_pressed)


root = tk.Tk()
root.geometry('500x300')
my_gui = lsys_gui(root)
root.mainloop()
