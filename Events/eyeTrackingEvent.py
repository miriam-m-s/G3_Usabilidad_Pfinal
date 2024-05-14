class EyeTrackingEvent:
    def __init__(self, timestamp,x,y):
        self.timestamp = timestamp
        self.x=x
        self.y=y
        
    def toJson(self):
        return f'{{\n "timestamp": {self.timestamp},\n "x": {self.x},\n "y": {self.y}\n}}'
    
    def setCoords(self,x,y):
        self.x=x
        self.y=y

