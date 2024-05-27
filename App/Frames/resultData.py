import os
import json

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from App.Utils import jsonUtils
from DataAnalyzer.HeatmapCreator import dataAnalyzer
from PIL import Image, ImageTk

class ResultData:

    frame_data_array = []
    title = None

    def set_up(self, parent_frame, data_path, init_row, test_name):
        self.parent_frame = parent_frame
        self.data_dir = data_path

        file_list = os.listdir(self.data_dir)

        # filtración de los archivos json
        json_files = [file for file in file_list if file.endswith('.json')]

        try:
            # primer archivo que empieza por 'event'
            event_file = next((file for file in json_files if file.startswith('event')))
        except:
            raise FileNotFoundError("Eye tracker events could not be found")
        
        try:
            #archivo de sliced_data
            sliced_data_file = next((file for file in json_files if file.endswith('data.json')))
        except:
            raise FileNotFoundError("Video has not been sliced")
            

        
        event_path = os.path.join(self.data_dir, event_file)
        event_json = jsonUtils.recover_json_from_file(path=event_path)
        
        sliced_path = os.path.join(self.data_dir, sliced_data_file)
        sliced_json = jsonUtils.recover_json_from_file(sliced_path)

        self.title = Label(self.parent_frame, text=f"Test: {test_name}", font=("Helvetica", 16, "bold"))
        self.title.grid(column=0, row=init_row)

        id = init_row + 1
        for slice in sliced_json['Slices']:
            self.generate_frame_data(self, event_json, event_path, slice, id)      
            id += 1   

    def clear(self):       
        for frame in self.frame_data_array:
            frame.destroy()

        self.frame_data_array = []

        if self.title != None:
            self.title.grid_forget()
        
        
    def generate_frame_data(self, this, event_data, event_path, processed_sliced_data, id):
        frameData = FrameData(this, self.parent_frame, event_path, event_data, id)
        frameData.display(processed_sliced_data)
        self.frame_data_array.append(frameData)


class FrameData:
    def __init__(self, result_data, parent_frame, event_path, data, id):
        self.frame = Frame(parent_frame, pady=10)
        self.frame.grid(column=0, row=id)
        self.event_data = data
        self.event_path = event_path
        self.result_data = result_data

    def display(self, sliced):
        name = sliced['Name']
        start_time = sliced['From']
        end_time = sliced['Until']
        duration = round(end_time - start_time, 2)
        timestamp = self.event_data['Events'][0]['timestamp']

        self.initial_timestamp = self.event_data['Events'][0]['timestamp'] + start_time
        
        title = Label(self.frame, text=f"Slice \"{name}\"", font=("Helvetica", 12, "bold"))
        title.pack()

        from_to = Label(self.frame, text=f"From: {str(start_time)} sec. To: {str(end_time)} sec.")
        from_to.pack()

        duration_label = Label(self.frame, text=f"Duration: {duration} sec")
        duration_label.pack()

        frame_img_path = f"{self.result_data.data_dir}/{name}.png"
        print(frame_img_path)
        self.heat_image, events = self.read_heat_map(start_time, duration, frame_img_path)

        gather_label = Label(self.frame, text=f"Look events in this time lapse: {str(len(events))}")
        gather_label.pack()

        map_label = Label(self.frame, image=self.heat_image)
        map_label.pack()


    def destroy(self):
        self.frame.destroy()

    def read_heat_map(self, init_time, duration, background_path):

        data, w, h = dataAnalyzer.readData(self.event_path, init_time, duration)

        fig = dataAnalyzer.createTimeHeatMap(data, w, h, background=background_path)
        
        # Leer la imagen del buffer y convertirla a un objeto ImageTk
        image = Image.open(fig)
        new_width = int(w * 0.4)
        new_height = int(h * 0.4)
        image = image.resize((new_width, new_height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)

        return photo, data
