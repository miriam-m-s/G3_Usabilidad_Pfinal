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
    
    initTime = eyePosData[0]['timestamp']

    startDataTime = 0
    endDataTime= len(eyePosData)

    #Avanzar hasta la primera marca de tiempo que se necesita
    for j in range(0, len(eyePosData)):
        if(eyePosData[j]['timestamp'] >= (initTime + startDataTime)):
            break

    print(j)
    print(eyePosData[j]['timestamp'])
    totalPositions= []
    for k in range(j,len(eyePosData)):
        if(eyePosData[k]['timestamp'] > (initTime + endDataTime)):
            break
        print
        totalPositions.append((eyePosData[k]['posX'], eyePosData[k]['posY']))

    print(len(totalPositions))

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



