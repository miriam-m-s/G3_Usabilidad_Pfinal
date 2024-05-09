from tkinter import *
from tkinter import ttk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from ScreenRecorderTest import videoPlayer

class VideoPlayerTab:

    def __init__(self, tab, videoPlayer):
        self.tab = tab
        self.playing = False
        self.videoPlayer = videoPlayer

    def setUp(self):
        ttk.Button(self.tab, text="Play/Pause", command=self.__debug).pack()

        self.canvas = tk.Canvas(self.tab, width=self.videoPlayer.width, height=self.videoPlayer.height)
        self.canvas.pack()

    def update(self):
        if self.playing:   
            frame = self.videoPlayer.getFrame()
            frame = cv2.resize(frame, (self.videoPlayer.width, self.videoPlayer.height))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.cam_img_id = self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)   

    def __debug(self):
        self.playing = not self.playing
        print(f"Reproduciendo: {self.playing}")