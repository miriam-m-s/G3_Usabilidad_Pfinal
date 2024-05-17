import pyautogui
import cv2
import numpy as np
import time
from PIL import Image, ImageDraw
import threading
import json
import os
from App.Tabs import videoPlayerTab

class VideoRecorder:

    playing = False   

    tempVideoIdx = None
    availableTempIndexes = []

    videoPath = 'TrackedEvents/'

    def __init__(self):

        self.width, self.height = pyautogui.size() 
        
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        if not os.path.exists(self.videoPath):
            os.makedirs(self.videoPath)

    def start(self,user_test_name):  

        self.__setAvailableTempIdx()
        self.out = cv2.VideoWriter(f'{self.videoPath}{user_test_name}/temp{self.tempVideoIdx}.mp4', 
            self.fourcc, 60, (self.width, self.height))

        self.nFrames = 0
        self.playing = True 
        self.startTime = time.time()

        self.thread = threading.Thread(target=self.__record)  
        self.thread.start()  

    def stop(self, filePath):

        self.playing = False
        self.thread.join()

        duration = time.time() - self.startTime
        fps = self.nFrames / duration

        print(f'Duración del video: {duration}')
        print(f'FPS: {fps}')
        print(f'Frames totales {self.nFrames}')

        self.out.release()

        with open(filePath, 'r') as jsonFile:
            events = json.load(jsonFile)["Events"]
        events = [event for event in events[:-1] if event["id"] == 0] 

        thread = threading.Thread(target=self.__processVideo, 
            args=(self.tempVideoIdx, self.startTime, fps, events))
        thread.start()

    def __setAvailableTempIdx(self):

        self.tempVideoIdx = None

        for i in range(len(self.availableTempIndexes)):
            if self.availableTempIndexes[i]:
                self.availableTempIndexes[i] = False
                self.tempVideoIdx  = i
                break
        
        if self.tempVideoIdx is None:
            self.tempVideoIdx  = len(self.availableTempIndexes)
            self.availableTempIndexes.append(False)

    def __record(self):  

        while self.playing:
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.out.write(frame)
            self.nFrames += 1

    def __processVideo(self, tempVideoIdx, time, fps, events):

        print('Procesando video...')
        
        temp = cv2.VideoCapture(f'{self.videoPath}temp{self.tempVideoIdx}.mp4')
        
        out = cv2.VideoWriter(f'{self.videoPath}video_{time}.mp4', self.fourcc, fps, (self.width, self.height))
        lastRecording = f'{self.videoPath}video_circle_{time}.mp4'
        out_circle = cv2.VideoWriter(lastRecording, self.fourcc, fps, (self.width, self.height))

        r = 30

        dt = 1 / fps
        idx = 0
        lastCapture = len(events) - 1

        ret, frame = temp.read()
        while ret:
            out.write(frame)

            # Calculo de la posición del círculo haciendo la media ponderada
            # de las capturas entre las que se encuentra el frame actual
            while idx <= lastCapture and events[idx]["timestamp"] < time:
                idx += 1

            # Obtener las capturas anterior y posterior al momento actual
            previousCapture = events[max(0, idx - 1)]
            laterCapture = events[min(idx, lastCapture)]

            # Calcular la diferencia total de tiempo entre las dos capturas
            totalDiff = laterCapture["timestamp"] - previousCapture["timestamp"]

            if totalDiff > 0:
                # Calcular la diferencia de tiempo desde la captura anterior hasta el momento actual
                diff = time - previousCapture["timestamp"]
                
                # Calcular la proporción de la diferencia de tiempo
                prop = diff / totalDiff
                
                # Calcular la posición ponderada del círculo en función de la proporción de tiempo
                x = (previousCapture["posX"] * prop + laterCapture["posX"] * (1 - prop)) * self.width
                y = (previousCapture["posY"] * prop + laterCapture["posY"] * (1 - prop)) * self.height
            else:
                # Si no hay diferencia de tiempo, usar la posición de la captura anterior
                x = previousCapture["posX"] * self.width
                y = previousCapture["posY"] * self.height

            time += dt

            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image)    
            draw.ellipse((x - r, y - r, x + r, y + r), outline="red", width=5)

            out_circle.write(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
            
            ret, frame = temp.read()

        temp.release()
        out.release()

        videoPlayerTab.lastRecording = lastRecording
        self.availableTempIndexes[tempVideoIdx] = True

        print('Video procesado')






        
        


        





