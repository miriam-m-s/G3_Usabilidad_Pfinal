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
        print(f"TopLeft: {self.left}")
        print(f"TopRight: {self.right}")
        print(f"BottomLeft: {self.bottom}")
        print(f"BottomRight: {self.up}")
        
    def addEvent(self, event):
        
        normX, normY = self.normalizeEvents(event.x, event.y)
        event.setCoords(normX, normY)
        
        self.events.append(event)

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

        print(f"CoordX: {coordX}")
        print(f"CoordY: {coordY}")
        print(f"NormX: {normX}")
        print(f"NormY: {normY}")
        print(f"SelfTopRight: {self.right}")
        print(f"self.topLeft: {self.left}")
        print(f"self.bottomLeft: {self.bottom}")
        print(f"self.bottomRight: {self.up}")
        
        return normX, normY
        
        
        