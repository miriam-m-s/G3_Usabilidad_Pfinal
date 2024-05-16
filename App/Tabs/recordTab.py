from App.Tabs.tab import Tab
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from App.Utils import jsonUtils
from App.appConsts import Consts

class RecordTab(Tab):

    playing = False

    def __init__(self, tab):
        self.tab = tab

    def set_up(self):
        self.play_button = ttk.Button(self.tab, text="Play", command=self.play, takefocus=False)
        self.stop_button = ttk.Button(self.tab, text="Stop", command = self.stop, takefocus=False)
        self.warning_label = ttk.Label(self.tab, text="Eye tracker sin calibrar o mal calibrado", foreground="red")

    def on_entry_tab(self):
        return

    def update(self, dt):
        return

    def show_buttons(self):
        self.warning_label.pack_forget()
        self.play_button.pack()
        self.stop_button.pack()

    def hide_buttons(self):
        self.play_button.pack_forget()
        self.stop_button.pack_forget()
        self.warning_label.pack()

    def play(self):
        print("Play no implementado")
        self.playing = True
        return
    
    def stop(self):
        self.playing = False

    def on_entry_tab(self):
        try:
            jsonObj = jsonUtils.recover_json_from_file(Consts.APP_DATA_PATH)
            if(jsonObj['bottom'] > jsonObj['up'] and jsonObj['screen_width'] > 0):
                self.show_buttons()
            else:
                self.hide_buttons()
        except:
            self.hide_buttons()