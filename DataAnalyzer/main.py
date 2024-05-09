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

    #Avanzar hasta la primera marca de tiempo que se necesita
    for j in range(0, len(eyePosData)):
        if(eyePosData[j]['timestamp'] >= (initTime + 3)):
            break

    print(j)
    print(eyePosData[j]['timestamp'])
    totalPositions= []
    for k in range(j,len(eyePosData)):
        if(eyePosData[k]['timestamp'] > (initTime + 100)):
            break
        print
        totalPositions.append((eyePosData[k]['posX'], eyePosData[k]['posY']))

    print(len(totalPositions))
    #guardar todas las posiciones x, y en un array

    
    # while not end:

    # eyePositions = 

