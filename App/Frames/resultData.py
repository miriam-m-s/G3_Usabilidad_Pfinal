import os
import json

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from App.Utils import jsonUtils

class ResultData:

    frame_data_array = []

    def __init__(self, parent_frame, data_path):
        self.parent_frame = parent_frame
        self.data_dir = data_path
        pass

    def set_up(self):
        file_list = os.listdir(self.data_dir)

        # filtración de los archivos json
        json_files = [file for file in file_list if file.endswith('.json')]

        # primer archivo que empieza por 'event'
        event_file = next((file for file in json_files if file.startswith('event')))

        if not event_file:
            raise FileNotFoundError("Eye tracker events could not be found")
        
        path = os.path.join(self.data_dir, event_file)
        event_json = jsonUtils.recover_json_from_file(path=path)
            

        

    def delete(self):
        if len(self.frame_data_array) == 0:
            return
        


class FrameData:
    def __init__(self, frame, data):
        self.frame = frame
        self.data = data

    def display(self, from_time, until_time):
        return