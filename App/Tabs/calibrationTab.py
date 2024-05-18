from tkinter import *
from tkinter import ttk
import tkinter as tk
import cv2

from PIL import Image, ImageTk
from EyeTracker import calibrate
from App.AppState import instructions
from App.Tabs.tab import Tab
from App.Utils import jsonUtils
from App.appConsts import Consts

import time
import json
from Events.eyeTrackingEvent import EyeTrackingEvent
from Events.calibrationEvent import CalibrationEvent

class CalibrationTab(Tab):

    cam_img_id = None 
    calibration_running = None
    corner_images = None

    gray_circle_path = "./App/Images/grayCircle.png"
    green_circle_path = "./App/Images/greenCircle.png"
    red_circle_path = "./App/Images/redCircle.png"
    orange_circle_path = "./App/Images/orangeCircle.png"

    wait_for_user_input = False

    circle_width = 90
    max_screen_w = 0
    max_screen_h = 0

    def __init__(self, tab, eyeTracker, app, calibrator_manager):
        self.tab = tab
        self.eyeTracker = eyeTracker
        self.playing = False
        self.app = app 
        self.calibrator_manager = calibrator_manager
 
    def set_up(self):
        self.canvas = tk.Canvas(self.tab, width=1000, height=600)
        self.canvas.pack()

        #self.play_button = ttk.Button(self.canvas, text="Play", command=self.play, takefocus=False)
        self.calibrate_button = ttk.Button(self.canvas, text="Calibrate", command = self.start_calibration, takefocus=False)
        self.stop_button = ttk.Button(self.canvas, text="Stop", command=self.stop, takefocus=False)
        self.instructions_button = ttk.Button(self.canvas, text="Instructions", command=self.show_instructions, takefocus=False)
        
        x = self.app.init_window_width * 0.45
        y = 10
        #self.play_button.place(x=x, y=y)
        self.calibrate_button.place(x=x, y=y + 30)
        self.instructions_button.place(x=x, y = y + 90)
        
        self.instructions = instructions.CalibrationInstructions()
        self.load_images()
        

    def load_images(self):
        gray_image = Image.open(self.gray_circle_path)
        red_image = Image.open(self.red_circle_path)
        green_image = Image.open(self.green_circle_path)
        orange_image = Image.open(self.orange_circle_path)

        w = self.circle_width

        resized_gray = gray_image.resize((w, w), Image.LANCZOS)
        resized_red = red_image.resize((w, w), Image.LANCZOS)
        resized_green = green_image.resize((w, w), Image.LANCZOS)
        resized_orange = orange_image.resize((w, w), Image.LANCZOS)

        self.gray_circle_photo   = ImageTk.PhotoImage(resized_gray)
        self.green_circle_photo  = ImageTk.PhotoImage(resized_green)
        self.red_circle_photo    = ImageTk.PhotoImage(resized_red)
        self.orange_circle_photo = ImageTk.PhotoImage(resized_orange)
        
    # MARK: BUTTON CALLBACKS
    def show_instructions(self):
        self.instructions.show_instructions_popup(self.tab)

    def play(self):
        self.playing = True

    def stop(self):
        if not self.playing:
            return
        
        if self.calibration_running:
            self.shut_down_calibration()

        self.playing = False
        self.app.set_fullscreen(False)

        if self.cam_img_id != None:
            self.canvas.delete(self.cam_img_id)
            self.cam_img_id = None

    # MARK: CALIBRATION

    def start_calibration(self):
        if self.playing:
            return
        self.play()

        #self.play_button.place_forget()
        self.instructions_button.place_forget()
        self.calibrate_button.place_forget()

        self.calibrator_manager.reset()
        self.app.set_fullscreen(True)
        self.calibration_running = True
        self.wait_for_user_input = True
       
        self.app.root.after(400, self.set_up_window_calibration)

    def set_up_window_calibration(self):
        self.max_screen_w = self.app.root.winfo_screenwidth()
        self.max_screen_h = self.app.root.winfo_screenheight()
        self.canvas.config(width=self.max_screen_w, height=self.max_screen_h)
        self.stop_button.place(anchor=CENTER, x = self.max_screen_w * 0.5, y = self.max_screen_h * 0.2)

        self.corner_coords = self.calibrator_manager.get_corner_calibration_order_position()
        self.calibrator_manager.get_current_relative_corner() 
             

        self.corner_images = []
        for corner in self.corner_coords:
            x = corner[0] * self.max_screen_w
            y = corner[1] * self.max_screen_h
            #self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)
            self.corner_images.append(self.canvas.create_image(x, y, anchor="center",image = self.gray_circle_photo))

        self.update_corner_view()
        
    def on_calibration_completed(self):
        self.app.set_fullscreen(False)
        self.calibrator_manager.get_calibration_map()
        print("Calibración completa")

        self.stop()

        left, right, up, bottom = self.calibrator_manager.mean_coordinates()
        self.save_calibration(left, right, up, bottom)


    def update_corner_view(self):
        current_corner = self.calibrator_manager.current_calibration

        # Ponemos en verde el punto de control ya analizado
        if current_corner > 0:
            img_id = self.corner_images[current_corner - 1]  
            self.canvas.itemconfig(img_id, image=self.green_circle_photo)

        # Comprobación de si hay puntos restantes
        if current_corner <= len(self.corner_images) - 1:
            img_id = self.corner_images[current_corner]
            self.canvas.itemconfig(img_id, image=self.red_circle_photo)
            self.wait_for_user_input = True 

    def shut_down_calibration(self):
        self.calibration_running = False
        if self.corner_images != None:
            for img_id in self.corner_images:
                self.canvas.delete(img_id)
    
        x = self.app.init_window_width * 0.45
        y = 10
        #self.play_button.place(x=x, y=y)
        self.calibrate_button.place(x=x, y=y + 30)
        self.stop_button.place_forget()
        self.instructions_button.place(x=x, y = y + 90)
    # MARK: UPDATE

    def update(self, dt):
        if self.playing == False: #or self.calibration_running para no mostrarlo en la calibración. Hay que borrar el id de la imagen también
            return
        
        frame, horizontal_gaze, vertical_gaze = self.eyeTracker.getFrame()     
        
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.cam_img_id = self.canvas.create_image(0, 100, image=self.photo, anchor=tk.NW)
        
        if self.calibration_running:
            self.update_calibration_(horizontal_gaze, vertical_gaze)

    def update_calibration_(self, left_pupil, right_pupil):
        if self.calibration_running == False or left_pupil is None or right_pupil is None:
            return

        if self.wait_for_user_input:
            return
        #print(f"Pupila izq: {left_pupil}")
        calibration_otuput = self.calibrator_manager.calibrate_update(horizontal_gaze=left_pupil, vertical_gaze=right_pupil)

        if calibration_otuput == calibrate.CalibrationOutput.CALIBRATION_COMPLETED:
            self.on_calibration_completed()
        elif calibration_otuput == calibrate.CalibrationOutput.CORNER_COMPLETED:
            self.update_corner_view()       

    # MARK: KEY EVENTS
    def key_pressed(self, event):
        if self.calibration_running == False:
            return
        
        if self.wait_for_user_input and event.keysym == "space":
            current_corner = self.calibrator_manager.current_calibration
            img_id = self.corner_images[current_corner]
            self.canvas.itemconfig(img_id, image=self.orange_circle_photo)
            self.wait_for_user_input = False

    def save_calibration(self, left, right, up, bottom):
        jsonMap = {
            "left": left,
            "right": right,
            "up": up,
            "bottom": bottom,
            "screen_width": self.max_screen_w,
            "screen_height": self.max_screen_h
        }
        jsonUtils.save_json_into_file(Consts.APP_DATA_PATH, jsonMap)
        