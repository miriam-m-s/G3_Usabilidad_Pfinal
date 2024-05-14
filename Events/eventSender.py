import time
import os
class EventSender:
    def __init__(self, serializer, interval, topLeft, topRight, bottomLeft, bottomRight):
        self.serializer = serializer
        self.interval = interval
        self.events = []
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        
        #Creacion de carpeta para eventos
        self.tracked_events_folder = "TrackedEvents"
        if not os.path.exists(self.tracked_events_folder):
            os.makedirs(self.tracked_events_folder)
            
        self.last_save_time = time.time()
            
    def setCalibrationPoints(self, topLeft, topRight, bottomLeft, bottomRight):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        print(f"TopLeft: {self.topLeft}")
        print(f"TopRight: {self.topRight}")
        print(f"BottomLeft: {self.bottomLeft}")
        print(f"BottomRight: {self.bottomRight}")
        
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

        
        if self.topRight[0] - self.topLeft[0] == 0:
            normX = 0
        else:
            normX = (coordX - self.topLeft[0]) / (self.topRight[0] - self.topLeft[0])

        if self.bottomLeft[1] - self.topLeft[1] == 0:
            normY = 0
        else:
            normY = (coordY - self.topLeft[1]) / (self.bottomLeft[1] - self.topLeft[1])

        print(f"CoordX: {coordX}")
        print(f"CoordY: {coordY}")
        print(f"NormX: {normX}")
        print(f"NormY: {normY}")
        
        
        return normX, normY
        
        
        