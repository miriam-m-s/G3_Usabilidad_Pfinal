from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from App.Tabs.tab import Tab
import os

from App.Frames.verticalScroller import VerticalScroller
from App.Frames.resultData import ResultData
from App.appConsts import Consts
from App.Utils import jsonUtils

class ResultsTab(Tab):
    json_path = "questions.json"
    sangria = 50

    result_data = None
    
    def __init__(self, tab):
        self.tab = tab

    def set_up(self):
        self.result_data = ResultData()
        
        self.vertical_scroller = VerticalScroller(self.tab)
        self.scrolled_frame = self.vertical_scroller.get_scrolled_frame()

        self.dir_combo = ttk.Combobox(self.scrolled_frame)
        self.dir_combo.grid(column=0,row=0)

        self.analyze_button = Button(self.scrolled_frame, text="Analyze", command=self.analyze_dir)
        self.analyze_button.grid(column=1, row=0)

        self.set_buttons()

    def on_entry_tab(self):   
        listdir = self.load_user_test_dirs()
        self.dir_combo['values'] = listdir
        return
    
    def update(self, dt):
        return
    
    def read_json(self, ruta_archivo):
        obj = None

        return obj
    
    def set_buttons(self):
        # self.load_questions_button = ttk.Button(self.scrolled_frame, text="Nada: Carmen Laforet")
        # self.load_questions_button.place(x=50, y = 50)
        return

    # MARK: CALLBACKS
       
    def load_user_test_dirs(self):
        listdir = []    
        user_tests_dir = Consts.USER_TESTS_DIR
        if os.path.exists(user_tests_dir) and os.path.isdir(user_tests_dir):
            for item in os.listdir(user_tests_dir):
                item_path = os.path.join(user_tests_dir, item)
                if os.path.isdir(item_path):
                    listdir.append(item)
        return listdir

    def analyze_dir(self):
        combo_string = self.dir_combo.get()

        if not combo_string:
            messagebox.showerror("Error", "No test was uploaded")
            return

        s_path = os.path.join(Consts.USER_TESTS_DIR, combo_string)

        self.result_data.clear()
        try: 
            self.result_data.set_up(self.scrolled_frame, s_path, 1, combo_string)
        except Exception as e:
            error_message = f"Data couldn't be analyzed:\n{str(e)}"
            messagebox.showerror("Error", error_message)

        self.actualize_scrollable_frame()
        
    def actualize_scrollable_frame(self):
        # Method to update the scrollregion
        self.vertical_scroller.canvas.update_idletasks()
        self.vertical_scroller.canvas.configure(scrollregion=self.vertical_scroller.canvas.bbox("all"))