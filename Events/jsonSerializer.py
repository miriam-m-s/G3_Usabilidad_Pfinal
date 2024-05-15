class JsonSerializer: 
    
        def endFileFormat(self):
                return "{}]}"

        def getFileExtension(self):
                return ".json"

        def initFileFormat(self):
                return "{\n \"Events\": [\n"

        def serialize(self, event):
                return event.toJson() + "," + "\n"