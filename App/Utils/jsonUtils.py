import json

def recover_json_from_file(path):
    json_data = None
    with open(path, "r") as archivo:    
        json_data = json.load(archivo)
    return json_data

def save_json_into_file(path, obj):
    with open(path, "w") as archivo:    
        json.dump(obj, archivo, indent=4)