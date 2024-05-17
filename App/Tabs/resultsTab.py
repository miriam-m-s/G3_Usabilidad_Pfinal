from tkinter import *
from tkinter import ttk
from App.Tabs.tab import Tab

from App.Frames.verticalScroller import VerticalScroller

class ResultsTab(Tab):
    json_path = "questions.json"
    sangria = 50
    
    def __init__(self, tab):
        self.tab = tab

    def set_up(self):
        
        self.vertical_scroller = VerticalScroller(self.tab)
        self.scrolled_frame = self.vertical_scroller.get_scrolled_frame()
        #self.set_scrollbar()
        self.set_buttons()

    def on_entry_tab(self):   
        return
    
    def update(self, dt):
        return
    
    def read_json(self, ruta_archivo):
        obj = None

        return obj
    
    def set_buttons(self):
        self.load_questions_button = ttk.Button(self.scrolled_frame, text="Nada: Carmen Laforet")
        self.load_questions_button.place(x=50, y = 50)

    # def set_scrollbar(self):
    #     self.scrollbar = Scrollbar(self.tab, orient=VERTICAL, command=self.canvas.yview)
    #     self.scrollbar.pack(side=RIGHT, fill=Y)

    #     # configure the canvas
    #     self.canvas.configure(yscrollcommand=self.scrollbar.set)
    #     self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    #     self.target_frame = ttk.Frame(self.canvas, width=1200, height=900)
    #     self.canvas.create_window((0, 0), window=self.target_frame, anchor="nw")
    #     self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    # MARK: CALLBACKS
       

    # Para desplazar la vista vertical con la entrada de la rueda del ratón
    # def on_mousewheel(self, event = None):
    #     if event.delta:
    #         self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")