import time
class EventSender:
    def __init__(self, serializer, interval):
        self.serializer = serializer
        self.interval = interval
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def send_events(self):
        while True:
            time.sleep(self.interval)
            self.save_events()

    def save_events(self):
        
        filename = f"event_{int(time.time())}{self.serializer.get_file_extension()}"
        with open(filename, 'w') as file:
            file.write(self.serializer.init_file_format())
            for event in self.events:
                file.write(self.serializer.serialize(event))
            file.write(self.serializer.end_file_format())
        self.events = []