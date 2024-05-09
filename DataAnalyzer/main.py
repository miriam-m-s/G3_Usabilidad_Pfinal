import json
import datetime

class dataAnalyzer:
    # def getTimeInSeconds(timestamp):
    #     fecha = datetime.datetime.fromtimestamp(timestamp)
    #     return fecha
    
    # Cargar el JSON desde un archivo
    with open('prueba.json', 'r') as json_data:
        data = json.load(json_data)
    eyePosData = data["eye_positions"]
    # while True:

    #     firstDataTime = input("First data time: ")
    #     lastDataTime = input ("Last data time: ")
    #     try:
    #         firstDataTime= int(firstDataTime)
    #         lastDataTime= int(lastDataTime)
    #         if(firstDataTime <= lastDataTime):
    #             break
    #         else:
    #             print("The second number must be larger than the first one")
    #     except ValueError:
    #         print("Invalid data types")
    initTime = eyePosData[0]['timestamp']

    startDataTime = 3
    endDataTime= 10

    i = 0
    #Avanzar hasta la primera marca de tiempo que se necesita
    for j in eyePosData:
        if(eyePosData[j]['timestamp'] > (initTime + 3)):
            break
        i += 1

    #guardar todas las posiciones x, y en un array
    end = False
    
    while not end:

   # eyePositions = 

   
#Paso el initialtime a segundos para saber cuantos se