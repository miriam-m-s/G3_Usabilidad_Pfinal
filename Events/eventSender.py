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
            
    def setCalibrationPoints(self, topLeft, topRight, bottomLeft, bottomRight):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        
    def addEvent(self, event):
        #TODO: normalizar eventos aqui
        normLeftPupilX, normLeftPupilY = self.normalizeEvents(event.leftPupilX, event.leftPupilY)
        normRightPupilX, normRightPupilY = self.normalizeEvents(event.rightPupilX, event.rightPupilY)
        
        event.setLeftPupilCoords(normLeftPupilX, normLeftPupilY)
        event.setRightPupilCoords(normRightPupilX, normRightPupilY)
        
        self.events.append(event)

    def sendEvents(self):
        while True:
            time.sleep(self.interval)            
            self.saveEvents()

    def saveEvents(self):
        
        filename = f"{self.tracked_events_folder}/event_{int(time.time())}{self.serializer.getFileExtension()}"
        with open(filename, 'w') as file:
            file.write(self.serializer.initFileFormat())
            for event in self.events:
                file.write(self.serializer.serialize(event))
            file.write(self.serializer.endFileFormat())
        self.events = []
        
    def normalizeEvents(self,coordX,coordY):
        normX=  (coordX - self.topLeft[0]) / (self.topRight[0] - self.topLeft[0])
        normY=  (coordY - self.topLeft[1]) / (self.bottomLeft[1] - self.topLeft[1])
        return normX,normY
        
        
        