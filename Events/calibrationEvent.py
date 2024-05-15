from Events.event import Event

class CalibrationEvent(Event):
    def __init__(self, timestamp,width,height):
        super().__init__(timestamp)
        self.event_type = 1
        self.width=width
        self.height=height
        
    def toJson(self):
        return f'{{\n "id": {self.event_type},\n "width": {self.width},\n "height": {self.height},\n "timestamp": {self.timestamp}\n}}'
    
    def setCoords(self,w,h):
        self.width=w
        self.height=h
        

