class EyeTrackingEvent:
    def __init__(self, timestamp,x,y):
        self.timestamp = timestamp
        self.x=x
        self.y=y
        
    def toJson(self):
        return f'{{\n "posX": {self.x},\n "posY": {self.y},\n "timestamp": {self.timestamp}\n}}'
    
    def setCoords(self,x,y):
        self.x=x
        self.y=y

