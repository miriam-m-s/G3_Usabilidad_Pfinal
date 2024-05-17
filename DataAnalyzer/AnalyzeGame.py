# Este archivo analiza el tiempo inicial y duración de una partida según un json que se le pase

import json
import math

def analyzeJson(jsonName):
    with open(jsonName, 'r') as json_data:
            data = json.load(json_data)

    data = data['Events']
    
    initMisionTime = 0
    endMisionTime = 0

    initMisionTimes = [event['Timestamp'] for event in data if 'type' in event and event['type'] == "MissionStartEvent"]
    endMisionTimes = [event['Timestamp'] for event in data if 'type' in event and event['type'] == "MissionEndEvent"]

    startMisionTime = initMisionTimes[0] - data[0]['Timestamp']

    misionDuration = endMisionTimes[0] - initMisionTimes[0]
    # minutos y segundos para completar la partida
    minutes = math.trunc(misionDuration / 60)
    seconds = misionDuration % 60
    print("El jugador ha tardado ", minutes," minutos y ", seconds , " segundos en completar la misión")

    return startMisionTime, misionDuration