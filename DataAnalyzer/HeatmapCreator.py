import json
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math 

class dataAnalyzer:

    #Creación un mapa de calor según el tiempo que se ha mirado a cada posición de la pantalla
    def createTimeHeatMap(coords, width,height,subdivisions =(1,1), background=""):
        #Cálculo del aspect ratio de la pantalla para hacer el mapa de calor de ese tamaño
        gcd = math.gcd(height,width)
        w = width// gcd
        h=height //gcd
        #Se crean tantas subdivisiones con respecto al aspect ratio como se soliciten(por defecto ninguna)
        w=math.trunc(subdivisions[0] * w / subdivisions[1])
        h=math.trunc(subdivisions[0] * h / subdivisions[1])
        #Dataframe para el mapa de calor, del tamaño del aspect ratio de la pantalla
        heatData = pd.DataFrame([[0]*(w+1)]*(h+1))
        xCoord=0
        yCoord=0

        #Recorrido de todo el array para parsear las posiciones a casillas del dataframe
        for c in coords:
            xCoord= math.trunc(c[0] * w)
            yCoord= math.trunc(c[1] * h)
            #Ajuste de las posiciones que se hayan salido de la pantalla
            if(xCoord < 0):
                xCoord = 0
            if(xCoord > w):
                xCoord = w
            if(yCoord<0):
                yCoord =0
            if(yCoord>h):
                yCoord=h
            heatData.iat[yCoord,xCoord] +=1 

        #Creación del heatmap
        figsize = (width / 100, height / 100) 
        plt.figure(figsize=figsize, dpi=100)
        #Si se le ha pasado una imagen mostrarla de fondo y poner el mapa semitransparente
        a=1
        if(background!=""):
            img = mpimg.imread(background)
            plt.imshow(img, extent=[0, w+1, h+1,0], aspect='auto')
            a=0.5
        map = sns.heatmap(heatData,cmap='coolwarm', annot=True, alpha=a, square=True, linewidths=.5, cbar=False)
        map.set_title('Mapa de calor según tiempo que se ha mirado a cada punto', fontsize =16)
        plt.show()

    #Creación un mapa de calor según cuantas veces se ha mirado cada posición de la pantalla
    def createCountHeatMap(coords, width, height,subdivisions = (1,1), background=""):
        #Cálculo del aspect ratio de la pantalla para hacer el mapa de calor de ese tamaño
        gcd = math.gcd(height,width)
        w = width// gcd
        h = height //gcd
        #Se crean tantas subdivisiones con respecto al aspect ratio como se soliciten(por defecto ninguna)
        w=math.trunc(subdivisions[0] * w / subdivisions[1])
        h=math.trunc(subdivisions[0] * h / subdivisions[1])

        #Creación del dataframe para el mapa de calor
        heatData = pd.DataFrame([[0]*(w+1)]*(h+1))
        xCoord = 0
        yCoord = 0
        #Se almacena la posición anterior para no repetir cuando se mira una vez durante más de un frame
        prevXcoord = -1
        prevYcoord = -1

        #Se recorre todo el array para parsear las posiciones a casillas del dataframe
        for c in coords:
            xCoord = math.trunc(c[0] * w)
            yCoord = math.trunc(c[1] * h)
            #Ajuste de las posiciones que se hayan salido de la pantalla
            if(xCoord < 0):
                xCoord = 0
            if(xCoord > w):
                xCoord = w
            if(yCoord < 0):
                yCoord = 0
            if(yCoord > h):
                yCoord = h
            #Comprobación de que la posición no sea igual a la anterior para añadirla al mapa
            if(prevXcoord == xCoord and prevYcoord == yCoord):
                continue
            heatData.iat[yCoord,xCoord] += 1
            prevXcoord = xCoord
            prevYcoord = yCoord

        #Creación del heatmap
        figsize = (width / 100, height / 100) 
        plt.figure(figsize=figsize, dpi=100)
        #Si se le ha pasado una imagen mostrarla de fondo y poner el mapa semitransparente
        a = 1
        if(background!=""):
            img = mpimg.imread(background)
            plt.imshow(img, extent=[0, w+1, h+1,0], aspect='auto')
            a = 0.5
        map = sns.heatmap(heatData,cmap='viridis', annot=True, alpha=a, square=True, linewidths=.5, cbar=False)
        map.set_title('Mapa de calor según cantidad de veces que se ha mirado un punto', fontsize=12)
        plt.show()
        
    def readData(nameFile, init, duration):
        #Carga del JSON desde el archivo que se le pida
        with open(nameFile, 'r') as json_data:
            data = json.load(json_data)

        #Almacenamiento el tiempo que registra el primer evento
        eyePosData = data["Events"]
        initTime = math.trunc(eyePosData[1]['timestamp'])
        
        startDataTime = init
        durationData = duration
        width = eyePosData[0]['width']
        height = eyePosData[0]['height']
        
        #Avance hasta la primera marca de tiempo que se necesita
        for j in range(1, len(eyePosData)-1):
            if(math.trunc(eyePosData[j]['timestamp']) >= (initTime + startDataTime)):
                break
        #Se almacenan todas las posiciones x e y del json del tiempo pedido en una lista de pares (x,y)
        totalPositions = []
        for k in range(j, len(eyePosData)-1):
            if(math.trunc(eyePosData[k]['timestamp']) > (initTime + startDataTime + durationData) + 1):
                break
            totalPositions.append((eyePosData[k]['posX'], eyePosData[k]['posY']))

        return totalPositions, width, height



