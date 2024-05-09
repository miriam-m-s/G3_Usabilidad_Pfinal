from tkinter import *
from tkinter import ttk
import tkinter as tk
import cv2

from PIL import Image, ImageTk
from EyeTracker import calibrate

class MainTab:

    cam_img_id = None 
    calibration_running = None

    def __init__(self, tab, eyeTracker):
        self.tab = tab
        self.eyeTracker = eyeTracker
        self.playing = False 
 
    def setUp(self):
        ttk.Button(self.tab, text="Play", command=self.play).pack()
        ttk.Button(self.tab, text="Calibrate", command = self.update_calibration_).pack()
        ttk.Button(self.tab, text="Stop", command=self.stop).pack()

        self.calibrator_manager = calibrate.CalibratorManager()
        
        self.canvas = tk.Canvas(self.tab, width=1000, height=600)
        self.canvas.pack()
    
    def update(self):
        if not self.playing:
            return
        
        frame = self.eyeTracker.getFrame()
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.cam_img_id = self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        if self.calibration_running:
            self.update_calibration_()

    
    def play(self):
        self.playing = True

    def stop(self):
        if not self.playing:
            return
        
        self.calibration_running = False
        self.playing = False

        if self.cam_img_id != None:
            self.canvas.delete(self.cam_img_id)
            self.cam_img_id = None

    # MARK: CALIBRATION

    def start_calibration(self):
        if not self.playing:
            self.play()

    def update_calibration_(self):
        if not self.calibration_running:
            return
        
        calibration_otuput = self.calibrator_manager.calibrate_update()
        
        
        



        