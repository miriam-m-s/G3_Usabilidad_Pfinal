class Event:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.event_type = -1
        
    def to_json(self):
        pass
    def set_coords(self,coord1,coord2):
        pass
    def get_type(self):
        return self.event_type
    
    

