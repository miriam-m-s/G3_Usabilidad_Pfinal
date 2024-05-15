from Events.event import Event

class EyeTrackingEvent(Event):
    def __init__(self, timestamp,x,y):
        super().__init__(timestamp)
        self.event_type = 0
        self.x=x
        self.y=y
        
    def to_json(self):
        return f'{{\n "id": {self.event_type},\n "posX": {self.x},\n "posY": {self.y},\n "timestamp": {self.timestamp}\n}}'
    
    def set_coords(self,x,y):
        self.x=x
        self.y=y

