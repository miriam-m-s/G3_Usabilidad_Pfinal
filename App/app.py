from tkinter import *
from tkinter import ttk
import sys
sys.path.append('./GazeTracking-master/')
sys.path.append('./EyeTracker/')

from App.Tabs import mainTab
from eyeTracker import EyeTracker


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

        # Creamos el notebok que manejará las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.eyeTracker = EyeTracker()
        self.eyeTracker.setUp()
        #Crear pestañas
        self.frame1 = ttk.Frame(self.root, padding = 20)

        # Agregar las pestañas al notebook
        self.notebook.add(self.frame1, text="Main")

        #Los hacemos pack
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.onTabChanged)
        
        # Creamos las clases que representan cada pestaña de la App
        self.mainTab = mainTab.MainTab(self.frame1, self.eyeTracker) 
        
        self.mainTab.setUp()
        
    def getWindowWidth(self): 
        return self.root.winfo_width()
    
    def getWindowHeight(self):
        return self.root.winfo_height()
    
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
        
        #self.currentTab.onEntryTab()
    
    def update_(self):
        if self.currentTab == None:
            return

        self.currentTab.update()
        self.root.after(self.updateMS, self.update_)