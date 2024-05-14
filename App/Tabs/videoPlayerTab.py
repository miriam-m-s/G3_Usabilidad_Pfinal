from tkinter import *
from tkinter import ttk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading

class VideoPlayerTab:

    def __init__(self, root, tab, videoPlayer):
        self.root = root
        self.tab = tab  
        self.videoPlayer = videoPlayer
        self.currentTime = 0
        self.increase = 0
        self.playing = False
        self.forceStop = False

    def setUp(self):

        relation = self.videoPlayer.height / self.videoPlayer.width
        self.width = int(self.videoPlayer.width * 0.5)
        self.height = round(self.width * relation)

        self.canvas = tk.Canvas(self.tab, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0)

        self.slider = tk.Scale(self.tab, 
                               from_=0, to=self.videoPlayer.duration, resolution=0.001,
                               orient=tk.HORIZONTAL, length=self.width, 
                               command=self.__changeVideoTime,
                               showvalue=0)
        self.slider.grid(row=1, column=0)
        self.slider.bind("<ButtonPress>", lambda event: setattr(self, 'forceStop', True))
        self.slider.bind("<ButtonRelease>", lambda event: setattr(self, 'forceStop', False))

        video_controller_frame = tk.Frame(self.tab)
        video_controller_frame.grid(row=2, column=0, sticky="ew")

        # Configuración de peso para las tres columnas dentro del video_controller_frame
        video_controller_frame.columnconfigure(0, weight=1)
        video_controller_frame.columnconfigure(1, weight=1)  
        video_controller_frame.columnconfigure(2, weight=1)  
        button_frame = tk.Frame(video_controller_frame)
        button_frame.grid(row=0, column=1)

        button_size = 3  
        ttk.Button(button_frame, text="<", width=button_size, command=lambda: self.__increaseTime(-self.videoPlayer.dt)).pack(side=tk.LEFT)     
        ttk.Button(button_frame, text="<<", width=button_size, command=lambda: self.__increaseTime(-1)).pack(side=tk.LEFT)  
        self.playButton = ttk.Button(button_frame, text="I >", command=self.__play, width=button_size)
        self.playButton.pack(side=tk.LEFT)
        ttk.Button(button_frame, text=">>", width=button_size, command=lambda: self.__increaseTime(1)).pack(side=tk.LEFT) 
        ttk.Button(button_frame, text=">", width=button_size, command=lambda: self.__increaseTime(self.videoPlayer.dt)).pack(side=tk.LEFT)

        self.videoTimeLabel = tk.Label(video_controller_frame, text="00:00:000")
        self.videoTimeLabel.grid(row=0, column=2, sticky="e")

        self.videoFrameLabel = tk.Label(video_controller_frame, text="00000000")
        self.videoFrameLabel.grid(row=0, column=0, sticky="w")
        

    def update(self, dt):
        
        if self.playing and not self.forceStop:   
            self.currentTime += dt
            self.slider.set(self.currentTime)

        if self.increase != 0:
            self.currentTime += self.increase
            self.currentTime = max(0, min(self.currentTime, self.videoPlayer.duration))
            self.slider.set(self.currentTime)
            self.forceStop = False
            self.increase = 0

        ret, frame = self.videoPlayer.getFrame(self.currentTime)

        frame = cv2.resize(frame, (self.width, self.height))
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.forceStop = True if not ret else self.forceStop

        self.videoTimeLabel.config(text=self.__MMSSMMM())
        self.videoFrameLabel.config(text=str(self.videoPlayer.currentFrame).zfill(8))   

    def __play(self):
        self.playing = not self.playing

        if self.playing:
            self.playButton.config(text="I I")
        else:
            self.playButton.config(text="I >")

    def __changeVideoTime(self, value):
        self.currentTime = float(value)

    def __MMSSMMM(self):

        minutes = int(self.currentTime / 60)
        seconds = int(self.currentTime - minutes * 60)
        milliseconds = int((self.currentTime - minutes * 60 - seconds) * 1000)

        return f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:{str(milliseconds).zfill(3)}'
    
    def __increaseTime(self, seconds):
        self.increase += seconds
    