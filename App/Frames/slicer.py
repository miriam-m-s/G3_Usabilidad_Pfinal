from tkinter import *
from tkinter import ttk
import tkinter as tk

class Slicer:

    def __init__(self, tab, frame, name):

        self.frame = frame

        title_frame = tk.Frame(self.frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="w")

        button_size = 3 
        ttk.Button(title_frame, text="X", width=button_size, 
                   command=lambda : tab.deleteSlicer(self)).pack(side=tk.LEFT)
        tk.Entry(title_frame, text=tk.StringVar(value=name)).pack(side=tk.LEFT)

        from_slice_frame = tk.Frame(self.frame)
        from_slice_frame.grid(row=1, column=0, sticky="w")
        Slice(tab, from_slice_frame, "From:", 0)

        until_slice_frame = tk.Frame(self.frame)
        until_slice_frame.grid(row=1, column=1, sticky="w")
        Slice(tab, until_slice_frame, "Until:", tab.videoPlayer.duration)

class Slice:

    def __init__(self, tab, frame, text, time):

        self.tab = tab
        self.time = time

        top_frame = tk.Frame(frame)
        top_frame.grid(row=0, column=0, sticky="w")

        button_size = 3
        ttk.Button(top_frame, text="C", width=button_size, command=self.__copy).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="P", width=button_size, command=self.__paste).pack(side=tk.LEFT)
        tk.Label(top_frame, text=text).pack(side=tk.LEFT)

        bottom_frame = tk.Frame(frame)
        bottom_frame.grid(row=1, column=0, sticky="w")

        ttk.Button(bottom_frame, text="V", width=button_size, command=self.__videoTime).pack(side=tk.LEFT)
        ttk.Button(bottom_frame, text="T", width=button_size, command=self.__saveTime).pack(side=tk.LEFT)
        self.label = tk.Label(bottom_frame, text=self.tab.MMMSSMMM(self.time))
        self.label.pack(side=tk.LEFT)

    def __copy(self):
        self.tab.clipboard = self.time

    def __paste(self):
        self.time = self.tab.clipboard
        self.label.config(text=self.tab.MMMSSMMM(self.time))

    def __saveTime(self):
        self.time = self.tab.currentTime
        self.label.config(text=self.tab.MMMSSMMM(self.time))

    def __videoTime(self):
        self.tab.timeChange = self.time
