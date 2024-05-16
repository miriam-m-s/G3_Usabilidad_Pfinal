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
        self.filename= f"{self.tracked_events_folder}/event_{int(time.time())}{self.serializer.get_file_extension()}"
        if not os.path.exists(self.tracked_events_folder):
            os.makedirs(self.tracked_events_folder)
            
        self.last_save_time = time.time()
    def set_start(self):
        self.filename= f"{self.tracked_events_folder}/event_{int(time.time())}{self.serializer.get_file_extension()}"
        with open(self.filename, 'w') as file:
            file.write(self.serializer.init_file_format())
    def set_end(self):
        self.save_events()
        self.last_save_time = time.time()
        with open(self.filename, 'a') as file:
            file.write(self.serializer.end_file_format())
        self.events = []       
    def set_calibration_points(self, left, right, up,bottom):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.up = up
        
    def add_event(self, event):
        
        self.events.append(event)
        
        if time.time() - self.last_save_time >= self.interval:
            self.save_events()
            self.last_save_time = time.time()

    def save_events(self):   

        with open(self.filename, 'a') as file:
            for event in self.events:
                file.write(self.serializer.serialize(event))
        self.events = []   
            
    
        
    def normalize_events(self,coordX,coordY):

        if self.right - self.left == 0:
            normX = 0
        else:
            normX = (coordX - self.left) / (self.right - self.left)

        if self.bottom - self.up == 0:
            normY = 0
        else:
            normY = (coordY - self.up) / (self.bottom - self.up)

        
        return normX, normY
        
        
        