import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import *
from tkinter.constants import DISABLED, NORMAL

import matplotlib
from matplotlib.colors import ListedColormap, LogNorm
import matplotlib.pyplot as plt
from PIL import Image as im
from PIL import ImageTk as imTk

from dicalum.coeffs  import *
from dicalum.DclPlot import *
from dicalum.RawRead import *
from dicalum.SetVig  import *

__all__ = ['DclGui']

global f1update
kRevIm=1

def rawr():
    rfile = tk.filedialog.askopenfilename()
    dcld = rawread(rfile,0,0,0,1)
    if (dcld!=-1):
       f1update(dcld.fce)
       dcldat.V = dcld.V
       dcldat.M = dcld.M
       dcldat.R = dcld.R
       dcldat.G = dcld.G
       dcldat.B = dcld.B
       dcldat.D = dcld.D
       dcldat.img = dcld.img
       dcldat.fce = dcld.fce
       dcldat.expo = dcld.expo
       dcldat.max = dcld.max

def darkr():
    rfile = tk.filedialog.askopenfilename()
    darkv = darkread(rfile)
    dcldat.dark = darkv

def revIm():
    global kRevIm
    imRGB=dcldat.fce
    if (kRevIm==1):
        imRGB=dcldat.img
    f1update(imRGB)
    kRevIm=1-kRevIm

