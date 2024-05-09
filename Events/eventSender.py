import time
import os
class EventSender:
    def __init__(self, serializer, interval):
        self.serializer = serializer
        self.interval = interval
        self.events = []
        self.tracked_events_folder = "TrackedEvents"
        if not os.path.exists(self.tracked_events_folder):
            os.makedirs(self.tracked_events_folder)
        
    def addEvent(self, event):
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
        
    def normalizeEvents(self,coordX,coordY,topLeft, topRight, bottomLeft, bottomRight):
        normX=  (coordX - topLeft[0]) / (topRight[0] - topLeft[0])
        normY=  (coordY - topLeft[1]) / (bottomLeft[1] - topLeft[1])
        
        
        