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
        heatData = pd.DataFrame([[0]*21]*11)
        xCoord=0
        yCoord=0
       #recorro todo el array para parsear las posiciones a casillas del dataframe
        for c in coords:
            xCoord= math.trunc(c[0] * 20)
            yCoord= math.trunc(c[1] * 10)
            heatData.iat[yCoord,xCoord] +=1 
        #Creación del heatmap
        plt.figure(figsize=(10,10))
        map = sns.heatmap(heatData,cmap='coolwarm', annot=True,  square=True, linewidths=.5)
        map.set_title('Mapa de calor según tiempo', fontsize =16)
        plt.show()
    #Crea un mapa de calor según cuantas veces se ha mirado cada posición de la pantalla
    def createCountHeatMap(coords):
        # dataframe para el mapa de calor
        heatData = pd.DataFrame([[0]*21]*11)
        xCoord=0
        yCoord=0
        prevXcoord=-1
        prevYcoord=-1
       #recorro todo el array para parsear las posiciones a casillas del dataframe
        for c in coords:
            xCoord= math.trunc(c[0] * 20)
            yCoord= math.trunc(c[1] * 10)
            #Comprueba que la posición no sea igual a la anterior para añadirla al mapa
            if(prevXcoord == xCoord and prevYcoord == yCoord):
                continue
            heatData.iat[yCoord,xCoord] += 1
            prevXcoord = xCoord
            prevYcoord = yCoord
        #Creación del heatmap
        plt.figure(figsize=(10,20))
        map = sns.heatmap(heatData,cmap='viridis', annot=True,  square=True, linewidths=.5)
        map.set_title('Mapa de calor según cantidad de veces que se ha mirado un punto', fontsize=12)
        plt.show()
    #def readData(nameFile):
    # Cargar el JSON desde un archivo
    with open('event_1715799433.json', 'r') as json_data:
        data = json.load(json_data)
    eyePosData = data["Events"]
    print (eyePosData[0])
    initTime = math.trunc(eyePosData[0]['timestamp'])
    print(initTime)
    startDataTime = 0
    endDataTime= len(eyePosData)

    #Avanzar hasta la primera marca de tiempo que se necesita
    for j in range(0, len(eyePosData)-1):
        if(math.trunc(eyePosData[j]['timestamp']) >= (initTime + startDataTime)):
            break
    posicionespochas=0
    totalPositions= []
    for k in range(j,len(eyePosData)-1):
        print(k)
        if(math.trunc(eyePosData[k]['timestamp']) > (initTime + endDataTime)):
            break
        # No meter las posiciones de x e y que se salgan de la pantalla
        if(eyePosData[k]['posX'] > 1 or eyePosData[k]['posX'] < 0 or eyePosData[k]['posY'] > 1 or eyePosData[k]['posY'] < 0):
            posicionespochas+=1
            continue
        totalPositions.append((eyePosData[k]['posX'], eyePosData[k]['posY']))
        print(posicionespochas)
    createTimeHeatMap(totalPositions)
    createCountHeatMap(totalPositions)