class DclFr00(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(text="Instrument", relief=tk.RIDGE)
        self.__create_widgets()
    def __create_widgets(self):
        def SetCamera(event):
            camsel = event.widget.get()
            dclinst.camera = cameras.index(camsel)
            SetLensForCamera()
            dummy=setvig()
        def SetLensForCamera():
            lenloc = []
            leka = CamList[dclinst.camera].lens
            k=0
            for le in lenses:
               if (leka[k]==1):
                  lenloc.append(le)
               k=k+1
            cbd['values'] = lenloc
            dclinst.lens=lenses.index(lenloc[0])
            cbd.current(0)
        def SetLens(event):
            lensel = event.widget.get()
            dclinst.lens=lenses.index(lensel)
            dummy=setvig()
        ttk.Label(self, text="Camera: ").grid(row=1, column=1, sticky=tk.W + tk.N)
        ttk.Label(self, text="Lens: ").grid(row=2, column=1, sticky=tk.W + tk.N)
        self.camera_value = tk.StringVar()
        cbb=ttk.Combobox(self, height=8, textvariable=self.camera_value)
        cbb.grid(row=1, column=2)
        cbb['values'] = cameras
        cbb.current(dclinst.camera)
        cbb.bind("<<ComboboxSelected>>", SetCamera)
        self.lens_value = tk.StringVar()
        cbd=ttk.Combobox(self, height=8, textvariable=self.lens_value)
        cbd.grid(row=2, column=2)
        #cbd['values'] = lenses
        #cbd.current(dclinst.lens)
        SetLensForCamera()
        dummy=setvig()

        cbd.bind("<<ComboboxSelected>>", SetLens)
        for widget in self.winfo_children():
            widget.grid(padx=3, pady=3)
class DclFr01(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(text="Input", relief=tk.RIDGE)
        self.__create_widgets()

    def __create_widgets(self):
        self.min = tk.StringVar()
        self.min.set(2.5)
        ttk.Button(self, text="RAW Read", command=rawr ).grid(column=1, row=1)
        ttk.Button(self, text="dsu Plot", command=lambda: DclPlot(0,float(En_low.get()),float(En_sat.get())) ).grid(column=2, row=2)
        ttk.Button(self, text="dsu LogPlot", command=lambda: DclPlot(1,float(En_low.get()),float(En_sat.get())) ).grid(column=3, row=2)
        ttk.Button(self, text="MPSAS Plot", command=lambda: DclPlot(2,float(En_low.get()),float(En_sat.get())) ).grid(column=4, row=2)
        ttk.Button(self, text="Histogram", command=lambda: DclHist()).grid(column=1, row=2)
        ttk.Label(self, text="min/max:").grid(column=2, row=1)
        self.min_w = ttk.Entry(self, textvariable=En_low, width=8).grid(row=1, column=3)
        self.max_w = ttk.Entry(self, textvariable=En_sat, width=10).grid(row=1, column=4)

        for widget in self.winfo_children():
            widget.grid(padx=3, pady=3)

class DclFr10a(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(text="Exposure", relief=tk.RIDGE)
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Label(self, text="ISO: ").grid(row=1, column=1, sticky=tk.W + tk.N)
        ttk.Label(self, text="Shutter: ").grid(row=2, column=1, sticky=tk.W + tk.N)
        ttk.Label(self, text="Aperture: ").grid(row=3, column=1, sticky=tk.W + tk.N)
        En_iso_w = ttk.Entry(self, textvariable=En_iso).grid(row=1, column=2, sticky=tk.W + tk.N)
        En_shu_w = ttk.Entry(self, textvariable=En_shu).grid(row=2, column=2, sticky=tk.W + tk.N)
        En_ape_w = ttk.Entry(self, textvariable=En_ape).grid(row=3, column=2, sticky=tk.W + tk.N)

        for widget in self.winfo_children():
            widget.grid(padx=3, pady=3)

class DclFr10b(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(text="Dark Level", relief=tk.RIDGE)
        self.__create_widgets()

    def __create_widgets(self):
        rbvar = tk.IntVar()
        def SetDark():
            dsel = rbvar.get()
            if (dsel==2):
               self.bu['state'] = NORMAL
            else:
               self.bu['state'] = DISABLED
        rba=ttk.Radiobutton(self,text="Default camera value",command=SetDark, variable=rbvar, value=0)
        rbb=ttk.Radiobutton(self,text="Corners (for fisheye lens)", command=SetDark, variable=rbvar, value=1)
        rbc=ttk.Radiobutton(self,text="Dark frame", command=SetDark, variable=rbvar, value=2)
        rba.grid(row=1, column=1,sticky=tk.W)
        rbb.grid(row=2, column=1,sticky=tk.W)
        rbc.grid(row=3, column=1,sticky=tk.W)
        self.bu=ttk.Button(self, text="Dark RAW Read", command=darkr)
        self.bu.grid(column=1, row=4)
        rbb['state'] = DISABLED
        self.bu['state'] = DISABLED

        for widget in self.winfo_children():
            widget.grid(padx=3, pady=3)

class DclFr10(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(text="", relief=tk.FLAT)
        self.__create_widgets()

    def __create_widgets(self):
        dcl10a_frame = DclFr10a(self)
        dcl10a_frame.grid(column=1, row=1)
        dcl10b_frame = DclFr10b(self)
        dcl10b_frame.grid(column=1, row=2)
        for widget in self.winfo_children():
            widget.grid(padx=0, pady=3)


class DclFr11(ttk.LabelFrame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(text="Photo", relief=tk.RIDGE)
        self.__create_widgets()

    def __create_widgets(self):
        global f1update
        button = ttk.Button(self, command=revIm)
        button.grid(row=1, column=1)
        def f1update(imRGB):
           self.buttonPhoto = imTk.PhotoImage(imRGB)
           button.configure(image=self.buttonPhoto)
        TestData = np.random.rand(200, 300)
        RGBa = (np.dstack((0.2*TestData,0.5*(1-TestData),TestData)) * 255.999) .astype(np.uint8)
        imRGB = im.fromarray(RGBa)
        self.buttonPhoto = imTk.PhotoImage(imRGB)
        button.configure(image=self.buttonPhoto)


class DclGui():
    def __init__(self):
        self.window = TopWin
        self.window.title("DiCaLum 3.95")
        self.create_widgets()

    def create_widgets(self):
        self.window['padx'] = 6
        self.window['pady'] = 6

        dcl00_frame = DclFr00(self.window)
        dcl00_frame.grid(column=1, row=1, sticky=tk.W + tk.N)

        dcl01_frame = DclFr01(self.window)
        dcl01_frame.grid(column=2, row=1, sticky=tk.W + tk.N)

        dcl10_frame = DclFr10(self.window)
        dcl10_frame.grid(column=1, row=2, sticky=tk.W + tk.N)

        dcl11_frame = DclFr11(self.window)
        dcl11_frame.grid(column=2, row=2, sticky=tk.W + tk.N)


        quit_button = ttk.Button(self.window, text="Quit", command=self.window.destroy)
        quit_button.grid(row=2, column=3)


