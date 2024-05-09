from tkinter import *
from tkinter import ttk
import sys
sys.path.append('./GazeTracking-master/')
sys.path.append('./EyeTracker/')

from App.Tabs import mainTab
from App.Tabs import videoPlayerTab
from EyeTracker.eyeTracker import EyeTracker
from ScreenRecorderTest.videoPlayer import VideoPlayer


class App:

    updateMS = 32 #miliseconds

    currentTab = None
    eyeTracker = None

    def init(self):
        #Creación de la aplicación raíz
        self.root = Tk()
        self.root.title("Eye Tracker")
        self.root.geometry("1152x648")
        #self.root.resizable(False, False)
        self.root.after(self.updateMS, self.update_)
        #sv_ttk.set_theme("dark")

        self.eyeTracker = EyeTracker()
        self.eyeTracker.setUp()
        self.videoPlayer = VideoPlayer("./ScreenRecorderTest/video.mp4")

        # Creamos el notebok que manejará las pestañas
        self.notebook = ttk.Notebook(self.root)

        #Crear pestañas
        self.frame1 = ttk.Frame(self.root, padding = 20)
        self.frame2 = ttk.Frame(self.root, padding = 20)

        # Agregar las pestañas al notebook
        self.notebook.add(self.frame1, text="Main")
        self.notebook.add(self.frame2, text="Video Player")

        #Los hacemos pack
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.onTabChanged)
        
        # Creamos las clases que representan cada pestaña de la App
        self.mainTab = mainTab.MainTab(self.frame1, self.eyeTracker) 
        self.videoPlayerTab = videoPlayerTab.VideoPlayerTab(self.frame2, self.videoPlayer)
        
        self.mainTab.setUp()
        self.videoPlayerTab.setUp()

    def run(self):
        self.root.mainloop()

    def onTabChanged(self, event):
        return
    
    def onTabChanged(self, event):
        
        #curentTab = self.notebook.select()
        selectedTab = self.notebook.select()
        id = self.notebook.index(selectedTab)  

        if id == 0:
            self.currentTab = self.mainTab
        elif id == 1:
            self.currentTab = self.videoPlayerTab
        
        #self.currentTab.onEntryTab()
    
    def update_(self):
        if self.currentTab == None:
            return

        self.currentTab.update()
        self.root.after(self.updateMS, self.update_)