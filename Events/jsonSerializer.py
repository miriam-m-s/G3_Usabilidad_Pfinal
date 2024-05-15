class JsonSerializer: 
    
        def endFileFormat(self):
                return "{}]}"

        def getFileExtension(self):
                return ".json"

        def initFileFormat(self):
                return "{\n \"eye_positions\": [\n"

        def serialize(self, event):
                return event.toJson() + "," + "\n"