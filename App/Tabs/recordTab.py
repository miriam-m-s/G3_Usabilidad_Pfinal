from App.Tabs.tab import Tab
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import cv2

import time
import re
import os
import uuid
from App.Utils import jsonUtils
from App.appConsts import Consts
from Events.calibrationEvent import CalibrationEvent
from Events.eyeTrackingEvent import EyeTrackingEvent
from Events.eventSender import EventSender
from Events.jsonSerializer import JsonSerializer
from VideoManagers.videoRecorder import VideoRecorder

class RecordTab(Tab):

    playing = False

    events_interval_secs= 5 #Intervalo que indica que cada 5 segundos se deben guardar los eventos en un archivo


    def __init__(self, tab, eyeTracker, calibrator_manager):
        self.tab = tab
        self.eyeTracker = eyeTracker
        self.calibrator_manager = calibrator_manager

    def set_up(self):
        self.canvas = tk.Canvas(self.tab, width=600, height=500)
     
        self.label = ttk.Label(self.tab, text="Insert name of test:")
        self.label.pack(pady=10)
        
        self.entry = ttk.Entry(self.tab)
        self.entry.pack(pady=10)
        self.play_button = ttk.Button(self.tab, text="Play", command=self.play, takefocus=False)
        self.stop_button = ttk.Button(self.tab, text="Stop", command = self.stop, takefocus=False)
        self.warning_label = ttk.Label(self.tab, text="Eye tracker sin calibrar o mal calibrado", foreground="red")

        self.serializer = JsonSerializer()
        self.eventSender = EventSender(self.serializer, self.events_interval_secs) 
        self.videoPlayer = VideoRecorder()    
   
    def show_buttons(self):
        self.warning_label.pack_forget()
        self.play_button.pack()
        self.stop_button.pack()
        self.canvas.pack()

    def hide_buttons(self):
        self.play_button.pack_forget()
        self.stop_button.pack_forget()
        self.canvas.pack_forget()
        self.warning_label.pack()

    def play(self):
        if self.playing:
            return
        
        user_test_path=self.get_user_test_path()
        self.eventSender.set_start(user_test_path)
        calEvent = CalibrationEvent(timestamp=time.time(),width=self.max_screen_w,height=self.max_screen_h)
        calEvent.set_coords(self.max_screen_w,self.max_screen_h)        
        self.eventSender.add_event(calEvent)

        self.videoPlayer.start(user_test_path)

        self.playing = True
        return

    def get_user_test_path(self):
        user_test = self.entry.get()
        user_test=re.sub(r'[^\w\s]', '', user_test).replace(' ', '')
        print(user_test)
        if not user_test:
            user_test = str(uuid.uuid4())
        filepath=f"UserTests/{user_test}"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        return filepath
        
    
    def stop(self):
        if not self.playing:
            return
        
        self.canvas.delete(self.cam_img_id)
        self.eventSender.set_end()
        self.videoPlayer.stop(self.eventSender.filename)
        self.playing = False

    def on_entry_tab(self):
        try:
            jsonObj = jsonUtils.recover_json_from_file(Consts.APP_DATA_PATH)
            if(jsonObj['bottom'] > jsonObj['up'] and jsonObj['screen_width'] > 0):
                self.show_buttons()
                self.actualice_calibration()
            else:
                self.hide_buttons()
        except:
            self.hide_buttons()

    def update(self, dt):
        if not self.playing:
            return
        
        frame, horizontal_gaze, vertical_gaze = self.eyeTracker.getFrame()    
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.cam_img_id = self.canvas.create_image(0, 100, image=self.photo, anchor=tk.NW)

        if horizontal_gaze is not None and vertical_gaze is not None:
            #todo: media x e y de las pupilas
            normX, normY = self.eventSender.normalize_events(horizontal_gaze, vertical_gaze)
            event=EyeTrackingEvent(timestamp=time.time(),x=horizontal_gaze,y=vertical_gaze)
            event.set_coords(normX, normY)
            self.eventSender.add_event(event)

    def actualice_calibration(self):
        obj = jsonUtils.recover_json_from_file(Consts.APP_DATA_PATH)
        up = obj['up']
        right = obj['right']
        left = obj['left']
        bottom = obj['bottom']
        self.max_screen_w = obj['screen_width']
        self.max_screen_h = obj['screen_height']
        self.eventSender.set_calibration_points(up=up, right=right, left=left, bottom=bottom) 

    def on_close_app(self):
        try:
            self.stop()
        except:
            return
        