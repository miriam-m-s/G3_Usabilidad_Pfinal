from tkinter import *
from tkinter import ttk
import sys
sys.path.append('./GazeTracking-master/')
sys.path.append('./EyeTracker/')

from App.Tabs import calibrationTab
from App.Tabs import videoPlayerTab
from EyeTracker.eyeTracker import EyeTracker

import time

class App:

    cap = 1 / 60
    capMS = round(cap * 1000)

    currentTab = None
    eyeTracker = None

    init_window_width = 1200
    init_window_height = 650

    def init(self):
        #Creación de la aplicación raíz
        self.root = Tk()
        self.root.title("Eye Tracker")
        self.root.geometry(f"{self.init_window_width}x{self.init_window_height}")
        #print(f"Width: {self.root.winfo_screenwidth()}, Height: {self.root.winfo_height()}")
        #self.root.resizable(False, False)
        self.root.after(1000, self.__update)
        #sv_ttk.set_theme("dark")

        self.eyeTracker = EyeTracker()
        self.eyeTracker.setUp()

        # Creamos el notebok que manejará las pestañas
        self.notebook = ttk.Notebook(self.root)

        #Crear pestañas
        self.frame1 = ttk.Frame(self.root, padding = 0)
        self.frame2 = ttk.Frame(self.root, padding = 0)

        # Agregar las pestañas al notebookªª
        self.notebook.add(self.frame1, text="Calibration")
        self.notebook.add(self.frame2, text="Video Player")

        #Los hacemos pack
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Creamos las clases que representan cada pestaña de la App
        self.mainTab = calibrationTab.CalibrationTab(self.frame1, self.eyeTracker, self) 
        self.videoPlayerTab = videoPlayerTab.VideoPlayerTab(self.frame2)
        
        self.mainTab.set_up()
        self.videoPlayerTab.set_up()  

        self.root.bind    ('<Key>', self.key_pressed)  

    def set_fullscreen(self, fullscren):
        self.root.attributes("-fullscreen", fullscren)
        self.fullscreen = fullscren

    def getWindowWidth(self): 
        return self.root.winfo_width()
    
    def getWindowHeight(self):
        return self.root.winfo_height()
    
    def run(self):
        self.lastUpdateTime = 0
        self.root.mainloop()

    
    def on_tab_changed(self, event):
        
        #curentTab = self.notebook.select()
        selectedTab = self.notebook.select()
        id = self.notebook.index(selectedTab)  

        if id == 0:
            self.currentTab = self.mainTab
        elif id == 1:
            self.currentTab = self.videoPlayerTab
        
        #self.currentTab.onEntryTab()
    
    def __update(self):
        currentTime = time.time()
        dt = currentTime - self.lastUpdateTime
        self.lastUpdateTime = currentTime

        if self.currentTab is not None:
            self.currentTab.update(dt)

        # Hace la resta para esperarse
        # waitTime = max(0, self.cap - dt)
        # self.root.after(round(waitTime * 1000), self.__update)

        # Se espera siempre
        self.root.after(self.capMS, self.__update)

        # FPS máximos
        # self.root.after(10, self.__update)

    def key_pressed(self, event):
        if self.currentTab is not None:
            self.currentTab.key_pressed(event)