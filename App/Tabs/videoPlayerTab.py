from tkinter import *
from tkinter import ttk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from ScreenRecorderTest import videoPlayer

class VideoPlayerTab:

    def __init__(self, root, tab, videoPlayer):
        self.root = root
        self.tab = tab
        self.playing = False
        self.forceStop = False
        self.videoTime = 0
        self.videoPlayer = videoPlayer

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

        button = ttk.Button(self.tab, text="Play/Pause", command=self.__debug)
        button.grid(row=2, column=0)

        # Texto a la izquierda del slider
        self.videoTimeLabel = tk.Label(self.tab, text="Valor:")
        self.videoTimeLabel.grid(row=1, column=1)

    def update(self, dt):
        if self.playing and not self.forceStop:   
            self.videoTime += dt
            self.slider.set(self.videoTime)

        frame = self.videoPlayer.getFrame(self.videoTime)
        if frame is not None:
            frame = cv2.resize(frame, (self.width, self.height))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)  
        else: 
            self.forceStop = True
        self.videoTimeLabel.config(text=self.__MM_SS_MMM())


    def __debug(self):
        self.playing = not self.playing
        print(f"Reproduciendo: {self.playing}")


    def __changeVideoTime(self, value):
        self.videoTime = float(value)

    def __MM_SS_MMM(self):

        minutes = int(self.videoTime / 60)
        seconds = int(self.videoTime - minutes * 60)
        milliseconds = int((self.videoTime - minutes * 60 - seconds) * 1000)

        return f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:{str(milliseconds).zfill(3)}'