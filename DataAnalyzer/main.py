import json
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math 
class dataAnalyzer:
    #Crea un mapa de calor según el tiempo que se ha mirado a cada posición de la pantalla
    def createTimeHeatMap(coords):
        # dataframe para el mapa de calor
        heatData = pd.DataFrame([[0]*10]*10)
        print(heatData)
        xCoord=0
        yCoord=0
       #recorro todo el array para parsear las posiciones a casillas del dataframe
        for c in coords:
            xCoord= math.trunc(c[0] * 10)
            yCoord= math.trunc(c[1] * 10)
            if(xCoord ==10):
                xCoord = 1
            if(yCoord == 10):
                yCoord = 1   
            heatData[xCoord][yCoord] = heatData[xCoord][yCoord] +1
        print(heatData) 
        #Creación del heatmap
        plt.figure(figsize=(10,10))
        sns.heatmap(heatData,cmap='coolwarm', annot=True,  square=True, linewidths=.5)
        plt.show()
    #Crea un mapa de calor según cuantas veces se ha mirado cada posición de la pantalla
    def createCountHeatMap(coords):
        # dataframe para el mapa de calor
        heatData = pd.DataFrame([[0]*10]*10)
        print(heatData)
        xCoord=0
        yCoord=0
        prevXcoord=-1
        prevYcoord=-1
       #recorro todo el array para parsear las posiciones a casillas del dataframe
        for c in coords:
            xCoord= math.trunc(c[0] * 10)
            yCoord= math.trunc(c[1] * 10)
            if(xCoord ==10):
                xCoord = 1
            if(yCoord == 10):
                yCoord = 1   
            #Comprueba que la posición no sea igual a la anterior para añadirla al mapa
            if(prevXcoord == xCoord and prevYcoord == yCoord):
                continue
            heatData[xCoord][yCoord] = heatData[xCoord][yCoord] +1
            prevXcoord = xCoord
            prevYcoord = yCoord
        print(heatData) 
        #Creación del heatmap
        plt.figure(figsize=(10,20))
        sns.heatmap(heatData,cmap='coolwarm', annot=True,  square=True, linewidths=.5)
        plt.show()
    # Cargar el JSON desde un archivo
    with open('prueba2.json', 'r') as json_data:
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
    createTimeHeatMap(totalPositions)
    createCountHeatMap(totalPositions)



