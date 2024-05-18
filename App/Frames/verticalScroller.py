from tkinter import *
from tkinter import ttk
import tkinter as tk

class VerticalScroller:
    def __init__(self, tab):
        self.tab = tab
        
        self.canvas = Canvas(self.tab)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar = Scrollbar(self.tab, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.scrolled_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrolled_frame, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event = None):
        if event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def get_scrolled_frame(self):
        return self.scrolled_frame
