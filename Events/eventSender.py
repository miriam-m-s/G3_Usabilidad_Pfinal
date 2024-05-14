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
        
    def addEvent(self, event):
        
        normLeftPupilX, normLeftPupilY = self.normalizeEvents(event.leftPupilX, event.leftPupilY)
        normRightPupilX, normRightPupilY = self.normalizeEvents(event.rightPupilX, event.rightPupilY)
        
        event.setLeftPupilCoords(normLeftPupilX, normLeftPupilY)
        event.setRightPupilCoords(normRightPupilX, normRightPupilY)
        
        self.events.append(event)

        if time.time() - self.last_save_time >= self.interval:
            self.saveEvents()
            print("Eventos guardados")
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

        return normX, normY
        
        
        