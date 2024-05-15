import time
import os
class EventSender:
    def __init__(self, serializer, interval, left, right, up,bottom):
        self.serializer = serializer
        self.interval = interval
        self.events = []
        self.left = left
        self.right = right
        self.bottom = bottom
        self.up = up
        
        #Creacion de carpeta para eventos
        self.tracked_events_folder = "TrackedEvents"
        if not os.path.exists(self.tracked_events_folder):
            os.makedirs(self.tracked_events_folder)
            
        self.last_save_time = time.time()
            
    def setCalibrationPoints(self, left, right, up,bottom):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.up = up
        
    def addEvent(self, event):
        
        self.events.append(event)
        print(f"Evento agregado")
        if time.time() - self.last_save_time >= self.interval:
            self.saveEvents()
            self.last_save_time = time.time()

    def saveEvents(self):
        
        filename = f"{self.tracked_events_folder}/event_{int(time.time())}{self.serializer.getFileExtension()}"
        with open(filename, 'w') as file:
            file.write(self.serializer.initFileFormat())
            for event in self.events:
                file.write(self.serializer.serialize(event))
            file.write(self.serializer.endFileFormat())
        self.events = []
    
        
    def normalizeEvents(self,coordX,coordY):

        if self.right - self.left == 0:
            normX = 0
        else:
            normX = (coordX - self.left) / (self.right - self.left)

        if self.bottom - self.up == 0:
            normY = 0
        else:
            normY = (coordY - self.up) / (self.bottom - self.up)

        
        return normX, normY
        
        
        