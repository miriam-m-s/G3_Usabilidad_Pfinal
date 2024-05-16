# Este archivo analiza el tiempo inicial y duración de una partida según un json que se le pase

import json
import math

def analyzeJson(jsonName):
    with open('AnalisisMonkey/Mision1/1715881367.json', 'r') as json_data:
            data = json.load(json_data)
    data= data['Events']
    #Busco hasta que encuentro el evento de inicio de misión
    initMisionTime = 0
    endMisionTime = 0
    initMisionTime = data[1]['Timestamp'] 
    endMisionTime = data[2]['Timestamp']
    startMisionTime = initMisionTime- data[0]['Timestamp']

    misionDuration = endMisionTime - initMisionTime
    #minutos y segundos para completar la partida
    minutes = math.trunc(misionDuration / 60)
    seconds= misionDuration % 60
    print("El jugador ha tardado ",minutes," minutos y ", seconds , " segundos en completar la misión")
    return startMisionTime, misionDuration