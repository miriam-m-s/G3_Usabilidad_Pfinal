class JsonSerializer: 
    
        def end_file_format(self):
                return "{}]}"

        def get_file_extension(self):
                return ".json"

        def init_file_format(self):
                return "{\n \"Events\": [\n"

        def serialize(self, event):
                return event.to_json() + "," + "\n"