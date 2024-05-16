from App.Tabs.tab import Tab
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

class RecordTab(Tab):

    playing = False

    def __init__(self, tab):
        self.tab = tab

    def set_up(self):
        self.play_button = ttk.Button(self.tab, text="Play", command=self.play, takefocus=False)
        self.calibrate_button = ttk.Button(self.tab, text="Stop", command = self.start_calibration, takefocus=False)

        return

    def on_entry_tab(self):
        return

    def update(self, dt):
        return

    def show_buttons(self):
        self.play_button.pack()
        self.calibrate_button.pack()

    def hide_buttons(self):
        self.play_button.pack_forget()
        self.calibrate_button.pack_forget()

    def play(self):
        print("Plat no implementado")
        self.playing = True
        return
    
    def stop(self):
        self.playing = False