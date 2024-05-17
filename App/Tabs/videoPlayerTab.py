from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from tktooltip import ToolTip
from PIL import Image, ImageTk
from App.Frames import slicer
from VideoManagers.videoPlayer import VideoPlayer
from App.Tabs.tab import Tab
import json

lastRecording = None

class VideoPlayerTab(Tab):

    currentTime = 0

    frameIncrease = 0
    timeIncrease = 0
    timeChange = -1

    playing = False
    sliding = False

    slicerList = []
    sliceCount = 0

    clipboard = 0

    videoPlayer = None
    loadNewVideo = False

    def __init__(self, tab):
        self.tab = tab  

    def set_up(self):

        relation = 1080 / 1920
        self.width = int(1920 * 0.5)
        self.height = round(self.width * relation)

        load_video_frame = tk.Frame(self.tab)
        load_video_frame.grid(row=0, column=0, sticky="w")

        ttk.Button(load_video_frame, text="Load video",  
            command=self.__loadVideo).pack(side=tk.LEFT) 
        ttk.Button(load_video_frame, text="Load last recording",  
            command=self.__loadLastRecording).pack(side=tk.LEFT)

        ttk.Button(self.tab, text="Save slices",  
            command=self.__saveSlices).grid(row=0, column=1, sticky="w")

        self.canvas = tk.Canvas(self.tab, width=self.width, height=self.height)
        self.canvas.grid(row=1, column=0)

        self.slider = tk.Scale(self.tab, 
                               from_=0, resolution=0.001,
                               orient=tk.HORIZONTAL, length=self.width, 
                               command=self.__setCurrentTime,
                               showvalue=0)
        self.slider.grid(row=2, column=0)
        self.slider.bind("<ButtonPress>", lambda _: setattr(self, 'sliding', True))
        self.slider.bind("<ButtonRelease>", lambda _: setattr(self, 'sliding', False))

        video_controller_frame = tk.Frame(self.tab)
        video_controller_frame.grid(row=3, column=0, sticky="ew")
        video_controller_frame.columnconfigure(0, weight=1)
        video_controller_frame.columnconfigure(1, weight=1)  
        video_controller_frame.columnconfigure(2, weight=1)  

        button_frame = tk.Frame(video_controller_frame)
        button_frame.grid(row=0, column=1)

        button_size = 3  
        ttk.Button(button_frame, text="<", width=button_size, 
                   command=lambda: setattr(self, 'frameIncrease', self.frameIncrease - 1)).pack(side=tk.LEFT)     
        ttk.Button(button_frame, text="<<", width=button_size, 
                   command=lambda: setattr(self, 'timeIncrease', self.timeIncrease - 1)).pack(side=tk.LEFT)      
        self.playButton = ttk.Button(button_frame, text="I >", command=self.__play, width=button_size)
        self.playButton.pack(side=tk.LEFT)
        ttk.Button(button_frame, text=">>", width=button_size, 
                   command=lambda: setattr(self, 'timeIncrease', self.timeIncrease + 1)).pack(side=tk.LEFT) 
        ttk.Button(button_frame, text=">", width=button_size, 
                   command=lambda: setattr(self, 'frameIncrease', self.frameIncrease + 1)).pack(side=tk.LEFT)

        self.videoTimeLabel = tk.Label(video_controller_frame, text="00:00:000")
        self.videoTimeLabel.grid(row=0, column=2, sticky="e")
        ToolTip(self.videoTimeLabel, msg="Tiempo de vídeo", delay=0.5)

        self.videoFrameLabel = tk.Label(video_controller_frame, text="00000000")
        self.videoFrameLabel.grid(row=0, column=0, sticky="w")  
        ToolTip(self.videoFrameLabel, msg="Fotograma", delay=0.5)

        self.slicer_frame = tk.Frame(self.tab)
        self.slicer_frame.grid(row=1, column=1, sticky="nw")

        self.add_button_frame = tk.Frame(self.slicer_frame)
        self.add_button_frame.pack(side=tk.TOP, anchor="w")  

        ttk.Button(self.add_button_frame, text="+", width=button_size,
                command=self.createSlicer).pack()
        
        for widget in self.tab.winfo_children():
            widget.grid_remove()

        load_video_frame.grid()
             
    def update(self, dt):

        self.__loadVideoChecker()

        if self.videoPlayer is None:
            return
        
        if self.playing and not self.sliding:   
            self.currentTime += dt

        self.__checkEvents()

        if self.frameIncrease != 0: 
            frame, self.currentTime = self.videoPlayer.getFrameFromFrameIncrease(self.frameIncrease)
            self.frameIncrease = 0        
        else: frame = self.videoPlayer.getFrame(self.currentTime)

        if frame is not None:
            frame = cv2.resize(frame, (self.width, self.height))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW) 
        
        if self.currentTime >= self.videoPlayer.duration:
            self.playButton.config(text="I >")
            self.playing = False

        self.slider.set(self.currentTime)
        self.videoTimeLabel.config(text=self.__MMMSSMMM())  
        self.videoFrameLabel.config(text=str(self.videoPlayer.lastFrame).zfill(9))    

    def __loadVideoChecker(self):     
        if self.loadNewVideo:
            self.loadNewVideo = False 

            self.videoPlayer = VideoPlayer(self.filePath)

            self.slider.config(to=self.videoPlayer.duration)  
            self.currentTime = 0
            self.playButton.config(text="I >")
            self.playing = False

            while self.slicerList:
                self.deleteSlicer(self.slicerList[0])

            for widget in self.tab.winfo_children():
                widget.grid()          

    def __loadVideo(self):
        self.filePath = filedialog.askopenfilename(title="Seleccionar video", filetypes=(("Archivos de video", "*.mp4 *.avi"), ("Todos los archivos", "*.*")))
        if self.filePath:
            self.loadNewVideo = True
            print("Ruta del archivo seleccionado:", self.filePath)
        

    def __loadLastRecording(self):
        if lastRecording is None:
            messagebox.showerror("Error", "You haven't recorded any video yet")
        else:
            self.filePath = lastRecording
            self.loadNewVideo = True

    def __checkEvents(self):

        if self.timeIncrease != 0:
            self.currentTime += self.timeIncrease
            self.currentTime = max(0, min(self.currentTime, self.videoPlayer.duration))
            self.timeIncrease = 0 

        if self.timeChange >= 0:
            self.currentTime = self.timeChange
            self.timeChange = -1

    def __play(self):
        self.playing = not self.playing

        if self.playing:
            if self.currentTime >= self.videoPlayer.duration:
                self.timeChange = 0
            self.playButton.config(text="I I")      
        else:
            self.playButton.config(text="I >")       

    def __setCurrentTime(self, value):
        self.currentTime = float(value)

    def createSlicer(self):
        frame = tk.Frame(self.slicer_frame)
        frame.pack(side=tk.TOP, in_=self.slicer_frame, before=self.add_button_frame)
        self.slicerList.append(slicer.Slicer(self, frame, f"Slice {self.sliceCount}"))
        self.sliceCount += 1

    def deleteSlicer(self, slicer):
        self.slicerList.remove(slicer)
        slicer.frame.destroy()
        print('Slicer eliminado')

    def MMMSSMMM(self, time):

        minutes = int(time / 60)
        seconds = int(time - minutes * 60)
        milliseconds = int((time - minutes * 60 - seconds) * 1000)

        return f'{str(minutes).zfill(3)}:{str(seconds).zfill(2)}:{str(milliseconds).zfill(3)}'

    def __MMMSSMMM(self):
        return self.MMMSSMMM(self.currentTime)
    
    def __saveSlices(self):

        if not self.slicerList:
            messagebox.showerror("Error", "You have not created any slice")
            return
            
        data = []

        for slice in self.slicerList: 
            data.append({
                "Name": slice.name.get(),
                "From": slice.from_slice.time,
                "Until": slice.until_slice.time
            })

        jsonData = json.dumps({"Slices" : data}, indent=4)
        with open('data.json', 'w') as archivo:
            archivo.write(jsonData)


      




        
    



    
    