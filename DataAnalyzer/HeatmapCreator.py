import json
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math 
class dataAnalyzer:
    #Crea un mapa de calor según el tiempo que se ha mirado a cada posición de la pantalla
    def createTimeHeatMap(coords, w,h):
        # dataframe para el mapa de calor
        heatData = pd.DataFrame([[0]*21]*11)
        xCoord=0
        yCoord=0
       #recorro todo el array para parsear las posiciones a casillas del dataframe
        for c in coords:
            xCoord= math.trunc(c[0] * 20)
            yCoord= math.trunc(c[1] * 10)
            if(xCoord < 0):
                xCoord = 0
            if(xCoord > 20):
                xCoord = 20
            if(yCoord<0):
                yCoord =0
            if(yCoord>10):
                yCoord=10
            heatData.iat[yCoord,xCoord] +=1 
        #Creación del heatmap
        figsize = (w / 100, h / 100) 
        plt.figure(figsize=figsize, dpi=100)
        
        map = sns.heatmap(heatData,cmap='coolwarm', annot=True,  square=True, linewidths=.5, cbar=False)
        map.set_title('Mapa de calor según tiempo que se ha mirado a cada punto', fontsize =16)
        plt.show()
    #Crea un mapa de calor según cuantas veces se ha mirado cada posición de la pantalla
    def createCountHeatMap(coords, w, h):
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
            if(xCoord < 0):
                xCoord = 0
            if(xCoord > 20):
                xCoord = 20
            if(yCoord<0):
                yCoord =0
            if(yCoord>10):
                yCoord = 10
            #Comprueba que la posición no sea igual a la anterior para añadirla al mapa
            if(prevXcoord == xCoord and prevYcoord == yCoord):
                continue
            heatData.iat[yCoord,xCoord] += 1
            prevXcoord = xCoord
            prevYcoord = yCoord
        #creación del heatmap
        figsize = (w / 100, h / 100) 
        plt.figure(figsize=figsize, dpi=100)
        map = sns.heatmap(heatData,cmap='viridis', annot=True,  square=True, linewidths=.5, cbar=False)
        map.set_title('Mapa de calor según cantidad de veces que se ha mirado un punto', fontsize=12)
        plt.show()
        
    def readData(nameFile,init, duration):
        # Cargar el JSON desde un archivo
        with open(nameFile, 'r') as json_data:
            data = json.load(json_data)
        eyePosData = data["Events"]
        initTime = math.trunc(eyePosData[1]['timestamp'])
        
        startDataTime = init
        durationData= duration
        width = eyePosData[0]['width']
        height = eyePosData[0]['height']
        
        #Avanzar hasta la primera marca de tiempo que se necesita
        for j in range(1, len(eyePosData)-1):
            if(math.trunc(eyePosData[j]['timestamp']) >= (initTime + startDataTime)):
                break
        totalPositions= []
        for k in range(j,len(eyePosData)-1):
            if(math.trunc(eyePosData[k]['timestamp']) > (initTime + startDataTime+durationData)+1):
                break
            # No meter las posiciones de x e y que se salgan de la pantalla
            #if(eyePosData[k]['posX'] > 1 or eyePosData[k]['posX'] < 0 or eyePosData[k]['posY'] > 1 or eyePosData[k]['posY'] < 0):
                #continue
            totalPositions.append((eyePosData[k]['posX'], eyePosData[k]['posY']))
        return totalPositions, width, height



